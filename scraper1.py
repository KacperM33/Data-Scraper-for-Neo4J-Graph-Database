import requests
from bs4 import BeautifulSoup
from py2neo import Graph, Node, Relationship


def scrape_links():
    response = requests.get(url_main)

    if response.status_code != 200:
        print(f"Błąd połączenia - tytuły. Status: {response.status_code}")
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
        print(f"Błąd połączenia - nazwy. Status: {response.status_code}")
        return True

    soup = BeautifulSoup(response.text, "html.parser")

    category_element = soup.find('h1', class_='header-breadcrumbs__title page-title')

    category = category_element.get_text(strip=True)

    return category


def scrape_animal_data(url2):
    response = requests.get(url)

    # Sprawdzenie, czy żądanie zakończyło się sukcesem
    if response.status_code != 200:
        print(f"Błąd połączenia - zwierzęta. Status: {response.status_code}")
        return True

    soup = BeautifulSoup(response.text, 'html.parser')

    divs = soup.find_all('div', class_='posts__item posts__item--zwierzeta')

    if not divs:
        print("Brak pasujących div - zwierzęta.")
        return True

    titles = []
    for div in divs:
        titles.extend(div.find_all('a', class_='posts__item__title'))

    if not titles:
        print("Brak nazw w wybranych divach - zwierzęta.")
        return True

    # Tworzenie węzłów dla kategorii
    category = scrape_names(url2)

    category_name = f"{category}"
    category_node = graph.nodes.match("Kategoria", name=category_name).first()
    if not category_node:
        category_node = Node("Kategoria", name=category_name)
        graph.create(category_node)
        relationship_core = Relationship(category_node, "SĄ", core_node)
        graph.create(relationship_core)
        print(f"Created category node: {category}")

    # Tworzenie węzłów dla każdego zwierzęcia i jego podkategorii
    for title in titles:
        animal_name = title.get_text(strip=True)
        words = animal_name.split()

        if len(words) > 1:
            subcategory_name = words[0]

            # Sprawdzanie, czy podkategoria już istnieje
            subcategory_node = graph.nodes.match("Podkategoria", name=subcategory_name).first()
            if not subcategory_node:
                # Tworzenie nowego węzła podkategorii
                subcategory_node = Node("Podkategoria", name=subcategory_name)
                graph.create(subcategory_node)
                relationship = Relationship(subcategory_node, "NALEŻY_DO", category_node)
                graph.create(relationship)
                print(f"Created subcategory node: {subcategory_name}")

            # Tworzenie węzła dla zwierzęcia i połączenie z podkategorią
            animal_node = Node("Zwierze", name=animal_name)
            graph.create(animal_node)
            relationship = Relationship(animal_node, "JEST", subcategory_node)
            graph.create(relationship)
            print(f"Created node for animal: {animal_name} and linked to subcategory: {subcategory_name}")

        else:
            # Jeżeli nazwa składa się z jednego wyrazu, tworzymy tylko węzeł zwierzęcia
            animal_node = Node("Zwierze", name=animal_name)
            graph.create(animal_node)
            relationship = Relationship(animal_node, "JEST", category_node)
            graph.create(relationship)
            print(f"Created node for animal: {animal_name}")


if __name__ == "__main__":
    graph = Graph("bolt://localhost:7687", auth=("neo4j", "")) # auth=("nazwa_użytkownika", "hasło")

    core_name = "Zwierzęta"
    core_node = Node("Zwierzęta", name=core_name)
    graph.create(core_node)

    # URL strony z danymi
    url_main = "https://www.ekologia.pl/atlas-zwierzat/"
    links = scrape_links()

    for link in links:
        for i in range(1, 51):
            url = f"{link}page/{i}/"
            if scrape_animal_data(url):
                break
