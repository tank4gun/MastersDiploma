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
    with open("../best_model_version.txt", "r") as model_version_file:
        best_model_version = model_version_file.readline()


    timestamps = [path.split("_")[1].split(".")[0] for path in os.listdir("./../data") if path.startswith("Linear")]
    candidates = []
    for timestamp in timestamps:
        if os.path.exists("../data/Linear-regression_{version}.node/R2.txt".format(version=timestamp)):
            with open("../data/Linear-regression_{version}.node/R2.txt".format(version=timestamp), "r") as r2_file:
                candidates.append((float(r2_file.readline()), timestamp))
    max_candidate = candidates[0]
    for candidate in candidates:
        if max_candidate[0] <= candidate[0] and int(max_candidate[1]) < int(candidate[1]):
            max_candidate = candidate
    with open("check.txt", "w") as check_file:
        check_file.write("Deploy_version {}".format(deploy_version))
        check_file.write("Candidates {}".format(candidates))
        check_file.write("Max_candidate {}".format(max_candidate))
    app.config['deploy_version'] = deploy_version or best_model_version  # max_candidate[1]
    print('Passed item: ', app.config['deploy_version'])
    return app


if __name__ == '__main__':
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('-deploy_version')
    args = parser.parse_args()
    app = create_app(args.deploy_version)
    app.run(host="0.0.0.0")

