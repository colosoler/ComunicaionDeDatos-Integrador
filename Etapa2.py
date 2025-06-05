from flask import Flask, render_template, request
import cv2
import io
from PIL import Image
import base64
import numpy as np

app=Flask(__name__)

def digitalizar_imagen(imagen, nueva_resolucion=(100, 100), bits_por_pixel=8):
    file_bytes = imagen.read()
    np_arr = np.frombuffer(file_bytes, np.uint8)
    original_cv = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    original_rgb = cv2.cvtColor(original_cv, cv2.COLOR_BGR2RGB)
    imagen_original = Image.fromarray(original_rgb)
    imagen_muestreada = imagen_original.resize(nueva_resolucion, Image.BILINEAR)

    # 3. Cuantización (reducción de bits)
    if bits_por_pixel == 1:
        imagen_cuantizada = imagen_muestreada.convert("1")  # 1 bit (blanco y negro)
    elif bits_por_pixel == 8:
        imagen_cuantizada = imagen_muestreada.convert("L")  # 8 bits (escala de grises)
    elif bits_por_pixel == 24:
        imagen_cuantizada = imagen_muestreada.convert("RGB")  # 24 bits (color completo)
    else:
        raise ValueError("Solo se admiten 1, 8 o 24 bits por píxel.")

    return imagen_original, imagen_cuantizada

def convertir_a_base64(pil_img):
    buffer = io.BytesIO()
    pil_img.save(buffer, format="JPEG")
    buffer.seek(0)
    img_str = base64.b64encode(buffer.read()).decode('utf-8')
    return f"data:image/jpeg;base64,{img_str}"

    
@app.route('/', methods=['GET', 'POST'])
def index():
    print("Entré a index")
    if request.method == 'POST':
        resolucion_str = request.form['resolucion']
        bits = int(request.form['bits'])
        imagen_file = request.files['imagen']

        w, h = map(int, resolucion_str.split('x'))

        original, modificada = digitalizar_imagen(
            imagen_file,
            nueva_resolucion=(w, h),
            bits_por_pixel=bits
        )

        original_b64 = convertir_a_base64(original)
        modificada_b64 = convertir_a_base64(modificada)

        # Renderizamos index.html con las imágenes para mostrar
        return render_template('index.html',
                               original_img=original_b64,
                               modificada_img=modificada_b64)
    else:
        return render_template('index.html')
 
import webbrowser
import threading

if __name__ == '__main__':
    def abrir_navegador():
        webbrowser.open_new("http://127.0.0.1:5000/")

    threading.Timer(1, abrir_navegador).start()
    app.run(debug=True, use_reloader=False)