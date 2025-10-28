#!/usr/bin/env python3
"""
Teste rápido do bot - executa apenas 2 ciclos
"""

import os
import sys
import time
from pathlib import Path

# Força modo simulação
os.environ['SIMULATION_MODE'] = 'True'
os.environ['CHECK_INTERVAL_SECONDS'] = '5'

# Importa bot
sys.path.insert(0, str(Path(__file__).parent))
from bot import ArbitrageBot

if __name__ == "__main__":
    print("\n" + "="*70)
    print("TESTE RÁPIDO DO BOT - 2 CICLOS")
    print("="*70)
    
    bot = ArbitrageBot()
    bot.check_interval = 5  # 5 segundos entre ciclos
    
    # Executa apenas 2 ciclos
    bot.running = True
    
    for i in range(2):
        bot.stats['cycles'] += 1
        
        bot.log(f"Ciclo #{bot.stats['cycles']} - Buscando oportunidades...", "INFO")
        
        try:
            opportunities = bot.analyzer.find_profitable_opportunities(
                min_amount=bot.trade_amount,
                min_profit=0
            )
            
            profitable = [
                opp for opp in opportunities
                if opp['profit_percent'] >= bot.min_profit_percent
            ]
            
            if profitable:
                bot.stats['opportunities_found'] += len(profitable)
                best = profitable[0]
                
                bot.log(
                    f"🎯 Oportunidade encontrada! " +
                    f"{' → '.join(best['triangle']['path'])} " +
                    f"({best['profit_percent']:.2f}%)",
                    "SUCCESS"
                )
                
                bot.log("Executando arbitragem...", "INFO")
                result = bot.executor.execute_arbitrage(best, bot.trade_amount)
                
                bot.stats['trades_executed'] += 1
                
                if result['success']:
                    bot.stats['trades_successful'] += 1
                    bot.stats['total_invested'] += result['initial_amount']
                    bot.stats['total_profit'] += result['profit']
                    
                    bot.log(
                        f"✅ Trade executado! Lucro: ${result['profit']:.2f} ({result['profit_percent']:.2f}%)",
                        "SUCCESS"
                    )
                else:
                    bot.stats['trades_failed'] += 1
                    bot.log(f"❌ Trade falhou: {result['errors']}", "ERROR")
            else:
                bot.log(
                    f"Nenhuma oportunidade acima de {bot.min_profit_percent}%",
                    "INFO"
                )
                if opportunities:
                    best = opportunities[0]
                    bot.log(
                        f"Melhor disponível: {best['profit_percent']:.2f}% - " +
                        f"{' → '.join(best['triangle']['path'])}",
                        "INFO"
                    )
        
        except Exception as e:
            bot.log(f"Erro no ciclo: {str(e)}", "ERROR")
        
        if i < 1:  # Não aguarda após o último ciclo
            bot.log(f"Aguardando {bot.check_interval}s...\n", "INFO")
            time.sleep(bot.check_interval)
    
    bot.print_stats()
    
    print("\n" + "="*70)
    print("✅ TESTE RÁPIDO CONCLUÍDO!")
    print("="*70 + "\n")
