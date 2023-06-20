import os # trabalhar com arquivos e diretórios
from http.server import SimpleHTTPRequestHandler # manipular requisições HTTP
from socketserver import TCPServer # criar um servidor TCP

class CustomRequestHandler(SimpleHTTPRequestHandler):
    def list_directory(self, path): # listar os arquivos e diretórios em um determinado caminho
        try:
            entries = os.scandir(path) # gera uma representação HTML dos arquivos e diretórios
            entries_list = []
            for entry in entries:
                entry_name = entry.name
                if entry.is_dir():
                    entry_name += '/'
                entries_list.append(f'<li><a href="{entry_name}">{entry_name}</a></li>')
            entries_list.sort()
            entries_html = '\n'.join(entries_list)
            content = f'''
                <html>
                <head>
                    <title>Servidor {self.path}</title>
                </head>
                <body>
                    <h1>Servidor {self.path}</h1>
                    <ul>
                        {entries_html}
                    </ul>
                </body>
                </html>
            '''
            encoded_content = content.encode('utf-8')
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.send_header('Content-Length', len(encoded_content))
            self.end_headers()
            self.wfile.write(encoded_content)
        except FileNotFoundError:
            self.send_error(404, "File not found")

    def do_GET(self):
        if self.path == '/HEADER':
            headers = self.headers
            self.send_response(200)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(str(headers).encode('utf-8'))
        else:
            path = self.translate_path(self.path)
            if os.path.isfile(path):
                self.send_response(200)
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', f'attachment; filename="{os.path.basename(path)}"')
                self.end_headers()
                with open(path, 'rb') as file:
                    self.wfile.write(file.read())
            else:
                self.list_directory(path)

def start_server(port, directory):
    os.chdir(directory)
    server_address = ('172.30.169.26', port)
    httpd = TCPServer(server_address, CustomRequestHandler)
    print(f"Servidor rodando em 172.30.169.26:{port}")
    httpd.serve_forever()

start_server(8000, '/home/leonardopj')
