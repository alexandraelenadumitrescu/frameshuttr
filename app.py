from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image, ImageEnhance, ImageFilter
import io
import json

app = Flask(__name__)
CORS(app)  # Permite cereri de la frontend (alt domeniu)

def apply_culling(image):
    """
    SIMULARE CULLING: Aici ar trebui să fie modelul tău de ML.
    De exemplu, un model care verifică claritatea (blur).
    Ca simulare, vom verifica dacă lățimea imaginii este mai mare de 1000px.
    """
    print("Step: Applying Culling...")
    if image.width < 1000:
        # Aruncăm o excepție pe care o vom prinde mai târziu
        raise ValueError("Imaginea nu a trecut de culling (prea mică).")
    # Dacă trece, returnăm imaginea nemodificată
    return image

def apply_style_transfer(image, style_option="style1"):
    """
    SIMULARE STYLE TRANSFER: Aici integrezi modelul tău de style transfer.
    Vom simula cele 3 stiluri cu filtre simple din Pillow.
    """
    print(f"Step: Applying Style Transfer with option: {style_option}...")
    if style_option == "style1": # Artistic -> Sepia-like
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(0.5)
        enhancer = ImageEnhance.Brightness(image)
        image = enhancer.enhance(1.2)
        return image.convert("L").convert("RGB") # Simplistic sepia
    elif style_option == "style2": # Abstract -> Sharpen + Edge Enhance
        return image.filter(ImageFilter.SHARPEN).filter(ImageFilter.EDGE_ENHANCE_MORE)
    elif style_option == "style3": # Modern -> Contrast Boost
        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(1.8)
    return image

@app.route('/process', methods=['POST'])
def process_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image file provided"}), 400

    image_file = request.files['image']
    workflow_data = json.loads(request.form['workflow'])
    
    try:
        # Deschidem imaginea
        image = Image.open(image_file.stream).convert("RGB")

        # Aici procesăm workflow-ul.
        # Aceasta este o implementare foarte simplistă care presupune o ordine liniară.
        # Pentru un sistem complex, ai avea nevoie de un graf pentru a parcurge nodurile.
        
        # Extragem nodurile din workflow
        nodes = workflow_data['drawflow']['Home']['data']
        
        # O listă simplă de acțiuni, poți face un graf mai complex
        # Aici doar simulăm o parcurgere. Într-o aplicație reală, ai parcurge conexiunile.
        # Pentru simplitate, presupunem că flow-ul este corect.
        
        if 'culling' in [node['name'] for node in nodes.values()]:
            image = apply_culling(image)

        style_node = next((node for node in nodes.values() if node['name'] == 'style_transfer'), None)
        if style_node:
            style_option = style_node['data'].get('style', 'style1')
            image = apply_style_transfer(image, style_option)

        # Salvăm imaginea procesată în memorie pentru a o trimite înapoi
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='JPEG')
        byte_arr.seek(0)

        return send_file(byte_arr, mimetype='image/jpeg')

    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)