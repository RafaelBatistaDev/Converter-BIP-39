import os
import hashlib
import re
import sys


def carregar_bip39_oficial():
    """Carrega a wordlist BIP-39 exclusivamente do arquivo english.txt local."""
    # Garante o caminho absoluto baseado no diretório do próprio script converter.py
    diretorio_script = os.path.dirname(os.path.abspath(__file__))
    caminho_txt = os.path.join(diretorio_script, "english.txt")

    if os.path.exists(caminho_txt):
        try:
            with open(caminho_txt, 'r', encoding='utf-8') as f:
                palavras = [w.strip() for w in f.readlines() if w.strip()]
                if len(palavras) == 2048:
                    return palavras
                else:
                    print(f"❌ Erro: O arquivo '{caminho_txt}' deve ter 2048 palavras. Encontradas: {len(palavras)}")
        except Exception as e:
            print(f"❌ Erro ao ler '{caminho_txt}': {e}")
    else:
        print(f"❌ Erro: Arquivo '{caminho_txt}' não encontrado.")

    return None

# Inicializa a lista global
bip39_words = carregar_bip39_oficial()
if not bip39_words:
    print("❌ Falha crítica: Não foi possível carregar a wordlist. O script requer o arquivo 'english.txt' na mesma pasta.")
    sys.exit(1)


def bytes_to_mnemonic(entropy_bytes):
    """Converte 16 bytes de entropia para 12 palavras BIP-39 padrão MetaMask."""
    if len(entropy_bytes) != 16:
        raise ValueError("A entropia deve ter exatamente 16 bytes.")

    # 1. SHA-256 para extrair os 4 bits de Checksum
    hash_bytes = hashlib.sha256(entropy_bytes).digest()
    checksum_bits = (hash_bytes[0] >> 4) & 0x0F

    # 2. String binária: 128 bits de entropia + 4 bits de checksum = 132 bits
    bit_string = "".join(f"{b:08b}" for b in entropy_bytes)
    bit_string += f"{checksum_bits:04b}"

    # 3. Bloca a string em 12 grupos de 11 bits para mapear os índices (0-2047)
    words = []
    for i in range(12):
        chunk = bit_string[i * 11: (i + 1) * 11]
        index = int(chunk, 2)
        words.append(bip39_words[index])

    return " ".join(words)


def parse_line_to_entropy(line):
    """Interpreta a linha de números e extrai os 16 bytes de entropia."""
    parts = line.strip().replace(',', ' ').split()
    if not parts:
        return None

    try:
        # Padrão de 24 números (pares Little Endian de 16 bits do hardware)
        if len(parts) == 24:
            entropy_bytes = bytearray()
            for i in range(0, 24, 2):
                low = int(parts[i])
                high = int(parts[i + 1])
                val = low + (high << 8)
                entropy_bytes.append(val & 0xFF)
                entropy_bytes.append((val >> 8) & 0xFF)
            return bytes(entropy_bytes[:16])

        # Padrão direto de 16 bytes brutos
        elif len(parts) == 16:
            return bytes(int(p) for p in parts)
    except ValueError:
        pass
    return None


# Fluxo de execução principal
diretorio_script = os.path.dirname(os.path.abspath(__file__))
input_filename = os.path.join(diretorio_script, 'input', 'numeros.txt')
# Define o caminho para a pasta de saída local ao conversor
output_dir = os.path.join(diretorio_script, 'output')

# Cria a pasta de saída se ela não existir
os.makedirs(output_dir, exist_ok=True)
output_filename = os.path.join(output_dir, 'frases_convertidas.txt')

if not os.path.exists(input_filename):
    print(f"❌ Erro: O arquivo '{input_filename}' não foi encontrado na pasta Wallet.")
    sys.exit(1)

print(f"📊 Carregando dados de entrada...")
with open(input_filename, 'r', encoding='utf-8') as f:
    linhas = [line for line in f if line.strip()]

total_linhas = len(linhas)
print(f"🚀 Convertendo {total_linhas} entradas para o padrão estrito MetaMask...")

contador = 0
linhas_ignoradas = 0

with open(output_filename, 'w', encoding='utf-8') as f_out:
    for idx, line in enumerate(linhas, 1):
        entropy = parse_line_to_entropy(line)

        if entropy and len(entropy) == 16:
            try:
                frase = bytes_to_mnemonic(entropy)
                f_out.write(frase + '\n')
                contador += 1
            except Exception:
                linhas_ignoradas += 1
        else:
            linhas_ignoradas += 1

        # Atualiza o terminal a cada 100 linhas ou no final
        if idx % 100 == 0 or idx == total_linhas:
            percentual = (idx / total_linhas) * 100
            sys.stdout.write(
                f"\r⏳ Progresso: {percentual:.2f}% | Processadas: {idx}/{total_linhas} | Sucessos: {contador}")
            sys.stdout.flush()
            f_out.flush()

print(f"\n\n✅ Conversão finalizada com sucesso!")
print(f"📝 Resultado salvo em: {output_filename}")
print(f"   ↳ Frases geradas: {contador}")
if linhas_ignoradas > 0:
    print(f"   ↳ Linhas ignoradas: {linhas_ignoradas}")