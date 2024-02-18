# Erdungsmessung
Jupyter  Notebook zur Vorbereitung, Durchführung und Auswertung von Erdungsmessungen. 

Einfach die Erdungsmessung_V000.bat Datei doppelt anklicken. 
Die Application öffnet sich im Browser.

Alternative 1:
Öffne Anaconda und aktiviere die Entwicklungsumgebung "DevGround".
Starte Jupyter Lab über das Menu und öffne die "Erdungsmessung_V000.ipy" Datei.
Führe den Code aus.

Alternative 2:
Öffne cmd und gebe "conda voila Erdungsmessung_V000.ipy" ein und führe dieses Kommando aus.

## Konfiguration
1. Windows Einstellungen -> Datenschutz und Sicherheit -> Standort:
    * Ortungsdienste: Ein
    * Apps den Zugriff auf Ihren Standort erlauben: Ein
    * Browser (Microsoft Edge, Google Chrome) -> Zulasssen, dass Desptop-Apps auf Ihren Standort zugreifen: Ein
   
2. Installation GPS-Sensor:
    * GPS-Sensor Columbus P-9 Race anschliessen.
    * Datei `ubloxGnssUsb.inf` per Rechtsklick installieren (Warnungen können ignorierd werden)

      ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/5163bf9c-a9b7-4060-8226-7ee23a383b34)
    * PC Neustarten. 
    * Nach Neustart im Gerätemanager die Installation des GPS-Sensors überprüfen.
                                                  
      ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/a89c181c-ce87-4510-b1ea-8d26bb195516)
  
3. JupyterLab Konfiguration -> Jupyter Terminal:
   Hintergrund: Standardmässig werden vom Jupyter Kernel nur Dateien bis 10MB verarbeitet.
    * Generiere default JupyterLab Konfigurationsdatei: `jupyter-lab --generate-config` 
    * Finden der Konfigurationsdatei: `C:\Users\<WindowsUserName>\.jupyter`
    * Editieren der Konfigurationsdatei: `"websocket_max_message_size": 1000 * 1024 * 1024` (um Dateien bis zu einer Grösse von 1GB zu erlauben).
      Die vollständige Zeile in der Konfigurationsdatei sieht dann wie folgt aus: `c.ServerApp.tornado_settings = {"websocket_max_message_size": 1000 * 1024 * 1024}`
      Dabei das auskommentieren nicht vergessen.
    * Aufruf des Notbboks über JupyterLab: `jupyter-lab --config="jupyter_notebook_config.py"  Erdungsmessung_V000.ipynb`
    * Aufruf des Notbboks über Voila: `voila --config="jupyter_notebook_config.py"  Erdungsmessung_V000.ipynb`
    * Aufruf des Notebooks über Voila (alternativ): `voila Erdungsmessung_V000.ipynb --Voila.tornado_settings="{'websocket_max_message_size': 1048576000}"`

## Anleitung und Erklärungen zur Applikation
1. Offline Katen (Locale Tile Maps):

    * Swiss Map Raster Dateien herunterladen: https://www.swisstopo.admin.ch/de/geodata/maps/smr/smr10.html
    * Die .tif Dateien im Projektverzeichnis `maps\swissmapraster` ablegen.
    * Beim Start der Applikation werden alle abgelegten offline Karten per Default initialisiert und den Karten als Layer hinzugefügt.
    * Die so hinzugefüten Layer können bei Bedarf abgewählt werden.
    * Werden Karten während der Laufzeit der Applikation hinzugefügt können diese folgend eingefügt werden:
       *  Liste der verfügbaren offline Karten aktualisieren.

          ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/e72b40bd-0dd4-45f5-886f-f98dff8cd92f)
       *  Gewünschte Karten markieren und mit Übernehmen zu den Karten hinzufügen. Es ist also möglich Karten nicht zu berücksichtigen.

          ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/765681de-1c5d-480a-b9be-29341ac89305)
       *  Die ausgewählten offline Karten werden in allen Karten in der Applikation hinzugefügt.

          ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/96d7ec17-98e6-4a72-9ce9-6f15ea8fdeb2)
       *  Die offline Karten können gesamthaft abgewählt werden indem Leeren angeklickt wird. Es könnenn alle offline Karten abgewählt und so geladen werden. In dem Fall wird keine der offline Karten hinzugefügt.

          ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/af076291-80fb-4f31-b9ea-f9595ce69938)
