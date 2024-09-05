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
GIT_SSH_COMMAND="ssh -i $ssh_key_path" git clone --branch KP-1007-taxbot-creation --filter=blob:none --sparse $repository_url

# Navigate to the cloned repository
cd kintsugi-tax-bot

# Enable sparse-checkout for the 'data' folder
git sparse-checkout init --cone
git sparse-checkout set taxbot/data

# Move the contents of the data folder to the parent directory
mv taxbot/datascrap/* .

# Remove the cloned folder
rm -rf taxbot

# Install any necessary dependencies (replace with actual command)
# For example, if you need to install Python dependencies, you can use:
# pip install -r requirements.txt

# Run the ingest.py script (replace with actual command)

# Clean up: remove the cloned repository
cd ..

mv "kintsugi-tax-bot" "data_vec"
chmod +x data_vec
rm -rf kintsugi-tax-bot
rm -rf data_vec/.gitignore
rm -rf data_vec/README.md

num_files=$(find data_vec -maxdepth 1 -type f | wc -l)

# Calculate the number of folders needed
num_folders=$(( (num_files + 9) / 10 ))

# Create folders if they don't exist
for i in $(seq 1 $num_folders); do
    mkdir -p "data_vec$i"
done

# Distribute data_vec files into folders
count=0
folder_index=1

for file in data_vec/*; do
    ((count++))

    if [ $((count % 10)) -eq 0 ]; then
        folder_name="data_vec$((count / 10))"
    else
        folder_namea="data_vec$folder_index"
    fi

    # Move the file to the corresponding folder
    sudo mv "$file" "$folder_name/"
done
rm -rf data_vec
chmod +x ingest.py
#chmod +x ingestscrap.py
#python ingest.py
#python ingestscrap.py
#rm -rf data_vec
#find . -type d -name 'data_vec*' -exec rm -rf {} +