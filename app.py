import os
import requests
import subprocess

from celery import Celery
from flask import Flask, Response, request, json


# Flask config
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yeahlemmegetuhhhhhhh'
app.config['DOCS_PATH'] = os.path.abspath(os.path.join(os.getcwd(), 'tmp'))
app.config['CELERY_BROKER_URL'] = 'redis://localhost:6379/0'
app.config['CELERY_BACKEND_URL'] = 'redis://localhost:6379/0'

# Celery config
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


# # # UTILITY METHODS # # #
def get_doc_name_from_url(url):
    return url.split('/').pop()


# # # CELERY TASKS # # #
@celery.task
def process_document(url):
    doc_name = get_doc_name_from_url(url)
    with open(os.path.join(app.config['DOCS_PATH'], doc_name), 'wb') as f:
        f.write(requests.get(url, stream=True).content)


# # # API ROUTES # # #
@app.route('/from-url', methods=['POST'])
def from_url():
    url = request.get_json().get('url')
    process_document.apply_async(args=[url])

    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
