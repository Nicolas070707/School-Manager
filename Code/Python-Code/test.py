import webuntis

# Anmeldeinformationen
WEBUNTIS_USERNAME = 'Nicolas.Theiner'
WEBUNTIS_PASSWORD = 'NSGJAF7TERTWPAUN'
WEBUNTIS_SERVER = 'webuntis.grupet.at:8080'
WEBUNTIS_SCHOOL = '7037700'  # Schulnummer

# Eine Verbindung zum WebUntis-Server herstellen und die Klassenliste abrufen
with webuntis.Session(
    username=WEBUNTIS_USERNAME,
    password=WEBUNTIS_PASSWORD,
    server=WEBUNTIS_SERVER,
    school=WEBUNTIS_SCHOOL,
    useragent='WebUntis Test'
).login() as s:
    # Klassenliste abrufen
    classes = s.klassen()
    
    # Klassen ausgeben
    print("Liste der Klassen:")
    for klasse in classes:
        print(klasse.name)
