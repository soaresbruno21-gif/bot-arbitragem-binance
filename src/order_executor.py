#!/usr/bin/env python3
"""
Módulo para execução de ordens de arbitragem triangular
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from binance.client import Client
from binance.enums import *
from dotenv import load_dotenv

# Carrega configurações
root_dir = Path(__file__).parent.parent
config_path = root_dir / 'config' / 'config.env'
load_dotenv(config_path)

class OrderExecutor:
    """Executor de ordens de arbitragem"""
    
    def __init__(self, simulation_mode=True):
        """
        Inicializa o executor
        
        Args:
            simulation_mode (bool): Se True, não executa ordens reais
        """
        self.simulation_mode = simulation_mode
        
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if not api_key or not api_secret:
            raise ValueError("Chaves da Binance não encontradas")
        
        self.client = Client(api_key, api_secret)
        
        # Log de operações
        self.log_file = root_dir / 'logs' / 'trades.log'
        self.log_file.parent.mkdir(exist_ok=True)
    
    def log(self, message):
        """Registra mensagem com timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        print(log_message)
        
        # Salva no arquivo
        with open(self.log_file, 'a') as f:
            f.write(log_message + '\n')
    
    def get_symbol_info(self, symbol):
        """
        Busca informações de um par
        
        Args:
            symbol (str): Símbolo do par (ex: BTCUSDT)
            
        Returns:
            dict: Informações do símbolo
        """
        try:
            info = self.client.get_symbol_info(symbol)
            return info
        except Exception as e:
            self.log(f"Erro ao buscar info de {symbol}: {str(e)}")
            return None
    
    def format_quantity(self, symbol, quantity):
        """
        Formata quantidade de acordo com as regras do par
        
        Args:
            symbol (str): Símbolo do par
            quantity (float): Quantidade a formatar
            
        Returns:
            str: Quantidade formatada
        """
        info = self.get_symbol_info(symbol)
        if not info:
            return str(quantity)
        
        # Busca precisão do LOT_SIZE
        for filter in info['filters']:
            if filter['filterType'] == 'LOT_SIZE':
                step_size = float(filter['stepSize'])
                
                # Calcula número de casas decimais
                precision = 0
                if step_size < 1:
                    step_str = str(step_size).rstrip('0')
                    if '.' in step_str:
                        precision = len(step_str.split('.')[1])
                
                # Arredonda para baixo
                quantity = float(quantity) - (float(quantity) % step_size)
                
                return f"{quantity:.{precision}f}"
        
        return str(quantity)
    
    def execute_arbitrage(self, opportunity, amount):
        """
        Executa arbitragem triangular
        
        Args:
            opportunity (dict): Oportunidade identificada
            amount (float): Valor em USDT para investir
            
        Returns:
            dict: Resultado da execução
        """
        triangle = opportunity['triangle']
        pairs = triangle['pairs']
        path = triangle['path']
        
        mode = "SIMULAÇÃO" if self.simulation_mode else "REAL"
        
        self.log("\n" + "="*70)
        self.log(f"EXECUTANDO ARBITRAGEM - MODO {mode}")
        self.log("="*70)
        self.log(f"Caminho: {' → '.join(path)}")
        self.log(f"Pares: {', '.join(pairs)}")
        self.log(f"Investimento: ${amount:.2f} USDT")
        self.log(f"Lucro esperado: ${opportunity['profit']:.4f} ({opportunity['profit_percent']:.4f}%)")
        
        results = {
            'success': False,
            'mode': mode,
            'path': path,
            'pairs': pairs,
            'initial_amount': amount,
            'final_amount': 0,
            'profit': 0,
            'orders': [],
            'errors': []
        }
        
        try:
            current_amount = amount
            current_asset = 'USDT'
            
            # Operação 1: USDT → Moeda A
            self.log(f"\n📍 Operação 1: Comprar {path[1]} com USDT")
            order1 = self._execute_order(
                symbol=pairs[0],
                side=SIDE_BUY,
                quantity_quote=current_amount,
                current_asset=current_asset
            )
            
            if not order1['success']:
                results['errors'].append(f"Operação 1 falhou: {order1.get('error', 'Erro desconhecido')}")
                return results
            
            results['orders'].append(order1)
            current_amount = order1['quantity_received']
            current_asset = path[1]
            self.log(f"✓ Recebido: {current_amount:.8f} {current_asset}")
            
            # Operação 2: Moeda A → Moeda B
            self.log(f"\n📍 Operação 2: Trocar {path[1]} por {path[2]}")
            order2 = self._execute_order(
                symbol=pairs[1],
                side=SIDE_SELL,
                quantity_base=current_amount,
                current_asset=current_asset
            )
            
            if not order2['success']:
                results['errors'].append(f"Operação 2 falhou: {order2.get('error', 'Erro desconhecido')}")
                return results
            
            results['orders'].append(order2)
            current_amount = order2['quantity_received']
            current_asset = path[2]
            self.log(f"✓ Recebido: {current_amount:.8f} {current_asset}")
            
            # Operação 3: Moeda B → USDT
            self.log(f"\n📍 Operação 3: Vender {path[2]} por USDT")
            order3 = self._execute_order(
                symbol=pairs[2],
                side=SIDE_SELL,
                quantity_base=current_amount,
                current_asset=current_asset
            )
            
            if not order3['success']:
                results['errors'].append(f"Operação 3 falhou: {order3.get('error', 'Erro desconhecido')}")
                return results
            
            results['orders'].append(order3)
            current_amount = order3['quantity_received']
            self.log(f"✓ Recebido: {current_amount:.8f} USDT")
            
            # Calcula resultado final
            results['final_amount'] = current_amount
            results['profit'] = current_amount - amount
            results['profit_percent'] = (results['profit'] / amount) * 100
            results['success'] = True
            
            self.log("\n" + "="*70)
            self.log(f"✅ ARBITRAGEM CONCLUÍDA COM SUCESSO!")
            self.log(f"Investido: ${amount:.2f} USDT")
            self.log(f"Retorno: ${current_amount:.2f} USDT")
            self.log(f"💰 Lucro: ${results['profit']:.4f} ({results['profit_percent']:.4f}%)")
            self.log("="*70)
            
        except Exception as e:
            error_msg = f"Erro na execução: {str(e)}"
            self.log(f"\n❌ {error_msg}")
            results['errors'].append(error_msg)
        
        return results
    
    def _execute_order(self, symbol, side, quantity_quote=None, quantity_base=None, current_asset=None):
        """
        Executa uma ordem individual
        
        Args:
            symbol (str): Par de negociação
            side (str): SIDE_BUY ou SIDE_SELL
            quantity_quote (float): Quantidade em moeda de cotação (para compra)
            quantity_base (float): Quantidade em moeda base (para venda)
            current_asset (str): Ativo atual
            
        Returns:
            dict: Resultado da ordem
        """
        result = {
            'success': False,
            'symbol': symbol,
            'side': side,
            'quantity_sent': 0,
            'quantity_received': 0,
            'price': 0,
            'order_id': None,
            'error': None
        }
        
        try:
            # Busca preço atual
            ticker = self.client.get_symbol_ticker(symbol=symbol)
            price = float(ticker['price'])
            result['price'] = price
            
            # Calcula quantidade
            if side == SIDE_BUY:
                # Comprando: usa quantity_quote (quanto vai gastar)
                quantity = quantity_quote / price
                result['quantity_sent'] = quantity_quote
            else:
                # Vendendo: usa quantity_base (quanto tem para vender)
                quantity = quantity_base
                result['quantity_sent'] = quantity_base
            
            # Formata quantidade (arredonda para baixo conforme regras)
            quantity_formatted = self.format_quantity(symbol, quantity)
            
            # Garante que não seja zero
            if float(quantity_formatted) == 0:
                # Usa quantidade mínima
                quantity_formatted = self.format_quantity(symbol, quantity * 1.01)
            
            if self.simulation_mode:
                # Modo simulação: apenas calcula
                self.log(f"   [SIMULAÇÃO] {side} {quantity_formatted} em {symbol} @ ${price:.8f}")
                
                if side == SIDE_BUY:
                    result['quantity_received'] = float(quantity_formatted)
                else:
                    result['quantity_received'] = float(quantity_formatted) * price
                
                result['success'] = True
                result['order_id'] = 'SIM_' + str(int(datetime.now().timestamp()))
                
            else:
                # Modo real: executa ordem de mercado
                self.log(f"   [REAL] Executando {side} {quantity_formatted} em {symbol}")
                
                order = self.client.create_order(
                    symbol=symbol,
                    side=side,
                    type=ORDER_TYPE_MARKET,
                    quantity=quantity_formatted
                )
                
                result['order_id'] = order['orderId']
                result['success'] = True
                
                # Calcula quantidade recebida
                executed_qty = float(order['executedQty'])
                if side == SIDE_BUY:
                    result['quantity_received'] = executed_qty
                else:
                    cummulative_quote_qty = float(order['cummulativeQuoteQty'])
                    result['quantity_received'] = cummulative_quote_qty
                
                self.log(f"   ✓ Ordem executada: ID {result['order_id']}")
            
        except Exception as e:
            result['error'] = str(e)
            self.log(f"   ❌ Erro: {str(e)}")
        
        return result


if __name__ == "__main__":
    """Teste do módulo"""
    
    print("\n" + "="*70)
    print("TESTE DO EXECUTOR DE ORDENS - MODO SIMULAÇÃO")
    print("="*70)
    
    # Cria executor em modo simulação
    executor = OrderExecutor(simulation_mode=True)
    
    # Simula uma oportunidade
    test_opportunity = {
        'triangle': {
            'path': ['USDT', 'BTC', 'ETH', 'USDT'],
            'pairs': ['BTCUSDT', 'ETHBTC', 'ETHUSDT']
        },
        'profit': 5.0,
        'profit_percent': 5.0
    }
    
    # Executa
    result = executor.execute_arbitrage(test_opportunity, amount=100)
    
    print("\n" + "="*70)
    if result['success']:
        print("✅ TESTE CONCLUÍDO COM SUCESSO!")
    else:
        print("❌ TESTE FALHOU")
        for error in result['errors']:
            print(f"   - {error}")
    print("="*70 + "\n")
