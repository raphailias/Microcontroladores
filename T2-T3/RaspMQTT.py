import Adafruit_DHT
import RPi.GPIO as GPIO
import time
import json
import paho.mqtt.client as mqttClient
import requests

sensor = Adafruit_DHT.DHT11
GPIO.setmode(GPIO.BOARD)
pino_sensor = 25
url = "things.ubidots.com"
topico = '/v1.6/devices/dht11'
devicelabel = "dht11"
variablename1 = "temp"
variablename2 = "umi"
token = "BBFF-2CpQFojHzjQweOb3TRIYal2cLaCu2d"
devicelabel = "dht11"
porta = 1883

URL = "https://api.openweathermap.org/data/2.5/weather"
PARAMS = {
    'appid' : '0317bc9beed8c75fe5a3cb576349bd7b',
    'lat'   : '-23.5537088',
    'lon'   : '-46.7086153', 
    'units' : 'metric'

    }


print("*** Lendo os valores de temperatura e humidade")

def funcao_publicar(client, userdata, result):
    print("Dados Publicados")
    print(client)
    print(userdata)
    print(result)

cliente = mqttClient.Client("meu_prog")
cliente.username_pw_set(token,password='')
cliente.on_publish = funcao_publicar
cliente.connect(url,port=porta)
cliente.loop_start()








while(1):
    res = requests.get(url = URL, params = PARAMS)
    data = res.json()
    pressao = data['main']['pressure']
    velocidade = data['wind']['speed']
    umid, temp = Adafruit_DHT.read_retry(sensor, pino_sensor)
    payload = json.dumps({"temp":{"value":temp},"umi":{"value":umid},"pressao":{"value":pressao},"velocidade":{"value":velocidade}})
    print("temperatura: ",temp)
    print("humidade: ",umid)
    cliente.publish(topico,payload)
    time.sleep(10)
        
