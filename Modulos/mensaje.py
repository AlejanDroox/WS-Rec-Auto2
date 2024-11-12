import requests
import time
import random as r
def sendMessage(para, mensaje):
    url = 'http://localhost:3001/lead'
    
    data = {
        "message": mensaje,
        "phone": para
    }
    headers = {
        'Content-Type':'application/json'
    }
    #print(data)
    response = requests.post(url, json=data, headers=headers)
    time.sleep(r.randint(2,5))
    print(response)
    return response

#sendMessage('584126468694', 'hola')