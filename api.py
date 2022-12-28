from flask import Flask
from flask_restful import Resource, Api
from google.cloud import bigquery
import pandas as pd
import datetime
import os

app = Flask(__name__)
api = Api(app)
dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(dir_path, 'credients.json')

class BigQueryExecuter(Resource):
    def get(self, start_ind):
        client = bigquery.Client()

        query = """
            select *  from `discount_db.discount_item`
            where load_date = '{1}'
            limit {0}
        """.format(start_ind + 100, datetime.date.today().__str__())
        results = client.query(query)
        
        list_of_item = [{
            'id': row['id'],
            'name_of_site': row['name_of_site'],
            'category': row['category'],
            'subcategory': row['subcategory'],
            'name': row['name'],
            'details': row['details'],
            'price': row['price'],
            'discount': row['discount'],
            'url': row['url'],
            'load_date': row['load_date']
        } for row in results ]

        return list_of_item[start_ind:]


class BigQueryExecuterWithParamOfResource(Resource):
    def get(self, start_ind, name_of_site):
        client = bigquery.Client()

        query = """
            select *  from `discount_db.discount_item`
            where load_date = '{1}' and name_of_site = '{2}'
            limit {0}
        """.format(start_ind + 100, datetime.date.today().__str__(), name_of_site)
        results = client.query(query)
        
        list_of_item = [{
            'id': row['id'],
            'name_of_site': row['name_of_site'],
            'category': row['category'],
            'subcategory': row['subcategory'],
            'name': row['name'],
            'details': row['details'],
            'price': row['price'],
            'discount': row['discount'],
            'url': row['url'],
            'load_date': row['load_date']
        } for row in results ]

        return list_of_item[start_ind:]


api.add_resource(BigQueryExecuter, '/<int:start_ind>')
api.add_resource(BigQueryExecuterWithParamOfResource, '/<string:name_of_site>/<int:start_ind>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)