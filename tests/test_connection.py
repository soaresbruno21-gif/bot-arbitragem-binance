#!/usr/bin/env python3
"""
Teste de conexão com a Binance
Verifica se as chaves API estão funcionando
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

from binance.client import Client
from dotenv import load_dotenv

# Carrega as configurações
config_path = root_dir / 'config' / 'config.env'
load_dotenv(config_path)

def test_connection():
    """Testa a conexão com a Binance"""
    
    print("=" * 50)
    print("TESTE DE CONEXÃO COM BINANCE")
    print("=" * 50)
    
    # Pega as chaves do arquivo de configuração
    api_key = os.getenv('BINANCE_API_KEY')
    api_secret = os.getenv('BINANCE_API_SECRET')
    
    if not api_key or not api_secret:
        print("❌ ERRO: Chaves não encontradas no arquivo config.env")
        return False
    
    print(f"\n✓ Chaves carregadas")
    print(f"  API Key: {api_key[:10]}...")
    
    try:
        # Cria conexão com a Binance
        print("\n⏳ Conectando na Binance...")
        client = Client(api_key, api_secret)
        
        # Testa pegando o status da conta
        print("⏳ Verificando status da conta...")
        account = client.get_account()
        
        print("\n✅ CONEXÃO ESTABELECIDA COM SUCESSO!")
        print(f"\n📊 Informações da conta:")
        print(f"  - Pode fazer trades: {account['canTrade']}")
        print(f"  - Pode fazer saques: {account['canWithdraw']}")
        print(f"  - Pode fazer depósitos: {account['canDeposit']}")
        
        # Mostra alguns saldos (apenas os que têm valor)
        print(f"\n💰 Saldos disponíveis:")
        balances = [b for b in account['balances'] if float(b['free']) > 0 or float(b['locked']) > 0]
        
        if balances:
            for balance in balances[:5]:  # Mostra apenas os 5 primeiros
                free = float(balance['free'])
                locked = float(balance['locked'])
                if free > 0 or locked > 0:
                    print(f"  - {balance['asset']}: {free:.8f} (livre) + {locked:.8f} (bloqueado)")
        else:
            print("  Nenhum saldo encontrado")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERRO NA CONEXÃO:")
        print(f"  {str(e)}")
        return False

if __name__ == "__main__":
    success = test_connection()
    print("\n" + "=" * 50)
    
    if success:
        print("Status: PRONTO PARA PRÓXIMA ETAPA ✅")
    else:
        print("Status: VERIFICAR CONFIGURAÇÕES ❌")
    
    print("=" * 50)
    sys.exit(0 if success else 1)
