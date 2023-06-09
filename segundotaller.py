# -*- coding: utf-8 -*-
"""segundoTaller.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1K0Ugn2FgroqhgwH2-vsPZnYlkQwBk9Fv

# Web Scraping
"""

#Hacemos la peticion a la pagina para traer todo el documento html
from requests import get
url = "https://www.civitatis.com/es/paris/paseo-barco-sena/opiniones/?withText=1"
response = get(url)
#Imprimimos los primeros 500 caracteres del código HTML de la página
response.text[:500]

#Usando BeautifulSoup para analizar el contenido HTML
from bs4 import BeautifulSoup
html_soup = BeautifulSoup(response.text, 'html.parser')
type(html_soup)
#print(html_soup)

#Para el caso de la pagina que seleccione https://www.civitatis.com/es/ estos son los parametros
#Ahora usemos el find_all() método para extraer todos los div contenedores que tienen un 'class': 'o-container-opiniones-small':
movie_containers = html_soup.find_all("div", {'class': 'o-container-opiniones-small'})
print(type(movie_containers))
print(len(movie_containers))

first_movie = movie_containers[18]
first_movie

#Tomamos el dato de la calificiacion
datoCalificacion = first_movie.find("span",{'class': 'm-rating__stars__full'}).text
datoCalificacion

#Tomamos la fecha del comentario
from datetime import datetime

datoFecha = first_movie.p.text
datoFecha = datoFecha.replace(' ', '')
datoFecha

#Tomamos el nombre de la persona que realizo el comentario
datoNombre = first_movie.find("div",{'class': 'opi-name'}).text
datoNombre = datoNombre.strip().strip('\n')
datoNombre

#Tomamos el dato del comentario del usuario
datoComentario = first_movie.find("div",{'class': 'container-opinion-txt'}).p.text
datoComentario = datoComentario.strip().strip('\n')
datoComentario

#Tomamos el dato de con quien viajo
datoViajero = first_movie.find("div",{'class': 'a-opiniones-type'}).div.text
datoViajero = datoViajero.strip().strip('\n')
datoViajero

#Ahora empezamos con el codigo para hacerlo no solo una vez, si no el numero de veces que necesitemos
from time import sleep
from random import randint
from time import time

from IPython.core.display import clear_output

from warnings import warn

datoCalificaciones = []
datoFechas = []
datoNombres = []
datoComentarios = []
datoViajeros = []
start_time = time()
requests = 0
pages = [str(i) for i in range(1,70)]
pais = 'paris'
actividad = 'paseo-barco-sena'

import pandas as pd

for page in pages:
  url = 'https://www.civitatis.com/es/' + pais + '/' + actividad + '/opiniones/' + page + '/?withText=1'
  print(url)
  response = get(url)
  # pausar el loop
  sleep(randint(8,15))
  # Monitoreando la solicitud
  requests += 1
  elapsed_time = time() - start_time
  print('Request:{}; Frequency: {} requests/s'.format(requests, requests/elapsed_time))
  clear_output(wait = True)
  #Lanzar una advertencia para códigos de estado que no sean 200
  if response.status_code != 200:
    warn('Request: {}; Status code: {}'.format(requests, response.status_code))
    # Romper el ciclo si el número de solicitudes es mayor de lo esperado
  if requests > 72:
    warn('El número de solicitudes fue mayor de lo esperado.')
    break

  #Analizar el contenido de la solicitud con BeautifulSoup
  page_html = BeautifulSoup(response.text, 'html.parser')
  mv_containers = page_html.find_all("div", {'class': 'o-container-opiniones-small'})
  for container in mv_containers:
    #Calificacion
    datoCalificacion = container.find("span",{'class': 'm-rating__stars__full'}).text
    datoCalificaciones.append(datoCalificacion)

    #Fecha
    datoFecha = container.p.text
    datoFecha = datoFecha.replace(' ', '')
    #datoFecha = datetime.strptime(datoFecha, "%d / %b / %Y").date()
    datoFechas.append(datoFecha)

    #Nombre
    datoNombre = container.find("div",{'class': 'opi-name'}).text
    datoNombre = datoNombre.strip().strip('\n')
    datoNombres.append(datoNombre)

    #Comentario
    datoComentario = container.find("div",{'class': 'container-opinion-txt'}).p.text
    datoComentario = datoComentario.strip().strip('\n')
    datoComentarios.append(datoComentario)

    #Con quien viajo
    datoViajero = container.find("div",{'class': 'a-opiniones-type'}).div.text
    datoViajero = datoViajero.strip().strip('\n')
    datoViajeros.append(datoViajero)

