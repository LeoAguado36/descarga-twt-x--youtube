from flask import Flask, render_template, request, jsonify, Response
import downloader as py
import threading

app = Flask(__name__)

# Definir globalmente progress_queue
progress_queue = []

# Función para enviar el progreso de la descarga
def progress_callback(d):
    if d['status'] == 'downloading':
        # Calculamos el porcentaje de progreso
        progress = d.get('downloaded_bytes', 0) / d.get('total_bytes', 1) * 100
        # Agregar el progreso a la cola para que el endpoint lo pueda transmitir
        progress_queue.append(f"data:{progress:.2f}\n\n")
    elif d['status'] == 'done':  # Cuando la descarga termine
        progress_queue.append("data:100.00\n\n")  # Aseguramos que llegue el 100% al final
        progress_queue.append("data:Download complete\n\n")  # Enviamos el mensaje de "descarga completa"

@app.route('/')
def index():
    return render_template('index.html')

# Este endpoint es el encargado de emitir el progreso en tiempo real
@app.route('/api/progress', methods=['GET'])
def get_progress():
    def generate():
        while not progress_queue:
            # Esperamos hasta que haya algo en el progreso (es decir, que se haya iniciado la descarga)
            pass
        # Emitimos los datos del progreso
        for data in progress_queue:
            yield data
    return Response(generate(), content_type='text/event-stream')

# Endpoint para manejar la solicitud de descarga y pasar el callback
@app.route('/api/data', methods=['POST'])
def received_data():
    link = request.get_json()
    link_url = link['name']
    
    # Usamos un hilo para descargar el video y pasar el callback de progreso
    threading.Thread(target=py.download_video, args=(link_url, progress_callback)).start()

    if "data:100.00\n\n" in progress_queue:
        # Enviamos una respuesta inicial
        return jsonify({'received_data': 'Descarga de video completa'})

if __name__ == '__main__':
    app.run(debug=True)
