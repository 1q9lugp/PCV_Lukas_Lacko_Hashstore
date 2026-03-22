# Zadanie: Klient pre HASHSTORE server

## Cieľ

Vašou úlohou je implementovať klientskú aplikáciu, ktorá komunikuje so
serverom pomocou vlastného textového protokolu.

------------------------------------------------------------------------

## Základné informácie

-   Komunikácia prebieha cez TCP
-   Protokol je riadkovo orientovaný (`\n`)
-   Server vždy odpovedá:

```{=html}
<!-- -->
```
    <status_code> <message>

------------------------------------------------------------------------

## Funkcionalita klienta

Klient musí podporovať:

1.  Zoznam súborov (`LIST`)
2.  Stiahnutie súboru (`GET`)
3.  Nahratie súboru (`UPLOAD`)

------------------------------------------------------------------------

## Protokol

### 1. LIST

#### Klient:

    LIST

#### Server:

    200 OK <count>
    <hash> <description>
    ...

------------------------------------------------------------------------

### 2. GET

#### Klient:

    GET <hash>

#### Server (úspech):

    200 OK <length> <description>
    <data>

#### Server (chyba):

    404 NOT_FOUND

------------------------------------------------------------------------

### 3. UPLOAD

#### Klient:

    UPLOAD <length> <description>
    <data>

-   `length` = počet bajtov dát
-   `description` = popis súboru

#### Server (úspech):

    200 STORED <hash>

#### Server (ak existuje):

    409 HASH_EXISTS <hash>


### 4. DELETE

#### Klient:
```
DELETE <hash>
```

- `<hash>` – hash súboru, ktorý chcete zmazať
- Posiela sa ako **jediný riadok** ukončený `\n`
- Žiadne ďalšie dáta sa neposielajú

#### Server:

##### Úspech:
```
200 OK
```

##### Ak súbor neexistuje:
```
404 NOT_FOUND
```

##### Nesprávny formát:
```
400 BAD_REQUEST
```

##### Interná chyba servera:
```
500 SERVER_ERROR
```

---



------------------------------------------------------------------------

## Stavové kódy

-   200 OK
-   400 BAD_REQUEST
-   404 NOT_FOUND
-   409 HASH_EXISTS
-   500 SERVER_ERROR

------------------------------------------------------------------------

## Požiadavky

-   správne parsovanie odpovedí
-   čítanie presného počtu bajtov
-   ošetrenie chýb
-   implementácia CLI rozhrania

------------------------------------------------------------------------

## Príkazy klienta

    list
    get <hash>
    upload <subor> <description>

------------------------------------------------------------------------
# Príkazy netcat ako klient

Tento súbor obsahuje všetky praktické príklady použitia `netcat` (nc) na testovanie komunikácie so serverom HASHSTORE.

---

## 1. Nahrať súbor s krátkym obsahom

```bash
printf "UPLOAD 5 test_subor\nhello" | nc localhost 9000
```

* Očakávaná odpoveď:

```
200 STORED <hash>
```

---

## 2. Nahrať dlhší textový súbor

```bash
printf "UPLOAD 11 dlhsi_text\nhello world" | nc localhost 9000
```

* Očakávaná odpoveď:

```
200 STORED <hash>
```

---

## 3. Získať zoznam súborov (LIST)

```bash
printf "LIST\n" | nc localhost 9000
```

* Očakávaná odpoveď:

```
200 OK 2
<hash1> test_subor
<hash2> dlhsi_text
```

---

## 4. Stiahnuť súbor (GET)

```bash
printf "GET <hash>\n" | nc localhost 9000
```

* Odpoveď servera pri úspechu:

```
200 OK <length> <description>
<data>
```

* Odpoveď servera pri chybe:

```
404 NOT_FOUND
```

---

## 5. Vymazať súbor (DELETE)

```bash
printf "DELETE <hash>\n" | nc localhost 9000
```

* Odpoveď servera pri úspechu:

```
200 OK
```

* Ak súbor neexistuje:

```
404 NOT_FOUND
```

* Nesprávny formát:

```
400 BAD_REQUEST
```

* Interná chyba servera:

```
500 SERVER_ERROR
```

---

## 6. Nahrať ľubovoľný súbor s automatickým výpočtom veľkosti

```bash
FILE=subor.txt
(printf "UPLOAD %s %s\n" "$(wc -c < "$FILE")" "$FILE"; cat "$FILE") | nc localhost 9000
```

* Tento príkaz automaticky spočíta počet bajtov a pošle ich spolu s popisom.

---

## 7. Nahrať binárny súbor (napr. obrázok) z /dev/urandom

```bash
head -c 20 /dev/urandom | (printf "UPLOAD 20 random_data\n"; cat) | nc localhost 9000
```

* Odpoveď:

```
200 STORED <hash>
```

---

## 8. Test presného počtu bajtov pri GET (voliteľné)

```bash
printf "GET <hash>\n" | nc localhost 9000 | hexdump -C
```

* Umožňuje zobraziť aj binárne dáta v hexadecimálnom formáte.

---

## Tipy

* Vždy zabezpeč, aby bol riadok ukončený `\n`.
* Používaj `printf` namiesto `echo`, aby sa nepridávalo neočakávané `\n`.
* Najprv over hash cez `LIST`, potom použij `GET` alebo `DELETE`.
* Pri binárnych súboroch dávaj pozor na presný počet bajtov (`length`).





    
------------------------------------------------------------------------
# ULOHA/ZADANIE

## Forma odovzdávania
- GIT repozitár, zašlete mi link
- Repozitár bude obsahovať:
    1. **zdrojový kód** klientskej aplikácie 
    2. v prípade použitia kompilovaných jazykov (C/C++, C#, ...) súčasťou bude aj spustitený binárný súbor pre amd64 (EXE, linux-binárka), v prípade jazyka python nie je nutné
    3. vami vytvorené **pomocné súbor** potrebné pre fungovanie klienta **vrátane dát pre upload** na server
    4. repozitár nesmie obsahovať súbory s prefixom **down_váš-názov alebo down_<hash>** tieto bude generovať vylucne program klient

## Načo si dať pozor?
- klinet musí fungovať nezávisle od dát na serveri
- server voči ktorému bude Váš program testovaný bude z tohto repozitáru s demo dátami ktoré v ňom aktáalne su
- nemeniť nastavenia portov klientu ani serveru


## Implementuje príkazy klienta v klientskej aplikácií
1.  naprogrmaujte upload dát na server, môže byť aj hardwritnute v kóde, BONUS bod za implemntáciu vstupu z STDIN 
2.  naprogramujte upload externých dát zo súboru na disku (súbor priložte do repozitára), fopen()...
3.  naprogramujte vypísanie zoznam súborov uložených na serveri  
4.  doprogramujtee a rozsirte stiahnutie ľubovelného súboru zo serveru podobne ako vzor (môže byť hardliknute, ale musí byť buď súbor ktorý klient nahrá na server pres stahovanim alebo niektorý z demo súborov) a jeho uloženie ako nového súboru na strane klienta v tom istom adresari ako je ulozeny klient **názov stiahnutého súbora bude začínať prefixom down_** , BONUS bod ak sa súbor dá zvoliť v klientskej aplikácií