#Construimos un DataFrame para los datos 
test_df = pd.DataFrame({'Fecha': datoFechas,
                        'Usuario': datoNombres,
                        'Comentario': datoComentarios,
                        'Calificacion': datoCalificaciones,
                        'Con_Quien_Viajo': datoViajeros
                        })
print(test_df.info())
test_df

#Montar el drive
from google.colab import drive
drive.mount('/content/drive')

#Se guarda la data en el drive como csv
test_df.to_csv('/content/drive/MyDrive/2- Unilibre/7moSemestre/programacionAvanzada/segundoCorte/data/datosWebScrapingCivitatis.csv', index=False, encoding='utf-8')

#Se guarda la data en el drive como excel
test_df.to_excel('/content/drive/MyDrive/2- Unilibre/7moSemestre/programacionAvanzada/segundoCorte/data/datosWebScrapingCivitatis.xlsx', index=False, encoding='utf-8')

#Se carga la data de la ubicacion en donde este guardada
import pandas as pd

nuevoDf = pd.read_csv('/content/drive/MyDrive/2- Unilibre/7moSemestre/programacionAvanzada/segundoCorte/data/datosWebScrapingCivitatis.csv')
nuevoDf

#Remplazo los meses por su respectivo en ingles paa poder transformar esta columna en dato fecha
nuevoDf['Fecha'] = nuevoDf['Fecha'].str.replace('Ene', 'Jan')
nuevoDf['Fecha'] = nuevoDf['Fecha'].str.replace('Dic', 'Dec')
nuevoDf['Fecha'] = nuevoDf['Fecha'].str.replace('Ago', 'Aug')
nuevoDf['Fecha'] = nuevoDf['Fecha'].str.replace('Abr', 'Apr')

#Convertimos la columna fecha al tipo de dato fecha
nuevoDf['Fecha'] = pd.to_datetime(nuevoDf['Fecha'], format='%d/%b/%Y')

nuevoDf.info()

#Se Instala la biblioteca que es utilizada como herramienta de analisis de sentimientos

pip install sentiment-analysis-spanish

pip install keras tensorflow

from sentiment_analysis_spanish import sentiment_analysis
sas = sentiment_analysis.SentimentAnalysisSpanish()

#Se hace el analisis de sentimiento textual incluyendo la columna de sentimiento y se hace un inclusion de una columna con el numero del comentario para despues graficar
nuevoDf["Sentimiento"] = nuevoDf["Comentario"].apply(lambda i: sas.sentiment(i))
nuevoDf['Numero'] = nuevoDf.reset_index().index
nuevoDf

#Se crea una serie con el sentimiento de cada registro
polaridad = nuevoDf["Sentimiento"]
polaridad

#Crear eje cartesiano
import matplotlib.pyplot as plt
plt.figure(figsize=(15,10))
axes = plt.gca()
axes.set_ylim([-0.5, 1.5])
plt.scatter(nuevoDf["Numero"], polaridad, color='green', alpha=0.5)
#Título
plt.title("Análisis de sentimiento")
plt.xlabel("Número de Opiniones")
plt.ylabel("Sentimiento")

"""# Comunicacion con los comentarios de youtube mediante la api"""

#Codigo para hacer la descarga de los comentarios de un video de YouTube
from googleapiclient.discovery import build
import pandas as pd

DEVELOPER_KEY = '<colocar clave de desarrollador>'
YOUTUBE_API_SERVICE_NAME = 'youtube'
YOUTUBE_API_VERSION = 'v3'

def get_video_comments(youtube, **kwargs):
    comments = []
    results = youtube.commentThreads().list(
        **kwargs
    ).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            author = item['snippet']['topLevelComment']['snippet']['authorDisplayName']
            date = item['snippet']['topLevelComment']['snippet']['publishedAt']
            comments.append({'Author': author, 'Comment': comment, 'Date': date})

        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = youtube.commentThreads().list(
                **kwargs
            ).execute()
        else:
            break

    return comments

def download_video_comments(video_id):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION, developerKey=DEVELOPER_KEY)

    comments = get_video_comments(youtube, part='snippet', videoId=video_id, textFormat='plainText')

    dfYou = pd.DataFrame(comments)
    dfYou.to_csv('comments.csv', index=False)

download_video_comments('fimAyQpVUYs')

#Se carga la data del archivo temporal que crea el codigo
dfYou = pd.read_csv('comments.csv')

#Se descarga la data a una ubicacion para almacenarla de forma permanente
dfYou.to_csv('/content/drive/MyDrive/2- Unilibre/7moSemestre/programacionAvanzada/segundoCorte/data/videoYoutube.csv', index=False, encoding='utf-8')
dfYou.to_excel('/content/drive/MyDrive/2- Unilibre/7moSemestre/programacionAvanzada/segundoCorte/data/videoYoutube.xlsx', index=False, encoding='utf-8')
dfYou

