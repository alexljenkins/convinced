#!/bin/bash
# chmod +x start.sh
# ./start.sh
read -sp "Enter a API_KEY (anything you like): " API_KEY
echo
read -sp "Enter the AI_KEY (from OpenAI API): " AI_KEY
echo

export API_KEY
export AI_KEY

docker-compose up
