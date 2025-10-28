#!/usr/bin/env python3
"""
Teste de validação do código
Verifica se tudo está configurado corretamente sem precisar conectar na Binance
"""

import os
import sys
from pathlib import Path

# Adiciona o diretório raiz ao path
root_dir = Path(__file__).parent.parent
sys.path.insert(0, str(root_dir))

def test_structure():
    """Testa se a estrutura do projeto está correta"""
    
    print("=" * 50)
    print("TESTE DE VALIDAÇÃO DO CÓDIGO")
    print("=" * 50)
    
    all_ok = True
    
    # Testa estrutura de pastas
    print("\n📁 Verificando estrutura de pastas...")
    required_dirs = ['src', 'config', 'logs', 'tests']
    
    for dir_name in required_dirs:
        dir_path = root_dir / dir_name
        if dir_path.exists():
            print(f"  ✓ {dir_name}/")
        else:
            print(f"  ✗ {dir_name}/ - NÃO ENCONTRADO")
            all_ok = False
    
    # Testa arquivo de configuração
    print("\n⚙️  Verificando arquivo de configuração...")
    config_path = root_dir / 'config' / 'config.env'
    
    if config_path.exists():
        print(f"  ✓ config.env encontrado")
        
        # Carrega e valida as chaves
        from dotenv import load_dotenv
        load_dotenv(config_path)
        
        api_key = os.getenv('BINANCE_API_KEY')
        api_secret = os.getenv('BINANCE_API_SECRET')
        
        if api_key and len(api_key) > 10:
            print(f"  ✓ BINANCE_API_KEY configurada ({len(api_key)} caracteres)")
        else:
            print(f"  ✗ BINANCE_API_KEY inválida ou ausente")
            all_ok = False
            
        if api_secret and len(api_secret) > 10:
            print(f"  ✓ BINANCE_API_SECRET configurada ({len(api_secret)} caracteres)")
        else:
            print(f"  ✗ BINANCE_API_SECRET inválida ou ausente")
            all_ok = False
    else:
        print(f"  ✗ config.env NÃO ENCONTRADO")
        all_ok = False
    
    # Testa bibliotecas instaladas
    print("\n📦 Verificando bibliotecas instaladas...")
    
    libraries = [
        ('binance', 'python-binance'),
        ('requests', 'requests'),
        ('dotenv', 'python-dotenv')
    ]
    
    for lib_import, lib_name in libraries:
        try:
            __import__(lib_import)
            print(f"  ✓ {lib_name}")
        except ImportError:
            print(f"  ✗ {lib_name} - NÃO INSTALADA")
            all_ok = False
    
    # Testa importação do cliente Binance
    print("\n🔌 Verificando cliente Binance...")
    try:
        from binance.client import Client
        print(f"  ✓ Cliente Binance importado com sucesso")
        print(f"  ✓ Código pronto para conectar (será testado no Digital Ocean)")
        
    except Exception as e:
        print(f"  ✗ Erro ao importar cliente: {str(e)}")
        all_ok = False
    
    return all_ok

if __name__ == "__main__":
    print()
    success = test_structure()
    
    print("\n" + "=" * 50)
    
    if success:
        print("✅ TODOS OS TESTES PASSARAM!")
        print("\nCódigo validado e pronto para:")
        print("  1. Ser transferido para o Digital Ocean")
        print("  2. Testar conexão real com Binance")
        print("  3. Iniciar desenvolvimento da lógica de arbitragem")
    else:
        print("❌ ALGUNS TESTES FALHARAM")
        print("\nVerifique os itens marcados com ✗")
    
    print("=" * 50)
    print()
    
    sys.exit(0 if success else 1)
