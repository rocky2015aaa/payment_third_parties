#!/bin/bash

echo "starting uvicorn server...."
export ENV_FILE_PATH="./.env.dev"
uvicorn app.main:app --reload