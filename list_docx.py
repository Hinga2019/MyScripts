import os
import glob

def listar_archivos_docx(carpetapadre):
    archivos_docx = []

    # Recorre la carpeta de forma recursiva
    for carpeta_actual, _, archivos in os.walk(carpetapadre):
        for archivo in archivos:
            if archivo.endswith('.docx'):
                ruta_completa = os.path.join(carpeta_actual, archivo)
                archivos_docx.append(ruta_completa)

    return archivos_docx

carpeta_inicial = 'C:/ruta/carpeta/'  # Reemplaza esto con la ruta de tu carpeta
archivos_docx_encontrados = listar_archivos_docx(carpeta_inicial)

for archivo in archivos_docx_encontrados:
    print(archivo)
