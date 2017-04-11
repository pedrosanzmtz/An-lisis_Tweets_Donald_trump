import tweepy
import re
import oandapy
import numpy as np
import pandas as pd


def obtener_precios(df, oa_at, oa_tk, oa_in, oa_ta,
                    oa_gn):
    oanda = oandapy.API(environment=oa_at, access_token=oa_tk)
    p_inicial = list()
    p_final = list()
    volatilidad = list()
    for indice, fila in df.iterrows():
        precios = oanda.get_history(instrument=oa_in, start=fila['t_inicial'], dailyAlignment=1,
                                    alignmentTimezone=oa_ta, granularity=oa_gn, count=12)
        precios = pd.DataFrame(precios['candles'])
        p_inicial.append(precios['closeAsk'][0])
        p_final.append(precios['closeAsk'][1])
        rendimientos = np.log(precios['closeAsk'] / precios['closeAsk'].shift(1))
        volatilidad.append(np.std(rendimientos) * 100)
    df['p_inicial'] = p_inicial
    df['p_final'] = p_final
    df['volatilidad'] = volatilidad
    return df


def retornar_api(consumer_key, consumer_secret, access_key, access_secret):
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api_retorno = tweepy.API(auth)
    return api_retorno


def consultar_tweets_usuario(tweeter_api, usuario, cantidad):
    indice = 0
    irregular = 0
    tweets = tweeter_api.user_timeline(screen_name=usuario, count=200)
    ultimo_tweet = tweets[-1].id - 1
    columnas = ('texto', 't_inicial', 'retweets', 'favoritos')
    df = pd.DataFrame(columns=columnas)
    for t in tweets:
        df.loc[indice] = t.text, t.created_at, t.retweet_count, t.favorite_count
        indice += 1
    while len(tweets) > 0 and df.shape[0] + irregular < cantidad:
        tweets = tweeter_api.user_timeline(screen_name=usuario, count=200, max_id=ultimo_tweet)
        irregular = irregular + (200 - len(tweets))
        for t in tweets:
            df.loc[indice] = t.text, t.created_at, t.retweet_count, t.favorite_count
            indice += 1
        ultimo_tweet = tweets[-1].id - 1
    return df


def palabras_en_texto(palabras, texto):
    texto = re.sub(r'\W', '', texto).lower()
    detectado = False
    lista = list()
    for palabra in palabras:
        palabra = palabra.lower()
        relacion = re.search(palabra, texto)
        if relacion:
            detectado = True
            lista.append(palabra)
    return detectado, '-'.join(lista)


def filtrar_por_palabras(df, palabras):
    retorno = df['texto'].apply(lambda tweet: palabras_en_texto(palabras, tweet))
    df['encontrado'] = tuple(map(lambda x: x[0], retorno))
    df['palabras'] = tuple(map(lambda x: x[1], retorno))
    df = df[df.encontrado]
    df = df.drop(['encontrado'], axis=1)
    return df


def filtrar_tiempos(df):
    df['t_inicial'] = pd.to_datetime(df['t_inicial'])
    # Remover los sabados
    sabado = df[df['t_inicial'].dt.dayofweek == 5]
    # Remover los viernes despues de las 22:00:00 utc-0
    viernes = df[df['t_inicial'].dt.dayofweek == 4]
    viernes = viernes[viernes['t_inicial'].dt.hour > 22]
    # Remover los domingos antes de las 12:00:00 utc-0
    domingo = df[df['t_inicial'].dt.dayofweek == 6]
    domingo = domingo[domingo['t_inicial'].dt.hour < 22]
    df = df.drop(sabado.index)
    df = df.drop(viernes.index)
    df = df.drop(domingo.index)
    return df


def formato_tiempo(df):
    df['t_inicial'] = df.t_inicial.apply(lambda x: x.strftime('%Y-%m-%dT%H:%M:%S'))
    return df


def marcar_tendencia(df):
    df['tendencia'] = ""
    df.loc[(df['p_inicial'] > df['p_final']), 'tendencia'] = 'bajista'
    df.loc[(df['p_inicial'] < df['p_final']), 'tendencia'] = 'alcista'
    df.loc[(df['p_inicial'] == df['p_final']), 'tendencia'] = 'igual'
    return df


def rendimientos_en_pips(df):
    df['rendimiento'] = 0.0
    df.loc[(df['tendencia'] == 'bajista'),
           'rendimiento'] = (df['p_inicial'] - df['p_final']) * 10000

    df.loc[(df['tendencia'] == 'alcista'),
           'rendimiento'] = (df['p_final'] - df['p_inicial']) * 10000
    return df
