"""
GUI Profesional para Spotify Downloader
Interfaz gráfica moderna y fácil de usar
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog, messagebox
import threading
from pathlib import Path
import sys
import subprocess

class SpotifyDownloaderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎵 Spotify Downloader PRO")
        self.root.geometry("700x600")
        self.root.resizable(False, False)
        
        # Colores modernos
        self.bg_color = "#1e1e1e"
        self.fg_color = "#ffffff"
        self.accent_color = "#1db954"  # Verde Spotify
        self.secondary_color = "#282828"
        
        self.setup_ui()
        self.is_downloading = False
        
    def setup_ui(self):
        """Configurar interfaz de usuario"""
        
        # Estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Título
        title_label = tk.Label(
            main_frame,
            text="🎵 SPOTIFY DOWNLOADER PRO",
            font=("Helvetica", 20, "bold"),
            bg=self.bg_color,
            fg=self.accent_color
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = tk.Label(
            main_frame,
            text="El mejor descargador de música del mundo",
            font=("Helvetica", 10),
            bg=self.bg_color,
            fg=self.fg_color
        )
        subtitle_label.pack(pady=(0, 20))
        
        # Frame de entrada
        input_frame = tk.Frame(main_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, pady=10)
        
        # URL Label
        url_label = tk.Label(
            input_frame,
            text="🔗 URL de la Playlist:",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg=self.fg_color
        )
        url_label.pack(anchor=tk.W)
        
        # URL Entry
        self.url_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            bd=5
        )
        self.url_entry.pack(fill=tk.X, pady=(5, 15))
        
        # Nombre del ZIP
        name_label = tk.Label(
            input_frame,
            text="📝 Nombre del archivo ZIP:",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg=self.fg_color
        )
        name_label.pack(anchor=tk.W)
        
        self.name_entry = tk.Entry(
            input_frame,
            font=("Helvetica", 10),
            bg=self.secondary_color,
            fg=self.fg_color,
            insertbackground=self.fg_color,
            relief=tk.FLAT,
            bd=5
        )
        self.name_entry.pack(fill=tk.X, pady=(5, 15))
        
        # Frame de opciones
        options_frame = tk.Frame(main_frame, bg=self.bg_color)
        options_frame.pack(fill=tk.X, pady=10)
        
        # Calidad
        quality_label = tk.Label(
            options_frame,
            text="🎚️ Calidad:",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg=self.fg_color
        )
        quality_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        
        self.quality_var = tk.StringVar(value="high")
        quality_combo = ttk.Combobox(
            options_frame,
            textvariable=self.quality_var,
            values=["low (128kbps)", "medium (192kbps)", "high (320kbps)"],
            state="readonly",
            width=20
        )
        quality_combo.grid(row=0, column=1, sticky=tk.W)
        
        # Hilos
        threads_label = tk.Label(
            options_frame,
            text="⚙️ Hilos:",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg=self.fg_color
        )
        threads_label.grid(row=0, column=2, sticky=tk.W, padx=(20, 10))
        
        self.threads_var = tk.IntVar(value=3)
        threads_spin = tk.Spinbox(
            options_frame,
            from_=1,
            to=5,
            textvariable=self.threads_var,
            width=10,
            bg=self.secondary_color,
            fg=self.fg_color,
            buttonbackground=self.secondary_color,
            relief=tk.FLAT
        )
        threads_spin.grid(row=0, column=3, sticky=tk.W)
        
        # Botón de descarga
        self.download_btn = tk.Button(
            main_frame,
            text="⬇️  DESCARGAR PLAYLIST",
            font=("Helvetica", 12, "bold"),
            bg=self.accent_color,
            fg="#000000",
            activebackground="#1ed760",
            relief=tk.FLAT,
            cursor="hand2",
            command=self.start_download,
            height=2
        )
        self.download_btn.pack(fill=tk.X, pady=20)
        
        # Barra de progreso
        self.progress = ttk.Progressbar(
            main_frame,
            mode='indeterminate',
            length=300
        )
        self.progress.pack(fill=tk.X, pady=(0, 10))
        
        # Área de log
        log_label = tk.Label(
            main_frame,
            text="📋 Log de descargas:",
            font=("Helvetica", 11),
            bg=self.bg_color,
            fg=self.fg_color
        )
        log_label.pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(
            main_frame,
            height=12,
            font=("Courier", 9),
            bg=self.secondary_color,
            fg=self.fg_color,
            relief=tk.FLAT,
            bd=5
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Footer
        footer = tk.Label(
            main_frame,
            text="Made with ❤️ by Alvaro Manzo | v2.0",
            font=("Helvetica", 8),
            bg=self.bg_color,
            fg=self.fg_color
        )
        footer.pack(pady=(10, 0))
        
    def log(self, message):
        """Agregar mensaje al log"""
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.root.update()
        
    def start_download(self):
        """Iniciar descarga en thread separado"""
        if self.is_downloading:
            messagebox.showwarning("Descarga en progreso", "Ya hay una descarga en curso")
            return
        
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showerror("Error", "Por favor ingresa una URL de Spotify")
            return
        
        name = self.name_entry.get().strip() or "MI_MUSICA"
        
        # Deshabilitar botón
        self.download_btn.config(state=tk.DISABLED, text="⏳ DESCARGANDO...")
        self.progress.start(10)
        self.is_downloading = True
        
        # Iniciar descarga en thread
        thread = threading.Thread(target=self.download_playlist, args=(url, name))
        thread.daemon = True
        thread.start()
        
    def download_playlist(self, url, name):
        """Descargar playlist (ejecutado en thread separado)"""
        try:
            self.log("🎵 Iniciando descarga...")
            self.log(f"URL: {url}")
            self.log(f"Nombre: {name}")
            self.log("")
            
            # Preparar comando
            quality = self.quality_var.get().split()[0]
            quality_map = {'low': '128k', 'medium': '192k', 'high': '320k'}
            
            temp_dir = Path("TEMPORAL")
            temp_dir.mkdir(exist_ok=True)
            
            cmd = [
                sys.executable, '-m', 'spotdl',
                url,
                '--output', str(temp_dir),
                '--format', 'mp3',
                '--bitrate', quality_map.get(quality, '320k'),
                '--threads', str(self.threads_var.get())
            ]
            
            # Ejecutar spotdl
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                universal_newlines=True
            )
            
            for line in process.stdout:
                self.log(line.strip())
            
            process.wait()
            
            # Crear ZIP
            import zipfile
            mp3_files = list(temp_dir.glob("*.mp3"))
            
            if mp3_files:
                zip_name = f"{name}.zip"
                self.log(f"\n📦 Creando {zip_name}...")
                
                with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for mp3 in mp3_files:
                        zipf.write(mp3, mp3.name)
                        self.log(f"  ✓ {mp3.name}")
                
                import shutil
                shutil.rmtree(temp_dir)
                
                size_mb = Path(zip_name).stat().st_size / (1024 * 1024)
                self.log("")
                self.log("✅ ¡DESCARGA COMPLETADA!")
                self.log(f"📁 Archivo: {zip_name}")
                self.log(f"🎵 Canciones: {len(mp3_files)}")
                self.log(f"📊 Tamaño: {size_mb:.2f} MB")
                
                messagebox.showinfo("¡Éxito!", f"Descarga completada\n{len(mp3_files)} canciones descargadas")
            else:
                self.log("\n❌ No se descargaron canciones")
                messagebox.showerror("Error", "No se pudo descargar ninguna canción")
                
        except Exception as e:
            self.log(f"\n❌ Error: {str(e)}")
            messagebox.showerror("Error", f"Error durante la descarga:\n{str(e)}")
        finally:
            self.is_downloading = False
            self.progress.stop()
            self.download_btn.config(state=tk.NORMAL, text="⬇️  DESCARGAR PLAYLIST")


def main():
    root = tk.Tk()
    app = SpotifyDownloaderGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
