#!/usr/bin/env python3
"""Porównuje deklarowany czas czytania odcinków z policzonym z treści.

Stopka każdego odcinka podaje „Czas czytania: ~N minut". Ta liczba jest wpisana
ręcznie, więc rozjeżdża się przy każdej większej dopisce — i rozjechała się już
raz o trzykrotność. Skrypt liczy ją z tekstu, żeby dało się to sprawdzić zamiast
zgadywać.

Model jest jawny i celowo prosty:

  proza   — 200 słów na minutę. Tyle mniej więcej daje ciche czytanie tekstu
            technicznego po polsku. Nie jest to stała uniwersalna, tylko
            założenie: przy 250 sł/min odcinek 1 wychodzi o jakieś 5 minut
            krócej i nadal nie jest to 12 minut, które kiedyś zadeklarowaliśmy.
  kod     — 2 sekundy na linię. Zakładamy przejrzenie, nie studiowanie;
            kto przepisuje przykłady, spędzi nad nimi wielokrotnie więcej.
  tabele  — 4 sekundy na wiersz, razem z nagłówkiem.

Wynik zaokrąglamy do 5 minut, bo dokładność tego szacunku i tak na więcej nie
pozwala, a „~35 minut" jest uczciwsze niż „~36 minut".

Użycie:  python3 scripts/metryka.py
Wyjście: kod 1, jeśli którykolwiek odcinek deklaruje co innego, niż wychodzi
         z treści — dzięki temu nadaje się do sprawdzenia przed publikacją.
"""

import glob
import os
import re
import sys

SLOWA_NA_MINUTE = 200
SEKUND_NA_LINIE_KODU = 2
SEKUND_NA_WIERSZ_TABELI = 4

SLOWO = re.compile(r"[0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż][0-9A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż-]*")


def zmierz(tekst):
    """Zwraca (słowa prozy, linie kodu, wiersze tabel)."""
    tekst = re.sub(r"^---\n.*?\n---\n", "", tekst, flags=re.S)

    bloki = re.findall(r"```.*?```", tekst, flags=re.S)
    # -2, bo pierwsza i ostatnia linia bloku to same ogrodzenia ```
    linie_kodu = sum(len(b.strip().split("\n")) - 2 for b in bloki)

    proza = re.sub(r"```.*?```", "", tekst, flags=re.S)
    wiersze_tabel = len([l for l in proza.split("\n") if l.strip().startswith("|")])

    proza = re.sub(r"^\|.*$", "", proza, flags=re.M)  # tabele liczymy osobno
    proza = re.sub(r"`[^`]*`", "", proza)             # kod w linii to nie proza
    proza = re.sub(r"https?://\S+", "", proza)        # adresów się nie czyta

    return len(SLOWO.findall(proza)), linie_kodu, wiersze_tabel


def minuty(slowa, kod, tabele):
    surowe = (
        slowa / SLOWA_NA_MINUTE
        + kod * SEKUND_NA_LINIE_KODU / 60
        + tabele * SEKUND_NA_WIERSZ_TABELI / 60
    )
    return max(5, round(surowe / 5) * 5)


def main():
    korzen = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
    pliki = sorted(glob.glob(os.path.join(korzen, "*", "*.md")))
    if not pliki:
        print("Nie znalazłem odcinków — uruchom skrypt z repozytorium abc-ai.")
        return 1

    print(f"{'odcinek':<34}{'proza':>7}{'kod':>6}{'tab.':>6}{'wynik':>8}{'w stopce':>11}")
    rozjazd = False

    for sciezka in pliki:
        tekst = open(sciezka, encoding="utf-8").read()
        slowa, kod, tabele = zmierz(tekst)
        policzone = minuty(slowa, kod, tabele)

        znalezione = re.search(r"Czas czytania: ~(\d+) minut", tekst)
        deklarowane = int(znalezione.group(1)) if znalezione else None

        if deklarowane != policzone:
            rozjazd = True
        znacznik = "" if deklarowane == policzone else "  <-- do poprawy"
        w_stopce = f"{deklarowane} min" if deklarowane else "brak"

        nazwa = os.path.basename(sciezka)
        print(
            f"{nazwa[:33]:<34}{slowa:>7}{kod:>6}{tabele:>6}"
            f"{str(policzone) + ' min':>8}{w_stopce:>11}{znacznik}"
        )

    if rozjazd:
        print("\nStopka odcinka rozjechała się z treścią. Popraw „Czas czytania”.")
        return 1

    print("\nWszystkie stopki zgadzają się z treścią.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
