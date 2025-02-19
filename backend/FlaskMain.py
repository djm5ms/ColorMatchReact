from flask import Flask, render_template, request, url_for, send_from_directory, jsonify
import os
from werkzeug.utils import secure_filename
from werkzeug.middleware.shared_data import SharedDataMiddleware
from colorChecker import detect_colors
from SegCloth import segment_clothing
from PIL import Image

app = Flask(__name__, static_folder='../frontend/my-react-app/build', static_url_path='/')

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['UPLOAD_FOLDER_URL'] = '/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}
app.config['SECRET_KEY'] = 'your_secret_key'

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

# Serve the uploads folder as a static folder
app.add_url_rule('/uploads/<filename>', 'uploaded_file', build_only=True)
app.wsgi_app = SharedDataMiddleware(app.wsgi_app, {
    '/uploads': app.config['UPLOAD_FOLDER']
})

class clothingItem(object):
    def __init__(self, img, type, colors=[], percemnts=[], name=""):
        self.name = name
        self.img = img
        self.type = type
        self.colors = colors
        self.percemnts = percemnts
    def getImg(self):
        return self.img
    def getType(self):
        return self.type
    def getColors(self):
        return self.colors
    def getPercemnts(self):
        return self.percemnts
    def setName(self, name):
        self.name = name
    def getName(self):
        return self.name
    def setImg(self, img):
        self.img = img
    def setType(self, type):
        self.type = type
    def setColors(self, colors):
        self.colors = colors
    def setPercemnts(self, percemnts):
        self.percemnts = percemnts
        
clothes=[]
updatedPaths=[]

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/api/upload', methods=['POST'])
def upload_file():
    if 'imageUpload' not in request.files:
        return jsonify({'error': 'No file part'}), 400
    file = request.files['imageUpload']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        if '.jpg' in filename:
            filename = filename.replace('.jpg', '.png')
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)

        image = Image.open(file_path)
        result = segment_clothing(img=image, clothes=["Upper-clothes"])

        result_filename = "result_" + filename
        result_path = os.path.join(app.config['UPLOAD_FOLDER'], result_filename)
        result.save(result_path)

        adjusted_path = url_for('uploaded_file', filename=result_filename)

        colors, percents = detect_colors(result_path, num_colors=10)
        if adjusted_path not in updatedPaths:
            clothes.append(clothingItem(adjusted_path, "Upper-clothes", colors, percents))
        updatedPaths.append(adjusted_path)
        return jsonify({
            'message': 'File successfully uploaded',
            'image': url_for('uploaded_file', filename=filename),
            'image2': url_for('uploaded_file', filename=result_filename),
            'colors': colors,
            'percents': percents,
            'clothes': [item.__dict__ for item in clothes]
        })
    else:
        return jsonify({'error': 'File type not allowed'}), 400

@app.route('/api/clothes', methods=['GET'])
def get_clothes():
    return jsonify([item.__dict__ for item in clothes])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

if __name__ == '__main__':
    app.run(debug=True)
