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
        imagem = [pixels[i * col:(i + 1) * col] for i in range(row)]
        return imagem

def mostrar_grid():
    nomes = ['lena_ascii', 'baboon_ascii', 'quadrado_ascii']
    estados = ['original', 'codificado', 'decodificado']
    arquivos = [
        [f'input/{nome}.pgm', f'encoded/{nome}.cod', f'decoded/{nome}-rec.pgm']
        for nome in nomes
    ]

    fig, axs = plt.subplots(3, 3, figsize=(10, 10))
    fig.suptitle("Imagens nos Três Estados (Original / Codificado / Decodificado)", fontsize=14)

    for i, nome in enumerate(nomes):
        for j in range(3):
            ax = axs[i][j]
            if j == 1:
                ax.text(0.5, 0.5, "Codestream\n(binário)", fontsize=12,
                        ha='center', va='center')
                ax.axis('off')
            else:
                imagem = ler_pgm_p2(arquivos[i][j])
                ax.imshow(imagem, cmap='gray', vmin=0, vmax=255)
                ax.axis('off')
            if i == 0:
                ax.set_title(estados[j])

        axs[i][0].set_ylabel(nomes[i], fontsize=12)

    plt.tight_layout()
    plt.subplots_adjust(top=0.90)
    plt.show()

if __name__ == '__main__':
    mostrar_grid()
