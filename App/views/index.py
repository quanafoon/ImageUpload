from flask import Blueprint, redirect, render_template, request, send_from_directory, jsonify, flash
from App.controllers import create_user, initialize, validate_upload, encode_image
from werkzeug.utils import secure_filename
from flask_jwt_extended import jwt_required
import os
import cv2
import base64

index_views = Blueprint('index_views', __name__, template_folder='../templates')

@index_views.route('/', methods=['GET'])
def index_page():
    return render_template('login.html')

@index_views.route('/init', methods=['GET'])
def init():
    initialize()
    return jsonify(message='db initialized!')

@index_views.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status':'healthy'})

@index_views.route('/uploadPage', methods=['GET'])
def upload_page():
    return render_template('upload.html')

@index_views.route('/upload', methods=['POST'])
def upload_image(): 
    if 'file' not in request.files:
        flash("No file")
        return render_template("index.html")
    file = request.files['file']
    validated = validate_upload(file.filename)
    if validated:
        filename = secure_filename(file.filename)
        file.save(os.path.join("App/uploads", filename))
        flash("file found")
        filepath = "App/uploads/" + filename
        upload = encode_image(filepath)
        return render_template("upload.html")
    flash("Invalid file")
    return render_template("upload.html")

@index_views.route("/loginPage" , methods=['GET'])
def loginPage():
    return render_template("login.html")

@index_views.route("/aboutUsPage", methods=['GET'])
def aboutUs():
    return render_template("aboutUs.html")

@index_views.route("/api/image", methods=['POST'])
def get_image():
    print("Here")
    file = request.files.get('file')  
    if not file:
        return jsonify({"error": "No file selected"})
    if validate_upload(file.filename):
        img = file.read()
        encode_image = base64.b64encode(img).decode("UTF-8")
        return jsonify({"image" : encode_image})
    return jsonify({"error": "Invalid image selected"})
