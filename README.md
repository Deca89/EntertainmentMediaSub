# EntertainmentMediaSub

Projektin tarkoituksena on luoda ohjelma, johon voidaan lisätä seurattavia media kohteita (anime/manga/tv-sarjoja/light novels), niiden seurattavat sivustot, linkkejä edelliseen läpikäytyyn jaksoon/kappaleeseen. Yksinkertaisemmin - kasata yhdelle sivustolle kaikki mahdollisesti seuratut mediamuodot, josta voidaan sitten edetä itse sarjoihin.

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan seurattavia medioita.
* Käyttäjä pystyy lisäämään median perustiedot - kuvan/genret/tagit.
* Käyttäjä näkee sovellukseen lisätyt kohteet.
* Käyttäjä voi lisätä myös itselleen seurattavaksi muiden lisäämiä medioita.
* Käyttäjä pystyy etsimään medioita hakusanalla/tagillä/genrellä.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät/seuraamat mediat.
* Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. media tyyppi, genre).
* Käyttäjä pystyy kommentoimaan medioita - mielipide/kehu/haukku.

Tunnettuja korjattavia: viestejä voitaisiin selkeyttää.
Sivustoa paremman näköiseksi.
Haussa tällä hetkellä jos genre valittuna ei tätä voida poistaa.
Tagit mukaan ja niihin funktioita.
Genren lisäys?

Sovelluksen käyttö:
Lataa repo palvelimelle (esim git clone https://github.com/Deca89/EntertainmentMediaSub.git)

Oletetaan tällä hetkellä käyttäjät kurssilaisiksi.

Repon pääkansion sisällä:

Suositellaan venv käyttöä.

$ pip install flask

Luo tietokanta. Riippuen OS esim:

C:\sqlite\sqlite3.exe database.db < schema.sql
Tässä polku -> polku missä sqlite3.exe sijaitsee

TAI

sqlite3 database.db

Käynnistä sovellus esim:

flask run

TAI

flask --app app:app run


Windows komentoja (venvissä):

Käynnistä appi:
flask --app app:app run

Tietokannan luonti:
C:\sqlite\sqlite3.exe database.db < schema.sql
Tässä polku -> polku missä sqlite3.exe sijaitsee