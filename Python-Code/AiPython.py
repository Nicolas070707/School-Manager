# Importiere die erforderlichen Module von Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
import time

# Setze den Pfad zum ausführbaren ChromeDriver
chromedriver_path = 'C:\\3bwi\\SWP\\Schoolmanager\\chromedriver_win32\\chromedriver.exe'

# Setze die Chrome-Optionen
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument(f'--webdriver-path={chromedriver_path}')

# Erstelle eine neue Instanz des Chrome-Treibers mit den Optionen
driver = webdriver.Chrome(options=chrome_options)

# Navigiere zu Google
driver.get('https://www.google.com')

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

for _ in range(12):
    ActionChains(driver).send_keys(Keys.TAB).perform()

# Drücke ENTER
ActionChains(driver).send_keys(Keys.ENTER).perform()

# Warte für 5 Sekunden, um das Ergebnis zu sehen (du kannst die Zeit nach Bedarf anpassen)
time.sleep(5)

for _ in range(5):
    ActionChains(driver).send_keys(Keys.TAB).perform()

# Drücke ENTER
ActionChains(driver).send_keys(Keys.ENTER).perform()

# Warte für 5 Sekunden, um das Ergebnis zu sehen (du kannst die Zeit nach Bedarf anpassen)
time.sleep(60)
