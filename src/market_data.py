#!/usr/bin/env python3
"""
Módulo para buscar dados do mercado spot da Binance
"""

import os
import sys
from pathlib import Path
from binance.client import Client
from dotenv import load_dotenv

# Carrega configurações
root_dir = Path(__file__).parent.parent
config_path = root_dir / 'config' / 'config.env'
load_dotenv(config_path)

class MarketData:
    """Classe para gerenciar dados do mercado"""
    
    def __init__(self):
        """Inicializa conexão com Binance"""
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            raise ValueError("Chaves da Binance não encontradas")
        
        self.client = Client(api_key, api_secret)
    
    def get_spot_symbols(self):
        """
        Busca todos os pares do mercado SPOT que estão ativos
        
        Returns:
            list: Lista de dicionários com informações dos pares
        """
        try:
            # Busca informações de todos os pares
            exchange_info = self.client.get_exchange_info()
            
            # Filtra apenas pares SPOT que estão em negociação
            spot_symbols = []
            
            for symbol_info in exchange_info['symbols']:
                # Verifica se é SPOT e está ativo
                if (symbol_info['status'] == 'TRADING' and 
                    symbol_info.get('isSpotTradingAllowed', False)):
                    
                    spot_symbols.append({
                        'symbol': symbol_info['symbol'],
                        'base': symbol_info['baseAsset'],      # Ex: BTC
                        'quote': symbol_info['quoteAsset'],    # Ex: USDT
                        'active': True
                    })
            
            return spot_symbols
            
        except Exception as e:
            print(f"Erro ao buscar pares: {str(e)}")
            return []
    
    def get_prices(self, symbols=None):
        """
        Busca preços atuais dos pares
        
        Args:
            symbols (list): Lista de símbolos. Se None, busca todos
            
        Returns:
            dict: Dicionário {símbolo: preço}
        """
        try:
            # Busca todos os preços
            all_prices = self.client.get_all_tickers()
            
            # Converte para dicionário
            prices = {item['symbol']: float(item['price']) for item in all_prices}
            
            # Se foi especificado símbolos, filtra
            if symbols:
                prices = {s: prices.get(s, 0) for s in symbols}
            
            return prices
            
        except Exception as e:
            print(f"Erro ao buscar preços: {str(e)}")
            return {}


if __name__ == "__main__":
    """Teste do módulo"""
    
    print("=" * 60)
    print("TESTE - BUSCA DE PARES DO MERCADO SPOT")
    print("=" * 60)
    
    try:
        market = MarketData()
        
        print("\n⏳ Buscando pares do mercado spot...")
        symbols = market.get_spot_symbols()
        
        print(f"\n✅ {len(symbols)} pares encontrados!")
        
        # Mostra alguns exemplos
        print("\n📊 Exemplos de pares (primeiros 10):")
        for i, symbol in enumerate(symbols[:10]):
            print(f"  {i+1}. {symbol['symbol']:12} - {symbol['base']:6} / {symbol['quote']}")
        
        # Busca preços de alguns pares
        print("\n⏳ Buscando preços de alguns pares...")
        test_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
        prices = market.get_prices(test_symbols)
        
        print("\n💰 Preços atuais:")
        for symbol, price in prices.items():
            if price > 0:
                print(f"  {symbol:12} = ${price:,.2f}")
        
        print("\n" + "=" * 60)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        sys.exit(1)