2. Frequenzeinfluss:

    * Es ist möglich die Methode der Anwednung von Korrekturfaktoren zu bestimmen.
    * Entsprechend der Auswahl der Anwendung von Korrekturfaktoren werden die Spannungen in den Tabellen, Karten und Charts dargestellt und angepasst.
    * Die gespeicherten Daten behalten dabei ihren ursprüunglich aufgenommen Wert. Es werden lediglich die Visualisierungen in den Tabellen, Karten und Charts angepasst.
    * Per Default wird beim Start der Applikation "Keine Anwendung" verwendet. D.h. es werden keine korrekturen an den gemessenen Spannugnen vorgenommen.
    * Es stehen folgende Mothoden zu Auswahl:
       *  Keine Anwendung: Die Spannungen bleiben unverändert und werden nicht korrigiert.
       *  Minima: Bei mehreren Korrekturfaktoren (mehrtägige Messung) wird der kleinste Korrekturfaktor verwendet.
       *  Maxima: Bei mehreren Korrekturfaktoren (mehrtägige Messung) wird der grösste Korrekturfaktor verwendet.
       *  Durchschnitt: Bei mehreren Korrekturfaktoren (mehrtägige Messung) wird der Durchschnitt aller Korrekturfaktoren verwendet.

          ![Image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/0a6c74a1-1085-4957-b4c9-5e458fb57205)
    * Ist nur ein Korrekturfaktor vorhanden (eintägige Messung), so kann dieser mit einer der drei Methoden Minima, Maxima oder Durchschnitt verwendet werden.
      Bei nur einen Korrekturfaktor gibt es also keine Unterschied zwischen rei Methoden Minima, Maxima und Durchschnitt.
2. Spannungstrichter:
    * Funktionsweise der Posionierungsschaltflächen:
       * Positionieren: Bei vorhandenen GPS Signal wird die Karte auf den aktuellen Standort zentriert.
       * Startpunkt Trichter: Bei vorhandenen GPS Signal werden die aktuellen Koordinaten des Standortes gespeichert und
         als Basis für die Bestimmung der Entfernungen der Messpunkte verwendet.
       * Entferneung: Bei vorhandenen GPS Signal wird die Entfernung zum zuvor gesetzten Startpunkt bestimmt.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/cb2691c1-82b3-4066-b9de-282efd7f461f)
    * Erfassung von Messdaten:
       * Bestimmung der Koordinaten des Messpunktes durch Platzierung eines Markes auf der Karte.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/99c3d261-9f50-4e7a-b681-55ce5215b2b5)
       * Eingabe der Messdaten in die Eingabemaske.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/20cd765c-7e52-4403-8aaa-6d79e4342994)
       * Falls nötig die Optionen über die Checkboxen 2. Messteam und Alterantive Konfiguration auswählen.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/f43e9949-b93a-4487-b737-bbbcbb4a9c76)
       * Die Winkel des Markers sowie die das Aussehen des Markes über Marker Winkel und Marker Style bestimmen.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/ab5e03b4-2dbb-4098-8fda-c8c4fe06e734)

         Hinweis: Der Winkel dreht im Uhrzeigersinn, wobei 0° 12 Uhr bedeutet.
       * Durch die Betätigung der Schaltfläche Übernehmen werden die Daten in der Karte und dem Diagramm sowie der
         Tabelle gespeichert.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/886e9f5e-5b28-4123-b714-69f366167dc3)
    * Ändern von Messdaten:\
       Achtung:    Sollte nur durchgeführt werden, wenn Frequenzeinfluss auf "Keine Anwendung" gesetzt ist!
                   Sonst werden durch die angewandte Methode des Frequenzeinflusses "orginale" Daten verfälscht.
       * Durch Auswahl der Checkbox Bearbeitungsmodus die Editierfunktion aktivieren. Es erscheint die Meldung Bearbeitungsmodus aktiv.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/c68ac917-9f81-44b7-9345-e08f5d01a179)
       * Auswahl des zu bearbeitenden Messpunktes in der Tabelle. Der Einrag wird in der Tabelle blau hinterlegt.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/adae5eac-9875-456b-aa0e-dd9bc9ae5eed)
       * Durch die Betätigung der Schaltfläche Editieren werden die Messdaten in die Eingabemaske geladen und können nun bearbeitet werden.
         Es können alle Daten wie bei der Erfassung von Messdaten geändert werden. D.h. es können auch Marker Winkel, Marker Style,
         2. Messteam oder Alternativkonfiguration geändert werden.\
         Hinweis: Wird nun auf der Karte ein neuer Marker platziert, so werden diese Koordinaten bei der Bearbeitung übernommen. Damit
                  die Position eines Markers nachträglich bearbeitet werden. Wird kein neuer Marker platziert, werden die alten Koordinaten
                  übernommen.
            
         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/05eaa331-6889-4d25-b6f6-c02cb59c0160)
       * Durch die Betätigung der Schaltfläche Übernehmen werden die bearbeiteten Daten in der Karte und dem Diagramm sowie der
         Tabelle gespeichert.\
         Hinweis: Die Funktion der Schaltfläche Übernhemen im Bearbeitungsmodus unterscheidet sich von der Funktion der Shcaltfläche bei
                  Erfassung von Messdaten. Im Bearbeitungsmodus werden Daten Ersetzt während beid er Erfassung Daten hinzugefügt werden.

         ![image](https://github.com/Kalandoros/Grounding_Measurement_Application/assets/129214458/465d0ca9-de54-4348-ae21-a983bdc13ab5)

          

         
