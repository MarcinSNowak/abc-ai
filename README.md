# ABC AI — lokalne środowisko AI dla programisty

Seria dla osób, które chcą pracować z modelami językowymi **bez wysyłania kodu
i danych do zewnętrznej chmury**. Zaczynamy od pustej maszyny i Ollamy, a kończymy
na kompletnym agencie programisty działającym lokalnie.

Lokalne środowisko nie jest tu jednak celem samym w sobie, tylko **pętlą
deweloperską**: uczysz się i debugujesz za darmo u siebie, a ten sam kod
przenosisz później na produkcję. Kolejne odcinki doprowadzą serię do dodatku
do Microsoft Teams opartego o Azure AI Foundry — napisanego i przetestowanego
w środowisku lokalnym.

## Odcinki

| # | Odcinek | Czego dotyczy |
|---|---------|---------------|
| 1 | [Uruchamianie lokalnych agentów AI w oparciu o Ollamę](01-lokalni-agenci-ai-ollama/01-lokalni-agenci-ai-ollama.md) | Instalacja, wybór modelu, lokalne REST API, integracja z edytorem |
| 2 | [Lokalny RAG — baza wiedzy o projekcie](02-lokalny-rag-baza-wiedzy/02-lokalny-rag-baza-wiedzy.md) | Indeksowanie repozytorium, embeddingi, wyszukiwanie, jakość odpowiedzi |
| 3 | [Pamięć długoterminowa agenta](03-pamiec-dlugoterminowa-agenta/03-pamiec-dlugoterminowa-agenta.md) | Wyciąganie faktów z rozmów, ocena istotności, trwałe przechowywanie |
| 4 | [Kompletny agent programisty](04-kompletny-agent-programisty/04-kompletny-agent-programisty.md) | Spięcie RAG, pamięci i narzędzi (tool calling) w jedną pętlę |

Odcinki 5 (przeniesienie na Azure AI Foundry) i 6 (dodatek do Microsoft Teams)
są w przygotowaniu.

## Czego potrzebujesz

- macOS, Linux albo Windows z WSL2
- 8 GB RAM (16 GB+ przy większych modelach)
- 5–20 GB wolnego miejsca na dysku, zależnie od liczby pobranych modeli

Nie potrzebujesz konta w żadnej chmurze ani karty płatniczej. Wszystko
w odcinkach 1–4 działa offline.

## Jak czytać

Artykuły renderują się poprawnie tutaj, na GitHubie — razem z diagramami.
Wygodniejsza w czytaniu wersja, z podświetlaniem składni i nawigacją między
odcinkami, jest na [www.qshmobile.com/abc-ai/](https://www.qshmobile.com/abc-ai/).

Odpowiedzi modeli pokazane w artykułach są rzeczywiste, ale **niedeterministyczne** —
u Ciebie wyjdzie podobnie, nie identycznie. To normalne i nie znaczy, że coś
skonfigurowałeś źle.

## Zgłaszanie błędów

Znalazłeś nieaktualną komendę, zmienioną nazwę modelu albo krok, który u Ciebie
nie działa? Załóż **Issue** — z podaniem systemu, wersji Ollamy i tego, co
zobaczyłeś. Ekosystem lokalnych modeli zmienia się szybko i takie zgłoszenia są
naprawdę pomocne.

## Licencja

Dwie licencje, bo dwie różne rzeczy:

- **Kod** — przykłady, skrypty i pliki konfiguracyjne: [MIT](LICENSE). Bierz
  i używaj, także komercyjnie, bez pytania.
- **Treść** — teksty, diagramy i ilustracje: [CC BY-NC 4.0](LICENSE-CONTENT).
  Możesz je kopiować i przetwarzać z podaniem autorstwa, ale nie sprzedawać ani
  odpłatnie na nich szkolić bez naszej zgody. Chcesz? Napisz na info@qshmobile.com.

## Kto za tym stoi

[QSHMOBILE](https://www.qshmobile.com) — software house działający od 2015 roku,
Microsoft Partner. Budujemy aplikacje na zamówienie i produkty SaaS na Azure,
wdrażamy AI w zespołach deweloperskich i szkolimy z Microsoft Azure. Zajęcia
prowadzi certyfikowany trener Microsoft (MCT) — ta sama osoba, która realizuje
wdrożenia u klientów.

Ollama oraz nazwy produktów i usług wymienione w artykułach są znakami
towarowymi swoich właścicieli.
