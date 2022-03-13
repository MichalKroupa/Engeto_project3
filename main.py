# By Michal Kroupa

import sys
import requests
from bs4 import BeautifulSoup



def main(odkaz, name):

    # Hlavička souboru
    hlavicka = "Číslo;Název;Voliči v seznamu;Vydané obálky;Volební účast v %;Odevzdané obálky;Platné hlasy; % platných hlasů;Občanská demokratická strana;Řád národa - Vlastenecká unie;" \
               "CESTA ODPOVĚDNÉ SPOLEČNOSTI;Česká str.sociálně demokrat.;Radostné Česko;STAROSTOVÉ A NEZÁVISLÍ;Komunistická str.Čech a Moravy;" \
               "Strana zelených;ROZUMNÍ-stop migraci,diktát.EU;Strana svobodných občanů;Blok proti islam.-Obran.domova;" \
               "Občanská demokratická aliance;Česká pirátská strana;Referendum o Evropské unii;TOP 09;ANO 2011;" \
               "Dobrá volba 2016;SPR-Republ.str.Čsl. M.Sládka;Křesť.demokr.unie-Čs.str.lid.;Česká strana národně sociální;" \
               "REALISTÉ;SPORTOVCI;Dělnic.str.sociální spravedl.;Svob.a př.dem.-T.Okamura (SPD);Strana Práv Občanů"

    # Pošlu request na danou url
    odpoved = requests.get(odkaz)

    # BeautifulSoup vytáhne html
    soup = BeautifulSoup(odpoved.text, "html.parser")

    # Najdu číslo a název města, podle tagu TD, kde je class cislo a overflow_name
    cislo = soup.find_all("td", class_="cislo")
    mesto = soup.find_all("td", class_="overflow_name")

    # Oba listy zazipuju do jednoho, kvůli for cyklu
    mesto_cislo_zip = zip(cislo, mesto)

    # Otevřu soubor, vložím do něj hlavičku
    f = open(name, "w")
    f.write(hlavicka + "\n")

    # Projedu zipovaný list, kde je jak číslo tak název města
    for cislo_mesta, nazev_mesta in mesto_cislo_zip:

        # Načtu url z daného čísla města (V čísle je schovaná url)
        tabulka_data = seber_url(cislo_mesta)

        # Přidám do proměnné (reprezentuje řádek) číslo a název města, jako oddělovač pro CSV soubour používám středník
        text = cislo_mesta.text + ";" + nazev_mesta.text
        # Už hotový list dat pro konkrétní okrsek projedu a pridám ho do řádku
        for atr in tabulka_data:

            text = text + ";" + atr

        # Přidám nový řádek, aby se další okrsek vypsal pod aktuální řádek
        text = text + "\n"
        # Zapíšu do souboru
        f.write(text)

    # Zavřu soubor
    f.close()

# Funkce kterou vypreparuji url z tagu pro číslo města, vstupní parametr je celý tag s číslem města
def seber_url(tag):

    # Proměnná s počáteční url, do které se později přidá další část, která odkazuje na statistiky konkrétního okrsku
    true_url = "https://volby.cz/pls/ps2017nss/"

    # cyklus, který hledá tag "a", a kde je href(url)
    for a in tag('a', href=True):

        # Do url přidám část url schovanou v tagu
        true_url = true_url + a['href']
        # Pošlu request na danou adresu
        odpoved = requests.get(true_url)
        # Vytáhnu html
        polevka = BeautifulSoup(odpoved.text, "html.parser")
        # Pošlu do funkce kde zpracuji data
        tabulka_data = nacti_tabulku(polevka)
        # Vrátím tabulku s kompletními daty o daném okrsku
        return tabulka_data

# Funkce, která projde tabulky na url daného okrsku, sebere data a přidá je do listu
def nacti_tabulku(tabulka):
    # Vytvořím prázdný list
    tabulka_data = []
    # Hledám v horní tabulce, podle tagu td a class cislo
    vysledky_horni = tabulka.findAll("td", class_="cislo")
    # Hledám ve spodních tabulkách, podle tagu tg, a dvou headerů, které označují tabulku
    vysledky_dolni = tabulka.findAll("td", headers="t1sa2 t1sb3") + tabulka.findAll("td", headers="t2sa2 t2sb3")

    # Projdu výsledky horní tabulky, vytahuji pouze data která mě zajímají
    for atr in vysledky_horni[3:9]:

        # Data přidám do tabulky
        tabulka_data.append(atr.text)

    # Projdu výsledky dolní tabulky, jelikož jeden řádek tabulky je vždy prázdný, vynechávám ho
    for atr in vysledky_dolni[:-1]:

        # Data přidám do tabulky
        tabulka_data.append(atr.text)

    # Vrátím tabulku s daty
    return tabulka_data




if __name__ == '__main__':
    # Zjistím, zda byly zadány vstupní argumenty, pokud ne, napíšu kde je chyba a program se ukončí
    try:
        url = str(sys.argv[1])

    except IndexError:
        print("wrong url")
        quit()

    try:
        name = str(sys.argv[2])

    except IndexError:
        print("wrong file format")
        quit()

    # Zjistím, zda uživatel zadává správný formát souboru (pouze csv)
    if not name.endswith(".csv"):

        print("wrong file format")
        quit()

    # Zjistím, zda uživatel používá správnou url
    if not url.startswith("https://volby.cz/pls/ps2017nss/"):

        print("wrong url")
        quit()

    main(url, name)
