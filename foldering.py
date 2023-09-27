import os

# Directorio donde se encuentran los archivos .txt
directorio_archivos = "C:/ruta/completa/del/folder"

# Obtener una lista de los nombres de los archivos en el directorio
archivos = os.listdir(directorio_archivos)

# Iterar sobre los archivos
for archivo in archivos:
    # Verificar que el archivo tenga la extensión .txt
    if archivo.endswith(".txt"):
        # Obtener el nombre del archivo sin la extensión
        nombre_sin_extension = os.path.splitext(archivo)[0]
        
        # Crear una carpeta con el mismo nombre que el archivo (sin extensión)
        carpeta = os.path.join(directorio_archivos, nombre_sin_extension)
        os.makedirs(carpeta, exist_ok=True)
        
        # Mover el archivo a la carpeta recién creada
        origen = os.path.join(directorio_archivos, archivo)
        destino = os.path.join(carpeta, archivo)
        os.rename(origen, destino)

print("Archivos movidos exitosamente.")
