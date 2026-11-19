# 🌐 Servidor HTTP em Python

Servidor HTTP feito com a biblioteca padrão do Python (`http.server` e `socketserver`) para a disciplina de **Redes de Computadores** da UFSJ.

Ele permite navegar pelas pastas de um diretório e baixar arquivos direto pelo navegador.

## ✨ Funcionalidades

- **Listagem de diretórios:** gera uma página HTML com links para cada arquivo e subpasta.
- **Download de arquivos:** ao clicar em um arquivo, o servidor o envia como download (`Content-Disposition: attachment`).
- **Rota `/HEADER`:** mostra os cabeçalhos HTTP enviados pelo navegador, útil para estudar o protocolo.
- **Erro 404** quando o caminho não existe.

## ▶️ Como executar

Requer apenas Python 3, sem dependências externas.

```bash
# Serve a pasta atual em http://127.0.0.1:8000
python Servidor_Redes.py

# Escolhendo pasta, porta e endereço
python Servidor_Redes.py --dir ~/Documentos --port 8080 --host 0.0.0.0
```

Depois, abra `http://127.0.0.1:8000` no navegador. Para ver os cabeçalhos da sua requisição, acesse `http://127.0.0.1:8000/HEADER`.

> ⚠️ Usar `--host 0.0.0.0` deixa a pasta visível para outros computadores da rede. Use apenas em redes confiáveis.

## 🧠 O que aprendi

- Como funciona o ciclo requisição/resposta do HTTP (método `GET`, códigos de status e cabeçalhos).
- Como estender o `SimpleHTTPRequestHandler` para mudar o comportamento padrão do servidor.
- Como montar respostas HTML dinamicamente a partir do sistema de arquivos.
