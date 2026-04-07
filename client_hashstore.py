#!/usr/bin/env python3
import socket
import os
import sys

HOST = "127.0.0.1"
PORT = 9000

def send_command(sock, command):
    """Pomocná funkcia na odoslanie príkazu a prijatie prvého riadku odpovede."""
    sock.sendall(f"{command}\n".encode())
    header = b""
    while not header.endswith(b"\n"):
        chunk = sock.recv(1)
        if not chunk: break
        header += chunk
    return header.decode().strip()

def list_files():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        header = send_command(sock, "LIST")
        print(f"Server: {header}")
        
        if header.startswith("200 OK"):
            parts = header.split()
            count = int(parts[2]) if len(parts) > 2 else 0
            for _ in range(count):
                line = b""
                while not line.endswith(b"\n"):
                    line += sock.recv(1)
                print(line.decode().strip())

def get_file(file_hash):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        header = send_command(sock, f"GET {file_hash}")
        print(f"Server: {header}")

        if header.startswith("200 OK"):
            parts = header.split()
            length = int(parts[2])
            description = parts[3] if len(parts) > 3 else "bez_popisu"
            
            # Čítanie presného počtu bajtov dát
            received_data = b""
            while len(received_data) < length:
                chunk = sock.recv(min(length - len(received_data), 4096))
                if not chunk: break
                received_data += chunk
            
            filename = f"down_{file_hash[:8]}" # Skrátený hash pre názov súboru
            with open(filename, "wb") as f:
                f.write(received_data)
            print(f"Súbor uložený ako: {filename} (Popis: {description})")
        else:
            print("Chyba: Súbor sa nenašiel alebo server vrátil chybu.")

def upload_file(filepath, description):
    if not os.path.exists(filepath):
        print(f"Chyba: Súbor {filepath} neexistuje.")
        return

    filesize = os.path.getsize(filepath)
    with open(filepath, "rb") as f:
        file_data = f.read()

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        # Formát: UPLOAD <length> <description>\n<data>
        header = f"UPLOAD {filesize} {description}\n"
        sock.sendall(header.encode() + file_data)
        
        response = b""
        while not response.endswith(b"\n"):
            response += sock.recv(1)
        print(f"Server: {response.decode().strip()}")

def delete_file(file_hash):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((HOST, PORT))
        response = send_command(sock, f"DELETE {file_hash}")
        print(f"Server: {response}")

def print_help():
    print("\nHashStore Client - Príkazy:")
    print("  list                         - Zoznam súborov na serveri")
    print("  get <hash>                   - Stiahnuť súbor podľa hašu")
    print("  upload <subor> <popis>       - Nahrať súbor z disku")
    print("  delete <hash>                - Vymazať súbor")
    print("  help                         - Zobraziť túto nápovedu")
    print("  exit                         - Ukončiť program\n")

def main():
    print("Vitajte v HashStore klientskej aplikácii.")
    print_help()
    
    while True:
        try:
            user_input = input("> ").strip().split()
            if not user_input: continue
            
            cmd = user_input[0].lower()
            
            if cmd == "list":
                list_files()
            elif cmd == "get" and len(user_input) > 1:
                get_file(user_input[1])
            elif cmd == "upload" and len(user_input) > 2:
                upload_file(user_input[1], user_input[2])
            elif cmd == "delete" and len(user_input) > 1:
                delete_file(user_input[1])
            elif cmd in ["help", "?"]:
                print_help()
            elif cmd == "exit":
                break
            else:
                print("Neplatný príkaz alebo chýbajúce parametre.")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Chyba: {e}")

if __name__ == "__main__":
    main()
