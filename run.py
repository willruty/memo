import os
import sys

if not os.getenv('DATABASE_URL'):
    print("⚠️  DATABASE_URL não configurada. Configurando automaticamente...")
    pooler_url = 'postgresql://postgres.lfweqsjmxtcgiikkhclj:memothreads123.@aws-1-sa-east-1.pooler.supabase.com:6543/postgres'
    os.environ['DATABASE_URL'] = pooler_url
    print(f"📡 Usando connection pooling do Supabase...")
    os.environ['SECRET_KEY'] = 'eb16510d9e5bae3983cd3cc8d762fd3190929034e643159037e7d3ba3c47dac6'

from database import init_db, create_sample_data
from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("Inicializando sistema Memo...")
    print("=" * 50)
    
    print("\n1. Inicializando banco de dados Supabase...")
    try:
        init_db()
        print("✅ Banco de dados inicializado!")
    except Exception as e:
        print(f"⚠️  Aviso: {e}")
        print("   Continuando mesmo assim...")
    
    print("\n2. Verificando dados de exemplo...")
    try:
        create_sample_data()
    except Exception as e:
        print(f"⚠️  Aviso ao criar dados: {e}")
    
    print("\n3. Iniciando servidor Flask...")
    print("=" * 50)
    print("🌐 Acesse: http://localhost:5000")
    print("👤 Usuário de exemplo: admin@memo.com")
    print("🔑 Senha: admin123")
    print("=" * 50)
    print("\nPressione Ctrl+C para parar o servidor\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
