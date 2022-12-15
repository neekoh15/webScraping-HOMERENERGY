# Scrpting HOMER Webpage.
import time

from bs4 import BeautifulSoup as Bs
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pynput import keyboard


class Account:
    def __init__(self, email, password):
        self.EMAIL = email
        self.PASSWORD = password


class Proyecto:
    def __init__(self, usuario, nombreProyecto, coordenadas, precioDiesel='0', tipo='RESIDENCIAL', averageLoad='0', solarCost='0', windTurbineType='1', bateryType='1', notas="PROYECTO UTN"):

        self.usuario = usuario
        self.nombre = nombreProyecto
        self.coords = coordenadas
        self.diesel = precioDiesel
        self.notas = notas
        self.tipo = tipo
        self.AvL = averageLoad
        self.SC = solarCost
        self.WTT = windTurbineType   # Turbine Type ( 1 - 9)
        self.BT = bateryType         # Batery type ( 1 - 84)


def createProyect(url, usuario, proyecto):

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    try:
        driver.get(url)
    except:
        print("URL INGRESADA NO ES VALIDA")

    def login():

        # Logging credentials to HomerEnergy.com
        cursor = driver.find_element('id', 'existing_user_email')
        cursor.send_keys(usuario.EMAIL)
        cursor = driver.find_element('id', 'existing_user_password')
        cursor.send_keys(usuario.PASSWORD)
        cursor = driver.find_element('id', 'sign_in_button')
        cursor.click()  # Log In to HomerEnergy.com

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="header"]/div/div/div[2]/a')) # Log Out Button
        )

        driver.get('http://quickstart.homerenergy.com') # Redirect to QUICKSTART

        cursor = driver.find_element('xpath', '//*[@id="content"]/div/div/div/p[3]/button')
        cursor.click() # Click "Next" Button

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="content"]/div[2]/div[1]/div/p[4]/a'))
        )

        cursor = driver.find_element('xpath', '//*[@id="content"]/div[2]/div[1]/div/p[4]/a')
        cursor.click()  # Proceed to Quickstart proyects

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div/div[1]/div/div/div/div/div[1]/p[1]/button'))
        )

        cursor = driver.find_element('xpath', '/html/body/div/div[1]/div/div/div/div/div[1]/p[1]/button')
        cursor.click()   # New Proyect

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[3]/hmr-wizard-controls/div/div[3]/button[1]'))
        )

        cursor = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[3]/hmr-wizard-controls/div/div[3]/button[1]')
        cursor.click()   # "Next" Option

    # -----------    NEW PROYECT WINDOW --------------
    def setupProyect():
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[3]/hmr-wizard-controls/div/div[3]/button[1]'))  # start new proyect
        )

        nombre = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[1]/div[1]/div[1]/input')
        notas = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[1]/div[1]/div[2]/textarea')
        diesel = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[2]/div[2]/span/input')

        nombre.clear()
        nombre.send_keys(proyecto.nombre)
        notas.clear()
        notas.send_keys(proyecto.notas)
        diesel.clear()
        diesel.send_keys(proyecto.diesel)

    # ----- Electrical Load -----------

    def electricalLoad():
        driver.get('http://quickstart.homerenergy.com/#/intro/wizard/load')

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[3]/hmr-wizard-controls/div/div[3]/button[1]'))
        )

        if proyecto.tipo == 'COMERCIAL':
            seleccionTipo = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/a[1]')

        elif proyecto.tipo == 'COMUNIDAD':
            seleccionTipo = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/a[2]')

        elif proyecto.tipo == 'INDUSTRIAL':
            seleccionTipo = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/a[3]')

        else:   # RESINDENCIAL
            seleccionTipo = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/a[4]')

        averageLoad = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div/span/input')

        seleccionTipo.click()

        averageLoad.clear()
        #averageLoad.send_keys("1")
        averageLoad.send_keys(proyecto.AvL)

    # ------- Solar Photovoltaic (PV) -----

    def solarPhotovoltaic():
        driver.get('http://quickstart.homerenergy.com/#/intro/wizard/pv')

        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/div[3]/hmr-wizard-controls/div/div[3]/button[1]'))
        )

        solarCost = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[2]/div/div[1]/div[2]/div/span/input')
        time.sleep(0.5)
        solarCost.clear()
        #solarCost.send_keys("1") # <------   COST
        solarCost.send_keys(proyecto.SC)

        time.sleep(1)

    #   --------- Wind Turbine ---------

    def windTurbine():
        driver.get('http://quickstart.homerenergy.com/#/intro/wizard/wt')

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, '/html/body/div[2]/div/div/div/div[3]/hmr-wizard-controls/div/div[3]/button[1]'))
        )
        time.sleep(1)
        try:
            windTurbineCheckbox = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[1]/div/p/label')
        except:
            windTurbineCheckbox = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[1]/div/p/label')

        time.sleep(0.5)
        windTurbineCheckbox.click()
        time.sleep(1)

        windTurbineDropdown = Select(driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[2]/div[1]/div/div[1]/div/select'))
        windTurbineDropdown.select_by_value(proyecto.WTT)   # Turbine Type ( 1 - 9)

        time.sleep(1)

    #   ---------- Batery ------------------

    def batery():

        driver.get('http://quickstart.homerenergy.com/#/intro/wizard/storage')

        time.sleep(1)

        try:
            bateryType = Select(driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[2]/div[1]/div/div[1]/div/select'))
        except:
            time.sleep(0.5)
            bateryType = Select(driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[2]/div[1]/div/div[1]/div/select'))

            # <-------BATERY TYPE -------->

        bateryType.select_by_value(proyecto.BT)         # Batery type ( 1 - 84)

        bateryCost = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[2]/div/fieldset/div[2]/div[1]/div/div[2]/div/span/input')
        time.sleep(0.5)
        bateryCost.clear()
        bateryCost.send_keys("1") # Cost

        time.sleep(1)

    # ----------- Summary -----------

    def summary():

        driver.get('http://quickstart.homerenergy.com/#/intro/wizard/summary')
        time.sleep(0.5)
        cursor = driver.find_element('xpath', '/html/body/div[2]/div/div/div/div[3]/hmr-wizard-controls/div/div[3]/button[1]')
        time.sleep(0.5)
        cursor.click()

    def scrap():

        WebDriverWait(driver, 9999).until(
            EC.element_to_be_clickable(
                ('xpath', '/html/body/div/div[1]/div/div/div/div/ui-view/div/div/ui-view/div/div[3]/div[2]/p[1]/a[1]'))
        )

        try:
            data1 = driver.find_element('xpath', '/html/body/div/div[1]/div/div/div/div')
            print('succes data 1')
            print(Bs(data1.text, 'lxml').prettify() + '\n----------')
        except:
            print('Fallo data1')
        try:
            data2 = driver.find_element('xpath', '/html/body/div/div[1]/div/div/div/div/ui-view/div/div/ui-view/div/div[3]/div[2]/div[2]/div[1]')
            print('succes data 2')
            print(Bs(data2.text, 'lxml').prettify() + '\n----------')
        except:
            print('Fallo data2')
        try:
            options = driver.find_element('xpath', '/html/body/div/div[1]/div/div/div/div/ui-view/div/div/ui-view/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[1]/div/div[13]/div/a')
        except:
            print('fallo options1')
        try:
            options = driver.find_element('xpath', '/html/body/div/div[1]/div/div/div/div/ui-view/div/div/ui-view/div/div[3]/div[2]/div[2]/div[1]/div[2]/div/div[2]/div/div[13]/div/a')
        except:
            print('fallo options2')

    login()
    setupProyect()
    electricalLoad()
    solarPhotovoltaic()
    windTurbine()
    batery()
    summary()
    scrap()

    while True:
        pass


if __name__ == '__main__':
    HOMER_URL = 'https://users.homerenergy.com/account/sign_in'
    cuenta = Account("YOUR HOMER ACCOUNT'S EMAIL HERE", "YOUR PASSWORD HERE")
    proyecto = Proyecto(cuenta, 'PROYECT-NAME', 'COORDENADAS', 'DIESEL-PRICE', 'RESIDENCIAL', 'AVERAGE-LOAD', 'SOLAR-COST', 'WINDTURBINE-TYPE', 'BATERY-TYPE', 'NOTES')
    createProyect(HOMER_URL, cuenta, proyecto)

