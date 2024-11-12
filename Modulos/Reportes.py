#from Modulos.reqSheets import Peticion
#from Modulos.genrecord import Reports_list
from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
import pandas as pd

from genrecord import Reports_list, Cut_list
from reqSheets import Peticion
from mensaje import sendMessage




def main():
    print('             ####################')
    print('             #                  #')
    print('             #   Recordatorios  #')
    print('             #     Rick Store   #')
    print('             #                  #')
    print('             ####################')

    print('Espere unos segundos en lo que Inicializa el servidor')
    print('             Y generamos los recordatorios ')


    print('Obteniendo datos de google sheets')
    global tasa # Globalizo la variable
    tasa = input('introduca la tasa del dia porfavor: ')
    try:
        tasa = float(tasa)
    except:
        print('error introduzca solo datos numericos')
        tasa = input('introduca la tasa del dia porfavor: ')
        tasa = float(tasa)
    Peticion(tasa) #llamo funciona que pide y procesa los datos de google sheets
    if opcion := input('Desea mandar los mensajesde 0 o normales? \nPulse 0 para los mismos de lo contrario se seleccionara los normales') == '0':
        reportes = Cut_list()
    else:
        reportes = Reports_list()
    print(f'Se generaron {len(reportes)} de reportes')
    input('precione enter para empezar a mandar  los mensajes ')
    contador = 0
    opcionNegada = None
    opcionSelect = None
    opcion = input('¿Desea mandar empezar a mandar a partir de cierto indice s/n ')
    if opcion.lower() == 's':
        index_select = input('introduzca el indice a partir del cual quiera mandar ')
    else:
        index_select = -1
    index_select = int(index_select)
    opcion = input('¿Desea mandar el lote completo o por grupos?\npresione g para grupos o deje vacio para completo ')
    if opcion.lower() == 'g':
        print('Usted ha elegido opcion por grupos')
        for i in reportes:
            if i.index_list < index_select:
                continue
            if i.Plataforma == opcionNegada:
                continue
            if i.Plataforma != opcionSelect:
                opcion = input(f'Viene el grupo de {i.Plataforma} ¿Desea mandarlos Y/N? ')
                if opcion.lower() != 'y':
                    opcionNegada = i.Plataforma
                    continue
                else:
                    opcionSelect = i.Plataforma
            print(i.Plataforma, ' ', i.index)
            print(i.index_list)
            sendMessage(f'{i.telefono}', i.mensaje)
            #print(i.index)

    else:        
        for i in reportes:
            if i.index_list <= index_select:
                continue
            print(i.Plataforma, ' ', i.index)
            print(i.index_list)
            #sendMessage(f'584147056701', i.mensaje)
            sendMessage(f'{i.telefono}', i.mensaje)
            #print(i.index)


        
if __name__ == '__main__':
    main()






