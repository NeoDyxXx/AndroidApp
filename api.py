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
    def get(self, start_ind, end_ind = -1):
        client = bigquery.Client()

        if end_ind == -1:
            end_ind = start_ind + 100

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

        return list_of_item[start_ind:end_ind:end_ind]


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


class BigQueryExecuterWithRegex(Resource):
    def get(self, start_ind, end_ind, regex):
        client = bigquery.Client()

        query = """
            select *  from `discount_db.discount_item`
            where load_date = '{1}' and ( lower(name) like lower('%{2}%') or lower(category) like lower('%{3}%') )
            limit {0}
        """.format(start_ind + 100, datetime.date.today().__str__(), regex, regex)
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

        return list_of_item[start_ind:end_ind]


api.add_resource(BigQueryExecuter, '/<int:start_ind>/<int:end_ind>')
api.add_resource(BigQueryExecuterWithRegex, '/<string:regex>/<int:start_ind>/<int:end_ind>')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)