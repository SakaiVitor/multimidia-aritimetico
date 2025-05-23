import os
import matplotlib.pyplot as plt

def ler_pgm_p2(path):
    with open(path, 'r') as f:
        assert f.readline().strip() == 'P2'
        while True:
            linha = f.readline()
            if not linha.startswith('#'):
                break
        col, row = map(int, linha.strip().split())
        maxval = int(f.readline().strip())
        pixels = [int(n) for n in f.read().split()]
        return pixels

def calcular_taxa_compressao(original, codificado):
    return os.path.getsize(original) / os.path.getsize(codificado)

def comparar_pixels(p1, p2):
    return all(a == b for a, b in zip(p1, p2))

def analisar_imagem(nome_base):
    original_path = f'input/{nome_base}.pgm'
    cod_path = f'encoded/{nome_base}.cod'
    rec_path = f'decoded/{nome_base}-rec.pgm'

    tamanho_original = os.path.getsize(original_path)
    tamanho_cod = os.path.getsize(cod_path)
    tamanho_dec = os.path.getsize(rec_path)

    taxa = calcular_taxa_compressao(original_path, cod_path)

    original_pixels = ler_pgm_p2(original_path)
    rec_pixels = ler_pgm_p2(rec_path)
    fidelidade = comparar_pixels(original_pixels, rec_pixels)

    return {
        'nome': nome_base,
        'original': tamanho_original,
        'codificado': tamanho_cod,
        'decodificado': tamanho_dec,
        'taxa': taxa,
        'fiel': fidelidade
    }

def gerar_graficos(metricas):
    nomes = [m['nome'] for m in metricas]
    orig = [m['original'] for m in metricas]
    cod = [m['codificado'] for m in metricas]
    dec = [m['decodificado'] for m in metricas]
    taxas = [m['taxa'] for m in metricas]

    x = range(len(nomes))
    fig, ax = plt.subplots(figsize=(10, 6))
    b1 = ax.bar([i - 0.2 for i in x], orig, width=0.2, label='Original')
    b2 = ax.bar(x, cod, width=0.2, label='Codificado')
    b3 = ax.bar([i + 0.2 for i in x], dec, width=0.2, label='Decodificado')
    ax.set_xticks(x)
    ax.set_xticklabels(nomes)
    ax.set_ylabel("Tamanho (bytes)")
    ax.set_title("Tamanho dos Arquivos por Imagem")
    ax.legend()
    ax.bar_label(b1, fmt='%d', padding=3)
    ax.bar_label(b2, fmt='%d', padding=3)
    ax.bar_label(b3, fmt='%d', padding=3)
    max_y = max(orig + cod + dec)
    ax.set_ylim(0, max_y * 1.15)
    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.show()

    fig, ax = plt.subplots(figsize=(8, 5))
    b = ax.bar(nomes, taxas)
    ax.set_ylabel("Taxa de Compressão")
    ax.set_title("Taxa de Compressão (Original / Codificado)")
    ax.bar_label(b, fmt='%.2f', padding=3)
    max_t = max(taxas)
    ax.set_ylim(0, max_t * 1.15)
    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.show()

def main():
    imagens = ['lena_ascii', 'baboon_ascii', 'quadrado_ascii']
    metricas = [analisar_imagem(nome) for nome in imagens]

    print("==== MÉTRICAS ====")
    for m in metricas:
        print(f"Imagem: {m['nome']}")
        print(f"  Original: {m['original']} bytes")
        print(f"  Codificado: {m['codificado']} bytes")
        print(f"  Decodificado: {m['decodificado']} bytes")
        print(f"  Taxa de compressão: {m['taxa']:.2f}")
        print(f"  Fidelidade: {'✅' if m['fiel'] else '❌'}")
        print("")

    gerar_graficos(metricas)

if __name__ == '__main__':
    main()
