import os
import zipfile
import shutil
import subprocess
import sys
from datetime import datetime

def descargar_y_comprimir_playlist(url_playlist, nombre_zip="MUSICA_WORKOUT.zip"):
    # Crear carpeta temporal para las descargas
    carpeta_descargas = "TEMPORAL"
    if os.path.exists(carpeta_descargas):
        shutil.rmtree(carpeta_descargas)
    os.makedirs(carpeta_descargas)
    
    print(f"📥 Descargando canciones en: {carpeta_descargas}/")
    print("⏳ Esto puede tomar varios minutos. Ten paciencia...")
    print("⚠️  Algunas canciones pueden fallar por límites de YouTube, pero continuará con las demás.\n")
    
    # Descargar las canciones usando spotdl con manejo de errores
    try:
        resultado = subprocess.run(
            [sys.executable, '-m', 'spotdl', url_playlist, '--output', carpeta_descargas],
            capture_output=False,
            check=False  # No lanzar error si el comando falla
        )
        if resultado.returncode != 0:
            print("\n⚠️  Algunas canciones no se pudieron descargar, pero continuando con las que sí...")
    except KeyboardInterrupt:
        print("\n⚠️  Descarga interrumpida. Creando ZIP con las canciones descargadas hasta ahora...")
    except Exception as e:
        print(f"\n⚠️  Error durante la descarga: {e}")
        print("Continuando con las canciones que se descargaron...")
    
    # Usar el nombre proporcionado
    if not nombre_zip.endswith('.zip'):
        nombre_zip += '.zip'
    
    print(f"\n📦 Creando archivo ZIP: {nombre_zip}")     
    
    # Comprimir todas las canciones
    canciones_descargadas = 0
    with zipfile.ZipFile(nombre_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(carpeta_descargas):
            for file in files:
                if file.endswith('.mp3'):
                    ruta_completa = os.path.join(root, file)
                    zipf.write(ruta_completa, file)
                    print(f"  ✓ {file}")
                    canciones_descargadas += 1
    
    # Limpiar carpeta temporal
    shutil.rmtree(carpeta_descargas)
    
    if canciones_descargadas == 0:
        print("\n❌ No se descargó ninguna canción. Eliminando ZIP vacío...")
        if os.path.exists(nombre_zip):
            os.remove(nombre_zip)
        print("\n💡 Intenta de nuevo en unos minutos (puede haber límite de YouTube)")
        return
    
    # Mostrar tamaño del ZIP
    tamano_mb = os.path.getsize(nombre_zip) / (1024 * 1024)
    print(f"\n✅ ¡Listo! Archivo creado: {nombre_zip}")
    print(f"🎵 Canciones descargadas: {canciones_descargadas}")
    print(f"📊 Tamaño: {tamano_mb:.2f} MB")
    print(f"📍 Ubicación: {os.path.abspath(nombre_zip)}")
    print("\n💾 Ahora puedes copiar este archivo a tu USB y extraerlo en tu teléfono")

if __name__ == "__main__":
    try:
        # Solicitar el link de la playlist
        print("🎵 DESCARGADOR DE PLAYLIST DE SPOTIFY 🎵")
        print("-" * 45)
        url = input("Pega aquí el link de tu playlist: ").strip()
        nombre = input("Nombre para el archivo ZIP (ej: MUSICA_WORKOUT): ").strip()
        
        if not url:
            print("❌ No ingresaste ninguna URL")
        else:
            if not nombre:
                nombre = "MUSICA_WORKOUT"
            descargar_y_comprimir_playlist(url, nombre)
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario.")
        print("Las canciones parcialmente descargadas están en la carpeta TEMPORAL/")
