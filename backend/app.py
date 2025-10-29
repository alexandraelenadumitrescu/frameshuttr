from flask import Flask, request, jsonify, send_file, render_template
from flask_cors import CORS
from PIL import Image, ImageEnhance
import io
import json
import base64

app = Flask(__name__
            ,template_folder='../frontend'
            
            
            )#app object 
CORS(app)  # leaga fe de be
@app.route('/')
def index():
    return render_template('index.html')

# route 1: Health check
@app.route('/health', methods=['GET'])
def health():
    #return {"status": "online-e ok"}
    return jsonify({"status": "online-e ok"})   


#
#ruta test
@app.route('/test', methods=['POST'])
def test():
    image_file = request.files['image']
    image=Image.open(image_file).convert("RGB")#intoarce o copie a imaginii in RGB

    #interpretam parametrii 
    brightness = float(request.form.get('brightness', 1.0))
    contrast = float(request.form.get('contrast', 1.0))

    #procesam param
    if(brightness != 1.0):
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(brightness)

    if(contrast != 1.0):
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(contrast)

    #trimitem inapoi imaginea procesata
    buffer=io.BytesIO()
    image.save(buffer, format="JPEG",quality=90)  
    buffer.seek(0)

    img_base64 = base64.b64encode(buffer.read()).decode()  
    return jsonify({'status':'success', 'image': f'data:image/jpeg;base64,{img_base64}'})


# #route 2: Process image
# @app.route('/process', methods=['POST'])
# def process_image():
#     """
#     Frontend-ul trimite:
#     - image: fișierul imaginii
#     - workflow: JSON cu setări
    
#     Backend-ul (Flask):
#     - Primește cererea
#     - Procesează imaginea
#     - Trimite înapoi imaginea procesată
#     """
    
#     try:
#         # Primesc cererea
#         if 'image' not in request.files:
#             return jsonify({"error": "No image"}), 400
        
#         image_file = request.files['image']
#         workflow = json.loads(request.form['workflow'])
        
#         # Procesez
#         image = Image.open(image_file.stream).convert("RGB")
#         # ... aplicare filtre, style transfer, etc ...
        
#         # Trimit răspunsul
#         byte_arr = io.BytesIO()
#         image.save(byte_arr, format='JPEG')
#         byte_arr.seek(0)
        
#         return send_file(byte_arr, mimetype='image/jpeg')
    
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
    


if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # debug=True = reload automat la schimbări
    # port=5000 = http://127.0.0.1:5000