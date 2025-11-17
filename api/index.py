import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from app import app
    
    def handler(request, response):
        try:
            return app(request.environ, response.start_response)
        except Exception as e:
            import traceback
            error = f"Handler Error: {str(e)}\n{traceback.format_exc()}"
            print(error, file=sys.stderr)
            response.start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [error.encode()]
            
except Exception as e:
    import traceback
    error = f"Import Error: {str(e)}\n{traceback.format_exc()}"
    print(error, file=sys.stderr)
    
    def handler(request, response):
        response.start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [error.encode()]
