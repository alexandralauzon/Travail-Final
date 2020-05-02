# coding : utf-8

import requests, csv
from bs4 import BeautifulSoup

url = "https://www.saq.com/fr/produits"

entetes = {
    "User-Agent": "Alexandra Lauzon, étudiante journalisme UQAM"
}


pages = list(range(1,149))

n=0

fichier = "touteSaq.csv"

for page in pages:
    # print(page)
    urlproduits = url + "?p=" + str(page) + "&product_list_limit=96"
    # print(urlproduits)

    site = requests.get(urlproduits, headers=entetes)
    # print(site.status_code) #Je vérifie ainsi si tout fonctionne bien. J'ai mon 200, je continue.
    p = BeautifulSoup(site.text, "html.parser")

    # print(p)

    lienproduits = p.find_all("a", class_="product-item-link")

    # print(lienproduits)


    for lienproduit in lienproduits:
        n+=1
        lien = lienproduit["href"]
        # print(lien)

        siteA = requests.get(lien, headers=entetes)
        pageA = BeautifulSoup(siteA.text,"html.parser")
    
    # # print(pageA)

        titre = pageA.find("meta",property="og:title")["content"]
        # print(titre)

        try:
            prix = pageA.find("meta",property="product:price:amount")["content"]
            # print(prix)
        except (NameError,TypeError):
            print("Ce produit n'est pas disponible")
            continue

        categorie = pageA.find("meta",property="product:category")["content"]
        # print(categorie)

        attributs = pageA.find("ul",class_="list-attributs").find_all("li")
        for attribut in attributs:

            if "Pays" in attribut.text:
                        nomPays = attribut.find("strong").text.strip()

            if "Format" in attribut.text:
                        formatproduit= attribut.find("strong").text.strip()

            if "Degré d'alcool" in attribut.text:
                        degre=attribut.find("strong").text.strip()

            if "Code SAQ" in attribut.text:
                        codeSAQ = attribut.find("strong").text.strip()

            if "Code CUP" in attribut.text:
                        codeCUP = attribut.find("strong").text.strip()


            
        # print(nomPays)
        # print(formatproduit)
        # print(degre)
        # print(codeSAQ)
        # print(codeCUP)

        siteinternet = pageA.find("meta",property="twitter:url")["content"]
        # print(siteinternet)

        infos = [n,page,titre,prix,categorie,nomPays,formatproduit,degre,codeSAQ,codeCUP,siteinternet]
        # print(infos)

        saq = open(fichier,"a")
        saqdonnees = csv.writer(saq)
        saqdonnees.writerow(infos)
        print(siteA)




  