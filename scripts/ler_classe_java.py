"""Leitor mínimo de classes Java (tipo "javap -c"), sem executar nada.

Serve para entender regras do jogo que ficam no Java (ex.: onde aparecem as
histórias de casa, veículo e zona), lendo o projectzomboid.jar como dados.

Uso:
  python -X utf8 scripts/ler_classe_java.py <jar> <prefixo-de-classe> [saida.txt]
  ex.: ... projectzomboid.jar zombie/randomizedWorld/randomizedZoneStory/RZSBBQParty
Com um prefixo de pasta, lê todas as classes dentro dela.
"""
import struct
import sys
import zipfile

OPS = {}
_ops = """00 nop 0;01 aconst_null 0;02 iconst_m1 0;03 iconst_0 0;04 iconst_1 0;05 iconst_2 0;06 iconst_3 0;07 iconst_4 0;08 iconst_5 0;
09 lconst_0 0;0a lconst_1 0;0b fconst_0 0;0c fconst_1 0;0d fconst_2 0;0e dconst_0 0;0f dconst_1 0;10 bipush b;11 sipush s;12 ldc c1;13 ldc_w c2;
14 ldc2_w c2;15 iload 1;16 lload 1;17 fload 1;18 dload 1;19 aload 1;1a iload_0 0;1b iload_1 0;1c iload_2 0;1d iload_3 0;1e lload_0 0;1f lload_1 0;
20 lload_2 0;21 lload_3 0;22 fload_0 0;23 fload_1 0;24 fload_2 0;25 fload_3 0;26 dload_0 0;27 dload_1 0;28 dload_2 0;29 dload_3 0;2a aload_0 0;
2b aload_1 0;2c aload_2 0;2d aload_3 0;2e iaload 0;2f laload 0;30 faload 0;31 daload 0;32 aaload 0;33 baload 0;34 caload 0;35 saload 0;36 istore 1;
37 lstore 1;38 fstore 1;39 dstore 1;3a astore 1;3b istore_0 0;3c istore_1 0;3d istore_2 0;3e istore_3 0;3f lstore_0 0;40 lstore_1 0;41 lstore_2 0;
42 lstore_3 0;43 fstore_0 0;44 fstore_1 0;45 fstore_2 0;46 fstore_3 0;47 dstore_0 0;48 dstore_1 0;49 dstore_2 0;4a dstore_3 0;4b astore_0 0;
4c astore_1 0;4d astore_2 0;4e astore_3 0;4f iastore 0;50 lastore 0;51 fastore 0;52 dastore 0;53 aastore 0;54 bastore 0;55 castore 0;56 sastore 0;
57 pop 0;58 pop2 0;59 dup 0;5a dup_x1 0;5b dup_x2 0;5c dup2 0;5d dup2_x1 0;5e dup2_x2 0;5f swap 0;60 iadd 0;61 ladd 0;62 fadd 0;63 dadd 0;64 isub 0;
65 lsub 0;66 fsub 0;67 dsub 0;68 imul 0;69 lmul 0;6a fmul 0;6b dmul 0;6c idiv 0;6d ldiv 0;6e fdiv 0;6f ddiv 0;70 irem 0;71 lrem 0;72 frem 0;73 drem 0;
74 ineg 0;75 lneg 0;76 fneg 0;77 dneg 0;78 ishl 0;79 lshl 0;7a ishr 0;7b lshr 0;7c iushr 0;7d lushr 0;7e iand 0;7f land 0;80 ior 0;81 lor 0;82 ixor 0;
83 lxor 0;84 iinc ii;85 i2l 0;86 i2f 0;87 i2d 0;88 l2i 0;89 l2f 0;8a l2d 0;8b f2i 0;8c f2l 0;8d f2d 0;8e d2i 0;8f d2l 0;90 d2f 0;91 i2b 0;92 i2c 0;
93 i2s 0;94 lcmp 0;95 fcmpl 0;96 fcmpg 0;97 dcmpl 0;98 dcmpg 0;99 ifeq j;9a ifne j;9b iflt j;9c ifge j;9d ifgt j;9e ifle j;9f if_icmpeq j;a0 if_icmpne j;
a1 if_icmplt j;a2 if_icmpge j;a3 if_icmpgt j;a4 if_icmple j;a5 if_acmpeq j;a6 if_acmpne j;a7 goto j;a8 jsr j;a9 ret 1;aa tableswitch T;ab lookupswitch L;
ac ireturn 0;ad lreturn 0;ae freturn 0;af dreturn 0;b0 areturn 0;b1 return 0;b2 getstatic c2;b3 putstatic c2;b4 getfield c2;b5 putfield c2;
b6 invokevirtual c2;b7 invokespecial c2;b8 invokestatic c2;b9 invokeinterface c4;ba invokedynamic c4;bb new c2;bc newarray 1;bd anewarray c2;
be arraylength 0;bf athrow 0;c0 checkcast c2;c1 instanceof c2;c2 monitorenter 0;c3 monitorexit 0;c4 wide W;c5 multianewarray c3;c6 ifnull j;
c7 ifnonnull j;c8 goto_w J;c9 jsr_w J"""
for item in _ops.replace("\n", "").split(";"):
    code, name, kind = item.split()
    OPS[int(code, 16)] = (name, kind)


