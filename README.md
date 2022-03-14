
Třetí projekt na Python Akademii od Engeta

POPIS PROJEKTU
Tento projekt slouží k extrahování výsledků z parlamentních voleb v roce 2017, odkaz zde https://volby.cz/pls/ps2017nss/ps3?xjazyk=CZ


INSTALACE KNIHOVEN
Knihovny, které jsou použity, jsou uložené v soboru requirements.txt . Pro instalaci doporučuji použít nové virtuální prostředí a s nainstalovaným manažerem spustit následovné:
pip3 --version (ověří verzi manageru)
pip3 install -r requirements.txt (nainstaluje knihovny)

SPUŠTĚNÍ PROJEKTU
Spuštění souboru main.py v rámci příkazového řádku požaduje dva povinné argumenty.
python main.py <"odkaz-uzemniho-celku"><"vysledny-soubor">

PRŮBĚH STAHOVÁNÍ
Stahuji data z url https://volby.cz/pls/ps2017nss/ps32?xjazyk=CZ&xkraj=12&xnumnuts=7103
Ukládám do souboru Prostejov.csv
Ukončuji Scraper

ČÁSTEČNÝ VÝSTUP
Číslo	 Název	         Voliči v seznamu	 Vydané obálky	Volební účast v %	Odevzdané obálky	Platné hlasy
506761 Alojzov	         205	             145	            70,73	            145	            144
589268 Bedihošť	      834	             527	            63,19	            527	            524
589276 Bílovice-Lutotín	431	             279	            64,73	            279	            275
   
