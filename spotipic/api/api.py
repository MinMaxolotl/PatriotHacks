from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import subprocess  # Import subprocess to run external scripts

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Path to save uploaded images
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    # Check if the 'image' key is in the request files
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    # Get the uploaded image file
    image = request.files['image']

    # If the filename is empty, return an error
    if image.filename == '':
        return jsonify({"error": "No selected image"}), 400

    # Save the image to the server
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    # After saving the image, call the external Python script (test.py)
    try:
        result = subprocess.run(
            ['python3', 'test.py', image_path],  # Command to run the script with the image path
            capture_output=True,  # Capture stdout and stderr
            text=True  # Get the output as a string (not bytes)
        )

        # Check if the subprocess returned an error
        if result.returncode != 0:
            return jsonify({"error": "Failed to process the image", "details": result.stderr}), 500

        # Return the result of the subprocess
        return jsonify({
            "message": "Image uploaded and processed successfully",
            "image_path": image_path,
            "output": result.stdout  # Output from test.py
        }), 200

    except Exception as e:
        # If an error occurs while running the subprocess, return an error response
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)
