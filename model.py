from tensorflow.keras.models import load_model
from PIL import Image, ImageOps
import numpy as np
def get_class(model_path, labels_path, image_path):
    np.set_printoptions(suppress=True)
    
    # Cargar el modelo con compatibilidad
    model = load_model(model_path, compile=False)
    
    # Cargar etiquetas
    with open(labels_path, "r", encoding="utf-8") as f:
        class_names = [line.strip() for line in f.readlines()]
 # Preprocesamiento de imagen
    image = Image.open(image_path).convert("RGB")
    size = (224, 224)
    image = ImageOps.fit(image, size, Image.Resampling.LANCZOS)
    image_array = np.asarray(image)
    normalized_image_array = (image_array.astype(np.float32) / 127.5) - 1
    
    # Crear array de entrada
    data = np.ndarray(shape=(1, 224, 224, 3), dtype=np.float32)
    data[0] = normalized_image_array
    
    # Predicción
    prediction = model.predict(data)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = float(prediction[0][index])
    
    return class_name[2:] if class_name.startswith("0 ") or class_name.startswith("1 ") else class_name, confidence_score