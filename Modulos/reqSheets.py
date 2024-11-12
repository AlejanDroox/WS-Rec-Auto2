from google.oauth2.credentials import Credentials
from googleapiclient.errors import HttpError
from googleapiclient.discovery import build
from google.oauth2 import service_account
from genrecord import ExtraerDatos
import pandas as pd
import json
import os 

def Peticion(tasa):
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    KEY = 'key.json'
    # Escribe aqui el ID de tu documento:
    SPREADSHEET_ID = '17bI-e8bjwffsfHT5iUaCeD9sfYu61X3_q2IUGV4MJ-g'
    creds = None    
    creds = service_account.Credentials.from_service_account_file(KEY, scopes=SCOPES)
    service = build('sheets', 'v4', credentials=creds)
    sheet = service.spreadsheets()
    with open(r'Modulos\precios.json', 'r') as archivo:
        datos = json.load(archivo)
    

    plataformas = datos.keys()
    for i in plataformas:
        try:
            RANGE_NAME = f'{i}!A1:Z'
            result = service.spreadsheets().values().get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME).execute()
            df = pd.DataFrame(result.get('values', []))
            name= f'{i}.csv'
            df.to_csv(name,index=False, header=False)
            
            ExtraerDatos(name=name, Servicio=i, precio=datos[i], tas=tasa)
            #os.remove(f'{i}.csv')
                
        except HttpError as e:
            resp = str(e.resp.status)
            if resp[0] == '5':
                print(f'ERROR DE SEVIDOR {resp}:')
            elif resp == '400':
                print(f'FALLO TIPO 1AL OBTENER DATOS DE LA TABLA {i}\nComprube si la tabla existe o si esta bien escrita')
            else:
                print(f'ERROR HTTP {resp}: Generando informe de error')
                with open(f'Informe_{resp}', 'a',encoding='utf-8') as a:
                    a.write(f'{resp}:\n\n')
                    a.write(e)
                    a.write('\n\n')
        except KeyError as error:
            print(f'FALLO TIPO 2 AL OBTENER DATOS DE LA TABLA {i} \n Verifique el nombre de las columnas ')
            print(F'COLUMNA DE ERROR: {error.args}')


                    
