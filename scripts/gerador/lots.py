"""Ler e regravar as células compiladas do mapa (.lotheader / .lotpack, B42).

Serve para trocar peças de chão depois de compilar (ex.: o calçadão de
Copacabana, D-45), sem passar pelas regras do WorldEd. Formato (o mesmo que
`zonas_historias.py` lê):

.lotheader: "LOTH" + int32 versão, int32 n, n nomes de peça terminados em "\\n",
    e o resto (tamanho, níveis, cômodos, prédios, zumbis), que não mudamos.
    Uma peça no .lotpack é o índice do nome nessa lista: nomes novos vão no fim,
    e os índices antigos continuam valendo.
.lotpack: "LOTP" + int32 versão, int32 n (32 x 32 pedaços de 8 x 8), n int64 com
    a posição de cada pedaço (negativo = vazio) e os pedaços. Cada pedaço: para
    cada nível (de baixo para cima), x (0..7), y (0..7): int32 c; c = -1 seguido
    de int32 r = r quadrados vazios em sequência (contando este); senão int32
    cômodo e c - 1 índices de peça.

Teste: `python lots.py <pasta lots>` lê e regrava tudo na memória e confere que
sai byte por byte igual.
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

CELL, CHUNKS, CHUNK = 256, 32, 8


class Cabecalho:
    def __init__(self, path: Path):
        self.path = path
        data = path.read_bytes()
        self.inicio = 8 if data[:4] == b"LOTH" else 4
        (n,) = struct.unpack_from("<i", data, self.inicio)
        pos = self.inicio + 4
        self.nomes = []
        for _ in range(n):
            fim = data.index(b"\n", pos)
            self.nomes.append(data[pos:fim].decode("latin-1"))
            pos = fim + 1
        self.prefixo = data[:self.inicio]
        self.resto = data[pos:]
        _cw, _ch, self.lo, self.hi = struct.unpack_from("<4i", self.resto, 0)
        self._idx = {n: i for i, n in enumerate(self.nomes)}

    def indice(self, nome: str) -> int:
        """Índice do nome; acrescenta no fim se ainda não existe."""
        if nome not in self._idx:
            self._idx[nome] = len(self.nomes)
            self.nomes.append(nome)
        return self._idx[nome]

    def bytes(self) -> bytes:
        nomes = b"".join(n.encode("latin-1") + b"\n" for n in self.nomes)
        return self.prefixo + struct.pack("<i", len(self.nomes)) + nomes + self.resto


class Pacote:
    """Um .lotpack com os pedaços decodificados sob demanda."""

    def __init__(self, path: Path, niveis: int):
        self.path = path
        data = path.read_bytes()
        self.data = data
        self.inicio = 8 if data[:4] == b"LOTP" else 4
        (self.n,) = struct.unpack_from("<i", data, self.inicio)
        self.offs = list(struct.unpack_from(f"<{self.n}q", data, self.inicio + 4))
        self.niveis = niveis
        self.pedacos: dict[int, list] = {}

    def _decodificar(self, i: int) -> tuple[list, int]:
        p = self.offs[i]
        total = self.niveis * CHUNK * CHUNK
        quad = []
        while len(quad) < total:
            (c,) = struct.unpack_from("<i", self.data, p); p += 4
            if c == -1:
                (r,) = struct.unpack_from("<i", self.data, p); p += 4
                quad.extend([None] * r)
                continue
            vals = struct.unpack_from(f"<{c}i", self.data, p); p += 4 * c
            quad.append([vals[0], list(vals[1:])])
        return quad, p - self.offs[i]

    def pedaco(self, i: int) -> list | None:
        """Lista de quadrados (None ou [cômodo, [índices]]), nível a nível, x, y."""
        if self.offs[i] < 0:
            return None
        if i not in self.pedacos:
            self.pedacos[i] = self._decodificar(i)[0]
        return self.pedacos[i]

    @staticmethod
    def _codificar(quad: list) -> bytes:
        out = bytearray()
        i = 0
        while i < len(quad):
            if quad[i] is None:
                j = i
                while j < len(quad) and quad[j] is None:
                    j += 1
                out += struct.pack("<2i", -1, j - i)
                i = j
                continue
            sala, ids = quad[i]
            out += struct.pack(f"<{2 + len(ids)}i", 1 + len(ids), sala, *ids)
            i += 1
        return bytes(out)

    def bytes(self) -> bytes:
        blobs, offs = [], []
        pos = self.inicio + 4 + 8 * self.n
        for i in range(self.n):
            if self.offs[i] < 0:
                offs.append(self.offs[i])
                continue
            if i in self.pedacos:
                b = self._codificar(self.pedacos[i])
            else:
                _q, tam = self._decodificar(i)
                b = self.data[self.offs[i]:self.offs[i] + tam]
            offs.append(pos)
            blobs.append(b)
            pos += len(b)
        return (self.data[:self.inicio] + struct.pack("<i", self.n) + struct.pack(f"<{self.n}q", *offs)
                + b"".join(blobs))


class Celula:
    def __init__(self, lots: Path, cx: int, cy: int):
        self.cx, self.cy = cx, cy
        self.cab = Cabecalho(lots / f"{cx}_{cy}.lotheader")
        self.pac = Pacote(lots / f"world_{cx}_{cy}.lotpack", self.cab.hi - self.cab.lo + 1)

    def quadrado(self, x: int, y: int, z: int = 0):
        """[cômodo, [índices]] do quadrado (x, y) do mundo, ou None."""
        lx, ly = x - self.cx * CELL, y - self.cy * CELL
        q = self.pac.pedaco((lx // CHUNK) * CHUNKS + ly // CHUNK)
        if q is None:
            return None
        return q[(z - self.cab.lo) * CHUNK * CHUNK + (lx % CHUNK) * CHUNK + ly % CHUNK]

    def trocar(self, x: int, y: int, nomes: list[str], z: int = 0) -> bool:
        """Põe a pilha de peças `nomes` no quadrado (mantém o cômodo)."""
        lx, ly = x - self.cx * CELL, y - self.cy * CELL
        q = self.pac.pedaco((lx // CHUNK) * CHUNKS + ly // CHUNK)
        if q is None:
            return False
        k = (z - self.cab.lo) * CHUNK * CHUNK + (lx % CHUNK) * CHUNK + ly % CHUNK
        sala = q[k][0] if q[k] is not None else -1
        q[k] = [sala, [self.cab.indice(n) for n in nomes]] if nomes else None
        return True

    def nomes_em(self, x: int, y: int, z: int = 0) -> list[str]:
        q = self.quadrado(x, y, z)
        return [self.cab.nomes[i] for i in q[1]] if q else []

    def gravar(self) -> None:
        self.cab.path.write_bytes(self.cab.bytes())
        self.pac.path.write_bytes(self.pac.bytes())


def conferir(lots: Path) -> str:
    """Lê e regrava cada célula na memória; tudo tem de sair igual."""
    n = 0
    for cab in sorted(lots.glob("*.lotheader")):
        cx, cy = (int(v) for v in cab.stem.split("_"))
        c = Celula(lots, cx, cy)
        assert c.cab.bytes() == cab.read_bytes(), f"cabeçalho diferente: {cab.name}"
        for i in range(c.pac.n):          # decodifica tudo e recodifica
            c.pac.pedaco(i)
        assert c.pac.bytes() == c.pac.path.read_bytes(), f"pacote diferente: {c.pac.path.name}"
        n += 1
    return f"{n} células lidas e regravadas iguais"


if __name__ == "__main__":
    print(conferir(Path(sys.argv[1])))
