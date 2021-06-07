from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as cond
from win10toast import ToastNotifier
import time

pagina = 'https://www.resultadossep.eleccionesgenerales2021.pe/SEP2021/EleccionesPresidenciales/RePres/T'
driver = webdriver.Chrome(executable_path="chromedriver.exe")


def obtener():
    driver.get(pagina)
    driver.minimize_window()
    actualizar()


def show(resultados, actas_porcentaje):
    ToastNotifier().show_toast(f"ACTUALIZACION AL  {actas_porcentaje}", resultados, None, 10)
    print(f"ACTUALIZACION AL  {actas_porcentaje}")
    print(resultados)


def actualizar():

    contador = 1
    driver.get(pagina)
    wait = WebDriverWait(driver, 60)
    castillo = '//*[@id="tableMovil"]/tr[3]/td[5]'
    keiko = '//*[@id="tableMovil"]/tr[4]/td[5]'
    actas = '//*[@id="porActasProcesadas"]'
    wait.until(cond.visibility_of_element_located((By.XPATH, actas and keiko and castillo)))
    actas_porcentaje = driver.find_element_by_xpath(actas).text
    porcentaje_anterior = float (actas_porcentaje[:-1])

    while True:
        driver.get(pagina)
        wait.until(cond.visibility_of_element_located((By.XPATH, keiko)))
        keiko_porcentaje = driver.find_element_by_xpath(keiko).text
        castillo_porcentaje = driver.find_element_by_xpath(castillo).text
        actas_porcentaje = driver.find_element_by_xpath(actas).text

        if float(actas_porcentaje[:-1]) > porcentaje_anterior:
            porcentaje_anterior = float(actas_porcentaje[:-1])
            float_keiko = float(keiko_porcentaje[:-1])
            float_castillo = float(castillo_porcentaje[:-1])
            if float_castillo > float_keiko:
                resultados = f"Adelante Castillo con {castillo_porcentaje} y " \
                             f"Keiko con {keiko_porcentaje} la diferencia es de " \
                             f"{(float_castillo - float_keiko).__round__(3)}%"
            else:
                resultados = f"Adelante Keiko con {keiko_porcentaje} y " \
                             f"Castillo con {castillo_porcentaje} la diferencia es de " \
                             f"{(float_keiko - float_castillo).__round__(3)}%"

            show(resultados, actas_porcentaje)
            print("Esperando media hora\n")
            time.sleep(1800)
        else:
            if contador == 1:
                driver.get("https://www.youtube.com/channel/UCVDWNiB0-My0CEPmYt3L82A")
                driver.maximize_window()
                ToastNotifier().show_toast(f"Suscribete", "Si deseas aprender programación suscribete a mi canal, subiré videos proximamente. El programa retomará automaticamente en 30 segundos", None, 15)
                time.sleep(30)
                driver.minimize_window()
                contador=2
                ToastNotifier().show_toast("Gracias","Pronto subiré tutoriales. Retomando el programa", None,10)

            print("Sincronizando con la ONPE")
            time.sleep(120)


obtener()
