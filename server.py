import socket

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server started on {host}:{port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connection from {client_address}")
        data = client_socket.recv(1024)
        if data:
            print(f"Received: {data.decode('utf-8')}")
            client_socket.sendall(b"Hello, Client!")
        client_socket.close()

if __name__ == "__main__":
    HOST = '10.0.0.217'
    PORT = 1869
    start_server(HOST, PORT)
