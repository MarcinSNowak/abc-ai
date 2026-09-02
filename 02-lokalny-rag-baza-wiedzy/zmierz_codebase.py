#!/usr/bin/env python3
"""Mierzy, co Continue naprawdę wysyła do Ollamy przy zapytaniu `@codebase`.

Skrypt staje między wtyczką a Ollamą: nasłuchuje na porcie 11435 i przekazuje
wszystko na 11434. Przy każdym zapytaniu czatu wypisuje jedną tabelkę — ile
tokenów zajął prompt, jakie okno kontekstu narzuciło Continue i ile miejsca
zostało na resztę.

Uruchomienie:

    python3 zmierz_codebase.py

Na Windowsie zamiast `python3` używaj `py`.

Potem w Continue, w pliku `config.yaml`, podmień adres modelu czatu:

    apiBase: http://localhost:11435

i zadaj w panelu czatu pytanie zaczynające się od `@codebase`.

Port jest celowo inny niż domyślny — w samej Ollamie nic nie trzeba zmieniać,
a gdy skrypt nie działa, wystarczy skasować tę jedną linię w konfiguracji.

Wymaga wyłącznie biblioteki standardowej Pythona.
"""

import json
import sys
import urllib.request
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

OLLAMA = "http://127.0.0.1:11434"
PORT = 11435

# Ollama nie udostępnia endpointu tokenizacji, więc liczbę tokenów trzeba
# oszacować z liczby znaków. Dla mieszanki kodu i polszczyzny wychodzi około
# 2,5 znaku na token — to szacunek, nie pomiar, i tak go niżej podpisujemy.
ZNAKI_NA_TOKEN = 2.5

POMIJANE = {"connection", "keep-alive", "transfer-encoding", "content-length", "upgrade"}


def rozmiar_promptu(zadanie):
    """Liczy znaki wszystkiego, co pojedzie do modelu jako prompt."""
    znaki = 0
    if zadanie.get("tools"):
        znaki += len(json.dumps(zadanie["tools"], ensure_ascii=False))
    for wiadomosc in zadanie.get("messages") or []:
        znaki += len(wiadomosc.get("content") or "")
    return znaki


def raport(zadanie, odpowiedz):
    opcje = zadanie.get("options") or {}
    okno = opcje.get("num_ctx")
    limit_odpowiedzi = opcje.get("num_predict")

    znaki = rozmiar_promptu(zadanie)
    szacunek = int(znaki / ZNAKI_NA_TOKEN)
    policzone = (odpowiedz or {}).get("prompt_eval_count")

    print("\n" + "=" * 62)
    print(f"model:                     {zadanie.get('model')}")
    print(f"wiadomości w rozmowie:     {len(zadanie.get('messages') or [])}")
    print(f"prompt:                    {znaki} znaków, czyli około {szacunek} tokenów")
    if policzone:
        print(f"tokeny policzone przez Ollamę: {policzone}")

    if okno:
        print(f"num_ctx narzucony przez Continue: {okno}")
        if limit_odpowiedzi:
            print(f"num_predict (limit odpowiedzi): {limit_odpowiedzi}")

        # Ollama przyjmuje jako prompt połowę okna — druga połowa jest
        # zarezerwowana na odpowiedź. `num_predict` nie ma na ten podział
        # wpływu, co sprawdzamy w odcinku 1.
        budzet = okno // 2
        zajete = round(100 * szacunek / budzet)
        print(f"budżet promptu (połowa num_ctx): {budzet}")
        print(f"wykorzystanie budżetu:     {zajete}%")

        if zajete > 100:
            print("\n>>> Prompt nie mieści się w budżecie.")
            print(">>> Został przycięty od najstarszej strony,")
            print(">>> czyli od instrukcji systemowej. Bez błędu.")
        if policzone and policzone < szacunek * 0.6:
            print("\n>>> Ollama policzyła znacznie mniej tokenów, niż wysłano.")
            print(">>> Część promptu do modelu nie dotarła.")
    else:
        print("num_ctx: nie podany w żądaniu (Ollama użyje swojego domyślnego)")

    print("=" * 62)
    sys.stdout.flush()


class Posrednik(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, *_):
        pass

    def do_GET(self):
        self._przekaz(None)

    def do_POST(self):
        dlugosc = int(self.headers.get("Content-Length") or 0)
        self._przekaz(self.rfile.read(dlugosc) if dlugosc else b"")

    def _przekaz(self, ciało):
        naglowki = {k: v for k, v in self.headers.items() if k.lower() not in POMIJANE}
        try:
            zrodlo = urllib.request.urlopen(
                urllib.request.Request(OLLAMA + self.path, data=ciało,
                                       headers=naglowki, method=self.command),
                timeout=600)
        except Exception as blad:
            self.send_error(502, f"Ollama nie odpowiada: {blad}")
            return

        self.send_response(zrodlo.status)
        for klucz, wartosc in zrodlo.headers.items():
            if klucz.lower() not in POMIJANE:
                self.send_header(klucz, wartosc)
        self.send_header("Transfer-Encoding", "chunked")
        self.end_headers()

        # Fragmenty przekazujemy natychmiast, żeby odpowiedź w edytorze nadal
        # pojawiała się na bieżąco.
        zebrane = []
        try:
            while True:
                fragment = zrodlo.read(4096)
                if not fragment:
                    break
                self.wfile.write(b"%X\r\n" % len(fragment) + fragment + b"\r\n")
                self.wfile.flush()
                zebrane.append(fragment)
            self.wfile.write(b"0\r\n\r\n")
            self.wfile.flush()
        except (BrokenPipeError, ConnectionResetError):
            return

        if self.path == "/api/chat" and ciało:
            try:
                ostatnia = None
                for linia in b"".join(zebrane).split(b"\n"):
                    if linia.strip():
                        obiekt = json.loads(linia)
                        if obiekt.get("done"):
                            ostatnia = obiekt
                raport(json.loads(ciało), ostatnia)
            except Exception as blad:
                print(f"(nie udało się zrobić raportu: {blad})")


if __name__ == "__main__":
    print(f"Nasłuchuję na http://localhost:{PORT}, przekazuję na {OLLAMA}")
    print("W Continue ustaw apiBase na adres powyżej. Ctrl+C kończy.")
    ThreadingHTTPServer(("127.0.0.1", PORT), Posrednik).serve_forever()
