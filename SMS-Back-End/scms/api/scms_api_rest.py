# -*- coding: utf-8 -*-

from flask import Flask
import json

# Import the segments of api
from marks_api_segment import marks_api
from attendance_controls_api_segment import attendance_controls_api
from disciplinary_notes_api_segment import disciplinary_notes_api

# Mainly definition of flask api, linked from scms.yaml file
app = Flask(__name__)

#####################################################
#  Definition of Data Base micro Service REST API   #
#####################################################

@app.route('/test',methods=['GET'])
def test():
    """
    Test resource.

    Example of use:
        curl -i -X GET localhost:8003/test
    """
    return json.dumps({'scms_api_rest_test_status': 'ok'})

app.register_blueprint(marks_api)
app.register_blueprint(attendance_controls_api)
app.register_blueprint(disciplinary_notes_api)

if __name__ == '__main__':
    app.run(debug=True)

