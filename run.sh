#! /bin/bash

SCRIPT_DIR=$(cd $(dirname $0); pwd)
cd $SCRIPT_DIR
cd ../

mcpo --port 8000 --host 0.0.0.0 --config ./mcp_apps/mcpo/config.json --api-key "top-secret"
