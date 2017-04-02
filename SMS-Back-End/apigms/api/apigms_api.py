from flask import Flask
from flask.ext.cors import CORS, cross_origin
from google.appengine.api import modules
import requests_toolbelt.adapters.appengine

# Use the App Engine Requests adapter. This makes sure that Requests uses URLFetch.
requests_toolbelt.adapters.appengine.monkeypatch()

app = Flask(__name__)

cors = CORS(app, resources={r"/*": {"origins": "*"}})

# Activating verbose mode
v = 1

module = modules.get_current_module_name()
instance = modules.get_current_instance_id()

from tdbms_segment.tdbms_api_segment import tdbms_segment_api
from scms_segment.scms_marks_api_segment import marks_api
from scms_segment.disciplinary_notes_api_segment import disciplinary_notes_api
from scms_segment.attendance_controls_api_segment import attendance_controls_api


@app.route('/helloworld', methods=['GET'])
def hello_world():
    """
     Test resource.

    :return:

     Example of use:
        curl -i -X GET localhost:8001/test
    """
    return 'Hello world!'

# Insert the rest of api sections.
app.register_blueprint(tdbms_segment_api)
app.register_blueprint(marks_api)
app.register_blueprint(disciplinary_notes_api)
app.register_blueprint(attendance_controls_api)

if __name__ == '__main__':
    app.run(debug=True)
