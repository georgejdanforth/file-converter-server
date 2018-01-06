import os
import requests
import subprocess

from flask import (
    Flask,
    Response,
    request,
    json
)


app = Flask(__name__)
docs_path = os.path.join(os.getcwd(), 'tmp')


def get_doc_name_from_url(url):
    return url.split('/').pop()


@app.route('/from_url', methods=['POST'])
def from_url():
    url = request.get_json().get('url')
    doc_name = get_doc_name_from_url(url)
    with open(os.path.join(docs_path, doc_name), 'wb') as f:
        f.write(requests.get(url, stream=True).content)

    return Response(status=200)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
