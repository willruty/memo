"""
Script de inicialização rápida do sistema Memo.
Executa a inicialização do banco de dados e inicia o servidor.
"""
from database import init_db, create_sample_data
from app import app

if __name__ == '__main__':
    print("=" * 50)
    print("Inicializando sistema Memo...")
    print("=" * 50)
    
    # Inicializa o banco de dados
    print("\n1. Inicializando banco de dados...")
    init_db()
    
    # Cria dados de exemplo (opcional)
    print("\n2. Criando dados de exemplo...")
    create_sample_data()
    
    print("\n3. Iniciando servidor Flask...")
    print("=" * 50)
    print("Acesse: http://localhost:5000")
    print("Usuário de exemplo: admin@memo.com / admin123")
    print("=" * 50)
    
    # Inicia o servidor
    app.run(debug=True, host='0.0.0.0', port=5000)

