#!/usr/bin/env python3

import logging
import os
import threading
import time
from datetime import date, datetime

import slack

from app import Config

###############################################################################

# Setting up we client
client = slack.WebClient(token=Config.SLACK_BOT_TOKEN)

###############################################################################


class Monitor:
    """
    Class defining monitor of various remote addresses.
    """

    def __init__(
        self, name, ip, port=None, slack_channel=None, email_addresses=[], auto_start=False
    ) -> None:
        """
        Object constructor.
        Runs at object creation.
        :param name: Name of the target being monitored
        :param ip: (str) IP address of the target being monitored
        :param ip: (int) Port number of the target beign monitored
        :param slack_channel: (str) Name of slack channel to post to, must begin with #
        :param email_addresses: (list of str) List of email addresses to send notifications to
        :param auto_start: (bool) If true monitor starts on object creation
        """
        self.started = False

        self._monitor_stop_flag = False
        self._monitor_tc_router_thread = None

        # Target Information
        self._name = name
        self._ip = ip
        self._port = port

        # Slack channel definition
        #   NOTE: Must add Slack App to targeted channel
        #         Must have "SLACK_BOT_TOKEN" in env. variable
        self._slack_channel = slack_channel

        # List of reporting email addresses
        self._email_addresses = email_addresses

        # Initialize status
        self.status = {}
        self.status = {
            "name": self._name,
            "ip_address": self._ip,
            "port": self._port,
            "status": None,
            "datetime": datetime.now(),
            "date": date.today(),
            "time": datetime.now().strftime("%H:%M:%S"),
            "time_unix": time.time(),
            "slack_channel": self._slack_channel,
            "email_addresses": self._email_addresses,
        }

        # Auto start monitor scan at object creation
        if auto_start:
            self.start()

    def __del__(self) -> None:
        """
        Object destructor
        Runs when object is deleted from memory.
        """
        if self.started:
            self.stop()

    ###########################################################################

    def start(self, scan_interval_sec=5) -> bool:
        """
        Start the monitor scanning.
        Starts a independent background thread
        :param scan_interval_sec: (int) Monitor scanning interval
        :return: If successfull, True, else False
        """
        # Start if it hasn't been started
        if not self.started:
            logging.info("Starting monitor scanning ...")
            logging.info("Creating background thread for monitor scanning ...")
            # Defining the independent thread
            self._monitor_tc_router_thread = threading.Thread(
                target=self._monitor_tc_router, args=[scan_interval_sec]
            )
            # Lower stopping flag
            self._monitor_stop_flag = False
            # Running the thread
            self._monitor_tc_router_thread.start()
            # Update monitor scan status
            self.started = True
            logging.info(
                "Successfully started monitor scanning (Thread ID: {}). Scanning every {} seconds ...".format(
                    self._monitor_tc_router_thread.ident, scan_interval_sec
                )
            )
            return True
        else:
            logging.warning(
                "Failed to start monitor scanning. It is already running (Thread ID: {})".format(
                    self._monitor_tc_router_thread.ident
                )
            )
            return False

    def stop(self) -> bool:
        """
        Stops the monitor scanning.
        Stops a independent background thread.
        :return: If successfull, True, else False
        """
        # Stop if it hasn been started
        if self.started:
            logging.info(
                "Stopping monitor scanning (Thread ID: {}) ...".format(
                    self._monitor_tc_router_thread.ident
                )
            )
            # Signal stopping of thread to thread
            self._monitor_stop_flag = True
            # Waiting until independent thread has stopped
            self._monitor_tc_router_thread.join()
            self._monitor_tc_router_thread = None
            # Update monitor scan status
            self.started = False
            logging.info("Successfully stopped monitor scanning")
            return True
        else:
            logging.warning("Failed to stop monitor. No monitoring in process")
            return False

    ###########################################################################

    def _monitor_tc_router(self, scan_interval_sec: int):
        """
        Independent thread that monitors TC router.
        Runs in a separate thread in the background.
        :param scan_interval_sec: (int) Monitor scanning interval
        """
        status_reachable = True

        # Give it a little
        time.sleep(0.50)
        while not self._monitor_stop_flag:

            # Pinging TC router
            status = self._ping()

            # Storing current results
            self.status = {
                "name": self._name,
                "ip_address": self._ip,
                "port": self._port,
                "status": status,
                "datetime": datetime.now(),
                "date": date.today(),
                "time": datetime.now().strftime("%H:%M:%S"),
                "time_unix": time.time(),
                "slack_channel": self._slack_channel,
                "email_addresses": self._email_addresses,
            }

            if status == 0:
                # Reachable and Online
                if not status_reachable:
                    # NOTE: Only report when previously not reachable
                    status_reachable = True
                    # Send slack message, only if slack channel was specified
                    if self._slack_channel:
                        self._send_slack_message(status=status)
                    # Send email messages, only if email addresses were specified
                    if self._email_addresses:
                        self._send_email_message(status=status)

            elif status == 1:
                # Local network issues, failed to send ping
                pass

            elif status == 2:
                # Not Reachable and Offline
                if status_reachable:
                    # NOTE: Only report when previously reachable
                    status_reachable = False
                    # Send slack message, only if slack channel was specified
                    if self._slack_channel:
                        self._send_slack_message(status=status)
                    # Send email messages, only if email addresses were specified
                    if self._email_addresses:
                        self._send_email_message(status=status)
            else:
                # Some un-anticipated network code
                pass

            # Pausing before next scan
            time.sleep(scan_interval_sec)

    ###########################################################################

    def _ping(self) -> int:
        """
        Pinging a IP address and returning if reachable or not
        :return: Map:
            0 = Successfully Reached (Return Code 0)
            1 = Local network issues, failed to send ping (Return Code 256)
            2 = Failed to reach remote target (Return Code 512)
            3 = Unanticipated Network Code Returned
        """
        # response = os.system("ping -c 1 " + ip_address + " > /dev/null 2>&1")
        response = os.system("nc -vz " + self._ip + " " + self._port + " > /dev/null 2>&1")
        if response == 0:
            # Successfully Reached
            logging.debug(
                '"{}:{}" is reachable and online ({})'.format(self._ip, self._port, response)
            )
            return 0
        elif response == 256:
            # Local network connection issues, failed to send ping (256)
            logging.warning(
                'Failed to send ping "{}:{}". Issues with local network connection ({})'.format(
                    self._ip, self._port, response
                )
            )
            return 1
        elif response == 512:
            # Unreachable (512)
            logging.warning(
                '"{}:{}" is not reachable and offline ({})'.format(self._ip, self._port, response)
            )
            return 2
        else:
            # Some un-anticipated network code
            logging.warning(
                '"{}:{}" has returned an unanticipated network code ({}). Netcat installed?'.format(
                    self._ip, self._port, response
                )
            )
            return 3

    ###########################################################################

    def _send_slack_message(self, status: bool) -> bool:
        """
        Sending a specified and formatted slack message
        :param status: (bool) The online/offline status of the monitored target
        :return: Send/Report of slack message was successfull, True, else False
        """
        # Configuring message title and status text
        if status:
            status_title = "{} BACK ONLINE".format(self._name)
            status_text = "Up and Running!"
        else:
            status_title = "{} NOT RESPONDING".format(self._name)
            status_text = "Unreachable / Offline"

        # Composing the message in parts
        # TODO: Add some templates from local file
        message_parts = [
            "```" "#################################################################",
            "      ATTENTION: {}       ".format(status_title),
            "#################################################################",
            "  • Datetime:          {}".format(datetime.now()),
            "  • Router IP:         {}".format(self._ip),
            "  • Router Port:       {}".format(self._port),
            "  • Router Status:     {}".format(status_text),
            "#################################################################",
            "```",
        ]
        # Combining all message parts
        message_text = "\n".join(message_parts)

        try:
            # Sending the message
            logging.warning(
                'Posting slack message to slack channel "{}" ...'.format(self._slack_channel)
            )
            response = client.chat_postMessage(channel=self._slack_channel, text=message_text)
            # Evaluating the response from slack server
            if response["ok"]:
                logging.debug(
                    'Successfully send slack message to channel "{}"'.format(self._slack_channel)
                )
                success = True
            else:
                logging.error(
                    'Failed to send slack message to channel "{}"'.format(self._slack_channel)
                )
                success = False

        except Exception as e:
            # Something went wrong while sending the message to slack servers
            logging.error(
                "Failed to send slack message. Possible local network connection issue. Exception: {}".format(
                    e
                )
            )
            success = False

        return success

    ###########################################################################

    def _send_email_message(self, status: bool) -> bool:
        """
        Sending a specified and formatted email messages.
        Emails will be send to specified list of individuals
        :param status: (bool) The online/offline status of the monitored target
        :return: Send/Report of email was successfull, True, else False
        """
        # TODO: Add email functionality
        #       Probably need to read some configuration file:
        #           SMTP Server (Set up on server level?)
        #           Sender Email:
        #           Password or Token (in env variable)
        # "Envelopes" module example:
        #    https://github.com/tomekwojcik/envelopes/blob/master/examples/example_flask.py
        #    Might need a config yml file to read from
        success = False
        return success

    ###########################################################################

    def get_monitor_started(self):
        """
        Getter for monitor scanning status
        """
        return self.started

    def get_tc_status(self):
        """
        Getter for tc status
        """
        return self.status
