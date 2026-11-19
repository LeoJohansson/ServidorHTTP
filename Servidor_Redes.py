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

def start_server(host, port, directory):
    os.chdir(directory)
    server_address = (host, port)
    httpd = TCPServer(server_address, CustomRequestHandler)
    print(f"Servidor rodando em http://{host}:{port} servindo '{directory}'")
    httpd.serve_forever()

if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Servidor HTTP simples para listar e baixar arquivos.')
    parser.add_argument('--host', default='127.0.0.1', help='endereço IP do servidor (padrão: 127.0.0.1)')
    parser.add_argument('--port', type=int, default=8000, help='porta do servidor (padrão: 8000)')
    parser.add_argument('--dir', default='.', help='diretório a ser servido (padrão: diretório atual)')
    args = parser.parse_args()

    start_server(args.host, args.port, os.path.abspath(args.dir))
