#!/bin/bash


#############################################################################
# THIS IS ONLY FOR JARVIS LABS INSTANCES
##### How to Use:
#Make it executable: chmod +x start_jupyter_tmux.sh
#Run the script: ./start_jupyter_tmux.sh
##### The script will now:
#Install tmux.
#Ask you for a tmux session name.
#Create a detached tmux session with that name.
#Perform all the installations and start JupyterLab inside that tmux session.
#Finally, it will print the JupyterLab access URL.
#####To access your JupyterLab session:
#tmux attach-session -t <YOUR_TMUX_SESSION_NAME>
#You can then detach from the session again by pressing Ctrl+b then d
##############################################################################

# Script to install JupyterLab, configure PATH, and run JupyterLab on Ubuntu.
# It now installs tmux, *then* installs JupyterLab, creates a new tmux session,
# and ensures JupyterLab runs correctly inside it. It also fetches the public IP.

# Function to get user input for the secret token
get_secret_token() {
    read -p "Please enter your desired secret token for JupyterLab: " secret_token
    echo "$secret_token"
}

# Function to get user input for tmux session name
get_tmux_session_name() {
    read -p "Please enter a name for your tmux session (e.g., jupyter-session): " tmux_session_name
    echo "$tmux_session_name"
}

# Function to get the public IPv4 address
get_public_ipv4() {
    # Using checkip.amazonaws.com as it's generally reliable and returns just the IP.
    # We add 'curl' installation just in case it's not present.
    if ! command -v curl &> /dev/null; then
        echo "curl not found, installing..." >&2 # Print to stderr
        sudo apt update > /dev/null
        sudo apt install curl -y > /dev/null
        if [ $? -ne 0 ]; then
            echo "Error: Failed to install curl. Cannot fetch public IP." >&2
            return 1
        fi
    fi

    PUBLIC_IP=$(curl -s checkip.amazonaws.com)

    if [ $? -eq 0 ] && [[ "$PUBLIC_IP" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
        echo "$PUBLIC_IP"
    else
        echo "Error: Could not determine public IPv4 address. Check your internet connection or firewall rules." >&2
        return 1
    fi
}

# --- Main Script ---

echo "Starting JupyterLab setup on Ubuntu..."

# 1. Update apt and install tmux FIRST
echo "1. Updating apt and installing tmux..."
sudo apt update
sudo apt install tmux -y

if [ $? -eq 0 ]; then
    echo "tmux installed successfully."
else
    echo "Error installing tmux. Exiting."
    exit 1
fi

# 2. Install pip (python3-pip)
echo "2. Installing pip (python3-pip)..."
sudo apt install python3-pip -y

if [ $? -eq 0 ]; then
    echo "pip installed successfully."
else
    echo "Error installing pip. Exiting."
    exit 1
fi

# 3. Install jupyterlab
echo "3. Installing jupyterlab..."
# pip3 install jupyterlab --user is good practice to install in ~/.local/bin
pip3 install jupyterlab --user

if [ $? -eq 0 ]; then
    echo "JupyterLab installed successfully."
else
    echo "Error installing JupyterLab. Exiting."
    exit 1
fi

# 4. Export PATH to include ~/.local/bin for the CURRENT SHELL and its children (like tmux)
echo "4. Exporting ~/.local/bin to PATH for current session..."
export PATH=~/.local/bin:$PATH
echo "PATH updated for current session: $PATH"

# Verify jupyter command is found in the current shell
if ! command -v jupyter &> /dev/null; then
    echo "Error: 'jupyter' command not found in PATH after installation. Exiting."
    echo "Please ensure ~/.local/bin is correctly added to your PATH or check pip installation logs."
    exit 1
fi

# Get user inputs
TMUX_SESSION_NAME=$(get_tmux_session_name)
if [ -z "$TMUX_SESSION_NAME" ]; then
    echo "Tmux session name cannot be empty. Exiting."
    exit 1
fi

YOUR_SECRET_TOKEN=$(get_secret_token)
if [ -z "$YOUR_SECRET_TOKEN" ]; then
    echo "Secret token cannot be empty. Exiting."
    exit 1
fi

# 5. Create new tmux session and run JupyterLab inside it
echo "5. Creating new tmux session: $TMUX_SESSION_NAME"
echo "Running JupyterLab inside the tmux session..."
# The jupyter lab command will now be executed in the foreground of the tmux session
# We pass the environment variables directly, and the PATH is already set
tmux new-session -d -s "$TMUX_SESSION_NAME" "env HOME=/home/cloud jupyter lab --ip=0.0.0.0 --NotebookApp.token='$YOUR_SECRET_TOKEN' --allow-root --port 8888"

if [ $? -eq 0 ]; then
    echo "JupyterLab command sent to tmux session."
else
    echo "Error: Failed to send JupyterLab command to tmux. Exiting."
    exit 1
fi

# Get the VM's Public IPv4 address (this is for display purposes, after tmux is running)
echo "Attempting to fetch public IPv4 address..."
YOUR_VM_IPV4=$(get_public_ipv4)

if [ $? -ne 0 ]; then
    echo "Script cannot proceed without public IP. Exiting."
    # If the tmux session was created, you might want to kill it here if the script exits.
    # tmux kill-session -t "$TMUX_SESSION_NAME"
    exit 1
fi

echo -e "\nJupyterLab setup initiated within tmux session '$TMUX_SESSION_NAME'."
echo "To attach to the session and see JupyterLab logs, run:"
echo -e "  tmux attach-session -t $TMUX_SESSION_NAME"
echo -e "\nAccess JupyterLab at the following URL:"
echo -e "http://$YOUR_VM_IPV4:8888/lab?token=$YOUR_SECRET_TOKEN"
echo -e "\nRemember to open port 8888 in your VM's firewall/security group settings."
echo "JupyterLab will continue running even if you close your SSH connection, as it's in a tmux session."
