
# -*- coding: utf-8 -*-

from app import app, db, utils
from flask import (request,
                   redirect,
                   render_template,
                   make_response,
                   url_for,
                   abort,
                   jsonify)
from flask.views import MethodView


info = utils.MonitoringInfo()


@app.route('/')
def index():
    return render_template('index.html')


class RoutesAPI(MethodView):
    """
    Transport API
    """
    def get(self, route_id):
        """
        Get route info. Returns all routes or certain route by ID.
        For certain route returns info about stops and path. 
        """
        if route_id:
            route = db['routes'].find_one({'id': route_id})
            if not route:
                abort(404)

            route = utils.make_public(route)

            route_path = db['route_paths'].find_one({'route_id': route['id']})
            route['path'] = route_path['path']

            route_stops = db['route_stops'].find_one({'route_id': route['id']})

            route['stops'] = []
            for stop in route_stops['stops']:
                route['stops'].append(utils.make_public(stop, stop=True))

            return jsonify(route)

        else:
            routes = db['routes'].find()
            response = list(map(utils.make_public, routes))
            return jsonify(count=len(response), routes=response)


class StopsAPI(MethodView):
    """
    Get stops info
    """
    def get(self):
        stops = db['stops'].find()
        response = []

        for stop in stops:
            response.append(utils.make_public(stop, stop=True))
        return jsonify(count=len(response), stops=response)


class RouteInfoAPI(MethodView):
    """
    Get Route monitoring info
    """
    def get(self, route_code):
        return info.route_info(route_code)


class StopInfoAPI(MethodView):
    """
    Get Stop monitoring info
    """
    def get(self, stop_code):
        return info.stop_info(stop_code)


# =====================   Register API endpoints   ==========================

routes_view = RoutesAPI.as_view('routes_api')
app.add_url_rule('/api/routes/',
                 defaults={'route_id': None},
                 view_func=routes_view,
                 methods=['GET'])
app.add_url_rule('/api/routes/<int:route_id>',
                 view_func=routes_view,
                 methods=['GET'])

stops_view = StopsAPI.as_view('stops_api')
app.add_url_rule('/api/stops/',
                 view_func=stops_view,
                 methods=['GET'])

route_monitoring_view = RouteInfoAPI.as_view('route_monitoring')
app.add_url_rule('/api/route_monitoring/<route_code>',
                 view_func=route_monitoring_view,
                 methods=['GET'])

stop_monitoring_view = StopInfoAPI.as_view('stop_monitoring')
app.add_url_rule('/api/stop_monitoring/<stop_code>',
                 view_func=stop_monitoring_view,
                 methods=['GET'])
