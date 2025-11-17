from app import app

def handler(request, response):
    return app(request.environ, response.start_response)
