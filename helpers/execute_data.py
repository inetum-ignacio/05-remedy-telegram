import os
import io
import time
import threading

from datetime import datetime
from data.extract_data import ExtractData


def path_temp():
    absolutepath = os.path.abspath(__file__)
    fileDirectory = os.path.dirname(absolutepath)
    parentDirectory = os.path.dirname(fileDirectory)
    file = os.path.join(parentDirectory, 'data', 'temp_file', 'Report.csv')
    return io.open(file, encoding='latin-1')


def path_temp_absolute():
    path_ruta = "C:\\Users\\Inetum-1421\\Documents\\GithuhWorkbeta\\05-remedy-telegram\\data\\temp_file\\Report.csv"
    return io.open(path_ruta, encoding='latin-1')


def ejecucion_horaria(segundos):
    while True:
        now = datetime.now()
        matriz = ExtractData(path_temp())
        hr_string = now.strftime("%H:%M")
        dt_string = now.strftime("%d/%m/%Y")

        print(f'Hora del sistema: {hr_string}')
        print(f'Fecha del sistema: {dt_string}')

        print(matriz.data_matriz(hr_string, dt_string))

        time.sleep(segundos)


def execute():
    hilo = threading.Thread(target=ejecucion_horaria, args=(60,))
    hilo.start()


if __name__ == '__main__':
    execute()
