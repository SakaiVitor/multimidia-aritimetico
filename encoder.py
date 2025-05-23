import os
import struct
from collections import Counter

PREC = 32
MAX_RANGE = (1 << PREC) - 1
HALF = 1 << (PREC - 1)
QUARTER = 1 << (PREC - 2)
THREE_QUARTER = QUARTER * 3

class BitWriter:
    def __init__(self, f):
        self.f = f
        self.acc = 0
        self.n = 0
    def write_bit(self, b):
        self.acc = (self.acc << 1) | b
        self.n += 1
        if self.n == 8:
            self.f.write(bytes((self.acc,)))
            self.acc = 0
            self.n = 0
    def write_bits(self, b, count):
        for _ in range(count):
            self.write_bit(b)
    def flush(self):
        if self.n:
            self.acc <<= (8 - self.n)
            self.f.write(bytes((self.acc,)))
            self.acc = 0
            self.n = 0

def ler_pgm_p2(path):
    with open(path) as f:
        assert f.readline().strip() == 'P2'
        while True:
            l = f.readline()
            if not l.startswith('#'):
                break
        col, row = map(int, l.split())
        maxv = int(f.readline().strip())
        pix = [int(x) for x in f.read().split()]
        return pix, col, row, maxv

def main():
    os.makedirs('encoded', exist_ok=True)
    for fn in os.listdir('input'):
        if not fn.endswith('.pgm'):
            continue
        pixels, col, row, maxv = ler_pgm_p2(os.path.join('input', fn))
        freq = Counter(pixels)
        total = sum(freq.values())
        cumul = {}
        s = 0
        for v in range(256):
            cumul[v] = s
            s += freq.get(v, 0)

        low, high = 0, MAX_RANGE
        underflow = 0

        base = fn[:-4]
        with open(f'encoded/{base}.meta', 'w') as m:
            m.write(f"{col} {row} {maxv}\n")

        with open(f'encoded/{base}.cod', 'wb') as f:
            f.write(struct.pack('>H', len(freq)))
            for v, cnt in freq.items():
                f.write(struct.pack('>B', v))
                f.write(struct.pack('>I', cnt))
            bw = BitWriter(f)

            for p in pixels:
                r = high - low + 1
                cl = cumul[p]
                ch = cl + freq[p]
                high = low + (r * ch // total) - 1
                low  = low + (r * cl // total)
                while True:
                    if high < HALF:
                        bw.write_bit(0)
                        for _ in range(underflow):
                            bw.write_bit(1)
                        underflow = 0
                        low  <<= 1
                        high = (high << 1) | 1
                    elif low >= HALF:
                        bw.write_bit(1)
                        for _ in range(underflow):
                            bw.write_bit(0)
                        underflow = 0
                        low  = (low - HALF) << 1
                        high = ((high - HALF) << 1) | 1
                    elif low >= QUARTER and high < THREE_QUARTER:
                        underflow += 1
                        low  = (low - QUARTER) << 1
                        high = ((high - QUARTER) << 1) | 1
                    else:
                        break

            underflow += 1
            if low < QUARTER:
                bw.write_bit(0)
                for _ in range(underflow):
                    bw.write_bit(1)
            else:
                bw.write_bit(1)
                for _ in range(underflow):
                    bw.write_bit(0)

            bw.flush()
        print(f"[ENC] {fn} → encoded/{base}.cod")

if __name__ == '__main__':
    main()
