import http.server
import socketserver
import json
import time
from pathlib import Path

REQUEST_COUNT = 0
PORT = 8000

class MyHttpRequestHandler(http.server.BaseHTTPRequestHandler):
    
    def _log_request(self):
        """Логує запит у консоль та збільшує лічильник."""
        global REQUEST_COUNT
        REQUEST_COUNT += 1
        
        print(f"--- [ЛОГ] Запит #{REQUEST_COUNT} ---")
        print(f"Час: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Метод: {self.command}, Шлях: {self.path}")
        print(f"Адреса: {self.client_address[0]}:{self.client_address[1]}")
        
    def _send_response(self, status_code, content_type, body):
        """Допоміжна функція для відправки відповіді."""
        self.send_response(status_code)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body.encode('utf-8'))

    def do_GET(self):
        """Обробник GET-запитів."""
        self._log_request()
        
        try:
            if self.path == '/':
                file_path = Path('index.html')
                if file_path.exists():
                    self._send_response(200, 'text/html', file_path.read_text('utf-8'))
                else:
                    self._send_response(404, 'text/plain', 'index.html не знайдено')
            
            elif self.path == '/styles.css':
                self._send_response(200, 'text/css', Path('styles.css').read_text('utf-8'))
            
            elif self.path == '/app.js':
                self._send_response(200, 'application/javascript', Path('app.js').read_text('utf-8'))

            elif self.path == '/status':
                status_data = {
                    "server_time": time.strftime('%Y-%m-%d %H:%M:%S'),
                    "requests_handled": REQUEST_COUNT
                }
                self._send_response(200, 'application/json', json.dumps(status_data, indent=2))
            
            else:
                self._send_response(404, 'text/plain', '404 Not Found')
                
        except FileNotFoundError:
            self._send_response(404, 'text/plain', f'404 Файл не знайдено: {self.path}')
        except Exception as e:
            self._send_response(500, 'text/plain', f'500 Внутрішня помилка сервера: {e}')

    def do_POST(self):
        """Обробник POST-запитів."""
        self._log_request()
        
        if self.path == '/data':
            try:
                content_length = int(self.headers['Content-Length'])
                post_body = self.rfile.read(content_length).decode('utf-8')
                try:
                    data = json.loads(post_body)        
                    print(f"Отримано JSON: {data}")
                    response_data = {
                        "status": "success",
                        "message": "Дані успішно отримано!",
                        "your_data": data
                    }
                    self._send_response(200, 'application/json', json.dumps(response_data, indent=2))
                    
                except json.JSONDecodeError:
                    print(f"[ПОМИЛКА] Не вдалося розпарсити JSON: {post_body}")
                    self._send_response(400, 'application/json', json.dumps({"error": "Bad Request: Некоректний JSON"}))

            except Exception as e:
                self._send_response(500, 'text/plain', f'500 Внутрішня помилка сервера: {e}')
        else:
            self._send_response(404, 'text/plain', '404 Not Found')
            
    def do_OPTIONS(self):
        """Обробник OPTIONS-запитів (для CORS)."""
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With, Content-Type")
        self.end_headers()
Handler = MyHttpRequestHandler
with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Сервер запущено на http://localhost:{PORT}")
    print("Логи запитів будуть з'являтися тут, у консолі.")
    httpd.serve_forever()