import os

# Abre el archivo de texto
with open("rutas.txt", "r") as f:
    # Lee cada ruta del archivo
    for ruta in f.readlines():
        # Borra el archivo
        os.remove(ruta.strip())

# Imprime un mensaje de éxito
print("Archivos borrados con éxito.")

