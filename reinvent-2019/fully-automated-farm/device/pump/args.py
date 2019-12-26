#!/usr/bin/python3
# -*- Coding: utf-8 -*-

import json
from argparse import ArgumentParser


def load_json_file(file_path):
    with open(file_path) as file:
        json_file = json.load(file)
    return json_file


class Args:
    def __init__(self):
        self._parser = ArgumentParser()


    def _set_argument(self, name, default, help):
        self._parser.add_argument(
            f"--{name}",
            action = 'store',
            default = default,
            dest = name,
            help = help,
        )


    def _set(self, arg):
        self._set_argument(
            name = arg.get('name'),
            default = arg.get('default'),
            help = arg.get('help'),
        )


    def _get_args_from(self, file_path):
        args_json = load_json_file(file_path)
        args = args_json.get('args')
        return args


    def set_args_of(self, file_path):
        args = self._get_args_from(file_path)
        for arg in args:
            self._set(arg)
        else:
            return self._parser.parse_args()
