#!/bin/bash
# chmod +x start.sh
# ./start.sh
read -sp "Enter the API_KEY: " API_KEY
echo
read -sp "Enter the AI_KEY: " AI_KEY
echo

export API_KEY
export AI_KEY

docker-compose up
