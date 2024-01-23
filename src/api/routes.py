"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint, Response
from api.models import FileUpload, db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200


@api.route("/files/<str: fname>", methods=["GET"])
def get_file(fname):
    f = FileUpload.query.filter_by(filename=fname).first()
    if not f:
        return "", 404
    return Response(
        f.data,
        mimetype=f.mimetype,
    )


@api.route("/files", methods=["POST"])
def get_file():
    formdata = request.form
    f = FileUpload(
        filename=formdata.get("files", [])[0]["name"],
        mimetype="image/png",
        data=formdata.get("files", [])[0]
    )
    return Response(
        f.data,
        mimetype=f.mimetype,
    )
