import hashlib
import os

def calcular_hash_archivo(archivo):
    sha256 = hashlib.sha256()
    with open(archivo, "rb") as f:
        while True:
            data = f.read(65536)  # Leer el archivo en bloques de 64KB
            if not data:
                break
            sha256.update(data)
    return sha256.hexdigest()

def calcular_hashes_carpeta(carpeta):
    resultados = {}
    for directorio_raiz, directorios, archivos in os.walk(carpeta):
        for archivo in archivos:
            ruta_completa = os.path.join(directorio_raiz, archivo)
            hash_archivo = calcular_hash_archivo(ruta_completa)
            resultados[ruta_completa] = hash_archivo
    return resultados

def guardar_resultados(resultados, archivo_salida):
    with open(archivo_salida, "w") as f:
        for ruta, hash_archivo in resultados.items():
            f.write(f"{ruta}: {hash_archivo}\n")

if __name__ == "__main__":
    carpeta_a_calcular = "./"  # Reemplaza con la ruta de tu carpeta
    archivo_salida = "hashes.txt"  # Nombre del archivo de salida

    resultados = calcular_hashes_carpeta(carpeta_a_calcular)
    guardar_resultados(resultados, archivo_salida)

    print("Cálculo de hashes completado. Los resultados se han guardado en", archivo_salida)

