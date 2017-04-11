# -*- coding: utf-8 -*-
from funciones_analisis import *

# variables para tweetpy
# Agrega tus llaves de tweeter
consumer_key = "XXXXXXXXXXXXXXXXXXXXXXXXX"
consumer_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_key = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
access_secret = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
# variables para oandapy

OA_At = "practice"           # Tipo de cuenta.
OA_Gn = "M5"                 # Frecuencia de muestra de precio.
OA_In = "USD_MXN"            # Instrumento Financiero a utilizar.
OA_Ai = 1742531              # ID de cuenta
OA_Ta = "America/Monterrey"  # Uso horario
# Aquí agrega tu token
OA_TK = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

if __name__ == '__main__':
    usuario_a_consultar = 'realDonaldTrump'
    cantidad_tweets = 1000
    lista_palabras = ['mexico', 'illega', 'nafta', 'immigra']
    api = retornar_api(consumer_key, consumer_secret, access_key, access_secret)
    datos = consultar_tweets_usuario(api, usuario_a_consultar, cantidad_tweets)
    datos = filtrar_por_palabras(datos, lista_palabras)
    datos = filtrar_tiempos(datos)
    datos = formato_tiempo(datos)
    datos = obtener_precios(datos, OA_At, OA_Tk, OA_In, OA_Ta, OA_Gn)
    datos = marcar_tendencia(datos)
    datos = rendimientos_en_pips(datos)
    writer = pd.ExcelWriter('datos_tweets.xlsx', engine='xlsxwriter')
    datos.to_excel(writer, sheet_name='Sheet1')
    writer.save()
    datos.to_csv("datos_tweets.csv", index=False)
