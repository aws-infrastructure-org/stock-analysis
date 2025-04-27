from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
import json
import os
from api.handler import lambda_handler

class StockHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        # Parse URL and query parameters
        parsed_url = urlparse(self.path)
        
        # Handle API requests
        if parsed_url.path == '/api/stocks':
            query_params = parse_qs(parsed_url.query)
            # Create mock Lambda event
            event = {
                'httpMethod': 'GET',
                'path': '/api/stocks',
                'queryStringParameters': {
                    'symbol': query_params.get('symbol', [''])[0]
                }
            }
            
            # Call the Lambda handler
            response = lambda_handler(event, None)
            
            # Set response headers
            self.send_response(response['statusCode'])
            for header, value in response.get('headers', {}).items():
                self.send_header(header, value)
            self.end_headers()
            
            # Send response body
            self.wfile.write(response['body'].encode())
            return

        # Set the directory containing static files
        static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
        os.chdir(static_dir)
            
        # Serve static files
        if parsed_url.path == '/':
            self.path = 'stock_ui.html'
        elif parsed_url.path.startswith('/static/'):
            self.path = parsed_url.path[8:]  # Remove /static/ prefix
            
        return SimpleHTTPRequestHandler.do_GET(self)

def run_server(port=8000):
    server_address = ('', port)
    httpd = HTTPServer(server_address, StockHandler)
    print(f"Server is running at http://localhost:{port}")
    httpd.serve_forever()

if __name__ == '__main__':
    run_server()