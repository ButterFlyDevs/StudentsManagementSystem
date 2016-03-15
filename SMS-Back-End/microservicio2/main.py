# -*- coding: utf-8 -*-
from flask import *

from gcloud import storage

app = Flask(__name__)


def upload_image_file(file):
    """
    Upload the user-uploaded file to Google Cloud Storage and retrieve its
    publicly-accessible URL.
    """
    if not file:
        return None

    public_url = storage.upload_file(
        file.read(),
        file.filename,
        file.content_type
    )

    current_app.logger.info(
        "Uploaded file %s as %s.", file.filename, public_url)

    return public_url




@app.route('/',methods=['GET'])
def saludo():
    f = open('profile.jpg', 'r')
    #jpgdata = f.read()
    return upload_image_file(f)
    #return 'Hola, soy el microservicio2\n'


if __name__ == '__main__':
    app.run(debug=True)
