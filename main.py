import subprocess 
import os

def start():
    comando = r"start cmd /k python Modulos\Reportes.py"
    subprocess.run(comando, shell=True)
    
    #iniciar un servidor que tengo en api whatsapp en esta terminal
    ruta = 'Modulos/api-whatsapp-ts'
    os.chdir(ruta)
    ejecutar = 'npm install'
    os.system(ejecutar)
    os.system('cls')
    ejecutar = 'npm run build'
    os.system(ejecutar)
    os.system('cls')
    ejecutar = 'npm run dev'
    os.system(ejecutar)
start()