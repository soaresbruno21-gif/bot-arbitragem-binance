#!/usr/bin/env python3
"""
Monitor em tempo real de oportunidades de arbitragem
"""

import os
import sys
import time
from datetime import datetime
from pathlib import Path
from arbitrage_analyzer import ArbitrageAnalyzer

class ArbitrageMonitor:
    """Monitor de oportunidades de arbitragem em tempo real"""
    
    def __init__(self, base_currency='USDT', fee_percent=0.1, 
                 min_profit_percent=0.5, check_interval=10):
        """
        Inicializa o monitor
        
        Args:
            base_currency (str): Moeda base
            fee_percent (float): Taxa por operação em %
            min_profit_percent (float): Lucro mínimo em % para alertar
            check_interval (int): Intervalo entre verificações em segundos
        """
        self.base_currency = base_currency
        self.fee_percent = fee_percent
        self.min_profit_percent = min_profit_percent
        self.check_interval = check_interval
        self.analyzer = ArbitrageAnalyzer(base_currency, fee_percent)
        self.running = False
        
    def log(self, message):
        """Registra mensagem com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] {message}")
    
    def start(self, amount=100, top_opportunities=5):
        """
        Inicia o monitoramento contínuo
        
        Args:
            amount (float): Valor para simular
            top_opportunities (int): Quantas oportunidades mostrar
        """
        self.running = True
        
        print("\n" + "="*70)
        print("MONITOR DE ARBITRAGEM TRIANGULAR - BINANCE SPOT")
        print("="*70)
        print(f"Moeda base: {self.base_currency}")
        print(f"Taxa por operação: {self.fee_percent}%")
        print(f"Lucro mínimo: {self.min_profit_percent}%")
        print(f"Valor simulado: ${amount}")
        print(f"Intervalo de verificação: {self.check_interval}s")
        print("="*70)
        print("\n⏳ Iniciando monitoramento...")
        print("(Pressione Ctrl+C para parar)\n")
        
        cycle = 0
        
        try:
            while self.running:
                cycle += 1
                
                self.log(f"Ciclo #{cycle} - Buscando oportunidades...")
                
                try:
                    # Busca oportunidades
                    opportunities = self.analyzer.find_profitable_opportunities(
                        min_amount=amount,
                        min_profit=0
                    )
                    
                    # Filtra por lucro mínimo percentual
                    filtered = [
                        opp for opp in opportunities 
                        if opp['profit_percent'] >= self.min_profit_percent
                    ]
                    
                    if filtered:
                        self.log(f"🎯 {len(filtered)} oportunidades encontradas acima de {self.min_profit_percent}%!")
                        self.display_top_opportunities(filtered, top_opportunities)
                    else:
                        self.log(f"⚠️  Nenhuma oportunidade acima de {self.min_profit_percent}% no momento")
                        
                        # Mostra a melhor mesmo que abaixo do mínimo
                        if opportunities:
                            best = opportunities[0]
                            self.log(f"   Melhor disponível: {best['profit_percent']:.4f}% - {' → '.join(best['triangle']['path'])}")
                    
                except Exception as e:
                    self.log(f"❌ Erro na análise: {str(e)}")
                
                # Aguarda próximo ciclo
                self.log(f"⏸️  Aguardando {self.check_interval}s para próxima verificação...\n")
                time.sleep(self.check_interval)
                
        except KeyboardInterrupt:
            self.log("\n\n🛑 Monitoramento interrompido pelo usuário")
            self.running = False
    
    def display_top_opportunities(self, opportunities, top=5):
        """
        Exibe as melhores oportunidades
        
        Args:
            opportunities (list): Lista de oportunidades
            top (int): Quantas mostrar
        """
        print("\n" + "-"*70)
        print(f"TOP {min(top, len(opportunities))} OPORTUNIDADES")
        print("-"*70)
        
        for i, opp in enumerate(opportunities[:top]):
            triangle = opp['triangle']
            
            print(f"\n  #{i+1} - {' → '.join(triangle['path'])}")
            print(f"       Pares: {', '.join(triangle['pairs'])}")
            print(f"       💰 Lucro: ${opp['profit']:.4f} ({opp['profit_percent']:.4f}%)")
        
        print("-"*70 + "\n")


if __name__ == "__main__":
    """Executa o monitor"""
    
    try:
        # Configurações
        monitor = ArbitrageMonitor(
            base_currency='USDT',
            fee_percent=0.1,
            min_profit_percent=0.5,  # Alerta apenas se lucro >= 0.5%
            check_interval=30  # Verifica a cada 30 segundos
        )
        
        # Inicia monitoramento
        monitor.start(amount=100, top_opportunities=5)
        
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
