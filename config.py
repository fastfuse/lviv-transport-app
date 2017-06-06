
"""
http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api/RouteMonitoring/?code=C1|xxx
# view certain route

http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api/stops/?code=0010
# certain stop

http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api/stops/
# all stops

http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api/CompositeRoute/?code=C1|1446957
# list of stops on route


####################################################

C1|1446957 - ID format
C2|1446957 - ID format

####################################################

http://82.207.107.126:13541/SimpleRIDE/LAD/SM.WebApi/api - base URL LAD
http://82.207.107.126:13541/SimpleRIDE/LET/SM.WebApi/api - base URL LET

<BASE_URL>/CompositeRoute/ - List of routes
<BASE_URL>/RouteMonitoring/<Route_ID> - List of vehicles on route and their coordinates(also time data)
<BASE_URL>/CompositeRoute/<Route_ID> - list of stops on route
<BASE_URL>/path/<Route_ID> - path coordinates to draw path
"""

# BASEDIR = os.path.abspath(os.path.dirname(__file__))

# BASE_URL = 'http://82.207.107.126:13541/SimpleRide/LAD/SM.WebApi/api'
# ALL_STOPS = BASE_URL + '/stops'
# ALL_ROUTES = BASE_URL + '/CompositeRoute'
# STOP_INFO = ALL_STOPS + '/?code='  # xxxx
# STOPS_ON_ROUTE = BASE_URL + '/CompositeRoute/?code=C2|'
# PATH = BASE_URL + '/path/?code=C2|'
# ROUTE_MONITORING = BASE_URL + '/RouteMonitoring/?code=C2|'




import os


class Config(object):
    DEBUG = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY',
                                '\xa8vt\xbf1iZ\x0e\xdaO\xc0\xb9\xc4\xf0I\xb1)\xc3\x92\xcc\xd91%\n')

    DATABASE_URL = 'transport_app'

class DevelopmentConfig(Config):
    DEVELOPMENT = True
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


# export APP_SETTINGS="config.DevelopmentConfig"
# export DATABASE_URL="postgresql://witness:street@localhost/street_witness"
