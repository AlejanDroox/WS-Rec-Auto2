import pandas as pd
from mensaje import sendMessage
lista_Reportes = []
lista_pre_Cortes = []
msg_last_resort = """Recordatorio de pago 🌑🌙
¿ya renovaste tu suscripción? Recuerda que hoy vence tu plan y perderás el acceso ☹.

_____________
Esto es un mensaje automático 🤖"""
msg_cut = """Notificación de corte ❌
¡Atención! tu servicio ha sido suspendido debido a que no has renovado tu suscripción. Para restablecerlo de inmediato, por favor ponte en contacto con nuestro soporte ☺.

_____________
Esto es un mensaje automático 🤖"""
#clases 
class ReporteN():
    def __init__(self, Plataforma:str, User:str, price:float, mail, telefono, index, DiasV):
        self.Plataforma = Plataforma
        self.User = User
        self.price = float(price)
        self.mail = mail
        self.telefono = telefono
        self.index = index
        self.VenceEn = DiasV
        self.mensaje = f"""¡Buen dia! {self.VenceEn}: 📆
📩 {self.mail}
👤  {self.User}
-------------------------
Total a cancelar🛒 Divisas 💰: {price} / Bolívares 🇻🇪:  {round(price*tasa,2)}
¿Deseas continuar con el servicio? 🤝"""
    def setter_index_list(self, i):
        self.index_list = i
class ReporteC():
    def __init__(self, Telefono:int, dias: int, Nombre: str, index:int, precio: int, Combo: str) -> None:
        self.Plataforma = Combo
        self.telefono = Telefono
        self.index = index 
        if dias >= 0:
            vence = f'Vence en {dias} dia{None if dias != 1 else 's'}'
        else:
            vence = f'Vence hoy'
        self.mensaje = f''' ¡Buen dia! Queremos informarte que tu *{Combo}* a nombre de {Nombre} {vence}: 📆
¿Deseas continuar con el servicio? 🤝
Total a cancelar🛒 Divisas 💰: {precio}$ / Bolívares 🇻🇪:  {round(precio * tasa,2)}Bs'''
    def setter_index_list(self, i):
        self.index_list = i


#funciones
def ExtraerDatos(name,precio, Servicio, tas):
    global tasa
    tasa = tas
    dias = ['0','2', '1', '-1', '-2', '-3'] # dias a los que se mandaran recordatorio
    TipoNormal = ['PANTALLA', 'CUENTA', 'X1', 'X2'] # lista de las opciones que pasararian como normal
    Combos = ['COMBO 2', 'COMBO 5']

    with open(f'R-{Servicio}.txt', 'w', encoding='utf-8') as archivo:
        archivo.write(f"\n\n##### REPORTES DE {Servicio}")
    df = pd.read_csv(name)
    df = df.fillna('valueNone')
    nulo = 'valueNone'
    for indice, fila in df.iterrows():
        if fila['STATUS'] != nulo:
            status = fila['STATUS']
        tipo = fila['TIPO']
        if Servicio == 'COMBOS':
            Nombre = fila['USUARIO']
        else:
            if fila['CORREO'] != nulo:
                correo = fila['CORREO']
        if fila['DIASV'] == nulo:
            continue
        #print(str(fila['DIASV']))
        if Servicio in ['MAX', 'PARAMOUNT'] and fila['DIAS'] != 'valueNone':
            if int(fila['DIAS']) == 1:
                msg = f""" La cuenta {Servicio}: {fila['CORREO']}
                indice: {indice+2}
                Le quedan {fila['DIAS']}"""
                #sendMessage('584147056701', msg)
        try:
            if str(int(fila['DIASV'])) not in dias or (status not in ['ACTIVA', 'HOGAR']):
                continue
        except ValueError as e:
            print(f'valor no valido en la columna DIASV en el indice {indice+2} de la tabla {Servicio} \nNo se pudo generar este reporte')
        
        valor = fila["DIASV"]
        tipo = fila['TIPO']
        if Servicio == 'COMBOS':
            combo = fila['TIPO']
            GenerarReporteCombo(Telefono=int(fila['TELEFONO']), Nombre=Nombre, index= indice +2, diasv=valor, Combo=combo, precio=precio[combo])
        else:
            try:
                Nombre = fila['PANTALLA']
            except:
                Nombre = None
            try:
                if fila['TIPO'] in TipoNormal:
                    Generar_Reporte(Mail=correo, price=precio[tipo], plat=Servicio, index= indice+2,Per=Nombre, Telefono=int(fila['TELEFONO']), dias=valor)
            except ValueError:
                print(ValueError)
                print(f'ERROR DE VALOR: compruebe los valores de la tabla {Servicio} indice: {indice+2}')
            except KeyError as error:
                print(f'Error de clave: verificar la sintaxis de la columna "TIPO" en la fila {indice+2} de la tabla {Servicio}')
                print(f'valor {error.args} no valido | este tiene que ser "PANTALLA" o "CUENTA"')

def Generar_Reporte(Per, Mail, price, plat, index, Telefono, dias):
    if Per != None:
        dias = int(dias)
        if dias == 0:
            tiempo = f'La siguiente Pantalla de {plat} Vence Hoy'
        else:
            tiempo = f'La siguiente Pantalla de {plat} vence en {dias} dia{'s' if dias != 1 else ''}'
    else:
        if dias == 0:
            tiempo = f'Su Cuenta de {plat} vence hoy'
        else:
            tiempo = f'Su Cuenta de {plat} vence en {dias} dia{'s' if dias != 1 else ''}'
        Per = ''
    
    New = ReporteN(User=Per, mail=Mail, price=price, Plataforma=plat, index= index, telefono=Telefono, DiasV=tiempo)
    if dias == 0: 
        lista_pre_Cortes.append(New)
    elif dias < 0:
        New.mensaje = msg_cut
    lista_Reportes.append(New)
    New.setter_index_list(len(lista_Reportes) - 1)
    with open(f'R-{plat}.txt', 'a', encoding='utf-8') as archivo:
        archivo.write(f"\n\n##### numero en tabla: {index} Telefono: {Telefono} #####\n\n")
        archivo.write(New.mensaje)

def GenerarReporteCombo(Telefono: int, Nombre: str, index:int, diasv:int, Combo: str, precio: float):
    New = ReporteC(Telefono=Telefono,dias=diasv, Nombre=Nombre,index=index, Combo=Combo, precio=precio)
    if diasv == 0:
        lista_pre_Cortes.append(New)
    elif dias < 0:
        New.mensaje = msg_cut
    lista_Reportes.append(New)
    New.setter_index_list(len(lista_Reportes) - 1)
    with open(f'R-Combos.txt', 'a', encoding='utf-8') as archivo:
        archivo.write(f"\n\n##### numero en tabla: {index} Telefono: {Telefono} #####\n\n")
        archivo.write(New.mensaje)


def Reports_list() -> list:
    return lista_Reportes
def Cut_list() -> list:
    for i in lista_pre_Cortes: i.mensaje = msg_last_resort
    return lista_pre_Cortes
