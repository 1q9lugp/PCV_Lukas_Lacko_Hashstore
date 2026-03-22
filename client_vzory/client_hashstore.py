#!/usr/bin/env python3

import socket

HOST = "127.0.0.1"
PORT = 9000
HASH = "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

def main():
    try:
        # vytvorenie socketu
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.connect((HOST, PORT))

            # --- ZACIATOK PRIKAZU GET HASH hardlinknuty hore ---
            # poslanie pirkazu na server
            sock.sendall(f"GET {HASH}\n".encode())

            # precitaj riadok hlavičky
            header = b""
            while not header.endswith(b"\n"):
                header += sock.recv(1)
            header = header.decode().rstrip("\n")
            print("Hlavička servera:", header)

            if not header.startswith("200"):
                exit(1)

            # jednoduche parsovanie length
            length = int(header.split()[2])
            description = header.split()[3]

            # precitaj a vypis obsah
            data = sock.recv(length)
            print("Obsah súboru:")
            print(data.decode(errors="replace"))
            # --- KONIEC UKAZKY PRIKAZU GET ---

            # pokračovať tu, mozete linearne alebo vytvorit funkcie/procedury/metody

    except Exception as e:
        print(f"Chyba: {e}")

    finally:
        sock.close()
        print("Spojenie zatvorené")


if __name__ == "__main__":
    main()
