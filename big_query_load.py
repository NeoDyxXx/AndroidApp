from google.cloud import bigquery
import pandas as pd
import datetime
import json
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = os.path.join(dir_path, 'credients.json')
client = bigquery.Client()

def example():
    client = bigquery.Client()

    query = """
        SELECT corpus AS title, COUNT(word) AS unique_words
        FROM `bigquery-public-data.samples.shakespeare`
        GROUP BY title
        ORDER BY unique_words
        DESC LIMIT 10
    """
    results = client.query(query)

    for row in results:
        title = row['title']
        unique_words = row['unique_words']
    print(f'{title:<20} | {unique_words}')


def get_last_ind():
    client = bigquery.Client()

    query = """
        select max(id) as max_id from `discount_db.discount_item`
    """
    results = client.query(query)
    for row in results:
        return row['max_id']


def insert_rows(table_name, rows_to_insert):
    table_id = bigquery.Table.from_string(table_name)
    errors = client.insert_rows_json(table_id, rows_to_insert)  # Make an API request.

    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))


def transform_data(name_of_file: str, name_of_site: str):
    data = pd.read_json(name_of_file)
    max_ind = get_last_ind()

    if max_ind == None:
        max_ind = 0

    data.rename(columns={'sub_category': 'subcategory'}, inplace=True)
    data.drop(data[ data['discount'] == '' ].index, axis=0, inplace=True) 
    data['name_of_site'] = name_of_site
    data['id'] = data.reset_index().index + 1 + max_ind
    data['load_date'] = datetime.date.today().__str__()
    out = data.to_json(orient='records')
    data_json = json.loads(out)

    return data_json

list_item = transform_data('list_of_item.json', '5element.by')
for i in range(0, list_item.__len__(), int(list_item.__len__() / 10)):
    insert_rows('courseproject-369920.discount_db.discount_item', list_item[i:(i + int(list_item.__len__() / 10))])

