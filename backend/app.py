# backend/app.py
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import os
import io
import base64

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate

# Create folders for uploads and outputs
UPLOAD_FOLDER = 'uploads'
OUTPUT_FOLDER = 'outputs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Store uploaded image path
current_image = None

@app.route('/')
def home():
    return jsonify({
        "message": "AI Interior Designer API",
        "status": "running",
        "endpoints": ["/upload", "/generate", "/styles"]
    })

@app.route('/upload', methods=['POST'])
def upload_image():
    """Handle room photo upload"""
    global current_image
    
    if 'image' not in request.files:
        return jsonify({"error": "No image provided"}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({"error": "No file selected"}), 400
    
    # Save uploaded image
    filepath = os.path.join(UPLOAD_FOLDER, 'room.jpg')
    
    # Open, resize, and save
    img = Image.open(file)
    img = img.resize((512, 512))
    img.save(filepath)
    
    current_image = filepath
    
    return jsonify({
        "message": "Image uploaded successfully",
        "filepath": filepath
    })

@app.route('/styles', methods=['GET'])
def get_styles():
    """Return available design styles"""
    styles = [
        {"id": "minimalist", "name": "Minimalist", "description": "Clean, simple, white"},
        {"id": "industrial", "name": "Industrial", "description": "Brick, metal, urban"},
        {"id": "cyberpunk", "name": "Cyberpunk", "description": "Neon, futuristic, RGB"},
        {"id": "modern_luxury", "name": "Modern Luxury", "description": "Gold, marble, elegant"},
        {"id": "scandinavian", "name": "Scandinavian", "description": "Light wood, cozy, hygge"},
        {"id": "midcentury_modern", "name": "Mid-Century Modern", "description": "Retro 1960s, teak"},
        {"id": "japanese_zen", "name": "Japanese Zen", "description": "Natural, peaceful, minimal"},
        {"id": "bohemian", "name": "Bohemian", "description": "Colorful, eclectic, cozy"}
    ]
    return jsonify(styles)

@app.route('/generate', methods=['POST'])
def generate_design():
    """Generate room transformation (will connect to Colab)"""
    global current_image
    
    if not current_image:
        return jsonify({"error": "No image uploaded"}), 400
    
    data = request.json
    style = data.get('style', 'minimalist')
    
    # TODO: This will call Colab API in next step
    # For now, just return placeholder
    return jsonify({
        "message": f"Generating {style} style...",
        "status": "processing",
        "note": "Colab connection coming in next step"
    })

if __name__ == '__main__':
    print("🚀 AI Interior Designer API Starting...")
    print("📍 Server running at: http://localhost:5000")
    print("📁 Upload folder:", UPLOAD_FOLDER)
    print("📁 Output folder:", OUTPUT_FOLDER)
    app.run(debug=True, port=5000)