#!/usr/bin/env python3
"""
Teste completo: busca oportunidade real e simula execução
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório src ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir / 'src'))

from arbitrage_analyzer import ArbitrageAnalyzer
from order_executor import OrderExecutor

def test_full_cycle():
    """Testa ciclo completo: análise + execução"""
    
    print("\n" + "="*70)
    print("TESTE COMPLETO - ANÁLISE + EXECUÇÃO SIMULADA")
    print("="*70)
    
    # 1. Busca oportunidades
    print("\n📊 Etapa 1: Buscando oportunidades...")
    analyzer = ArbitrageAnalyzer(base_currency='USDT', fee_percent=0.1)
    
    opportunities = analyzer.find_profitable_opportunities(
        min_amount=100,
        min_profit=0
    )
    
    if not opportunities:
        print("❌ Nenhuma oportunidade encontrada")
        return False
    
    # Pega a melhor oportunidade
    best = opportunities[0]
    
    print(f"\n✅ Melhor oportunidade encontrada:")
    print(f"   Caminho: {' → '.join(best['triangle']['path'])}")
    print(f"   Lucro esperado: ${best['profit']:.4f} ({best['profit_percent']:.4f}%)")
    
    # 2. Executa em modo simulação
    print(f"\n🔄 Etapa 2: Executando em modo simulação...")
    executor = OrderExecutor(simulation_mode=True)
    
    result = executor.execute_arbitrage(best, amount=100)
    
    # 3. Verifica resultado
    print(f"\n📈 Etapa 3: Verificando resultado...")
    
    if result['success']:
        print(f"✅ Execução simulada concluída com sucesso!")
        print(f"\n   Resumo:")
        print(f"   - Investido: ${result['initial_amount']:.2f}")
        print(f"   - Retorno: ${result['final_amount']:.2f}")
        print(f"   - Lucro: ${result['profit']:.4f} ({result['profit_percent']:.4f}%)")
        print(f"   - Ordens executadas: {len(result['orders'])}")
        
        return True
    else:
        print(f"❌ Execução falhou:")
        for error in result['errors']:
            print(f"   - {error}")
        return False

if __name__ == "__main__":
    try:
        success = test_full_cycle()
        
        print("\n" + "="*70)
        if success:
            print("✅ TESTE COMPLETO PASSOU!")
        else:
            print("❌ TESTE COMPLETO FALHOU")
        print("="*70 + "\n")
        
        sys.exit(0 if success else 1)
        
    except Exception as e:
        print(f"\n❌ ERRO: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
