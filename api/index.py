import sys
import os
import traceback

try:
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    from app import app
    
    def handler(request):
        try:
            return app(request.environ, request.start_response)
        except Exception as e:
            error_msg = f"Handler error: {str(e)}\n{traceback.format_exc()}"
            print(error_msg, file=sys.stderr)
            response = request.start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
            return [error_msg.encode()]
    
except Exception as e:
    error_msg = f"Import error: {str(e)}\n{traceback.format_exc()}"
    print(error_msg, file=sys.stderr)
    
    def handler(request):
        response = request.start_response('500 Internal Server Error', [('Content-Type', 'text/plain')])
        return [error_msg.encode()]
