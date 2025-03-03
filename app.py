import yt_dlp
import imageio_ffmpeg as ffmpeg
import tkinter as tk
from tkinter import scrolledtext, filedialog, BooleanVar
import flet as ft
import streamlit as st
import threading
import os

# Obtener la ruta de ffmpeg desde imageio_ffmpeg
FFMPEG_PATH = ffmpeg.get_ffmpeg_exe()

# -----------------------------
# FUNCIONES GENERALES PARA DESCARGA
# -----------------------------
def obtener_info_video(url):
    """Obtiene información del video sin descargarlo."""
    ydl_opts = {"quiet": True, "no_warnings": True, "skip_download": True}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)

def seleccionar_carpeta(permitir_subcarpeta=True):
    """Abre el explorador de archivos para elegir una carpeta y crea una subcarpeta 'Video' si es necesario."""
    path = filedialog.askdirectory()
    if not path:
        return None
    
    if permitir_subcarpeta:
        path = os.path.join(path, "Video")
        os.makedirs(path, exist_ok=True)  # Crea la carpeta solo si no existe

    return path

def download_video(url, formato, log_callback, path):
    """Descarga el video y fusiona audio/video si es necesario."""
    def progress_hook(d):
        if d["status"] == "downloading":
            log_callback(f"Descargando... {d['_percent_str']} ({d['_eta_str']} restantes)\n")
        elif d["status"] == "finished":
            log_callback("\nDescarga completa. Fusionando video y audio...\n")

    ydl_opts = {
        "format": f"{formato}+bestaudio/best",
        "outtmpl": os.path.join(path, "%(title)s.%(ext)s"),
        "progress_hooks": [progress_hook],
        "ffmpeg_location": FFMPEG_PATH,
        "postprocessors": [{
            "key": "FFmpegVideoConvertor",
            "preferedformat": "mp4"
        }]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    log_callback("\n✅ Video listo!\n")

# -----------------------------
# INTERFAZ STREAMLIT
# -----------------------------
def streamlit_ui():
    st.title("YouTube Downloader - Streamlit")
    url = st.text_input("URL del video")

    if url:
        info = obtener_info_video(url)
        formatos = {
            f["format_id"]: f.get("format_note", "N/A")
            for f in info["formats"]
            if f.get("vcodec") != "none" or f.get("acodec") != "none"
        }
        formato = st.selectbox("Selecciona un formato", list(formatos.keys()), format_func=lambda x: formatos[x])

        # Preguntar dónde guardar el archivo
        path = st.text_input("Ruta donde guardar el archivo", value=os.getcwd())
        crear_subcarpeta = st.checkbox("Crear carpeta 'Video'", value=True)

        if st.button("Descargar"):
            if not os.path.isdir(path):
                st.error("❌ Ruta no válida")
            else:
                if crear_subcarpeta:
                    path = os.path.join(path, "Video")
                    os.makedirs(path, exist_ok=True)
                
                st.text("Descargando... espera un momento")
                download_video(url, formato, lambda d: st.text(d), path)

# -----------------------------
# EJECUTAR INTERFAZ
# -----------------------------
if _name_ == "_main_":
    streamlit_ui()  # Para probar Streamlit
