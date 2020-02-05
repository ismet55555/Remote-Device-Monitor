#!/usr/bin/env python3

# ---------------------------------------------------------
# Picture-Frame: Main flask application entry point
# Run with command: python3 main.py
# ---------------------------------------------------------

# Import all modules for app
import logging
from app import api  # Flask application
from gevent.pywsgi import WSGIServer


# Running flask server
if __name__ == '__main__':
    logging.info('Starting flask server application (Device-Monitor) ...  ')
    logging.info('Web application port:  7777')
    logging.info('Local Access:          http://localhost:7777/')

    # # NOTE: DEVELOPMENT: Using default flask server
    # logging.info('NOTE: Using default flask server (DEVELOPMENT ONLY)')
    # api.run(host='0.0.0.0', port=7777)

    # NOTE: PRODUCTION: Using gevent standalone Web Server Gateway Interface (WSGI) container
    logging.info('NOTE: Using gevent standalone Web Server Gateway Interface (WSGI) server for production deployment\n\n')
    http_server = WSGIServer(('', 7777), api, log=logging)
    http_server.serve_forever()

    # NOTE: Enviromental variables and settings are set in .flaskenv
