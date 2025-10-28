import mysql.connector
from mysql.connector import Error
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv('config/config.env')

class Database:
    def __init__(self):
        self.connection = None
        self.connect()
    
    def connect(self):
        """Conecta ao banco de dados MySQL"""
        try:
            # Parse da URL de conexão
            db_url = os.getenv('DATABASE_URL')
            if not db_url:
                # Usar URL hardcoded como fallback
                db_url = 'mysql://4L7JSaogBTaENVd.root:8WhKCU3v58e8SV0xMwtr@gateway02.us-east-1.prod.aws.tidbcloud.com:4000/6PL7EYXJU5qC4D6yXv3KLA'
                print("[Database] Usando DATABASE_URL padrão")
            
            # Extrair componentes da URL
            # mysql://user:pass@host:port/database?ssl=...
            parts = db_url.replace('mysql://', '').split('@')
            user_pass = parts[0].split(':')
            host_db = parts[1].split('/')
            host_port = host_db[0].split(':')
            database = host_db[1].split('?')[0]
            
            user = user_pass[0]
            password = user_pass[1]
            host = host_port[0]
            port = int(host_port[1])
            
            self.connection = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                ssl_ca=None,
                ssl_verify_cert=False
            )
            
            if self.connection.is_connected():
                print("[Database] ✓ Conectado ao banco de dados")
                return True
        except Error as e:
            print(f"[Database] ✗ Erro ao conectar: {e}")
            self.connection = None
            return False
    
    def ensure_connection(self):
        """Garante que a conexão está ativa"""
        if not self.connection or not self.connection.is_connected():
            self.connect()
        return self.connection and self.connection.is_connected()
    
    def save_opportunity(self, opportunity):
        """Salva uma oportunidade encontrada"""
        if not self.ensure_connection():
            return False
        
        try:
            cursor = self.connection.cursor()
            
            query = """
            INSERT INTO opportunities 
            (path, pairs, profitPercent, createdAt)
            VALUES (%s, %s, %s, %s)
            """
            
            # Concatenar símbolos em um texto
            pairs_text = ','.join(opportunity['symbols'])
            
            values = (
                opportunity['path'],
                pairs_text,
                int(opportunity['profit_percent'] * 100),  # Converter para basis points
                datetime.now()
            )
            
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"[Database] Erro ao salvar oportunidade: {e}")
            return False
    
    def save_trade(self, trade_data):
        """Salva um trade executado"""
        print("[Database] Tentando salvar trade...")
        if not self.ensure_connection():
            print("[Database] Falha na conexão")
            return False
        
        try:
            print(f"[Database] Dados do trade: {trade_data['path']}")
            cursor = self.connection.cursor()
            
            query = """
            INSERT INTO trade_history 
            (path, pairs, initialAmount, finalAmount, profit, profitPercent, 
             simulationMode, success, createdAt)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            
            # Criar pairs text
            pairs_text = f"{trade_data['step1']['symbol']},{trade_data['step2']['symbol']},{trade_data['step3']['symbol']}"
            
            values = (
                trade_data['path'],
                pairs_text,
                int(trade_data['initial_amount'] * 100),  # Converter para centavos
                int(trade_data['final_amount'] * 100),
                int(trade_data['profit_amount'] * 100),
                int(trade_data['profit_percent'] * 100),  # Converter para basis points
                trade_data.get('simulation_mode', True),
                True,  # success
                datetime.now()
            )
            
            print(f"[Database] Executando query...")
            cursor.execute(query, values)
            self.connection.commit()
            cursor.close()
            print("[Database] ✓ Trade salvo com sucesso!")
            return True
        except Error as e:
            print(f"[Database] ✗ Erro ao salvar trade: {e}")
            return False
    
    def get_config(self):
        """Busca configurações do banco"""
        if not self.ensure_connection():
            return None
        
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM botConfig WHERE id = 1")
            config = cursor.fetchone()
            cursor.close()
            return config
        except Error as e:
            print(f"[Database] Erro ao buscar config: {e}")
            return None
    
    def update_bot_status(self, is_running):
        """Atualiza o status do bot"""
        if not self.ensure_connection():
            return False
        
        try:
            cursor = self.connection.cursor()
            query = "UPDATE botConfig SET isRunning = %s, updatedAt = %s WHERE id = 1"
            cursor.execute(query, (is_running, datetime.now()))
            self.connection.commit()
            cursor.close()
            return True
        except Error as e:
            print(f"[Database] Erro ao atualizar status: {e}")
            return False
    
    def close(self):
        """Fecha a conexão com o banco"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("[Database] Conexão fechada")
