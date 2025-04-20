# 🌍 Data Scraper for Neo4J Graph Database

This project was developed to scrape data from a web application about **animals around the world** and store it as nodes and relationships between them in a Neo4J graph database.

## 📚 About This Project

This project was completed as the final assignment for the *Semantic Networks* course during my engineering studies.

## 🧰 Development Tools

- Python 3.11
- [Neo4J](https://neo4j.com) (for graph database)
- [Beautiful-Soup-4](https://beautiful-soup-4.readthedocs.io/en/latest/) (for data scraping)

## ⚙️ Functionality

- **Data scraping:** A script designed to collect data from a web application.
- **Integration with Neo4J:** Creates nodes and relationships between them in a Neo4J graph database.

## 📝 How the scraper works

The script connects to already existing **Neo4J database** and creates nodes and relationships based on the scraped data. The data is retrieved from the [Ekologia.pl](https://www.ekologia.pl/atlas-zwierzat/) website.
<br>To achieve this, the script sends an HTTP request to the target URL, downloads the full HTML content of the page, and then processes the hypertext using the **Beautiful-Soup-4** library.

## 🌐 Graph Database Structure

### 🔸 Full database after scraping:

![image](https://github.com/user-attachments/assets/50372ae8-caed-4354-a6ce-6073bf5bb85a)

The database contains a total of **2,827** nodes and **9,968** relationships.

### 🔸 Nodes are divided into **six** main categories:

- Zwierzęta (Animals) - a single node serving as the root for all animal-related categories
 
![image](https://github.com/user-attachments/assets/7f7001b6-5567-4fa6-b951-48aceed9a95a)

- **"Zwierze" (Animal)** - a node representing an individual animal
 
![image](https://github.com/user-attachments/assets/d0d73559-df1d-44ae-9ae7-4b029aba9f62)

- **"Lokacje" (Locations)** - a single node acting as the root for all location-related nodes
 
![image](https://github.com/user-attachments/assets/5eba5388-bd03-443b-addc-a6c28f5bdede)

- **"Lokacja" (Single location)**  - a node representing a specific location (e.g., country or continent)
 
![image](https://github.com/user-attachments/assets/fe9710c2-5b23-46de-bfbd-931d888a0973)

- **"Podkategoria" (Subcategory)** - a node representing a subcategory (subspecies) of animals
 
![image](https://github.com/user-attachments/assets/39914e08-b156-4c5d-b150-1018820aa217)

- **"Kategoria" (Main category)** - a node representing a main category (species) of animals
 
![image](https://github.com/user-attachments/assets/5fd5367c-38a6-49a6-bf9c-62e2dfe910cc)

### 🔸 Relationships are divided into **seven** main types:

- **"SĄ_HIPONIMEM_OD" (ARE_HYPONYMS_OF)** - connects specific animal categories to the general "Zwierzęta" (Animals) node

![image](https://github.com/user-attachments/assets/ef3842ac-ffde-490d-86ad-6aa44f7f45a3)

- **"NALEŻY_DO_KATEGORII" (BELONGS_TO_CATEGORY)** - indicates which main category a subcategory belongs to

![image](https://github.com/user-attachments/assets/029abdbe-8098-4fed-9a09-995991c51767)

- **"ZAWIERA_PODKATEGORIE" (CONTAINS_SUBCATEGORIES)** - indicates which subcategories are included in a main category

![image](https://github.com/user-attachments/assets/4244bb91-50e7-4f00-99b3-e93ac15d1647)

- **"JEST_PODKATEGORII" (IS_SUBCATEGORY_OF)** - shows which subcategory an animal belongs to (if applicable)

![image](https://github.com/user-attachments/assets/bae80b51-5d10-4426-84c3-994074896add)

- **"JEST_KATEGORII" (IS_CATEGORY_OF)** - shows which main category an animal belongs to 

![image](https://github.com/user-attachments/assets/199028c7-3dfd-4b48-adaa-231788ee7cdf)

- **"TO_HIPONIM_OD" (THIS_IS_A_HYPONYM_FROM)** - connects specific locations (countries, continents, etc.) to the general "Lokacje" (Locations) node

![image](https://github.com/user-attachments/assets/b722a543-5233-40ef-a260-d344dd6dcc2d)

- **"WYSTĘPUJE_W" (OCCURRING_IN)** - indicates the locations where a given animal can be found

![image](https://github.com/user-attachments/assets/62a38cc0-a5e4-4937-b2af-8c2cb660ab28)


## ✏️ Credits
Animal data was scraped from [Ekologia.pl](https://www.ekologia.pl/atlas-zwierzat/)
