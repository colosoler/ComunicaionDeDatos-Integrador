import cv2
from PIL import Image
import io

def digitalizar_imagen(ruta_imagen, nueva_resolucion=(100, 100), bits_por_pixel=8, calidad_jpeg=75):
    """
    Simula la digitalización de una imagen: muestreo, cuantización y compresión.
    
    Args:
        ruta_imagen (str): Ruta del archivo de imagen de entrada.
        nueva_resolucion (int): Nuevo tamaño (imagen cuadrada nueva_resolucion x nueva_resolucion).
        bits_por_pixel (int): Profundidad de bits: 1, 8 o 24.
        calidad_jpeg (int): Calidad de compresión JPEG (1 a 100).

    Returns:
        imagen_original (PIL.Image): Imagen original cargada.
        imagen_modificada (PIL.Image): Imagen digitalizada.
        bytes_comprimidos (bytes): Bytes de imagen JPEG comprimida.
    """

    # 1. Cargar imagen original (OpenCV usa BGR, convertimos a RGB)
    original_cv = cv2.imread(ruta_imagen)
    original_rgb = cv2.cvtColor(original_cv, cv2.COLOR_BGR2RGB)

    # Convertimos a PIL para facilitar los pasos siguientes
    imagen_original = Image.fromarray(original_rgb)

    # 2. Muestreo - cambiar resolución
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

    # 4. Compresión - guardar como JPEG en memoria
    buffer = io.BytesIO()
    imagen_cuantizada.save(buffer, format="JPEG", quality=calidad_jpeg)
    buffer.seek(0)
    bytes_comprimidos = buffer.getvalue()

    return imagen_original, imagen_cuantizada, bytes_comprimidos

from PIL import Image
import matplotlib.pyplot as plt

# Ruta de una imagen de prueba
ruta = "ejemplo.jpg"

original, modificada, salida = digitalizar_imagen(
    ruta_imagen=ruta,
    nueva_resolucion=(100,100),
    bits_por_pixel=8,
    calidad_jpeg=50
)

# Mostrar imágenes lado a lado
plt.subplot(1, 2, 1)
plt.title("Original")
plt.imshow(original)
plt.axis('off')

plt.subplot(1, 2, 2)
plt.title("Digitalizada")
plt.imshow(modificada)
plt.axis('off')

plt.show()