#Se hace el analisis de sentimiento textual incluyendo la columna de sentimiento y se hace un inclusion de una columna con el numero del comentario para despues graficar
dfYou["Sentimiento"] = dfYou["Comment"].apply(lambda i: sas.sentiment(i))
dfYou['Numero'] = dfYou.reset_index().index
dfYou.head(30)

#Se crea una serie con el sentimiento de cada registro
polaridad = dfYou["Sentimiento"]
polaridad

#Crear eje cartesiano
import matplotlib.pyplot as plt
plt.figure(figsize=(15,10))
axes = plt.gca()
axes.set_ylim([-0.5, 1.5])
plt.scatter(dfYou["Numero"], polaridad, color='green', alpha=0.5)
#Título
plt.title("Análisis de sentimiento")
plt.xlabel("Número de Opiniones")
plt.ylabel("Sentimiento")

"""# Descargar csv de mi correo electronico"""

import imaplib
import email
import csv

# Conéctate a la cuenta de Outlook
mail = imaplib.IMAP4_SSL('outlook.office365.com', '993')
mail.login('<colocarCOrreo>', '<colocarClave>')
mail.select('sent')

# Busca todos los correos electrónicos y guárdalos en una lista
typ, data = mail.search(None, 'ALL')
mail_ids = data[0].split()

# Crea un archivo CSV y escribe los encabezados de columna
with open('emails.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['From', 'Subject', 'Date', 'Body'])

    # Recorre todos los correos electrónicos y escribe sus datos en el archivo CSV
    for num in mail_ids:
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        sender = email_message['From']
        subject = email_message['Subject']
        date = email_message['Date']
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    if "text/plain" in content_type:
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')

        writer.writerow([sender, subject, date, body])

# Cierra la conexión con el servidor de correo electrónico
mail.close()
mail.logout()

import imaplib
import email
import csv

# Conéctate a la cuenta de Outlook
mail = imaplib.IMAP4_SSL('outlook.office365.com', '993')
mail.login('<colocarCOrreo>', '<colocarClave>')
mail.select('sent')

# Busca todos los correos electrónicos y guárdalos en una lista
typ, data = mail.search(None, 'ALL')
mail_ids = data[0].split()

# Crea un archivo CSV y escribe los encabezados de columna
with open('emails.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['From', 'Subject', 'Date', 'Body'])

    # Recorre todos los correos electrónicos y escribe sus datos en el archivo CSV
    for num in mail_ids:
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        sender = email_message['From']
        subject = email_message['Subject']
        date = email_message['Date']
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    if "text/plain" in content_type:
                        for charset in ["utf-8", "ISO-8859-1", "windows-1252"]:
                            try:
                                body = part.get_payload(decode=True).decode(charset)
                                break
                            except UnicodeDecodeError:
                                pass
                        break
        else:
            for charset in ["utf-8", "ISO-8859-1", "windows-1252"]:
                try:
                    body = email_message.get_payload(decode=True).decode(charset)
                    break
                except UnicodeDecodeError:
                    pass

        writer.writerow([sender, subject, date, body])

# Cierra la conexión con el servidor de correo electrónico
mail.close()
mail.logout()

import imaplib
import email
import csv

# Conéctate a la cuenta de Gmail
mail = imaplib.IMAP4_SSL('imap.gmail.com')
mail.login('<colocar correo>', '<colocar clave>')
mail.select('sent')

# Busca todos los correos electrónicos y guárdalos en una lista
typ, data = mail.search(None, 'ALL')
mail_ids = data[0].split()

# Crea un archivo CSV y escribe los encabezados de columna
with open('emails.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['From', 'Subject', 'Date', 'Body'])

    # Recorre todos los correos electrónicos y escribe sus datos en el archivo CSV
    for num in mail_ids:
        typ, data = mail.fetch(num, '(RFC822)')
        raw_email = data[0][1]
        email_message = email.message_from_bytes(raw_email)

        sender = email_message['From']
        subject = email_message['Subject']
        date = email_message['Date']
        body = ""

        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))

                if "attachment" not in content_disposition:
                    if "text/plain" in content_type:
                        body = part.get_payload(decode=True).decode('utf-8')
                        break
        else:
            body = email_message.get_payload(decode=True).decode('utf-8')

        writer.writerow([sender, subject, date, body])

# Cierra la conexión con el servidor de correo electrónico
mail.close()
mail.logout()