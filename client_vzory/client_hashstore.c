#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SERVER_IP "127.0.0.1"
#define SERVER_PORT 9000
#define HASH "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"

int main() {
    int sock;
    struct sockaddr_in server_addr;
    char c;
    char header[256];
    int n = 0;

    // vytvorenie socketu
    if ((sock = socket(AF_INET, SOCK_STREAM, 0)) < 0) {
        perror("socket error");
        return 1;
    }

    memset(&server_addr, 0, sizeof(server_addr));
    server_addr.sin_family = AF_INET;
    server_addr.sin_port = htons(SERVER_PORT);

    if (inet_pton(AF_INET, SERVER_IP, &server_addr.sin_addr) <= 0) {
        perror("inet_pton error");
        close(sock);
        return 1;
    }

    // pripojenie na server
    if (connect(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        perror("connect error");
        close(sock);
        return 1;
    }

    printf("Pripojené na %s:%d\n", SERVER_IP, SERVER_PORT);


    // =====================================================
    // --- ukazka volania GET ---
    // ======================================================
    char cmd[512];
    snprintf(cmd, sizeof(cmd), "GET %s\n", HASH);
    send(sock, cmd, strlen(cmd), 0);

    // precitaj hlavičku
    while(read(sock, &c, 1) == 1 && c != '\n') header[n++] = c;
    header[n] = '\0';
    printf("Hlavička servera: %s\n", header);

    if(strncmp(header, "200", 3) != 0){
        close(sock);
        return 1;
    }

    int length;
    char desc[128];
    char ok[8];
    sscanf(header, "200 %7s %d %127[^\n]", ok, &length, desc);

    printf("Obsah súboru:\n");
    for(int i=0; i<length; i++){
        if(read(sock, &c, 1) <= 0) break;
        putchar(c);
    }
    putchar('\n');
    // --- KONIEK UKAZKY ---

    // tu implementovať protokol dalej, mozno pisat linearne alebo vytvorit procedury/funkcie v pripade c++ aj metody

    close(sock);
    printf("Spojenie zatvorené\n");
    return 0;
}
