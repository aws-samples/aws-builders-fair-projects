import boto3
import botocore

import os
import glob
import json
import requests

from datetime import datetime
from time import sleep
from time import gmtime, strftime

import sys, getopt

import argparse

import subprocess

from shutil import copyfile, rmtree

import logging

import configparser

__CONFIG_FILE_PATH__ = "cerebro.config"
__SSM_BASE_PATH__ = "/Cerebro"

class Configuration(object):
    def __init__(self,config_file=__CONFIG_FILE_PATH__):
        self.config_file = config_file
        self.config_parser = configparser.ConfigParser()
        self.config_parser.read(self.config_file)
        self.get_config_entries()
        self._ssm = boto3.client('ssm')

    def get_config_entries(self):
        self.config_entries = {}
        for section in self.config_parser.sections():
            #print("Section: %s" % section)

            for item in self.config_parser.items(section):
                #print("Item: ")
                #print(item)
                #print(item[0], item[1])
                param_name = item[0].upper()
                param_value = "%s/%s/%s" % (__SSM_BASE_PATH__, section, item[1])
                param_dict = {param_name:param_value}
                #print(param_dict)
                self.config_entries.update(param_dict)

        return True

    def getConfig(self, configEntry):
        if configEntry not in self.config_entries:
            return None
        ssm_param_name = self.config_entries[configEntry]
        #print(ssm_param_name)

        response = self._ssm.get_parameter(
            Name=ssm_param_name
            )
        #print(response)

        if ("Parameter" in response) and ("Name" in response["Parameter"]) and ("Value" in response["Parameter"]):
            ssm_param_value = response["Parameter"]["Value"]
            #print(ssm_param_value)
        else:
            return None

        return ssm_param_value

        '''
        config_entry = self.config_parser.get("Cerebro", configEntry)
        print(config_entry)
        if "ssm:" in config_entry:
            # then this means that we need to retrieve the actual value from the SSM Param store
            config_entry = "foobar"
        
        return config_entry
        '''

    @property
    def __QUEUE_URL__(self):
        return self.getConfig("__QUEUE_URL__")

    @property
    def __SQS_QUEUE_NAME__(self):
        return self.getConfig("__SQS_QUEUE_NAME__")

    @property
    def __SQS_BACKEND_QUEUE__(self):
        return self.getConfig("__SQS_BACKEND_QUEUE__")

    @property
    def __APIGW_X_API_KEY__(self):
        return self.getConfig("__APIGW_X_API_KEY__")

    @property
    def __APIGW_X_API_KEY_QR_CODE__(self):
        return self.getConfig("__APIGW_X_API_KEY_QR_CODE__")

    @property
    def __APIGW_API__(self):
        return self.getConfig("__APIGW_API__")

    @property
    def __APIGW_API_QR_CODE__(self):
        return self.getConfig("__APIGW_API_QR_CODE__")

    @property
    def __S3_BUCKET__(self):
        return self.getConfig("__S3_BUCKET__")

    @property
    def __CEREBRO_TEMP_DIR__(self):
        return self.getConfig("__CEREBRO_TEMP_DIR__")

    @property
    def __CEREBRO_MEDIA_DIR__(self):
        return self.getConfig("__CEREBRO_MEDIA_DIR__")

    @property
    def __CEREBRO_LOGS_DIR__(self):
        return self.getConfig("__CEREBRO_LOGS_DIR__")

    @property
    def __CEREBRO_PROFILES_DIR__(self):
        return self.getConfig("__CEREBRO_PROFILES_DIR__")

    @property
    def __CEREBRO_SYSTEM_DIR__(self):
        return self.getConfig("__CEREBRO_SYSTEM_DIR__")

    @property
    def __IMAGE_MAX_COUNT__(self):
        return int(self.getConfig("__IMAGE_MAX_COUNT__"))

    @property
    def __GREEN_LED__(self):
        return int(self.getConfig("__GREEN_LED__"))

    @property
    def __GREEN_BUTTON__(self):
        return int(self.getConfig("__GREEN_BUTTON__"))

    @property
    def __YELLOW_LED__(self):
        return int(self.getConfig("__YELLOW_LED__"))

    @property
    def __YELLOW_BUTTON__(self):
        return int(self.getConfig("__YELLOW_BUTTON__"))

    @property
    def __IOT_TOPIC__(self):
        return self.getConfig("__IOT_TOPIC__")

    @property
    def __IOT_HOST__(self):
        return self.getConfig("__IOT_HOST__")

    @property
    def __IOT_ROOT_CA_PATH__(self):
        return self.getConfig("__IOT_ROOT_CA_PATH__")

    @property
    def __IOT_CERTIFICATE_PATH__(self):
        return self.getConfig("__IOT_CERTIFICATE_PATH__")

    @property
    def __IOT_PRIVATE_KEY_PATH__(self):
        return self.getConfig("__IOT_PRIVATE_KEY_PATH__")

    @property
    def __IOT_CLIENT_ID_REQUESTER__(self):
        return self.getConfig("__IOT_CLIENT_ID_REQUESTER__")

    @property
    def __IOT_CLIENT_ID_PROCESSOR__(self):
        return self.getConfig("__IOT_CLIENT_ID_PROCESSOR__")

    @property
    def __CEREBRO_AUDIO_DIR__(self):
        return self.getConfig("__CEREBRO_AUDIO_DIR__")
        
    @property
    def __PUSHBUTTON_DELAY__(self):
        return int(self.getConfig("__PUSHBUTTON_DELAY__"))

    @property
    def __S3_BUCKET__(self):
        return self.getConfig("__S3_BUCKET__")

    @property
    def __ACCEPT_INPUT__(self):
        return int(self.getConfig("__ACCEPT_INPUT__"))

    @property
    def __CHOOSE_AGAIN__(self):
        return int(self.getConfig("__CHOOSE_AGAIN__"))

    @property
    def __CADENCE__(self):
        return int(self.getConfig("__CADENCE__"))

    @property
    def __DDB_TABLE__(self):
        return self.getConfig("__DDB_TABLE__")

    @property
    def __PRINTER_TYPE__(self):
        return self.getConfig("__PRINTER_TYPE__")

    @property
    def __FILTERED_IMAGE_NAME__(self):
        return self.getConfig("__FILTERED_IMAGE_NAME__")

    @property
    def __PIG_NOSE_FILTER__(self):
        return self.getConfig("__PIG_NOSE_FILTER__")

    @property
    def __FLOWER_CROWN_FILTER__(self):
        return self.getConfig("__FLOWER_CROWN_FILTER__")

    @property
    def __EYE_MASK_FILTER__(self):
        return self.getConfig("__EYE_MASK_FILTER__")

    @property
    def __DOG_NOSE_FILTER__(self):
        return self.getConfig("__DOG_NOSE_FILTER__")

    @property
    def __DOG_LEFT_EAR_FILTER__(self):
        return self.getConfig("__DOG_LEFT_EAR_FILTER__")

    @property
    def __DOG_RIGHT_EAR_FILTER__(self):
        return self.getConfig("__DOG_RIGHT_EAR_FILTER__")

    @property
    def __DOG_TONGUE_FILTER__(self):
        return self.getConfig("__DOG_TONGUE_FILTER__")

