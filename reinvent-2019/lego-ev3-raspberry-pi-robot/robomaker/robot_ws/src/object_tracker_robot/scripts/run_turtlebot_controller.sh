#!/usr/bin/env bash

set -ex

MODEL_PATH="$(dirname "$0")/../../share/object_tracker_robot/model.pb"
python3 -m robomaker.inference_worker ${MODEL_PATH}
