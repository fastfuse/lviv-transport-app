
import requests
import json
from flask import make_response, jsonify, url_for
from app import app
from pprint import pprint


class MonitoringInfo:
    """
    Class to handle calls to get monitoring information for route and stop.
    """

    BASE_URL = 'http://82.207.107.126:13541/SimpleRIDE/LAD/SM.WebApi/api'
    ROUTE_INFO = BASE_URL + '/RouteMonitoring/?code=LAD|'
    STOP_INFO = BASE_URL + '/stops/?code='

    def route_info(self, code):
        url = self.ROUTE_INFO + code
        response = requests.get(url)
        response = json.loads(response.json())
        # check status and add message
        return jsonify(monitoring_info=response,
                       vehicles_count=len(response))

    def stop_info(self, code):
        url = self.STOP_INFO + code
        response = requests.get(url)
        response = json.loads(response.json())
        # check status and add message
        return jsonify(monitoring_info=response,
                       vehicles_count=len(response))


def make_public(object, stop=False):
    """
    Function to add monitoring url to response.
    Also pops internal ID from route object.
    """

    if stop:
        if '_id' in object:
            object.pop('_id')

        object['monitoring_url'] = url_for('stop_monitoring',
                                           stop_code=object['code'],
                                           _external=True)
    else:
        object.pop('_id')
        object['monitoring_url'] = url_for('route_monitoring',
                                           route_code=object['id'],
                                           _external=True)
    return object


# ============================   Error handlers   ===========================

@app.errorhandler(404)
def not_found(error):
    """
    RESTful 404 error
    """

    return make_response(jsonify({'error': 'Not found', 'code': 404})), 404

