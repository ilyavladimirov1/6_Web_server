import socket
import os


def handle_request(data):
    """ Обработка входящего запроса и определение запрашиваемого ресурса """
    headers = data.split('\n')
    first_line = headers[0]
    filename = first_line.split()[1]

    if filename == '/':
        filename = '/index.html'

    return filename


def serve_file(filepath):
    """ Попытка чтения файла и возврат его содержимого с HTTP-заголовками """
    try:
        with open(filepath, 'rb') as f:
            content = f.read()
        response = b'HTTP/1.1 200 OK\n\n' + content
    except FileNotFoundError:
        response = b'HTTP/1.1 404 NOT FOUND\n\nFile Not Found'
    return response


def start_server(host='', port=80):
    """ Запуск сервера, который слушает порт 80 """
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Сервер запущен на порту {port}...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Подключен клиент: {addr}")
        request = client_socket.recv(1024).decode('utf-8')
        filename = handle_request(request)
        filepath = os.path.join(os.getcwd(), 'server_workdir', filename.strip('/'))
        response = serve_file(filepath)
        client_socket.sendall(response)
        client_socket.close()


# Запуск сервера
if __name__ == "__main__":
    start_server()
