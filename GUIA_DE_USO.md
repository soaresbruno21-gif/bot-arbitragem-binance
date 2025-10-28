# 📖 GUIA DE USO - Bot de Arbitragem

Guia simples para usar o bot no seu servidor Digital Ocean.

---

## 🔐 Dados do Servidor

- **IP:** 104.248.144.162
- **Usuário:** root
- **Senha:** BotBinance2025x

---

## 🚀 Como Conectar no Servidor

### No Windows:
1. Baixe o **PuTTY**: https://www.putty.org/
2. Abra o PuTTY
3. Em "Host Name" digite: `104.248.144.162`
4. Clique em "Open"
5. Digite usuário: `root`
6. Digite senha: `BotBinance2025x`

### No Mac/Linux:
1. Abra o Terminal
2. Digite: `ssh root@104.248.144.162`
3. Digite senha: `BotBinance2025x`

---

## ▶️ Como Rodar o Bot

Depois de conectado no servidor, execute:

```bash
# 1. Entre na pasta do bot
cd /root/bot-arbitragem-binance

# 2. Atualize o código (se houver mudanças)
git pull

# 3. Rode o bot
python3 bot.py
```

**O bot vai começar a funcionar!**

---

## ⚙️ Configurações

Para mudar as configurações, edite o arquivo:

```bash
nano config/config.env
```

**Configurações disponíveis:**

```
MIN_PROFIT_PERCENT=0.5          # Lucro mínimo para executar (%)
TRADE_AMOUNT_USDT=100           # Valor por trade
CHECK_INTERVAL_SECONDS=30       # Intervalo entre verificações
SIMULATION_MODE=True            # True = simulação, False = real
```

**Depois de editar:**
- Aperte `Ctrl + O` para salvar
- Aperte `Enter` para confirmar
- Aperte `Ctrl + X` para sair

---

## 🛑 Como Parar o Bot

Quando o bot estiver rodando:

**Aperte:** `Ctrl + C`

O bot vai parar e mostrar as estatísticas finais.

---

## 📊 Ver Histórico de Operações

```bash
# Ver últimas 50 linhas do log
tail -50 logs/bot.log

# Ver log de trades
tail -50 logs/trades.log

# Ver log em tempo real (enquanto bot roda)
tail -f logs/bot.log
```

---

## ⚠️ MODO REAL (Executar ordens reais)

**ATENÇÃO:** Só faça isso quando tiver certeza!

1. Edite a configuração:
   ```bash
   nano config/config.env
   ```

2. Mude para:
   ```
   SIMULATION_MODE=False
   ```

3. Salve e rode o bot:
   ```bash
   python3 bot.py
   ```

4. O bot vai pedir confirmação antes de iniciar

---

## 🧪 Testar Sem Rodar o Bot Completo

```bash
# Testar conexão
python3 tests/test_connection.py

# Testar busca de oportunidades
python3 tests/test_monitor.py

# Testar execução completa
python3 tests/test_full_execution.py

# Teste rápido (2 ciclos)
python3 test_bot_quick.py
```

---

## 🔄 Atualizar o Bot

Se eu fizer melhorias no código:

```bash
cd /root/bot-arbitragem-binance
git pull
```

---

## 💡 Dicas

1. **Sempre comece em modo simulação**
2. **Monitore os logs** para ver o que está acontecendo
3. **Comece com valores pequenos** quando for para modo real
4. **Não feche o terminal** enquanto o bot estiver rodando
5. **Anote suas estatísticas** para acompanhar o desempenho

---

## ❓ Comandos Úteis

```bash
# Ver se o bot está rodando
ps aux | grep bot.py

# Ver uso de memória
free -h

# Ver espaço em disco
df -h

# Desconectar do servidor (sem parar o bot)
# Use 'screen' ou 'tmux' (vou ensinar se precisar)
```

---

## 📞 Precisa de Ajuda?

Me chame que eu te ajudo! 😊

---

**Última atualização:** 28/10/2025
