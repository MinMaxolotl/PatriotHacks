from flask import Flask, request, jsonify
import os

app = Flask(__name__)

# Path to save uploaded images
UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/upload-image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"error": "No image part in the request"}), 400

    image = request.files['image']

    if image.filename == '':
        return jsonify({"error": "No selected image"}), 400

    image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
    image.save(image_path)

    return jsonify({"message": "Image uploaded successfully", "image_path": image_path}), 200

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, request, jsonify
# import os
# import subprocess  # To run the external Python file

# app = Flask(__name__)

# # Path to save uploaded images
# UPLOAD_FOLDER = './uploads'
# app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# # Ensure the upload directory exists
# if not os.path.exists(UPLOAD_FOLDER):
#     os.makedirs(UPLOAD_FOLDER)

# @app.route('/upload-image', methods=['POST'])
# def upload_image():
#     # Check if an image file is in the request
#     if 'image' not in request.files:
#         return jsonify({"error": "No image part in the request"}), 400

#     image = request.files['image']

#     # Check if the file has a filename
#     if image.filename == '':
#         return jsonify({"error": "No selected image"}), 400

#     # Save the image to the server
#     image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
#     image.save(image_path)

#     try:
#         # Run the external Python file (process_image.py) with the image path as an argument
#         result = subprocess.run(
#             ['python', 'process_image.py', image_path],  # Command to run
#             capture_output=True,  # Capture stdout and stderr
#             text=True  # Get the output as a string (not bytes)
#         )

#         # Check for errors in the subprocess execution
#         if result.returncode != 0:
#             return jsonify({"error": "Failed to process image", "details": result.stderr}), 500

#         # Return the result of the external script
#         return jsonify({"message": "Image uploaded and processed successfully", "output": result.stdout}), 200

#     except Exception as e:
#         return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# if __name__ == '__main__':
#     app.run(debug=True)