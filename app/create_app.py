import logging
import os

from flask import Flask, url_for, request, render_template
from markupsafe import escape
from argparse import ArgumentParser
import werkzeug._internal

def demi_logger(type, message,*args,**kwargs):
    pass

werkzeug._internal._log = demi_logger

logging.basicConfig(filename='record.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')

app = Flask(__name__)
from views import *


def create_app(deploy_version=None):
    timestamps = [path.split("_")[1].split(".")[0] for path in os.listdir("./../data") if path.startswith("Linear")]
    candidates = []
    for timestamp in timestamps:
        if os.path.exists("../data/Linear-regression_{version}.node/R2.txt".format(version=timestamp)):
            with open("../data/Linear-regression_{version}.node/R2.txt".format(version=timestamp), "r") as r2_file:
                candidates.append((float(r2_file.readline()), timestamp))
    max_candidate = candidates[0]
    for candidate in candidates:
        if max_candidate[0] <= candidate[0]:
            max_candidate = candidate
    app.config['deploy_version'] = deploy_version or max_candidate[1]
    print('Passed item: ', app.config['deploy_version'])
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-deploy_version')
    args = parser.parse_args()
    app = create_app(args.deploy_version)
    app.run(host="0.0.0.0")

