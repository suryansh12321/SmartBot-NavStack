#!/bin/bash

# Clear the screen for a clean boot
clear

# --- NEON GREEN ASCII ART ---
echo -e "\e[32m"
echo "███╗   ██╗ █████╗ ██╗   ██╗ ██████╗ ██████╗ ██████╗ ███████╗"
echo "████╗  ██║██╔══██╗██║   ██║██╔════╝██╔═══██╗██╔══██╗██╔════╝"
echo "██╔██╗ ██║███████║██║   ██║██║     ██║   ██║██████╔╝█████╗  "
echo "██║╚██╗██║██╔══██║╚██╗ ██╔╝██║     ██║   ██║██╔══██╗██╔══╝  "
echo "██║ ╚████║██║  ██║ ╚████╔╝ ╚██████╗╚██████╔╝██║  ██║███████╗"
echo "╚═╝  ╚═══╝╚═╝  ╚═╝  ╚═══╝   ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝"
echo -e "\e[0m"

echo -e "\e[36m>>> INITIALIZING NAVCORE HARDWARE DEPLOYMENT SEQUENCE...\e[0m\n"

# Step 1: System Check & Dependencies
echo -e "\e[33m[1/4] Verifying Robot OS Dependencies...\e[0m"
sudo apt-get update -y > /dev/null 2>&1
sudo apt-get install -y gcc python3 python3-pip portaudio19-dev python3-pyaudio > /dev/null 2>&1
echo "      Done."

# Step 2: Python Libraries
echo -e "\e[33m[2/4] Injecting Python Neural/Vision Modules...\e[0m"
pip3 install SpeechRecognition Pillow --break-system-packages > /dev/null 2>&1
echo "      Done."

# Step 3: Compiling the C-Engine for Linux Hardware
echo -e "\e[33m[3/4] Compiling Native C-Engine for local architecture...\e[0m"
if [ -f "pathfinder.c" ]; then
    gcc pathfinder.c -o pathfinder_linux
    if [ $? -eq 0 ]; then
        echo "      C-Engine successfully compiled to 'pathfinder_linux'."
    else
        echo -e "\e[31m[ERROR] C compilation failed. Check GCC installation.\e[0m"
        exit 1
    fi
else
    echo -e "\e[31m[ERROR] pathfinder.c not found in deployment package.\e[0m"
    exit 1
fi

# Step 4: Database Verification
echo -e "\e[33m[4/4] Synchronizing Memory Bank...\e[0m"
if [ ! -f "locations.json" ]; then
    echo '{ "metadata": {"width": 10, "height": 10}, "targets": {}, "obstacles": {} }' > locations.json
    echo "      Generated fresh locations.json memory matrix."
else
    echo "      locations.json memory matrix found and linked."
fi

echo -e "\n\e[32m=====================================================\e[0m"
echo -e "\e[32m   [SYSTEM ONLINE] NavCore successfully integrated.  \e[0m"
echo -e "\e[32m=====================================================\e[0m\n"
echo -e "To launch the OS, run: \e[36mpython3 smartbot_os.py\e[0m\n"