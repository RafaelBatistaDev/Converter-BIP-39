# 🔄 Converter de Números para Frases BIP-39 - converter.py


# Executar
## Setup Inicial

```bash
# 1. Cria o toolbox (se for a primeira vez, ele vai baixar a imagem)
toolbox create 2-Convverter-BIP-39
```

```bash
# 2. Entra no container isolado
toolbox enter 2-Convverter-BIP-39
```


```bash
#(Opcional, mas recomendado) Cria um ambiente virtual para isolar ainda mais as libs do projeto
uv init
uv venv
source .venv/bin/activate
uv sync --all-groups
uv lock
```

```bash
python3 converter.py
```

## 📋 Descrição

Script Python que converte **números indexados** em **frases BIP-39 válidas** usando a wordlist oficial do BIP-39.

Cada frase é representada como 24 números (12 pares de bytes baixo/alto) que são convertidos para as 12 palavras correspondentes.

---

## ⚙️ Funcionalidades

### O que o Script Faz

1. **Lê arquivo de entrada** (`numeros.txt`) com linhas de números
2. **Valida o formato** (deve ter 24 números por linha)
3. **Converte para índices** usando interpretação little-endian (byte baixo + byte alto << 8)
4. **Mapeia para palavras** usando a wordlist BIP-39 oficial (2048 palavras)
5. **Salva resultado** em arquivo único (`frases_convertidas.txt`)
6. **Reutiliza arquivo** se ele já existe com conteúdo

### Características

- ✅ Suporta reutilização automática de conversões anteriores
- ✅ Valida formato de entrada (24 números por linha)
- ✅ Usa wordlist BIP-39 oficial completa (2048 palavras)
- ✅ Interpretação little-endian correta de bytes
- ✅ Lida com erros de formato graciosamente
- ✅ Mostra progresso durante a conversão

---

## 🚀 Como Usar

### Pré-requisitos

- Python 3.6+
- Arquivo `numeros.txt` no mesmo diretório

### Estrutura do Arquivo de Entrada (numeros.txt)

Cada linha deve conter **24 números** (pares de bytes):

```
75 4 200 1 100 0 50 2 75 1 200 0 100 1 50 0 75 2 200 1 100 0 50 1 200 0
100 1 75 0 50 2 200 1 100 0 75 1 50 0 200 1 100 2 75 0 50 1 200 0 100 1
```

**Formato:**
- Separados por espaços ou vírgulas
- 24 números por linha (12 pares)
- Cada par: `byte_baixo byte_alto`

### Executar o Script

```bash
# Navegar até a pasta
cd ~/OneDrive/Frases-MyEtherWallet/Wallet
# Executar
python3 converter.py
```

### Saída Esperada

**Primeira execução:**
```
🚀 Convertendo números para frases BIP-39...

✅ frases_convertidas.txt salvo com 1000 frases convertidas!
Conversão concluída. Frases salvas em frases_convertidas.txt
```

**Execuções subsequentes:**
```
📂 Arquivo frases_convertidas.txt já existe!
✅ Reutilizando arquivo com 1000 frases convertidas.
Conversão concluída. Frases salvas em frases_convertidas.txt
```

---

## 📁 Arquivos

### Entrada: `numeros.txt`
- **Localização**: Mesmo diretório que o script
- **Formato**: 24 números por linha (pares de bytes baixo/alto)
- **Exemplo**: `75 4 200 1 100 0 ...` (24 números)

### Saída: `frases_convertidas.txt`
- **Localização**: Mesmo diretório que o script
- **Formato**: Uma frase por linha (12 palavras separadas por espaços)
- **Exemplo**:
```
abandon ability able about above absent absorb abstract absurd abuse access accident
account accuse achieve acid acoustic acquire across act action actor actress actual
adapt add addict address adjust admit adult advance advice aerobic affair afford afraid
...
```

---

## 🔄 Reutilização Automática

O script verifica se `frases_convertidas.txt` já existe **e tem conteúdo**:

- ✅ **Se existe com conteúdo** → Reutiliza (não regenera)
- ❌ **Se não existe ou está vazio** → Regenera

### Forçar Regeneração

Delete o arquivo e execute novamente:

```bash
rm frases_convertidas.txt
python3 converter.py
```

---

## 🔍 Formato de Conversão

### Entendendo os Bytes

Cada par de números (byte_baixo, byte_alto) é convertido para um índice:

```
Índice = byte_baixo + (byte_alto << 8)
```

**Exemplo:**
```
Entrada: 75 4
byte_baixo = 75
byte_alto = 4
Índice = 75 + (4 × 256) = 75 + 1024 = 1099
Palavra = bip39_words[1099] = "network"
```

### Interpretação

- **24 números** = 12 pares de bytes
- **12 pares** = 12 índices de 16 bits
- **12 índices** = 12 palavras BIP-39
- **12 palavras** = 1 frase BIP-39 válida

---

## 🛠️ Troubleshooting

### Erro: "Arquivo numeros.txt não encontrado"
Crie o arquivo `numeros.txt` no mesmo diretório com as linhas de números:
```bash
echo "75 4 200 1 100 0 50 2 75 1 200 0 100 1 50 0 75 2 200 1 100 0 50 1 200 0" > numeros.txt
```

### Erro: "Linha ignorada (formato inválido)"
Verifique se cada linha tem exatamente **24 números**:
```bash
# Contar números em uma linha
head -1 numeros.txt | wc -w  # Deve retornar 24
```

### Arquivo de saída vazio
Execute novamente para regenerar:
```bash
rm frases_convertidas.txt
python3 converter.py
```

### Verificar conteúdo
```bash
# Ver primeiras frases
head -5 frases_convertidas.txt

# Contar total
wc -l frases_convertidas.txt
```

---

## 📊 Exemplo Completo

### Criar entrada
```bash
# Gerar 10 linhas de números aleatórios
for i in {1..10}; do
  for j in {1..24}; do
    echo -n "$((RANDOM % 256)) "
  done
  echo
done > numeros.txt
```

### Executar conversão
```bash
python3 converter.py
```

### Verificar saída
```bash
cat frases_convertidas.txt
```

---

## 📝 Observações Importantes

- ⚠️ **Validação**: O script valida o formato (24 números por linha)
- 🔐 **BIP-39**: Usa a wordlist oficial (2048 palavras)
- 🔄 **Reutilização**: Arquivo vazio agora força regeneração
- 💾 **Performance**: Processa ~1000 frases em segundos
- 📋 **Preservação**: Espaços no início/fim são descartados durante o split

---

## 🔗 Relacionado

- **Gerador**: `gerador_metamask.js` - Gera 1000 frases BIP-39 aleatórias
- **Validador**: `automacao_contador.py` - Valida frases em MyEtherWallet
- **Documentação**: Ver `/Contador/Contador.MD` e `gerador_metamask.MD`

---

## 📜 Licença

BIP-39 Wordlist: Domínio público
Script: MIT
