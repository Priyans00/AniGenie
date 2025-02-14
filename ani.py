import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from bs4 import BeautifulSoup
import requests
import csv
from datetime import datetime

k = datetime.now()

cred = credentials.Certificate("firebase_key.json")
firebase_admin.initialize_app(cred)

db = firestore.client()


#c.writerow(["No","Anime_name","Genres","Characters","Ratings","Episodes"])


def scrape_anime_info(n):
    url = f"website-url"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }
    try:
        anime_info = []
        anime_info.append(n)
        response = requests.get(url, headers=headers)
        response.raise_for_status()  

        soup = BeautifulSoup(response.content, "html.parser")

        

        
        name = []
        # Anime name japanese
        title_element_jap = soup.find_all("span", itemprop="name")
        if title_element_jap:
            name.append(title_element_jap[-1].text.strip())
        else:
            name.append("N/A")

        # Anime Name English
        title_element_eng = soup.find("p",class_="title-english title-inherit")
        if title_element_eng:
            name.append(title_element_eng.text.strip())
        else:
            name.append("N/A")

        anime_info.append(name)


        # Genres
        genre_elements = soup.find_all("span", itemprop="genre")
        genres = [genre.text.strip() for genre in genre_elements]
        anime_info.append(genres)

        # Characters 
        character_elements = soup.find_all("h3", class_="h3_characters_voice_actors")
        characters = [x.text.strip() for x in character_elements]
        anime_info.append(characters)


        # Rating 
        score_element = soup.find("span", itemprop="ratingValue")
        if score_element:
            anime_info.append(score_element.text.strip())
        else:
           anime_info.append("N/A")

        #episodes
        episode_element = soup.find_all("div",class_="spaceit_pad")
        if episode_element:
            anime_info.append(episode_element[3].text.strip().split()[-1])
        else:
            anime_info.append("N/A")

        
    
        return anime_info
    except Exception as e:
        print(e)
        return None


def fool(a,n):
    with open("anime.csv","a",newline = '',encoding = "utf-8") as f:
        c = csv.writer(f)
        for i in range(a,n+1):
            anime_data = scrape_anime_info(i)

            if anime_data:
                print(f"done for {i}")
                c.writerow(anime_data)
            else:
                print(f"not done for {i}")



def poo():
    k = int(input("how many to enter"))
    with open("anime.csv","r",encoding = "utf-8") as f:
        columns = csv.reader(f,delimiter=',')
        reversed_data = reversed(list(columns))
        last_entry = next(reversed_data)
        entries = last_entry[0]
    print(last_entry )
    entries = int(last_entry[0])

    print(entries)
    fool(entries+1,entries+k)


poo()
p = datetime.now()
print(p-k)