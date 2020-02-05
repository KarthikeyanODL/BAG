from api import core
from flask import Flask, jsonify, send_file, render_template
from flask import request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# 1. init
@app.route('/index')
def student():
    return render_template('index.html')


# 2.Method to upload bundle
@app.route("/create/bundle", methods=['POST', 'PUT'])
def create_bundle():
    if request.method == 'POST':
        try:
            core.create_bundle(request)
        except Exception as exception:
            return jsonify(status=exception.args[0], code=500)
    else:
        return jsonify(status='Invalid request type', code=500)

    return jsonify(status='Bundle is created', code=201)


# 3.Method to upload bundle
@app.route("/upload/bundle", methods=['POST', 'PUT'])
def upload_models():
    print(request.method)
    if request.method == 'POST':

        try:
            core.save_file_to_disk(request)
        except Exception as exception:
            return jsonify(status=exception.args[0], code=500)
    else:
        return jsonify(status='Invalid request type', code=500)

    return jsonify(status='Bundle is saved', code=201)


# 4.Method to get the encoded file as zip
@app.route("/get/encoded_zip" , methods=['GET'])
def get_encoded_zipfile():
    if request.method == 'GET':
        try:
            zip_file = core.get_encoded_zip_file()
            return send_file(zip_file, attachment_filename='bundle.zip', as_attachment=True)

        except Exception as exception:
            return jsonify(status=exception.args[0], code=500)

    return jsonify(status='Invalid request type', code=500)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
