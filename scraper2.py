import requests
from bs4 import BeautifulSoup
import textacy.extract
import spacy


def scrape_links():
    response = requests.get(url_main)

    if response.status_code != 200:
        print(f"Błąd połączenia - linki. Status: {response.status_code}")
        return True

    soup = BeautifulSoup(response.text, "html.parser")

    linkers = soup.find_all('a', class_='animals2__item__link')

    names = []

    for linker in linkers:
        names.append(linker['href'])

    return names


def scrape_names(url2):
    response = requests.get(url2)

    if response.status_code != 200:
        print(f"Blad polaczenia - zwierzeta. Status: {response.status_code}")
        return True

    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')

    divs = soup.find_all('div', class_='posts__item posts__item--zwierzeta')

    if not divs:
        print("Brak pasujacych div - zwierzęta.")
        return True

    a = []
    for div in divs:
        a.extend(div.find_all('a', class_='posts__item__title'))

    titles = []
    for title in a:
        titles.append(title['href'])

    if not titles:
        print("Brak nazw w wybranych divach - zwierzęta.")
        return []

    return titles


# Funkcja pobierająca stronę i zwracająca tekst
def get_page_text(url):
    response = requests.get(url)

    if response.status_code != 200:
        print(f"Błąd połączenia - tekst. Status: {response.status_code}")
        return True

    response.encoding = response.apparent_encoding

    soup = BeautifulSoup(response.text, 'html.parser')
    section_header = soup.find(lambda tag: tag.name in ['div', 'h2'] and tag.get('id') == 'section-wystepowanie')

    if section_header:
        # Znalezienie następnego <p> po znalezionym <h2>
        section_paragraph = section_header.find_next('p')
        if section_paragraph:
            return section_paragraph.get_text()
    return ""


# Funkcja do wyciągania nazw państw z tekstu używając geograpy
def extract_countries(text):
    try:
        # Użyjmy textacy do ekstrakcji nazw krajów
        nlp = spacy.load('pl_core_news_sm')
        doc = nlp(text)
        countries = textacy.extract.entities(doc, include_types=None)
        return [country.text for country in countries]
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        return []


# Główna funkcja
def main(url):
    text = get_page_text(url)
    if text:
        print(f"Analizowany tekst: {text}")
        found_countries = extract_countries(text)
        print(found_countries)
    else:
        print("Nie znaleziono sekcji 'Występowanie' lub brak tekstu w <p>.")


# Przykładowe użycie
if __name__ == "__main__":
    url_main = "https://www.ekologia.pl/atlas-zwierzat/"
    links = scrape_links()

    for link in links:
        for i in range(1, 51):
            url_cat = f"{link}page/{i}/"
            urls = scrape_names(url_cat)
            for url_name in urls:
                print(url_name)
                main(url_name)
