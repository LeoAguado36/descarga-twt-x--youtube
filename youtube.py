import yt_dlp

def descargar_video(url, carpeta_destino="."):
    opciones = {
        "format": "best",  # Elige la mejor calidad disponible
        "outtmpl": f"{carpeta_destino}/%(title)s.%(ext)s"
    }
    with yt_dlp.YoutubeDL(opciones) as ydl:
        ydl.download([url])

if __name__ == "__main__":
    url = input("Ingresa la URL del video de YouTube: ")
    descargar_video(url)