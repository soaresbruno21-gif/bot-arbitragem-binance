#!/usr/bin/env python3
"""
Módulo para identificar triângulos de arbitragem no mercado spot
"""

import os
import sys
from pathlib import Path
from market_data import MarketData

class TriangleFinder:
    """Classe para encontrar triângulos de arbitragem"""
    
    def __init__(self, base_currency='USDT'):
        """
        Inicializa o buscador de triângulos
        
        Args:
            base_currency (str): Moeda base para começar e terminar (ex: USDT)
        """
        self.base_currency = base_currency
        self.market = MarketData()
        self.symbols = []
        self.prices = {}
        
    def load_market_data(self):
        """Carrega dados do mercado"""
        print(f"⏳ Carregando pares do mercado...")
        self.symbols = self.market.get_spot_symbols()
        print(f"✓ {len(self.symbols)} pares carregados")
        
        print(f"⏳ Carregando preços...")
        self.prices = self.market.get_prices()
        print(f"✓ {len(self.prices)} preços carregados")
    
    def find_triangles(self):
        """
        Encontra todos os triângulos possíveis começando com a moeda base
        
        Returns:
            list: Lista de triângulos encontrados
        """
        triangles = []
        
        # Cria índice de pares por moeda
        pairs_by_base = {}
        pairs_by_quote = {}
        
        for symbol_info in self.symbols:
            base = symbol_info['base']
            quote = symbol_info['quote']
            symbol = symbol_info['symbol']
            
            if base not in pairs_by_base:
                pairs_by_base[base] = []
            pairs_by_base[base].append(symbol_info)
            
            if quote not in pairs_by_quote:
                pairs_by_quote[quote] = []
            pairs_by_quote[quote].append(symbol_info)
        
        # Busca triângulos começando com base_currency
        print(f"\n⏳ Buscando triângulos começando com {self.base_currency}...")
        
        # Passo 1: base_currency -> moeda A
        if self.base_currency in pairs_by_quote:
            for pair1 in pairs_by_quote[self.base_currency]:
                coin_a = pair1['base']  # Primeira moeda
                
                # Passo 2: moeda A -> moeda B
                if coin_a in pairs_by_base:
                    for pair2 in pairs_by_base[coin_a]:
                        coin_b = pair2['quote']  # Segunda moeda
                        
                        # Passo 3: moeda B -> base_currency (volta para o início)
                        if coin_b in pairs_by_base:
                            for pair3 in pairs_by_base[coin_b]:
                                if pair3['quote'] == self.base_currency:
                                    # Encontrou um triângulo!
                                    triangle = {
                                        'path': [self.base_currency, coin_a, coin_b, self.base_currency],
                                        'pairs': [pair1['symbol'], pair2['symbol'], pair3['symbol']],
                                        'operations': [
                                            f"Comprar {coin_a} com {self.base_currency}",
                                            f"Trocar {coin_a} por {coin_b}",
                                            f"Vender {coin_b} por {self.base_currency}"
                                        ]
                                    }
                                    triangles.append(triangle)
        
        return triangles
    
    def calculate_profit(self, triangle, amount=100):
        """
        Calcula o lucro potencial de um triângulo
        
        Args:
            triangle (dict): Informações do triângulo
            amount (float): Valor inicial em base_currency
            
        Returns:
            dict: Resultado com lucro e percentual
        """
        try:
            pair1, pair2, pair3 = triangle['pairs']
            
            # Verifica se temos os preços
            if pair1 not in self.prices or pair2 not in self.prices or pair3 not in self.prices:
                return None
            
            price1 = self.prices[pair1]
            price2 = self.prices[pair2]
            price3 = self.prices[pair3]
            
            if price1 == 0 or price2 == 0 or price3 == 0:
                return None
            
            # Simula as operações
            # Operação 1: Comprar coin_a com base_currency
            amount_coin_a = amount / price1
            
            # Operação 2: Trocar coin_a por coin_b
            amount_coin_b = amount_coin_a * price2
            
            # Operação 3: Vender coin_b por base_currency
            final_amount = amount_coin_b * price3
            
            # Calcula lucro
            profit = final_amount - amount
            profit_percent = (profit / amount) * 100
            
            return {
                'initial': amount,
                'final': final_amount,
                'profit': profit,
                'profit_percent': profit_percent,
                'prices': [price1, price2, price3]
            }
            
        except Exception as e:
            return None


if __name__ == "__main__":
    """Teste do módulo"""
    
    print("=" * 70)
    print("TESTE - BUSCA DE TRIÂNGULOS DE ARBITRAGEM")
    print("=" * 70)
    
    try:
        finder = TriangleFinder(base_currency='USDT')
        
        # Carrega dados do mercado
        finder.load_market_data()
        
        # Busca triângulos
        triangles = finder.find_triangles()
        
        print(f"\n✅ {len(triangles)} triângulos encontrados!")
        
        # Mostra alguns exemplos
        print(f"\n📊 Exemplos de triângulos (primeiros 5):")
        for i, triangle in enumerate(triangles[:5]):
            print(f"\n  Triângulo {i+1}:")
            print(f"    Caminho: {' → '.join(triangle['path'])}")
            print(f"    Pares: {', '.join(triangle['pairs'])}")
            
            # Calcula lucro potencial
            result = finder.calculate_profit(triangle, amount=100)
            if result:
                print(f"    Lucro simulado (com $100): ${result['profit']:.4f} ({result['profit_percent']:.4f}%)")
        
        print("\n" + "=" * 70)
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
        print("=" * 70)
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
