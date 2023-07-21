import imaplib
import os
from imapclient import IMAPClient
import sys
import logging
import re
import html
from datetime import datetime

# Configuración de conexión
host = '' # servidor de correos, ejemplo mail.munilima.gob.pe
username = '' # correo de roundcube
password = '' # contraseña del correo

# Establecer la codificación de caracteres para la salida
sys.stdout.reconfigure(encoding='utf-8')

# Configuración de registro (logs)
log_file = './correo_log.txt'
logging.basicConfig(filename=log_file, level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Conexión al servidor IMAP
with IMAPClient(host) as client:
    client.login(username, password)

    # Obtener el nombre del usuario del correo (parte izquierda del correo)
    user_folder = re.match(r'([^@]+)@', username).group(1)

    # Carpeta local para guardar los correos descargados
    output_dir = f'./correos/{user_folder}'
    inbox_dir = os.path.join(output_dir, 'Entrada')
    sent_dir = os.path.join(output_dir, 'Enviados')

    # Crear la carpeta del usuario si no existe
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(inbox_dir, exist_ok=True)
    os.makedirs(sent_dir, exist_ok=True)

    # Descargar correos de la carpeta "Entrada"
    client.select_folder('INBOX')
    messages = client.search()
    for uid, message_data in client.fetch(messages, 'RFC822').items():
        email_filename = f'{uid}.eml'
        email_path = os.path.join(inbox_dir, email_filename)

        # Obtener el asunto del correo
        subject_data = client.fetch([uid], ['BODY[HEADER.FIELDS (SUBJECT)]'])
        subject = subject_data[uid][b'BODY[HEADER.FIELDS (SUBJECT)]'].decode(errors='replace')

        # Limpiar y normalizar el asunto del correo para usarlo como nombre de archivo
        subject = re.sub('[^A-Za-z0-9]+', '_', subject)
        subject = html.unescape(subject)
        subject = subject.replace("Subject_", "")
        
        # Limitar el nombre del archivo a 40 caracteres
        subject = subject[:40]
        
        # Obtener la fecha y hora del correo
        date_data = client.fetch([uid], ['INTERNALDATE'])
        internal_date = date_data[uid][b'INTERNALDATE']

        # Formatear la fecha y hora en el formato deseado ("aaaa-MM-dd_HH-mm-ss_")
        parsed_date = datetime.fromtimestamp(internal_date.timestamp())
        formatted_date = parsed_date.strftime("%Y-%m-%d_%H-%M-%S")

        # Reemplazar "Subject_" con la fecha y hora en el nombre del archivo
        new_email_filename = f'{formatted_date}_{subject}.eml'
        new_email_path = os.path.join(inbox_dir, new_email_filename)

        # Guardar el correo en el directorio de salida
        with open(new_email_path, 'wb') as f:
            f.write(message_data[b'RFC822'])

        logging.info(f'Se ha descargado el correo "{subject}" en la carpeta "Entrada"')

    # Descargar correos de la carpeta "Enviados"
    client.select_folder('INBOX.Sent')
    messages = client.search()
    for uid, message_data in client.fetch(messages, 'RFC822').items():
        email_filename = f'{uid}.eml'
        email_path = os.path.join(sent_dir, email_filename)

        # Obtener el asunto del correo
        subject_data = client.fetch([uid], ['BODY[HEADER.FIELDS (SUBJECT)]'])
        subject = subject_data[uid][b'BODY[HEADER.FIELDS (SUBJECT)]'].decode(errors='replace')

        # Limpiar y normalizar el asunto del correo para usarlo como nombre de archivo
        subject = re.sub('[^A-Za-z0-9]+', '_', subject)
        subject = html.unescape(subject)

        # Limitar el nombre del archivo a 40 caracteres
        subject = subject[:40]
        subject = subject.replace("Subject_", "")
        
        # Obtener la fecha y hora del correo
        date_data = client.fetch([uid], ['INTERNALDATE'])
        internal_date = date_data[uid][b'INTERNALDATE']

        # Formatear la fecha y hora en el formato deseado ("aaaa-MM-dd_HH-mm-ss_")
        parsed_date = datetime.fromtimestamp(internal_date.timestamp())
        formatted_date = parsed_date.strftime("%Y-%m-%d_%H-%M-%S")

        # Reemplazar "Subject_" con la fecha y hora en el nombre del archivo
        new_email_filename = f'{formatted_date}_{subject}.eml'
        new_email_path = os.path.join(sent_dir, new_email_filename)

        # Guardar el correo en el directorio de salida
        with open(new_email_path, 'wb') as f:
            f.write(message_data[b'RFC822'])

        logging.info(f'Se ha descargado el correo "{subject}" en la carpeta "SENT"')

print('Descarga de correos completa.')
