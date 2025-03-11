import yt_dlp
import imageio_ffmpeg as ffmpeg
import glob
import subprocess
import os

def download_video(link, progress_callback):
    ffmpeg_path = ffmpeg.get_ffmpeg_exe()

    if not ffmpeg_path:
        raise Exception("No se pudo encontrar FFmpeg a través de imageio_ffmpeg.")

    # Configurar opciones de yt-dlp para descargar video en MP4 y audio en M4A
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',  # Video MP4, audio M4A
        'outtmpl': '%(title)s.%(ext)s',  # Nombre del archivo
        'ffmpeg_location': ffmpeg_path,
        'noplaylist': True,  # Si es un video de lista de reproducción, solo descarga el primero
        'progress_hooks': [progress_callback]
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])
        print("Descarga Completa")

    except Exception as e:
        print(f"Hubo un problema al descargar o fusionar el video: {e}")

# Main
if (__name__ == '__main__'):
    link = str(input("Pega la URL del video a descargar: ")).strip()
    download_video(link)
