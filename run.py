import os

os.environ['SECRET_KEY'] = 'eb16510d9e5bae3983cd3cc8d762fd3190929034e643159037e7d3ba3c47dac6'

from database import init_db, create_sample_data
from app import app

if __name__ == '__main__':
    init_db()
    create_sample_data()
    
    print("Servidor iniciado em http://localhost:5001")
    print("Usuario: admin@memo.com | Senha: admin123")
    
    app.run(debug=True, host='0.0.0.0', port=5001)
