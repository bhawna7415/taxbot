#!/bin/bash

# Check if the correct number of arguments are provided
# if [ "$#" -ne 2 ]; then
#     echo "Usage: $0 <repository_url> <folder_path>"
#     exit 1
# fi

# Assign input arguments to variables
repository_url='git@github.com:kintsugi-tax/kintsugi-tax-bot.git'
folder_path='datascrap'

# Set the path to the SSH key you want to use
ssh_key_path=~/.ssh/id_ed25519

# Clone the repository using the specified SSH key and branch, only fetching the 'data' folder
GIT_SSH_COMMAND="ssh -i $ssh_key_path" git clone --branch main --filter=blob:none --sparse $repository_url

# Navigate to the cloned repository
cd kintsugi-tax-bot

# Enable sparse-checkout for the 'data' folder
git sparse-checkout init --cone
git sparse-checkout set taxbot/datascrap

# Move the contents of the data folder to the parent directory
mv taxbot/datascrap/* .

# Remove the cloned folder
# rm -rf taxbot

# Install any necessary dependencies (replace with actual command)
# For example, if you need to install Python dependencies, you can use:
# pip install -r requirements.txt

# Run the ingest.py script (replace with actual command)

# Clean up: remove the cloned repository
cd ..

mv "kintsugi-tax-bot" "data_vec"
rm -rf kintsugi-tax-bot
rm -rf data_vec/.gitignore
rm -rf data_vec/README.md
chmod +x ingest.py
python ingest.py
rm -rf data_vec