"""Filtro de estilo: aproxima as peças do Kit Brasil do desenho do jogo.

Aprovado pelo usuário em 09/11/2026 e aplicado a todas as folhas: `kit_favela._gravar`
(favela, laje, botequim) e `calcadao.folha` passam cada folha por `filtrar_folha` antes
de gravar, e marcam `"estilo": "pz_v1"` no .json. `aplicar_em_disco` filtra uma folha
já gravada (só uma vez: confere a marca).

As peças do jogo são pintadas à mão: cores mais chapadas, pouco granulado,
contorno levemente borrado, menos contraste. As nossas saem de textura
procedural, nítidas e "fotográficas". O filtro, por peça (128 x 256):
1. alisa o granulado com filtro bilateral (áreas de cor lisas, bordas nítidas);
2. menos contraste e menos saturação, com um leve tom quente;
3. objetos ganham um contorno escuro suave, como os móveis do jogo.

Uso: python -I -X utf8 estilo_pz.py <kits/tiles>   (filtra as folhas que ainda não têm a marca)
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter


def _media_alfa(rgb, a, raio):
    """Desfoque que não puxa o fundo transparente para dentro da peça."""
    pre = Image.fromarray(np.clip(rgb * a[..., None], 0, 255).astype(np.uint8))
    al = Image.fromarray((a * 255).astype(np.uint8))
    num = np.array(pre.filter(ImageFilter.GaussianBlur(raio)), float)
    den = np.array(al.filter(ImageFilter.GaussianBlur(raio)), float)[..., None] / 255
    return num / np.maximum(den, 1e-3)


def _bilateral(rgb, a, raio=2, sig_s=1.6, sig_c=20.0):
    """Alisa as áreas de cor mantendo as bordas (filtro bilateral), só na parte visível."""
    H, W = a.shape
    pad = np.pad(rgb, ((raio, raio), (raio, raio), (0, 0)), mode="edge")
    pa = np.pad(a, raio)
    num = np.zeros_like(rgb)
    den = np.zeros(a.shape)
    for dy in range(-raio, raio + 1):
        for dx in range(-raio, raio + 1):
            viz = pad[raio + dy:raio + dy + H, raio + dx:raio + dx + W]
            va = pa[raio + dy:raio + dy + H, raio + dx:raio + dx + W]
            dc = ((viz - rgb) ** 2).sum(-1)
            w = np.exp(-(dx * dx + dy * dy) / (2 * sig_s ** 2)) * np.exp(-dc / (2 * sig_c ** 2)) * va
            num += viz * w[..., None]
            den += w
    return num / np.maximum(den, 1e-6)[..., None]


def filtrar_peca(cel: np.ndarray, tipo: str, forca: float = 1.0, m=None) -> np.ndarray:
    rgb = cel[..., :3].astype(float)
    a = cel[..., 3].astype(float) / 255
    if a.max() == 0:
        return cel
    # 1. granulado: alisa as áreas de cor sem borrar as bordas (2 passadas)
    liso = _bilateral(_bilateral(rgb, a), a)
    rgb = rgb * (1 - forca) + liso * forca
    # 2. contraste e saturação (em volta da média da folha, para não criar emendas), tom quente
    if m is None:
        m = (rgb * a[..., None]).sum((0, 1)) / max(a.sum(), 1)
    rgb = m + (rgb - m) * (1 - 0.12 * forca)
    cinza = rgb.mean(-1, keepdims=True)
    rgb = cinza + (rgb - cinza) * (1 - 0.15 * forca)
    rgb = rgb * np.array([1.02, 1.0, 0.96])
    # 3. contorno escuro suave nos objetos, como os móveis do jogo
    if tipo == "objeto":
        al = Image.fromarray((a * 255).astype(np.uint8))
        dentro = np.array(al.filter(ImageFilter.MinFilter(3)), float) / 255
        borda = np.clip(a - dentro, 0, 1) * (a > 0.6)
        rgb = rgb * (1 - 0.4 * forca * borda)[..., None]
    out = cel.copy()
    out[..., :3] = np.clip(rgb, 0, 255).astype(np.uint8)
    return out


ESTILO = "pz_v1"


def filtrar_folha(folha, tipo: str, forca: float = 1.0, sem_contorno=()) -> Image.Image:
    """`folha`: Image ou caminho do PNG. Devolve a folha filtrada (RGBA)."""
    im = np.array((folha if isinstance(folha, Image.Image) else Image.open(folha)).convert("RGBA"))
    a = im[..., 3].astype(float) / 255
    m = (im[..., :3].astype(float) * a[..., None]).sum((0, 1)) / max(a.sum(), 1)
    out = im.copy()
    for y in range(0, im.shape[0], 256):
        for x in range(0, im.shape[1], 128):
            i = (y // 256) * (im.shape[1] // 128) + x // 128
            t = "peca" if i in sem_contorno else tipo     # peça de um conjunto (letreiro, quadro): sem contorno na emenda
            out[y:y + 256, x:x + 128] = filtrar_peca(im[y:y + 256, x:x + 128], t, forca, m)
    return Image.fromarray(out, "RGBA")


def aplicar_em_disco(png: Path) -> bool:
    js = png.with_suffix(".json")
    man = json.loads(js.read_text(encoding="utf-8"))
    if man.get("estilo") == ESTILO:
        return False
    filtrar_folha(png, man.get("tipo", "piso")).save(png)
    man["estilo"] = ESTILO
    js.write_text(json.dumps(man, ensure_ascii=False, indent=1), encoding="utf-8")
    return True


if __name__ == "__main__":
    kit = Path(sys.argv[1])
    for png in sorted(kit.glob("rsb_*.png")):
        if png.with_suffix(".json").exists():
            print(png.name, "filtrada" if aplicar_em_disco(png) else "já estava", flush=True)
