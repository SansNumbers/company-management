import json
import os

import pandas as pd
from flask import Flask
from flask import request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)


class Audit(Resource):
    def get(self):
        if not request.headers.get('Auth-sync') == os.environ.get('SECRET_SYNC_KEY'):
            return {
                'message': 'Sync key is invalid. Please enter correct sync key.'
            }, 403
        data = json.dumps(eval(request.data))
        df = pd.DataFrame(eval(data))
        df.to_excel('excelfile.xlsx', index=False)
        return {
            'message': 'Success.'
        }


api.add_resource(Audit, '/')
