import os
import zipfile
import shutil
import subprocess
import sys
import json
import threading
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib

class MusicDownloader:
    """Clase profesional para descargar música de Spotify con características avanzadas"""
    
    def __init__(self, output_dir="downloads", max_workers=3, quality="high"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)
        self.max_workers = max_workers
        self.quality = quality
        self.cache_file = Path(".cache_downloads.json")
        self.cache = self._load_cache()
        self.stats = {
            'total': 0,
            'downloaded': 0,
            'skipped': 0,
            'failed': 0
        }
        
    def _load_cache(self):
        """Cargar caché de canciones ya descargadas"""
        if self.cache_file.exists():
            with open(self.cache_file, 'r') as f:
                return json.load(f)
        return {}
    
    def _save_cache(self):
        """Guardar caché de canciones descargadas"""
        with open(self.cache_file, 'w') as f:
            json.dump(self.cache, f, indent=2)
    
    def _get_song_hash(self, url):
        """Generar hash único para cada canción"""
        return hashlib.md5(url.encode()).hexdigest()
    
    def _is_downloaded(self, song_url):
        """Verificar si una canción ya fue descargada"""
        song_hash = self._get_song_hash(song_url)
        return song_hash in self.cache
    
    def get_playlist_info(self, url):
        """Obtener información de la playlist antes de descargar"""
        try:
            import spotipy
            from spotipy.oauth2 import SpotifyClientCredentials
            
            # Usar credenciales públicas (limitadas pero funcionales)
            sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
            
            playlist_id = url.split('/')[-1].split('?')[0]
            playlist = sp.playlist(playlist_id)
            
            return {
                'name': playlist['name'],
                'total_tracks': playlist['tracks']['total'],
                'description': playlist.get('description', ''),
                'owner': playlist['owner']['display_name']
            }
        except:
            return {'name': 'Unknown', 'total_tracks': 0}
    
    def download_playlist(self, url, zip_name=None, progress_callback=None):
        """
        Descarga una playlist completa con características avanzadas
        
        Args:
            url: URL de la playlist de Spotify
            zip_name: Nombre personalizado para el archivo ZIP
            progress_callback: Función callback para reportar progreso
        """
        print("🎵 SPOTIFY PLAYLIST DOWNLOADER PRO")
        print("=" * 50)
        
        # Obtener info de la playlist
        info = self.get_playlist_info(url)
        print(f"📀 Playlist: {info['name']}")
        print(f"🎼 Total de canciones: {info['total_tracks']}")
        print()
        
        # Crear carpeta temporal
        temp_dir = Path("TEMPORAL")
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir()
        
        print("📥 Iniciando descarga...")
        print(f"⚙️  Hilos paralelos: {self.max_workers}")
        print(f"🎚️  Calidad: {self.quality}")
        print()
        
        # Descargar usando spotdl con opciones avanzadas
        try:
            quality_map = {
                'low': '128k',
                'medium': '192k', 
                'high': '320k'
            }
            
            cmd = [
                sys.executable, '-m', 'spotdl',
                url,
                '--output', str(temp_dir),
                '--format', 'mp3',
                '--bitrate', quality_map.get(self.quality, '320k'),
                '--threads', str(self.max_workers),
                '--print-errors'
            ]
            
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            # Mostrar progreso en tiempo real
            for line in process.stdout:
                print(line, end='')
                if progress_callback:
                    progress_callback(line)
            
            process.wait()
            
        except KeyboardInterrupt:
            print("\n⚠️  Descarga interrumpida por el usuario")
        except Exception as e:
            print(f"\n⚠️  Error durante la descarga: {e}")
        
        # Contar archivos descargados
        mp3_files = list(temp_dir.glob("*.mp3"))
        self.stats['downloaded'] = len(mp3_files)
        
        if not mp3_files:
            print("\n❌ No se descargó ninguna canción")
            shutil.rmtree(temp_dir)
            return None
        
        # Crear ZIP
        if not zip_name:
            zip_name = f"{info['name'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}"
        
        if not zip_name.endswith('.zip'):
            zip_name += '.zip'
        
        zip_path = self.output_dir / zip_name
        
        print(f"\n📦 Creando archivo ZIP: {zip_name}")
        print("-" * 50)
        
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for mp3_file in mp3_files:
                zipf.write(mp3_file, mp3_file.name)
                print(f"  ✓ {mp3_file.name}")
        
        # Limpiar temporal
        shutil.rmtree(temp_dir)
        
        # Mostrar estadísticas
        size_mb = zip_path.stat().st_size / (1024 * 1024)
        
        print("\n" + "=" * 50)
        print("✅ ¡DESCARGA COMPLETADA!")
        print("=" * 50)
        print(f"📁 Archivo: {zip_name}")
        print(f"🎵 Canciones: {len(mp3_files)}/{info['total_tracks']}")
        print(f"📊 Tamaño: {size_mb:.2f} MB")
        print(f"📍 Ubicación: {zip_path.absolute()}")
        print()
        print("💡 SIGUIENTE PASO:")
        print("   1. Copia el ZIP a tu USB")
        print("   2. Extrae el ZIP en tu teléfono")
        print("   3. ¡Disfruta tu música offline! 🎧")
        
        return str(zip_path)
    
    def download_multiple_playlists(self, urls):
        """Descargar múltiples playlists en batch"""
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*50}")
            print(f"PLAYLIST {i}/{len(urls)}")
            print(f"{'='*50}")
            
            result = self.download_playlist(url)
            results.append(result)
        
        return results
    
    def get_stats(self):
        """Obtener estadísticas de descargas"""
        return self.stats


def main():
    """Función principal mejorada con menú interactivo"""
    
    print("╔════════════════════════════════════════════════╗")
    print("║   🎵 SPOTIFY DOWNLOADER PRO - v2.0 🎵        ║")
    print("║   El mejor descargador de música del mundo    ║")
    print("╚════════════════════════════════════════════════╝")
    print()
    
    # Configuración
    print("⚙️  CONFIGURACIÓN")
    print("-" * 50)
    
    quality = input("Calidad de audio (low/medium/high) [high]: ").strip().lower() or "high"
    threads = input("Hilos paralelos (1-5) [3]: ").strip() or "3"
    
    try:
        threads = min(max(int(threads), 1), 5)
    except:
        threads = 3
    
    downloader = MusicDownloader(max_workers=threads, quality=quality)
    
    print()
    print("📋 MODO DE DESCARGA")
    print("-" * 50)
    print("1. Una playlist")
    print("2. Múltiples playlists")
    
    mode = input("\nSelecciona una opción [1]: ").strip() or "1"
    
    try:
        if mode == "1":
            url = input("\n🔗 Pega el link de tu playlist: ").strip()
            nombre = input("📝 Nombre para el ZIP (opcional): ").strip() or None
            
            if url:
                downloader.download_playlist(url, nombre)
            else:
                print("❌ No ingresaste ninguna URL")
                
        elif mode == "2":
            urls = []
            print("\n📝 Ingresa las URLs de tus playlists (Enter vacío para terminar):")
            
            while True:
                url = input(f"  Playlist {len(urls)+1}: ").strip()
                if not url:
                    break
                urls.append(url)
            
            if urls:
                downloader.download_multiple_playlists(urls)
            else:
                print("❌ No ingresaste ninguna URL")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Programa interrumpido por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
