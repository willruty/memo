from app import app

def handler(request):
    return app(request.environ, request.start_response)
