Eine Deutschland-Karte der Funkamateure basierend auf der Rufzeichenliste der Bundesnetzagentur

von [Ulrich Thiel, VK2UTL/DK1UT](mailto:u-thiel@gmx.net)

---



Neben wirklich **sehr vielen positiven** Kommentaren (vielen Dank dafür) gab es vereinzelt Beschwerden bezüglich des Datenschutz. Die Daten stammten 1:1 aus der [öffentlichen PDF-Datei der Bundesnetzagentur](https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Telekommunikation/Unternehmen_Institutionen/Frequenzen/Amateurfunk/Rufzeichenliste/Rufzeichenliste_AFU.html), und es gab von mir nie eine Möglichkeit zum Download von Daten. Da ich aber anderweitig relativ beschäftigt bin und auf die Diskussion keinen Wert lege, habe ich mich entschlossen, die Karte nach nur knapp einem Tag ganz zu entfernen (sie war nur am 23. Mai 2017 sichtbar). Die Idee sollte jetzt aber klar sein und mit der Anleitung unten kann sich jeder selbst eine vollständige Datenbank und Karte erstellen.

Ich hatte das ganze Projekt an einem Abend zwecks zeitvertreib realisiert, weil ich Python klasse finde und etwas über das Geocoding lernen wollte. Die Idee und meine Skripte dazu sind wirklich extrem simpel. Fragen und Anmerkungen zur Programmierung sind dennoch willkommen, am besten zu Diskutieren auf der [Github Website](https://github.com/thielul/CallmapGermany.git) des Projekts. 

73 und mit der Bitte um Verständnis, dass ich meine Zeit effektiver einbringen möchte   
VK2UTL/DK1UT


# Vorgehen

Die folgende Anleitung ist an Linux und MacOS Benutzer gerichtet. Unter Windows funktioniert natürlich im Prinzip auch alles, da wir aber ein vernünftiges Terminal benötigen und ich (aus genau diesem Grund) kein Windows benutze, will ich das jetzt hier nicht näher erörtern. Ich denke, es ist wirklich kein großer Aufwand, alles analog unter Windows umzusetzen.

## Quellen
Die Quellen meiner Skripte gibt es auf der [Github Website](https://github.com/thielul/CallmapGermany) des Projekts (oder [hier](https://github.com/thielul/CallmapGermany.git) direkt zum Zip-Archiv). Diese lädt man runter. Es handelt sich dabei um Python2-Skripte.

## Externe Tools

Wir benötigen folgende externe Tools:

* Eine [Python2](https://www.python.org/downloads/) Installation. Ich empfehle, gleich ein komplettes Bundle mit vielen Bibliotheken wie z.B. [Anaconda](https://www.continuum.io/downloads) zu installieren. Falls man bereits eine Python-Installation hat, sollte man beachten, dass man python2 aufruft, nicht python3 (beide Versionen können ko-existieren).

* Wir benötigen für Python die Bibliotheken [sqlite3](https://docs.python.org/2/library/sqlite3.html), [tqdm](https://pypi.python.org/pypi/tqdm) und [geocoder](https://pypi.python.org/pypi/geocoder). Falls nicht vorhanden, kann man diese einfach mittels [pip](https://pip.pypa.io/en/stable/installing/) installieren:

```
pip install sqlite3
pip install tqdm
pip install geocoder
```

Falls pip selbst nicht vorhanden, kann man dies mittels

```
python get-pip.py
```

installieren.

* Ein Tool zum Konvertieren von PDF-Datein in Text-Datein. Ich habe dazu ps2ascii verwendet. Ich bin mir nicht mehr ganz sicher, glaube aber, es ist Teil des [GhostScript Bundles](https://www.ghostscript.com/download/gsdnld.html). Für MacOS gibt es [hier](http://pages.uoregon.edu/koch/) ein fertiges Paket oder man installiert mittels [Homebrew](https://brew.sh/index_de.html) und ```brew install ghostscript```. Für Linux wird sich das auch mittels eines Paketmanagers installieren lassen.

## Rufzeichenliste
Bei der [öffentlichen PDF-Datei der Bundesnetzagentur](https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Telekommunikation/Unternehmen_Institutionen/Frequenzen/Amateurfunk/Rufzeichenliste/Rufzeichenliste_AFU.html) handelt es sich um eine ca. 9MB große PDF-Datei. Diese benötigen wir.

## Umwandlung in Text-Datei 
Die runtergeladene Rufzeichenliste wandeln wir wie folgt in eine Text-Datei um:

```
ps2ascii Rufzeichenliste_AFU.pdf > calls.txt
``` 
Da die PDF-Datei relativ groß ist, dauert es einen Moment (ca. 15 Minuten auf einem sehr schnellen Computer). Die entstandene Text-Datei ist ca. 4MB groß. Im Prinzip ist es egal, welches Tool man dazu benutzt; mein Skript im nächsten Schritt berücksichtigt aber gewisse Eigenarten von ps2ascii, wird daher also ohne Modifikationen wahrscheinlich nur dafür richtig funktionieren.

## Erstellung der Datenbank

Das Rückgrat des Projekts ist eine SQL-Datenbank (genauer, SQLite-Datenbank), die wir aus der Text-Datei mittels

```
python makedb.py
```

erstellen. Dieses Skript geht die Text-Datei ```calls.txt``` zeilenweise durch, extrahiert die relevanten Daten, und speichert sie in die SQLite-Datenbank ```calls.db```. Dieser Teil ist natürlich am schwierigsten zu Programmieren. Ich verwende zum Parsen reguläre Ausdrücke. Es gibt leider ein paar Formatierfehler in der Rufzeichenliste selbst, die ich im Skript auch berücksichtigen muss. 

Die Datenbank selbst kann man sich z.B. mit dem netten Tool [SQLite Browser](http://sqlitebrowser.org) anschauen (im Tab *Browse Data*). Die Spakten der Datenbank sind:

```
Id, Callsign, Class, Category, Name, Street, Zip, City, Lng,  Lat, Geocode, Visible
```

Die Spalte Id ist einfach nur eine fortlaufende Id, die restlichen Spalten sollten zum Großteil selbsterklärend sein. Hier könnte man natürlich noch weitere Spalten mit Daten hinzufügen. Das nette an SQL ist, dass man ganz leicht sehr komplexe Datenabfragen machen kann, z.B.

```
SELECT Count(*) FROM Callsigns WHERE City="Berlin"
```

### Zu erledigen
  
1. Beim Parsen wird es bestimmt noch den einen oder anderen Fehler geben, vielleicht kann das jemand noch verbessern. Ich denke aber, zu 99.9% sollte alles in Ordnung sein.
2. Die Spalte *Category* wird momentan noch nicht gesetzt. Die Idee wäre, je nach Art der Station (Klubstation, Relais, etc.) die Kategorie zu setzen.

## Geocoding

Wie kommen wir nun von den in der Datenbank vorhandenen (und hoffentlich korrekt geparsten) Adressen zu Punkten in einer geographischen Karte? Die Antwort heißt *Geocoding*, womit wir dann schließlich im 21. Jahrhundert angekommen sind. Dabei handelt es sich um Datenbanken, die Adressen in geographische Koordinaten umwandeln (Länge/Breitengrad), und diese lassen sich dann in einer Karte visualisieren. Es gibt Geocoding-Schnittstellen von Google (diese habe ich benutzt), aber auch von OpenStreetMap und anderen Diensten. Weiterhin gibt es Python-Bibliotheken mit Schnittstellen zu diesen Schnittstellen. Ich habe [geocoder](https://pypi.python.org/pypi/geocoder) verwendet, das wir wie oben geschildert installiert haben. Wir machen einen kurzen Test mit dem Skript aus dem Archiv:

```
python geocode.py
Address: Alter Hellweg 56, 44379 Dortmund, Deutschland
7.37648 51.49813
```

Das Geocoding war erfolgreich und wir haben Längen- und Breitengrad erhalten. Ist die Adresse nicht vorhanden (in der Realitärt oder in der Geocoding-Datenbank), geht das natürlich nicht. Ein simpler Schreibfehler kann hier schon Probleme bereiten.

Mittels

```
python makegeo.py
```

werden die Adressen in der Datenbank einzeln durchgegangen, ein Geocoding abgefragt und die Koordinaten in die Spalten Lng/Lat eingefügt. Gibt es vom Server keine Fehlermeldung (Adresse nicht gefunden oder ähnlich), wird in der Spalte Geocode eine 1 gesetzt, ansonsten eine 0. Man kann das Skript jederzeit unterbrechen und erneut starten; alle Einträge mit erfolgreichem Geocoding (Geocode=1) werden dabei übersprungen.

Da das Geocoding aus einzelnen Abfragen besteht, dauert dies sehr lange (1 Sekunde je Abfrage). Erschwerend kommt hinzu, dass Google ein Limit von 2,500 Abfragen pro Tag hat. Die 70,000 Adressen zu geocoden, dauert also eine Weile, wenn man nicht mehrere Computer mit verschiedenen IPs benutzen kann. Eine Alternative wäre hier das Geocoding mittels OpenStreetMap. Dazu kann man in ```makegeo.py``` einfach *google* durch *osm* ersetzen (oder durch jeden anderen unterstützten Dienst). 

### Zu erledigen
  
1. Fehler in den Adressen erkennen und korrigieren.  
2. Geocoding-Fehler korrekt abfangen (ganz selten ist das Geocoding "erfolgreich", aber die Koordinaten stimmen nicht).  
3. Andere Dienste nutzen, wie z.B. OpenStreetMap.

## CSV-Datei

Mittels 

```
python makecsv.py
```

erstellt man eine CSV-Datei aus der Datenbank. Dabei gehe ich so vor, dass ich mittels der SQL-Abfrage

```
SELECT Lng, Lat FROM Callsigns WHERE Geocode=1 GROUP BY Lat, Lng
```

zunächst sämtliche Standorte sammle. In einem zweiten Schritt werden für jeden Standort alle Stationen an diesem Ort gesucht. Die Daten dazu werden in der Spalte *Label* der CSV-Datei eingefügt. In der Spalte *Marker* ist eine Anweisung für die Art der Markierung an diesem Ort.

### Zu erledigen

1. Weitere verschiedene Marker, z.B. für Relais oder Klubstationen.

## Google Fusion Tables

Jetzt haben wir alles zusammen für die Visualisierung der Daten. Wir erstellen jetzt eine [Google Fusion Table](https://fusiontables.google.com). Dazu benötigt man einen Google-Account und klickt bei dem gerade genannten Link auf *Create a fusion table*. Dann kann man die erstellte CSV-Datei ```calls.csv``` hochladen. Bei erfolgreichem Import (es sollte eigentlich keine Probleme geben), kan man auf *Map of Lat* klicken und sieht sofort die Punkte visualisiert. Man kann jetzt noch unter *Change map styles* auf *Column* gehen und dort die Spalte *Marker* selektieren. Dann werden unsere individuellen Markierungen übernommen. Weiterhin kann man unter *Change info window* auf *Custom* klicken und dort *{Label}* eingeben, sodass unser individuell erstelltes Label verwendet wird. Fertig!

### Zu erledigen

1. Andere Dienste ausprobieren (obwohl die Fusion Tables recht genial sind).
2. Mit dem Skript ```makekml.py``` kann man auch eine KML-Datei mit den Daten erstellen, die man in viele Programme importieren kann. Ich habe das nicht weiter aktualisiert, aber dies bietet auch noch viele Möglichkeiten.