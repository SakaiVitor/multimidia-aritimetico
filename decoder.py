import os
import struct

PREC = 32
MAX_RANGE = (1 << PREC) - 1
HALF = 1 << (PREC - 1)
QUARTER = 1 << (PREC - 2)
THREE_QUARTER = QUARTER * 3

class BitReader:
    def __init__(self, f):
        self.f = f
        self.acc = 0
        self.n = 0
    def read_bit(self):
        if self.n == 0:
            b = self.f.read(1)
            if not b:
                return 0
            self.acc = b[0]
            self.n = 8
        bit = (self.acc >> 7) & 1
        self.acc = (self.acc << 1) & 0xFF
        self.n -= 1
        return bit

def salvar_pgm_p2(path, pix, col, row, maxv):
    with open(path, 'w') as f:
        f.write('P2\n')
        f.write(f"{col} {row}\n{maxv}\n")
        for i in range(row):
            f.write(" ".join(map(str, pix[i*col:(i+1)*col])) + "\n")

def main():
    os.makedirs('decoded', exist_ok=True)
    for fn in os.listdir('encoded'):
        if not fn.endswith('.cod'):
            continue
        base = fn[:-4]
        with open(f'encoded/{base}.meta') as m:
            col, row, maxv = map(int, m.read().split())
        total = col * row

        with open(f'encoded/{base}.cod', 'rb') as f:
            n, = struct.unpack('>H', f.read(2))
            freq = {}
            for _ in range(n):
                v, = struct.unpack('>B', f.read(1))
                cnt, = struct.unpack('>I', f.read(4))
                freq[v] = cnt
            br = BitReader(f)

            cumul = {}
            s = 0
            for v in range(256):
                cumul[v] = s
                s += freq.get(v, 0)

            low, high = 0, MAX_RANGE
            value = 0
            for _ in range(PREC):
                value = (value << 1) | br.read_bit()

            pixels = []
            for _ in range(total):
                r = high - low + 1
                scaled = ((value - low + 1) * s - 1) // r
                for v in sorted(freq):
                    cl = cumul[v]
                    ch = cl + freq[v]
                    if cl <= scaled < ch:
                        pixels.append(v)
                        high = low + (r * ch // s) - 1
                        low  = low + (r * cl // s)
                        break
                while True:
                    if high < HALF:
                        pass
                    elif low >= HALF:
                        low  -= HALF
                        high -= HALF
                        value -= HALF
                    elif low >= QUARTER and high < THREE_QUARTER:
                        low  -= QUARTER
                        high -= QUARTER
                        value -= QUARTER
                    else:
                        break
                    low  <<= 1
                    high = (high << 1) | 1
                    value = (value << 1) | br.read_bit()

        salvar_pgm_p2(f"decoded/{base}-rec.pgm", pixels, col, row, maxv)
        print(f"[DEC] encoded/{base}.cod → decoded/{base}-rec.pgm")

if __name__ == '__main__':
    main()
