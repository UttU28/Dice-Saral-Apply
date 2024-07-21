import socket

def connect_to_server(host, port):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print(f"Connected to server at {host}:{port}")
    
    client_socket.sendall(b"Hello, Server!")
    response = client_socket.recv(1024)
    print(f"Received: {response.decode('utf-8')}")
    
    client_socket.close()

if __name__ == "__main__":
    HOST = '10.0.0.217'
    PORT = 1869
    connect_to_server(HOST, PORT)
