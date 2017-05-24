Eine Deutschland-Karte der Funkamateure basierend auf der Rufzeichenliste der Bundesnetzagentur

von [Ulrich Thiel, VK2UTL/DK1UT](mailto:u-thiel@gmx.net)

---

Zur Demonstration der Leichtigkeit der Datenverarbeitung mit  Python habe ich mittels eines Python-Skripts und GoogleMaps die Daten der öffentlichen [Rufzeichenliste der Bundesnetzagentur](https://www.bundesnetzagentur.de/SharedDocs/Downloads/DE/Sachgebiete/Telekommunikation/Unternehmen_Institutionen/Frequenzen/Amateurfunk/Rufzeichenliste/Rufzeichenliste_AFU.html)  visualisiert. Das Resultat ist unten und **[hier](https://fusiontables.googleusercontent.com/embedviz?q=select+col8+from+1lGAOwlSUK7nCUsA0FlRRG9buB1QV51zNzJFUr7yj&viz=MAP&h=false&lat=51.2482144526009&lng=10.020759216308534&t=1&z=6&l=col8&y=2&tmplt=2&hml=TWO_COL_LAT_LNG)** im Vollbild zu sehen. Die Makierungen sind einzelne Koordinaten; an einer Koordinate kann es mehrere Amateurfunkstationen geben. Informationen dazu erscheinen beim Klick auf die Markierung. Eine rote Markierung steht für Klasse A, eine violette für Klasse E und eine blaue für Klasse A und E am selben Ort. Ich beschreibe unten kurz, wie ich vorgegangen bin, denn vielleicht kann das für andere Projekte auch nützlich sein. Stand: Mai 2017.

<iframe width="500" height="600" scrolling="no" frameborder="no" src="https://fusiontables.google.com/embedviz?q=select+col8+from+1lGAOwlSUK7nCUsA0FlRRG9buB1QV51zNzJFUr7yj&amp;viz=MAP&amp;h=false&amp;lat=51.2482144526009&amp;lng=10.020759216308534&amp;t=1&amp;z=6&amp;l=col8&amp;y=2&amp;tmplt=2&amp;hml=TWO_COL_LAT_LNG"></iframe><br>


### Kommentare

* Neben **sehr vielen positiven** Kommentaren gab es vereinzelt Beschwerden bezüglich des Datenschutz. Da ich anderweitig relativ beschäftigt bin und auf die Diskussion keinen Wert lege,  habe ich mich entschlossen, die Karte zu anonymisieren, d.h. keine näheren Informationen zu den Markierungen mehr anzuzeigen. Diese kann man entweder aus der Rufzeichenliste bekommen (nach dem Straßennamen im PDF suchen z.B.) oder indem man sich nach der Anleitung unten eine eigene Karte erstellt. 
* Ich habe die Daten 1:1 aus der PDF-Datei der Bundesnetzagentur übernommen und keine sonstigen Daten erhoben. Die PDF-Datei ist öffentlich verfügbar. 
* Mit der Anleitung unten kann sich jeder selbst die Datenbank und Karte erstellen. Es gibt hier keine Daten zum Download.
* Aufgrund vieler Nachfragen, werde ich die Anleitung noch etwas verbessern.
* Die Vollständigkeit und Aktualität der Karte lässt sich schwer angeben. Die Daten sind aus der PDF-Datei von Mai 2017. Von 76,000 Einträgen sind knapp 5,000 ohne Adressangabe. Wer von den verbleibenden noch aktiv ist oder nicht, kann ich nicht sagen. Einige Adressen beinhalten Tippfehler oder Zusätze, die das automatische Geocoden haben scheitern lassen. 
 
|   | Total  | Class A  | Class E |
|---|---|---|---|
| Records  |  76143 | 67975  |  8168 |
Distinct call signs|		 72322|64224|8098 |
Records w/ address|		 71338|64621|6717|
Distinct call signs w/ address|	 67517|60870|6647|
Records w/ geocode|		 70823|64141|6682|
Distinct call signs w/ geocode|	 67159|60545|6614| 


### Vorgehen

Bei der Rufzeichenliste der Bundesnetzagentur handelt es sich um eine PDF-Datei. Diese habe ich zunächst mit dem Linux-Tool ```ps2ascii``` in eine Text-Datei umgewandelt: 

```
ps2ascii Rufzeichenliste_AFU.pdf > calls.txt
``` 

Mit meinem Python-Skript ```makedb.py``` habe ich diese Text-Datei nun verarbeitet und aus den Daten eine SQL-Datenbank erstellt. Dies ist natürlich der schwierigste Teil. Erschwerend kommt hinzu, dass einige Rufzeichen mehrere Adressangaben haben und, dass Adress-Formatierungen teilweise schlicht fehlerhaft sind. Mein Skript sollte beide Fälle einigermaßen gut behandeln.   
Als nächstes habe ich mit meinem Skript ```makegeo.py``` geographische Koordinaten für die Adressen bestimmt (das nennt man *geocoding*). Für Python gibt es eine eigene Bibliothek namens geocoder, die direkten Zugriff auf die Google-API ermöglicht. Einziger Haken hier ist ein täglicher Limit von 2,500 Abfragen. Das könnte man "umgehen", wenn man Zugriff auf mehrere Computer hat. Bei mir sind schließlich ca. 500 Adressen übrig geblieben, für die ein Geocoding nicht erfolgreich war. Zum einen handelt es sich hierbei schlicht um Schreibfehler, die ich in dieser Menge nicht korrigieren wollte. Zum anderen scheinen es veraltete Adressen zu sein (z.B. "...weg" anstatt "...straße"). Nun habe ich mit meinem Python-Skript ```makecsv.py``` aus den Daten der SQL-Datenbank eine CSV-Datei erstellt. Diese Datei habe ich schließlich in eine [Google Fusion Table](usiontables.google.com) geladen, von wo aus sich die Daten sofort visualisieren lassen. 

*Alternative zum Geocoden:* Man könnte das Skript ```makecsv.py``` so modifizieren, dass die Adressen ebenfalls in der CSV-Datei stehen und dann kann man diese Adresse direkt in der Google Fusion Table geocoden, man braucht also genau genommen ```makegeo.py``` nicht; es ist aber komfortabler.

### Bugs & Zu erledigen
Ich werde wegen Zeitmangel nicht mehr wesentlich weiter an der Karte arbeiten, Beiträge (vor allem Bugfixes) sind aber sehr gerne willkommen. 


1. Bei einigen Records wird das Geocoding fehlgeschlagen sein und irgendwo lokalisiert worden sein, ohne dass dies als fehlerhaftes Geocoding erkannt wurde. Das sollten aber nicht mehr als 50 Fälle sein. Man könnte das vielleicht durch zusätzlichen Vergleich mit OSM-Geocoding erkennen.
2. Man müsste nun ein weiteres Skript erstellen, dass die Datenbank aktualisiert, d.h. nicht mehr vorhandene Einträge erkennt und entfernt, neue hinzufügt. Das sollte mit dem SQL-Backend nicht zu schwer sein.