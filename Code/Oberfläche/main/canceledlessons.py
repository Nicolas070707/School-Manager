import sys
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
import time
import os

def find_canceled_lessons(week):
    url = f'https://hypate.webuntis.com/timetable-students-my/{week}'

    # Starte den Webdriver
    driver = webdriver.Chrome()

    # Lade die Seite
    driver.get(url)


    # Gib "HTL Dornbirn" ein, ohne das Suchfeld zu spezifizieren
    time.sleep(5)
    driver.switch_to.active_element.send_keys('HTL Dornbirn')
    driver.switch_to.active_element.send_keys(Keys.RETURN)

    # Warte für 5 Sekunden
    time.sleep(5)

    # Warte darauf, dass der Stundenplan-Link sichtbar wird und klicke darauf
    try:
        WebDriverWait(driver, 20).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="loader"]'))
        )
        print("Seite vollständig geladen.")
    except TimeoutException:
        print("Zeitüberschreitung beim Warten auf das vollständige Laden der Seite.")

    # Klicke auf den Text "HTL Dornbirn"
    try:
        htl_dornbirn_text = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//*/text()[contains(.,"HTL Dornbirn")]/parent::*'))
        )
        htl_dornbirn_text.click()
    except TimeoutException:
        print("Zeitüberschreitung beim Warten auf das Erscheinen des Texts 'HTL Dornbirn'.")

    # Logging
    print("Clicked on 'HTL Dornbirn'")

    # Warte darauf, dass der Stundenplan-Link sichtbar wird und klicke darauf
    try:
        WebDriverWait(driver, 10).until(
            EC.invisibility_of_element_located((By.XPATH, '//*[@id="loader"]'))
        )
        print("Seite vollständig geladen.")
    except TimeoutException:
        print("Zeitüberschreitung beim Warten auf das vollständige Laden der Seite.")

    # Setzen Sie den Fokus auf das erste fokussierbare Element der Seite
    first_focusable_element = driver.find_element(By.TAG_NAME, 'body')
    first_focusable_element.click()

    for _ in range(100):  # Begrenzen Sie die Anzahl der Versuche
        first_focusable_element.send_keys(Keys.TAB)
        time.sleep(0.5)

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

    driver.switch_to.active_element.send_keys(username)
    driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(5)

    driver.switch_to.active_element.send_keys(password)
    driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(5)

    driver.switch_to.active_element.send_keys(Keys.ENTER)
    time.sleep(5)

    driver.fullscreen_window()

    # Wechseln Sie in den iFrame, falls das Element darin ist
    try:
        iframe = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, 'iframe'))
        )
        driver.switch_to.frame(iframe)
        print("Wechselte in den iFrame.")
    except TimeoutException:
        print("Kein iFrame gefunden.")

    # Versuche das div-Element zu finden
    try:
        rendered_entry_divs = WebDriverWait(driver, 30).until(
            EC.presence_of_all_elements_located((By.CLASS_NAME, 'renderedEntry'))
        )
        print("renderedEntry divs gefunden.")
    except TimeoutException:
        print("Zeitüberschreitung beim Warten auf das div mit der Klasse 'renderedEntry'.")

    # Speichern der Elemente mit der gewünschten Hintergrundfarbe
    filtered_divs = []
    for div in rendered_entry_divs:
        try:
            background_color = div.value_of_css_property('background-color')
            if background_color == 'rgba(177, 179, 180, 0.7)':
                filtered_divs.append(div)
        except StaleElementReferenceException:
            print("Stale element reference exception encountered. Element is no longer in the DOM.")

    print(f"Anzahl der renderedEntry divs mit Hintergrundfarbe 'rgba(177, 179, 180, 0.7)': {len(filtered_divs)}")

    # Ausgabe der Werte der gefilterten Divs
    lessons = []
    for div in filtered_divs:
        try:
            inner_html = div.get_attribute('innerHTML')
            soup = BeautifulSoup(inner_html, 'html.parser')
            spans = soup.find_all('span')
            time_div = soup.find('div', class_='topBottomRow')  # Zeitinformation extrahieren
            time_text = time_div.text.strip() if time_div else 'Unbekannte Zeit'
            if len(spans) >= 4:
                klasse = spans[0].text if spans[0] else 'Unbekannt'
                lehrer = spans[1].text if spans[1] else 'Unbekannt'
                fach = spans[2].text if spans[2] else 'Unbekannt'
                raum = spans[3].text if spans[3] else 'Unbekannt'
                lessons.append(f"Zeit: {time_text}, Klasse: {klasse}, Lehrer: {lehrer}, Fach: {fach}, Raum: {raum}")
            else:
                print("Nicht genügend Span-Tags gefunden.")
        except StaleElementReferenceException:
            print(f"Stale element reference exception encountered. Element is no longer in the DOM.")

    driver.quit()
    return lessons

if __name__ == "__main__":
    week = sys.argv[1] if len(sys.argv) > 1 else '2024-05-17'
    output_file = 'output.txt'
    canceled_lessons = find_canceled_lessons(week)
    with open(output_file, 'w') as f:
        if canceled_lessons:
            for lesson in canceled_lessons:
                f.write(f"{lesson}\n")
        else:
            f.write("Keine Fehlstunden in dieser Woche\n")
