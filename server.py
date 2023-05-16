import socket
import random
import threading

# Function to handle a client connection
def handle_client(client_socket):
    secret_number = random.randint(1, 100)
    attempts = 0

    while True:
        guess = client_socket.recv(1024).decode().strip()
        attempts += 1

        if not guess.isdigit():
            client_socket.send("Invalid input. Please enter a number.".encode())
        else:
            guess = int(guess)
            if guess < secret_number:
                client_socket.send("Higher".encode())
            elif guess > secret_number:
                client_socket.send("Lower".encode())
            else:
                client_socket.send(f"Correct! You guessed the number in {attempts} attempts.".encode())
                break

    client_socket.close()

# Function to start the server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)

    print("Server started. Listening for connections...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"New connection from {addr[0]}:{addr[1]}")
        client_thread = threading.Thread(target=handle_client, args=(client_socket,))
        client_thread.start()

start_server()