class Classe:
    def __init__(self, data):
        self.d = data
        self.p = 8
        n = self.u2()
        self.cp = [None] * n
        i = 1
        while i < n:
            tag = self.u1()
            if tag == 1:
                ln = self.u2()
                self.cp[i] = ("utf8", self.d[self.p:self.p + ln].decode("utf-8", "replace"))
                self.p += ln
            elif tag in (3, 4):
                raw = self.d[self.p:self.p + 4]; self.p += 4
                v = struct.unpack(">i", raw)[0] if tag == 3 else struct.unpack(">f", raw)[0]
                self.cp[i] = ("num", v)
            elif tag in (5, 6):
                raw = self.d[self.p:self.p + 8]; self.p += 8
                v = struct.unpack(">q", raw)[0] if tag == 5 else struct.unpack(">d", raw)[0]
                self.cp[i] = ("num", v)
                i += 1
            elif tag in (7, 8, 16, 19, 20):
                self.cp[i] = ({7: "class", 8: "str", 16: "mtype", 19: "mod", 20: "pkg"}[tag], self.u2())
            elif tag in (9, 10, 11, 12, 17, 18):
                self.cp[i] = ({9: "ref", 10: "ref", 11: "ref", 12: "nat", 17: "dyn", 18: "dyn"}[tag], self.u2(), self.u2())
            elif tag == 15:
                self.cp[i] = ("mh", self.u1(), self.u2())
            else:
                raise ValueError("tag %d" % tag)
            i += 1
        self.p += 2
        self.nome = self.txt(self.u2())
        sup = self.u2()
        self.super = self.txt(sup) if sup else ""
        n_interfaces = self.u2()
        self.p += 2 * n_interfaces
        self.campos = [self.membro() for _ in range(self.u2())]
        self.metodos = [self.membro() for _ in range(self.u2())]

    def u1(self):
        v = self.d[self.p]; self.p += 1; return v

    def u2(self):
        v = struct.unpack(">H", self.d[self.p:self.p + 2])[0]; self.p += 2; return v

    def u4(self):
        v = struct.unpack(">I", self.d[self.p:self.p + 4])[0]; self.p += 4; return v

    def txt(self, i):
        e = self.cp[i]
        if e is None:
            return "?"
        k = e[0]
        if k == "utf8":
            return e[1]
        if k == "num":
            return repr(e[1])
        if k in ("class", "str", "mtype"):
            s = self.txt(e[1])
            return '"%s"' % s if k == "str" else s
        if k == "ref":
            return "%s.%s" % (self.txt(e[1]).split("/")[-1], self.txt(e[2]))
        if k == "nat":
            return self.txt(e[1])
        if k == "dyn":
            return "dyn:" + self.txt(e[2])
        return str(e)

    def membro(self):
        self.p += 2
        nome = self.txt(self.u2()); desc = self.txt(self.u2())
        code = None
        for _ in range(self.u2()):
            an = self.txt(self.u2()); ln = self.u4()
            if an == "Code":
                code = self.d[self.p + 8:self.p + 8 + struct.unpack(">I", self.d[self.p + 4:self.p + 8])[0]]
            self.p += ln
        return nome, desc, code

    def dis(self, code):
        out = []
        p = 0
        while p < len(code):
            op = code[p]; nm, k = OPS.get(op, ("op%02x" % op, "0")); a = ""; q = p + 1
            if k == "b":
                a = str(struct.unpack(">b", code[q:q + 1])[0]); q += 1
            elif k == "s":
                a = str(struct.unpack(">h", code[q:q + 2])[0]); q += 2
            elif k == "1":
                a = str(code[q]); q += 1
            elif k == "c1":
                a = self.txt(code[q]); q += 1
            elif k in ("c2", "c3", "c4"):
                a = self.txt(struct.unpack(">H", code[q:q + 2])[0]); q += {"c2": 2, "c3": 3, "c4": 4}[k]
            elif k == "ii":
                a = "%d %d" % (code[q], struct.unpack(">b", code[q + 1:q + 2])[0]); q += 2
            elif k == "j":
                a = "-> %d" % (p + struct.unpack(">h", code[q:q + 2])[0]); q += 2
            elif k == "J":
                a = "-> %d" % (p + struct.unpack(">i", code[q:q + 4])[0]); q += 4
            elif k == "T":
                q += (4 - q % 4) % 4
                dflt, lo, hi = struct.unpack(">iii", code[q:q + 12])
                alvos = struct.unpack(">%di" % (hi - lo + 1), code[q + 12:q + 12 + 4 * (hi - lo + 1)])
                a = "padrao->%d %s" % (p + dflt, " ".join("%d->%d" % (lo + j, p + t) for j, t in enumerate(alvos)))
                q += 12 + 4 * (hi - lo + 1)
            elif k == "L":
                q += (4 - q % 4) % 4
                n = struct.unpack(">i", code[q + 4:q + 8])[0]
                keys = [struct.unpack(">i", code[q + 8 + 8 * j:q + 12 + 8 * j])[0] for j in range(n)]
                a = "keys=%s" % keys[:12]; q += 8 + 8 * n
            elif k == "W":
                q += 5 if code[q] == 0x84 else 3
            out.append("%5d %s %s" % (p, nm, a))
            p = q
        return out


def main():
    jar, pref = sys.argv[1], sys.argv[2]
    saida = open(sys.argv[3], "w", encoding="utf-8") if len(sys.argv) > 3 else sys.stdout
    z = zipfile.ZipFile(jar)
    for n in sorted(z.namelist()):
        if not n.endswith(".class") or not n.startswith(pref):
            continue
        try:
            c = Classe(z.read(n))
        except Exception as e:  # formatos raros (ex.: records); só avisa
            print("(nao li %s: %s)" % (n, e), file=saida)
            continue
        print("=" * 70, file=saida)
        print("classe %s  (herda de %s)" % (c.nome, c.super), file=saida)
        for nome, desc, _ in c.campos:
            print("  campo %s %s" % (nome, desc), file=saida)
        for nome, desc, code in c.metodos:
            print("-- metodo %s%s" % (nome, desc), file=saida)
            if code:
                for linha in c.dis(code):
                    print(linha, file=saida)


if __name__ == "__main__":
    main()
