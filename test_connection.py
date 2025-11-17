"""
Script para testar a conexão com o banco de dados Supabase.
"""
import os
from database import get_db, init_db

def test_connection():
    """
    Testa a conexão com o banco de dados Supabase.
    """
    try:
        print("Testando conexão com Supabase...")
        
        # Verifica se DATABASE_URL está configurada
        if not os.getenv('DATABASE_URL'):
            print("❌ ERRO: DATABASE_URL não está configurada!")
            print("\nConfigure a variável de ambiente:")
            print("Windows (PowerShell):")
            print('  $env:DATABASE_URL="postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres"')
            print("\nLinux/Mac:")
            print('  export DATABASE_URL="postgresql://postgres:memothreads123@db.lfweqsjmxtcgiikkhclj.supabase.co:5432/postgres"')
            return False
        
        # Tenta conectar
        conn = get_db()
        cursor = conn.cursor()
        
        # Testa uma query simples
        cursor.execute('SELECT version()')
        version = cursor.fetchone()
        
        print(f"✅ Conexão bem-sucedida!")
        print(f"   PostgreSQL versão: {version[0]}")
        
        # Verifica se as tabelas existem
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        if tables:
            print(f"\n📊 Tabelas encontradas: {len(tables)}")
            for table in tables:
                print(f"   - {table[0]}")
        else:
            print("\n⚠️  Nenhuma tabela encontrada. Execute 'python database.py' para criar as tabelas.")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ ERRO na conexão: {e}")
        return False

if __name__ == '__main__':
    test_connection()

