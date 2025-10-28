#!/usr/bin/env python3
"""
Teste rápido do monitor (executa apenas 1 ciclo)
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório src ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir / 'src'))

from arbitrage_analyzer import ArbitrageAnalyzer

def test_single_scan():
    """Executa uma única varredura"""
    
    print("\n" + "="*70)
    print("TESTE DO MONITOR - VARREDURA ÚNICA")
    print("="*70)
    
    # Cria analisador
    analyzer = ArbitrageAnalyzer(base_currency='USDT', fee_percent=0.1)
    
    # Busca oportunidades
    opportunities = analyzer.find_profitable_opportunities(
        min_amount=100,
        min_profit=0
    )
    
    # Filtra por lucro mínimo
    min_profit_percent = 0.5
    filtered = [
        opp for opp in opportunities 
        if opp['profit_percent'] >= min_profit_percent
    ]
    
    print(f"\n📊 RESULTADOS:")
    print(f"   Total de oportunidades: {len(opportunities)}")
    print(f"   Acima de {min_profit_percent}%: {len(filtered)}")
    
    if filtered:
        print(f"\n🎯 TOP 5 OPORTUNIDADES:")
        for i, opp in enumerate(filtered[:5]):
            triangle = opp['triangle']
            print(f"\n   #{i+1} - {' → '.join(triangle['path'])}")
            print(f"        Pares: {', '.join(triangle['pairs'])}")
            print(f"        💰 Lucro: ${opp['profit']:.4f} ({opp['profit_percent']:.4f}%)")
    else:
        print(f"\n⚠️  Nenhuma oportunidade acima de {min_profit_percent}%")
        if opportunities:
            best = opportunities[0]
            print(f"   Melhor disponível: {best['profit_percent']:.4f}%")
    
    print("\n" + "="*70)
    print("✅ TESTE CONCLUÍDO!")
    print("="*70 + "\n")

if __name__ == "__main__":
    try:
        test_single_scan()
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
