from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import io
import json

app = Flask(__name__)
CORS(app)  # Permite frontend-ul să acceseze backend-ul

# ROUTE 1: Health check
@app.route('/health', methods=['GET'])
def health():
    return {"status": "online"}

# ROUTE 2: Process image
@app.route('/process', methods=['POST'])
def process_image():
    """
    Frontend-ul trimite:
    - image: fișierul imaginii
    - workflow: JSON cu setări
    
    Backend-ul (Flask):
    - Primește cererea
    - Procesează imaginea
    - Trimite înapoi imaginea procesată
    """
    
    try:
        # Primesc cererea
        if 'image' not in request.files:
            return jsonify({"error": "No image"}), 400
        
        image_file = request.files['image']
        workflow = json.loads(request.form['workflow'])
        
        # Procesez
        image = Image.open(image_file.stream).convert("RGB")
        # ... aplicare filtre, style transfer, etc ...
        
        # Trimit răspunsul
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)
        
        return send_file(byte_arr, mimetype='image/jpeg')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # debug=True = reload automat când schimbi codul
    # port=5000 = http://127.0.0.1:5000