# Bot de Arbitragem Triangular - Binance Spot

Bot automatizado para identificar e executar oportunidades de arbitragem triangular na Binance.

## 🚀 Funcionalidades

- ✅ Busca automática de triângulos de arbitragem
- ✅ Cálculo de lucro com taxas da Binance
- ✅ Execução automática de ordens
- ✅ Modo simulação e modo real
- ✅ Logs detalhados de todas operações
- ✅ Estatísticas em tempo real

## 📋 Requisitos

- Python 3.10+
- Conta na Binance com API Key
- Servidor (recomendado: Digital Ocean)

## 🔧 Instalação

```bash
# Clone o repositório
git clone https://github.com/soaresbruno21-gif/bot-arbitragem-binance.git
cd bot-arbitragem-binance

# Instale as dependências
pip3 install -r requirements.txt

# Configure suas chaves da Binance
cp config/config.example.env config/config.env
nano config/config.env
```

## ⚙️ Configuração

Edite o arquivo `config/config.env`:

```env
# Chaves da Binance
BINANCE_API_KEY=sua_chave_aqui
BINANCE_API_SECRET=sua_chave_secreta_aqui

# Configurações do Bot
BASE_CURRENCY=USDT              # Moeda base para arbitragem
FEE_PERCENT=0.1                 # Taxa por operação (%)
MIN_PROFIT_PERCENT=0.5          # Lucro mínimo para executar (%)
TRADE_AMOUNT_USDT=100           # Valor por trade
CHECK_INTERVAL_SECONDS=30       # Intervalo entre verificações
SIMULATION_MODE=True            # True = simulação, False = real
```

## 🎯 Como Usar

### Modo Simulação (Recomendado para testes)

```bash
python3 bot.py
```

### Modo Real (⚠️ Executa ordens reais!)

1. Edite `config/config.env` e mude:
   ```
   SIMULATION_MODE=False
   ```

2. Execute:
   ```bash
   python3 bot.py
   ```

## 📊 Testes

```bash
# Testar conexão com Binance
python3 tests/test_connection.py

# Testar busca de oportunidades
python3 tests/test_monitor.py

# Testar execução completa
python3 tests/test_full_execution.py
```

## 📁 Estrutura do Projeto

```
bot-arbitragem-binance/
├── bot.py                      # Bot principal
├── config/
│   ├── config.env             # Configurações (não versionado)
│   └── config.example.env     # Exemplo de configuração
├── src/
│   ├── market_data.py         # Busca dados do mercado
│   ├── triangle_finder.py     # Identifica triângulos
│   ├── arbitrage_analyzer.py  # Analisa oportunidades
│   ├── arbitrage_monitor.py   # Monitor em tempo real
│   └── order_executor.py      # Executa ordens
├── logs/
│   ├── bot.log               # Log do bot
│   └── trades.log            # Log de trades
└── tests/
    ├── test_connection.py    # Teste de conexão
    ├── test_monitor.py       # Teste de monitoramento
    └── test_full_execution.py # Teste completo
```

## ⚠️ Avisos Importantes

- **Sempre teste em modo simulação primeiro!**
- **Arbitragem tem riscos:** preços mudam rapidamente
- **Taxas da Binance:** 0.1% por operação (0.3% total no triângulo)
- **Slippage:** em ordens de mercado, o preço pode variar
- **Nunca invista mais do que pode perder**

## 📈 Exemplo de Resultado

```
Oportunidade encontrada: USDT → SKL → BTC → USDT
Lucro esperado: 10.15%
Investimento: $100.00
Retorno: $110.39
Lucro líquido: $10.39
```

## 🛠️ Manutenção

### Atualizar código do GitHub

```bash
cd bot-arbitragem-binance
git pull
```

### Ver logs

```bash
tail -f logs/bot.log
tail -f logs/trades.log
```

## 📝 Status

✅ **Versão 1.0 - Funcional**

- Etapa 1: Estrutura inicial ✅
- Etapa 2: Conexão com Binance ✅
- Etapa 3: Identificação de oportunidades ✅
- Etapa 4: Execução de ordens ✅
- Etapa 5: Bot completo ✅

---

**Desenvolvido com ❤️ para arbitragem automatizada**
