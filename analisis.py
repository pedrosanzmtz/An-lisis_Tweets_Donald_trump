# -*- coding: utf-8 -*-
from funciones_analisis import *

# variables para tweetpy

consumer_key = "gBlPQ75wdroVezt5HoYIvErzm"
consumer_secret = "LJNbWEqePHa7GiNpCRKKSS01FoIOZV7Wdfmnxo9V1GHlHXOVrM"
access_key = "784264322893557761-SkRdYJjnWUiqbauxRaBBTvMNGA4yP8i"
access_secret = "BC9p8mnkyTsIqXH7ydYtzbs3QYJ6lvoasy7okjsXgYEdO"

# variables para oandapy

OA_At = "practice"           # Tipo de cuenta.
OA_Gn = "M5"                 # Frecuencia de muestra de precio.
OA_In = "USD_MXN"            # Instrumento Financiero a utilizar.
OA_Ai = 1742531              # ID de cuenta
OA_Ta = "America/Monterrey"  # Uso horario
OA_Tk = "ada4a61b0d5bc0e5939365e01450b614-4121f84f01ad78942c46fc3ac777baa6"

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
