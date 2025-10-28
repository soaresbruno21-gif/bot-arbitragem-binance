#!/usr/bin/env python3
"""
Módulo para análise de oportunidades de arbitragem com cálculo de taxas
"""

import os
import sys
from pathlib import Path
from triangle_finder import TriangleFinder

class ArbitrageAnalyzer:
    """Classe para analisar oportunidades de arbitragem"""
    
    def __init__(self, base_currency='USDT', fee_percent=0.1):
        """
        Inicializa o analisador
        
        Args:
            base_currency (str): Moeda base
            fee_percent (float): Taxa por operação em % (padrão Binance: 0.1%)
        """
        self.base_currency = base_currency
        self.fee_percent = fee_percent
        self.finder = TriangleFinder(base_currency)
        
    def calculate_with_fees(self, triangle, amount=100):
        """
        Calcula lucro considerando as taxas da exchange
        
        Args:
            triangle (dict): Informações do triângulo
            amount (float): Valor inicial
            
        Returns:
            dict: Resultado com lucro líquido após taxas
        """
        try:
            pair1, pair2, pair3 = triangle['pairs']
            
            # Verifica se temos os preços
            if (pair1 not in self.finder.prices or 
                pair2 not in self.finder.prices or 
                pair3 not in self.finder.prices):
                return None
            
            price1 = self.finder.prices[pair1]
            price2 = self.finder.prices[pair2]
            price3 = self.finder.prices[pair3]
            
            if price1 == 0 or price2 == 0 or price3 == 0:
                return None
            
            # Taxa por operação (0.1% = 0.001)
            fee_multiplier = 1 - (self.fee_percent / 100)
            
            # Operação 1: Comprar coin_a com base_currency
            amount_after_fee1 = amount * fee_multiplier
            amount_coin_a = amount_after_fee1 / price1
            
            # Operação 2: Trocar coin_a por coin_b
            amount_after_fee2 = amount_coin_a * fee_multiplier
            amount_coin_b = amount_after_fee2 * price2
            
            # Operação 3: Vender coin_b por base_currency
            amount_after_fee3 = amount_coin_b * fee_multiplier
            final_amount = amount_after_fee3 * price3
            
            # Calcula lucro líquido
            profit = final_amount - amount
            profit_percent = (profit / amount) * 100
            
            # Calcula total de taxas pagas
            total_fees = amount - final_amount - profit
            
            return {
                'initial': amount,
                'final': final_amount,
                'profit': profit,
                'profit_percent': profit_percent,
                'total_fees': abs(total_fees),
                'prices': [price1, price2, price3],
                'triangle': triangle
            }
            
        except Exception as e:
            return None
    
    def find_profitable_opportunities(self, min_amount=100, min_profit=0):
        """
        Encontra oportunidades lucrativas após descontar taxas
        
        Args:
            min_amount (float): Valor mínimo para simular
            min_profit (float): Lucro mínimo em $ (padrão: qualquer lucro > 0)
            
        Returns:
            list: Lista de oportunidades ordenadas por lucro
        """
        print(f"\n{'='*70}")
        print(f"ANÁLISE DE OPORTUNIDADES DE ARBITRAGEM")
        print(f"{'='*70}")
        print(f"Moeda base: {self.base_currency}")
        print(f"Taxa por operação: {self.fee_percent}%")
        print(f"Valor simulado: ${min_amount}")
        print(f"Lucro mínimo: ${min_profit}")
        
        # Carrega dados do mercado
        self.finder.load_market_data()
        
        # Busca triângulos
        triangles = self.finder.find_triangles()
        
        print(f"\n⏳ Analisando {len(triangles)} triângulos...")
        
        # Analisa cada triângulo
        opportunities = []
        
        for triangle in triangles:
            result = self.calculate_with_fees(triangle, min_amount)
            
            if result and result['profit'] > min_profit:
                opportunities.append(result)
        
        # Ordena por lucro (maior primeiro)
        opportunities.sort(key=lambda x: x['profit'], reverse=True)
        
        return opportunities
    
    def display_opportunities(self, opportunities, top=10):
        """
        Exibe as melhores oportunidades
        
        Args:
            opportunities (list): Lista de oportunidades
            top (int): Quantas mostrar
        """
        if not opportunities:
            print(f"\n❌ Nenhuma oportunidade lucrativa encontrada no momento")
            return
        
        print(f"\n✅ {len(opportunities)} oportunidades lucrativas encontradas!")
        print(f"\n{'='*70}")
        print(f"TOP {min(top, len(opportunities))} MELHORES OPORTUNIDADES")
        print(f"{'='*70}")
        
        for i, opp in enumerate(opportunities[:top]):
            triangle = opp['triangle']
            
            print(f"\n🔸 Oportunidade #{i+1}")
            print(f"   Caminho: {' → '.join(triangle['path'])}")
            print(f"   Pares: {', '.join(triangle['pairs'])}")
            print(f"   ")
            print(f"   Investimento: ${opp['initial']:.2f}")
            print(f"   Retorno: ${opp['final']:.2f}")
            print(f"   Taxas pagas: ${opp['total_fees']:.4f}")
            print(f"   💰 Lucro líquido: ${opp['profit']:.4f} ({opp['profit_percent']:.4f}%)")


if __name__ == "__main__":
    """Teste do módulo"""
    
    try:
        # Cria analisador
        analyzer = ArbitrageAnalyzer(base_currency='USDT', fee_percent=0.1)
        
        # Busca oportunidades lucrativas
        opportunities = analyzer.find_profitable_opportunities(
            min_amount=100,
            min_profit=0  # Qualquer lucro > 0
        )
        
        # Exibe as melhores
        analyzer.display_opportunities(opportunities, top=10)
        
        print(f"\n{'='*70}")
        print(f"✅ ANÁLISE CONCLUÍDA!")
        print(f"{'='*70}\n")
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
