import logging

from flask import Flask, url_for, request, render_template
from markupsafe import escape
from argparse import ArgumentParser

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
from views import *


def create_app(deploy_version):
    app.config['deploy_version'] = deploy_version
    print('Passed item: ', app.config['deploy_version'])
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-deploy_version')
    args = parser.parse_args()
    app = create_app(args.deploy_version)
    app.run(host="0.0.0.0")

