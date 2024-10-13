from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import subprocess
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    # Check if the 'image' key is in the request files
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "No selected image"}), 400

    # Save the image to the server
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    try:
        # Run the external Python script and capture the output
        result = subprocess.run(
            ['python3', 'Data2Spotify.py', image_path],  # Command to run the script with the image path
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            return jsonify({
                "error": "Failed to process the image",
                "stderr": result.stderr  # Return stderr for debugging
            }), 500

        # Now we expect the output from the subprocess to be JSON formatted
        try:
            data = json.loads(result.stdout)  # Parse the output into a JSON object
        except json.JSONDecodeError:
            return jsonify({
                "error": "Output from the image processing script is not valid JSON",
                "stdout": result.stdout
            }), 500

        return jsonify({
            "message": "Image uploaded and processed successfully",
            "image_path": image_path,
            "mapThisString": data  # Send the parsed JSON as part of the response
        }), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True)
