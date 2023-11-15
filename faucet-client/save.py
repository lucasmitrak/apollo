#!/usr/bin/env python
import csv
from sensors import DS1307
import time
import datetime
import requests
from requests.exceptions import Timeout, ConnectionError
import os


class BadResultException(Exception):
    """ Thrown when requests get bad results
    """


class Save():

    def __init__(self, config):
        self.config = config
        # set if saving local config
        self.local = self.config.get('default', 'save_local') == 'true'
        # set if saving db config
        self.db = self.config.get('default', 'save_db') == 'true'
        # set if using external clock
        self.rtc = self.config.get('default', 'rtc') == 'true'

        if self.local:
            # open csv file for writing
            self.ofile = open('output.csv', "a")
            self.writer = csv.writer(self.ofile, delimiter=' ',
                                     quotechar='"', quoting=csv.QUOTE_ALL)

        if self.db:
            # set misc objects for db connection
            self.token = None
            self.token_timestamp = None

        if self.rtc:
            # external clock
            self.clock = DS1307()

    def save(self, sensor, value):
        """ save function which saves to local and db depending on config
        """
        if self.local:
            self.save_local(sensor.get_key(), value,
                            sensor.get_units(), sensor.get_sensor_name())
        if self.db:
            self.save_db(sensor.get_key(), value,
                         sensor.get_units(), sensor.get_sensor_name())
        time.sleep(0.5)

    def save_local(self, key, value, units, name):
        """ try to save to the local csv file
        """
        try:
            self.writer.writerow([
                key,
                value,
                units,
                name,
                self.config.get('default', 'host_id'),
                self.config.get('default', 'host_type'),
                self.ldt()
            ])
        except Exception as e:
            print e

    def save_db(self, key, value, units, name):
        """ try to use token and send a request
        """
        try:
            # if the token is dead
            if not self.token_timestamp or \
                    int(time.time()) - self.token_timestamp > 570:
                # get new token
                r = requests.post(
                    self.config.get('default', 'auth_endpoint'),
                    data=dict(
                        username=self.config.get('default', 'auth_user'),
                        password=self.config.get('default', 'auth_password')
                    ),
                    timeout=(10, 25),
                    verify=False
                )

                # if could not get new token, error out
                if r.status_code != 200:
                    print r.status_code, " ", r.text
                    raise BadResultException("Failed to get new token")

                # otherwise, set variable as token
                self.token = r.json().get("token")
                self.token_timestamp = int(time.time())

            # send request
            r = requests.post(
                self.config.get('default', 'data_endpoint'),
                data=dict(
                    key=key,
                    value=value,
                    units=units,
                    sensor=name,
                    token=self.token,
                    location_id=self.config.get('default', 'location'),
                    host_id=self.config.get('default', 'host_id'),
                    host_machine_type=self.config.get('default', 'host_type'),
                    host_software_version=self.config.get(
                        'default', 'version'),
                    timestamp=self.ldt()
                ),
                timeout=(10, 25),
                verify=False
            )

            # if request failed
            if r.status_code != 201:
                print r.status_code, " ", r.text
                raise BadResultException(
                    "Failed to save data {} for key {}".format(value, key)
                )
        except (Timeout, ConnectionError, BadResultException):
            os.system('/sbin/shutdown -r now')

    def ldt(self):
        """ return the proper clock depending on the config
        """
        if self.rtc:
            self.clock.getTime()
            ldt = self.clock.ldt
            return ldt
        else:
            local_time = time.localtime()
            ldt = datetime.datetime(*local_time[:6])
            return ldt

    def close(self):
        if self.local:
            # close file
            self.ofile.close()
