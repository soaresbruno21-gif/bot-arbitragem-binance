#!/usr/bin/env python3
"""
BOT DE ARBITRAGEM TRIANGULAR - BINANCE SPOT
Monitora e executa oportunidades de arbitragem automaticamente
"""

import os
import sys
import time
from pathlib import Path
from datetime import datetime
from dotenv import load_dotenv

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from arbitrage_analyzer import ArbitrageAnalyzer
from order_executor import OrderExecutor
from database import Database

class ArbitrageBot:
    """Bot de arbitragem triangular automatizado"""
    
    def __init__(self, config_file='config/config.env'):
        """
        Inicializa o bot
        
        Args:
            config_file (str): Caminho para arquivo de configuração
        """
        # Carrega configurações
        config_path = Path(__file__).parent / config_file
        load_dotenv(config_path)
        
        # Configurações do bot
        self.base_currency = os.getenv('BASE_CURRENCY', 'USDT')
        self.fee_percent = float(os.getenv('FEE_PERCENT', '0.1'))
        self.min_profit_percent = float(os.getenv('MIN_PROFIT_PERCENT', '0.5'))
        self.trade_amount = float(os.getenv('TRADE_AMOUNT_USDT', '100'))
        self.check_interval = int(os.getenv('CHECK_INTERVAL_SECONDS', '30'))
        self.simulation_mode = os.getenv('SIMULATION_MODE', 'True').lower() == 'true'
        
        # Componentes
        self.analyzer = ArbitrageAnalyzer(self.base_currency, self.fee_percent)
        self.executor = OrderExecutor(simulation_mode=self.simulation_mode)
        self.database = Database()
        
        # Estatísticas
        self.stats = {
            'cycles': 0,
            'opportunities_found': 0,
            'trades_executed': 0,
            'trades_successful': 0,
            'trades_failed': 0,
            'total_profit': 0,
            'total_invested': 0
        }
        
        self.running = False
    
    def log(self, message, level='INFO'):
        """Registra mensagem com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        
        # Salva em arquivo
        log_file = Path(__file__).parent / 'logs' / 'bot.log'
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def print_header(self):
        """Imprime cabeçalho do bot"""
        print("\n" + "="*70)
        print("BOT DE ARBITRAGEM TRIANGULAR - BINANCE SPOT")
        print("="*70)
        print(f"Modo: {'SIMULAÇÃO' if self.simulation_mode else '🔴 REAL 🔴'}")
        print(f"Moeda base: {self.base_currency}")
        print(f"Taxa por operação: {self.fee_percent}%")
        print(f"Lucro mínimo: {self.min_profit_percent}%")
        print(f"Valor por trade: ${self.trade_amount}")
        print(f"Intervalo de verificação: {self.check_interval}s")
        print("="*70)
        
        if not self.simulation_mode:
            print("\n⚠️  ATENÇÃO: MODO REAL ATIVADO!")
            print("⚠️  O bot executará ordens reais na Binance!")
            print("⚠️  Certifique-se de que está tudo correto!")
            print("\nPressione ENTER para continuar ou Ctrl+C para cancelar...")
            input()
    
    def print_stats(self):
        """Imprime estatísticas do bot"""
        print("\n" + "-"*70)
        print("ESTATÍSTICAS")
        print("-"*70)
        print(f"Ciclos executados: {self.stats['cycles']}")
        print(f"Oportunidades encontradas: {self.stats['opportunities_found']}")
        print(f"Trades executados: {self.stats['trades_executed']}")
        print(f"  - Sucesso: {self.stats['trades_successful']}")
        print(f"  - Falhas: {self.stats['trades_failed']}")
        
        if self.stats['total_invested'] > 0:
            roi = (self.stats['total_profit'] / self.stats['total_invested']) * 100
            print(f"Total investido: ${self.stats['total_invested']:.2f}")
            print(f"Lucro total: ${self.stats['total_profit']:.2f}")
            print(f"ROI: {roi:.2f}%")
        
        print("-"*70 + "\n")
    
    def run(self):
        """Executa o bot"""
        self.running = True
        self.print_header()
        
        self.log("Bot iniciado", "INFO")
        self.log(f"Modo: {'SIMULAÇÃO' if self.simulation_mode else 'REAL'}", "INFO")
        
        print("\n⏳ Iniciando monitoramento...")
        print("(Pressione Ctrl+C para parar)\n")
        
        try:
            while self.running:
                self.stats['cycles'] += 1
                
                self.log(f"Ciclo #{self.stats['cycles']} - Buscando oportunidades...", "INFO")
                
                try:
                    # Busca oportunidades
                    opportunities = self.analyzer.find_profitable_opportunities(
                        min_amount=self.trade_amount,
                        min_profit=0
                    )
                    
                    # Filtra por lucro mínimo
                    profitable = [
                        opp for opp in opportunities
                        if opp['profit_percent'] >= self.min_profit_percent
                    ]
                    
                    if profitable:
                        self.stats['opportunities_found'] += len(profitable)
                        
                        # Salva oportunidades no banco
                        for opp in profitable[:5]:  # Salva top 5
                            self.database.save_opportunity({
                                'path': ' → '.join(opp['triangle']['path']),
                                'profit_percent': opp['profit_percent'],
                                'symbols': [
                                    opp['triangle']['pairs'][0],
                                    opp['triangle']['pairs'][1],
                                    opp['triangle']['pairs'][2]
                                ]
                            })
                        
                        # Pega a melhor
                        best = profitable[0]
                        
                        self.log(
                            f"🎯 Oportunidade encontrada! " +
                            f"{' → '.join(best['triangle']['path'])} " +
                            f"({best['profit_percent']:.2f}%)",
                            "SUCCESS"
                        )
                        
                        # Executa
                        self.log("Executando arbitragem...", "INFO")
                        result = self.executor.execute_arbitrage(best, self.trade_amount)
                        
                        self.stats['trades_executed'] += 1
                        
                        if result['success']:
                            self.stats['trades_successful'] += 1
                            self.stats['total_invested'] += result['initial_amount']
                            self.stats['total_profit'] += result['profit']
                            
                            # Salva trade no banco
                            self.database.save_trade({
                                'path': ' → '.join(best['triangle']['path']),
                                'initial_amount': result['initial_amount'],
                                'final_amount': result['final_amount'],
                                'profit_amount': result['profit'],
                                'profit_percent': result['profit_percent'],
                                'step1': result['steps'][0],
                                'step2': result['steps'][1],
                                'step3': result['steps'][2],
                                'simulation_mode': self.simulation_mode
                            })
                            
                            self.log(
                                f"✅ Trade executado! Lucro: ${result['profit']:.2f} ({result['profit_percent']:.2f}%)",
                                "SUCCESS"
                            )
                        else:
                            self.stats['trades_failed'] += 1
                            self.log(f"❌ Trade falhou: {result['errors']}", "ERROR")
                    
                    else:
                        self.log(
                            f"Nenhuma oportunidade acima de {self.min_profit_percent}%",
                            "INFO"
                        )
                        
                        # Mostra a melhor disponível
                        if opportunities:
                            best = opportunities[0]
                            self.log(
                                f"Melhor disponível: {best['profit_percent']:.2f}% - " +
                                f"{' → '.join(best['triangle']['path'])}",
                                "INFO"
                            )
                
                except Exception as e:
                    self.log(f"Erro no ciclo: {str(e)}", "ERROR")
                
                # Mostra estatísticas a cada 10 ciclos
                if self.stats['cycles'] % 10 == 0:
                    self.print_stats()
                
                # Aguarda próximo ciclo
                self.log(f"Aguardando {self.check_interval}s...\n", "INFO")
                time.sleep(self.check_interval)
        
        except KeyboardInterrupt:
            self.log("\n🛑 Bot interrompido pelo usuário", "INFO")
            self.running = False
        
        except Exception as e:
            self.log(f"Erro fatal: {str(e)}", "ERROR")
            import traceback
            traceback.print_exc()
        
        finally:
            self.log("Bot finalizado", "INFO")
            self.print_stats()


if __name__ == "__main__":
    """Executa o bot"""
    
    try:
        bot = ArbitrageBot()
        bot.run()
        
    except Exception as e:
        print(f"\n❌ ERRO FATAL: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
