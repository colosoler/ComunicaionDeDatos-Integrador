from flask import Flask, request, send_file
from PIL import Image
import io
import cv2

app = Flask(__name__)

def digitalizar_imagen(imagen_bytes, nueva_resolucion=(100, 100), bits_por_pixel=8, calidad_jpeg=75):
    original_cv = cv2.imdecode(np.frombuffer(imagen_bytes, np.uint8), cv2.IMREAD_COLOR)
    original_rgb = cv2.cvtColor(original_cv, cv2.COLOR_BGR2RGB)
    imagen_original = Image.fromarray(original_rgb)

    imagen_muestreada = imagen_original.resize(nueva_resolucion, Image.BILINEAR)

    if bits_por_pixel == 1:
        imagen_cuantizada = imagen_muestreada.convert("1")
    elif bits_por_pixel == 8:
        imagen_cuantizada = imagen_muestreada.convert("L")
    elif bits_por_pixel == 24:
        imagen_cuantizada = imagen_muestreada.convert("RGB")
    else:
        raise ValueError("Bits no válidos")

    buffer = io.BytesIO()
    imagen_cuantizada.save(buffer, format="JPEG", quality=calidad_jpeg)
    buffer.seek(0)
    return buffer

import numpy as np

@app.route('/procesar', methods=['POST'])
def procesar():
    imagen = request.files['imagen']
    resolucion = request.form['resolucion']  # ej: "1920x1080"
    bits = int(request.form['bits'])

    ancho, alto = map(int, resolucion.lower().split('x'))
    calidad = int(request.form.get('calidad', 75))  # por si querés ajustar compresión también

    imagen_bytes = imagen.read()
    imagen_modificada = digitalizar_imagen(
        imagen_bytes,
        nueva_resolucion=(ancho, alto),
        bits_por_pixel=bits,
        calidad_jpeg=calidad
    )

    return send_file(imagen_modificada, mimetype='image/jpeg')

if __name__ == '__main__':
    app.run(debug=True)

