# Importiere die erforderlichen Module von Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time
import sys
import re

# Ausgabe der Python- und PIP-Versionen
print("Python-Version:", sys.version)
print("PIP-Version:")
try:
    import pip
    print(pip.__version__)
except ImportError:
    print("PIP ist nicht installiert oder nicht gefunden.")

# Setze den Pfad zum ausführbaren ChromeDriver
chromedriver_path = 'C:\\3bwi\\SWP\\Schoolmanager\\chromedriver_win32\\chromedriver.exe'

# Setze die Chrome-Optionen
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--webdriver-path={chromedriver_path}')

# Erstelle eine neue Instanz des Chrome-Treibers mit den Optionen
driver = webdriver.Chrome(options=chrome_options)

# Navigiere zu Google
driver.get('https://www.google.com')

time.sleep(5)

ActionChains(driver).send_keys(Keys.TAB, Keys.TAB, Keys.TAB, Keys.ENTER).perform()

# Finde das Suchfeldelement anhand seines Namen-Attributs (könnte sich im Laufe der Zeit ändern)
search_bar = driver.find_element(By.NAME, 'q')

# Gib etwas in das Suchfeld ein
search_bar.send_keys('webuntis')

# Drücke Enter, um die Suche durchzuführen
search_bar.send_keys(Keys.RETURN)

# Warte einige Sekunden, um das Ergebnis zu sehen (du kannst die Zeit nach Bedarf anpassen)
driver.implicitly_wait(5)

# Versuche, das Element mit partiellem Link-Text zu finden
try:
    Webuntis_link = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, 'WebUntis'))
    )
    # Klicke auf den Link "WebUntis"
    Webuntis_link.click()
except TimeoutException:
    print("Zeitüberschreitung beim Warten auf das Erscheinen des Links 'WebUntis'.")


# Warte darauf, dass die Seite nach dem Klicken auf den Link "WebUntis" geladen wird
WebDriverWait(driver, 20).until(EC.title_contains('WebUntis'))

# Gib "HTL Dornbirn" ein, ohne das Suchfeld zu spezifizieren
driver.switch_to.active_element.send_keys('HTL Dornbirn')

# Drücke Enter, um die Suche durchzuführen
driver.switch_to.active_element.send_keys(Keys.RETURN)

# Warte für 5 Sekunden
time.sleep(5)

# Warte darauf, dass der Stundenplan-Link sichtbar wird und klicke darauf (ersetze dies durch den tatsächlichen Locator)
try:
    WebDriverWait(driver, 20).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="loader"]'))
    )
    print("Seite vollständig geladen.")
except TimeoutException:
    print("Zeitüberschreitung beim Warten auf das vollständige Laden der Seite.")


# Klicke auf den Text "HTL Dornbirn" (ersetze dies durch den tatsächlichen Locator)
try:
    htl_dornbirn_text = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*/text()[contains(.,"HTL Dornbirn")]/parent::*'))
    )
    # Klicke auf den Text "HTL Dornbirn"
    htl_dornbirn_text.click()
except TimeoutException:
    print("Zeitüberschreitung beim Warten auf das Erscheinen des Texts 'HTL Dornbirn'.")

# Logging
print("Clicked on 'HTL Dornbirn'")

# Warte darauf, dass der Stundenplan-Link sichtbar wird und klicke darauf (ersetze dies durch den tatsächlichen Locator)
try:
    WebDriverWait(driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, '//*[@id="loader"]'))
    )
    print("Seite vollständig geladen.")
except TimeoutException:
    print("Zeitüberschreitung beim Warten auf das vollständige Laden der Seite.")

# Klicken auf das gefundene Template, wenn es über dem Schwellenwert liegt

# Setzen Sie den Fokus auf das erste fokussierbare Element der Seite
first_focusable_element = driver.find_element(By.TAG_NAME, 'body')
first_focusable_element.click()

for _ in range(100):  # Begrenzen Sie die Anzahl der Versuche
    # Drücken Sie die Tabulator-Taste
    first_focusable_element.send_keys(Keys.TAB)
    time.sleep(0.5)  # Kurze Verzögerung

    # Überprüfen Sie das aktuell fokussierte Element
    focused_element_text = driver.execute_script(
        "return document.activeElement.textContent || document.activeElement.innerText;"
    )

    if "Office" in focused_element_text:
        print("Das Wort 'Office' gefunden und fokussiert.")
        time.sleep(1)  # Kurze Wartezeit
        break
driver.switch_to.active_element.send_keys(Keys.ENTER)

time.sleep(5)

driver.switch_to.active_element.send_keys('nicolas.theiner@student.htldornbirn.at')

time.sleep(40)

# Maximiere das Browser-Fenster auf Vollbild
driver.fullscreen_window()

time.sleep(5)

# Funktion, um die Farbe in allen Elementen zu überprüfen
def rgba_to_rgb(color):
    """Konvertiert RGBA zu RGB, falls nötig."""
    match = re.match(r'rgba\((\d+), (\d+), (\d+), [\d.]+\)', color)
    if match:
        return f'rgb({match.group(1)}, {match.group(2)}, {match.group(3)})'
    return color
# Stellen Sie sicher, dass die Farbe im richtigen Format ist
color_to_check = 'rgb(196, 198, 198)' # #dedfdf in RGB
def check_color_in_elements(driver, color):
    elements = driver.find_elements(By.XPATH, "//*")
    for element in elements:
        background_color = element.value_of_css_property('background-color')
        color_property = element.value_of_css_property('color')

        # Konvertiere die Farben von RGBA zu RGB, falls nötig
        background_color = rgba_to_rgb(background_color)
        color_property = rgba_to_rgb(color_property)

        if color in [background_color, color_property]:
            print(f"Farbe gefunden in Element mit Tag: {element.tag_name}, Klasse: {element.get_attribute('class')}, ID: {element.get_attribute('id')}")
            return True

    return False

# Überprüfe, ob die Farbe vorhanden ist
if check_color_in_elements(driver, color_to_check):
    print("Farbcode gefunden.")
else:
    print("Farbcode nicht gefunden.")

time.sleep(180)
