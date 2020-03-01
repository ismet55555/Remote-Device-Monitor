#!/usr/bin/env python3

# ---------------------------------------------------------
# Definition off all flask app endpoints/routes
# ---------------------------------------------------------

import logging
import os
import subprocess
import time

from flask import jsonify, render_template, request

from app import api, monitor

# Flask application base directory
base_app_dir = os.path.abspath(os.path.dirname(__file__))
base_dir = os.path.join(base_app_dir, "..")

###############################################################################

# Starting the independent monitor scanning
monitor_obj = monitor.Monitor(
    name="Florida Test Center Router", ip="71.41.66.6", port="443", slack_channel="#test-centre",
)
monitor_obj.start()

###############################################################################


@api.route("/")
@api.route("/index", methods=["GET"])
def index():
    """
    REST API endpoint for home page (index).
    :return: html of index processed by jinja2
    """

    # Rendering index.html
    return render_template("index.html")


###############################################################################


@api.route("/start_monitor_scan", methods=["GET", "POST"])
def start_monitor_scan():
    """
    REST API endpoint to start monitor scanning
    :return: json confirmation message
    """
    success = monitor_obj.start()
    if success:
        message = "Successfully started monitor scanning"
    else:
        message = "Failed to start monitor scanning"
    return jsonify({"success": success, "message": message})


@api.route("/stop_monitor_scan", methods=["GET", "POST"])
def stop_monitor_scan():
    """
    REST API endpoint to stop monitor scanning
    :return: json confirmation message
    """
    success = monitor_obj.stop()
    if success:
        message = "Successfully stopped monitor scanning"
    else:
        message = "Failed to stop monitor scanning"
    return jsonify({"success": success, "message": message})


@api.route("/monitor_status", methods=["GET"])
def monitor_status():
    """
    REST API endpoint to get the monitor scan status
    :return: json confirmation message
    """
    started = monitor_obj.get_monitor_started()
    status = {}
    status["running"] = started
    success = True
    return jsonify({"success": success, "status": status})


###############################################################################


@api.route("/tc_status", methods=["GET"])
def tc_status():
    """
    REST API endpoint to get the complete status of slideshow
    :return: json confirmation message
    """
    current_status = monitor_obj.get_status()

    success = True
    message = "Successfully retrieved current TC status"
    # Logging message
    logging.debug(message) if success else logging.error(message)
    return jsonify({"success": success, "message": message, "status": current_status})


###############################################################################


@api.route("/kill", methods=["GET", "POST"])
def kill():
    """
    REST API endpoint to command system to shutdown flask application.
    :return: json confirmation message
    """
    try:
        # Get all processes matching web application process. Reformat, strip, and split.
        process_port = "7777"
        processes = (
            subprocess.Popen(
                ["lsof -i :{}".format(process_port)], stdout=subprocess.PIPE, shell=True
            )
            .stdout.read()
            .decode("utf-8")
            .strip()
            .split("\n")
        )
        if processes[0]:
            # Loop through all running processes (omit heading row)
            pids = []
            for process in processes[1:]:
                # Split string by space
                process_parts = process.split(" ")
                # Strip all white space
                map(str.strip, process_parts)
                # Filter data_storage from blank data_storage
                process_columns = []
                for process_part in process_parts:
                    if process_part != "":
                        process_columns.append(process_part)
                # Store the PID for process (second column)
                pids.append(process_columns[1])
            logging.info(
                'Web application endpoint "/kill" was engaged. Terminating web application ...'
            )
            # Remove duplicates
            pids = list(set(pids))
            # Kill application (ommiting PID heading item)
            logging.critical(
                "Local processes with the following PID will be killed: {}".format(pids)
            )
            for pid in pids:
                os.system("kill -9 {}".format(pid))
        else:
            success = False
            message = "Failed to shut down web application. Local system process running on port {} was not found.".format(
                process_port
            )
    except Exception as e:
        success = False
        message = "Failed to shut down web application running on port {}. Exception: {}".format(
            process_port, e
        )
    # Logging message
    logging.info(message) if success else logging.error(message)
    return jsonify({"success": success, "message": message})


###############################################################################


@api.errorhandler(404)
def page_not_found(e):
    """
    REST API endpoint for any 404 page
    :return: html of 404 page processed by jinja2
    """
    return render_template("404.html"), 404


###############################################################################
