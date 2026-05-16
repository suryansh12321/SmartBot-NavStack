# 🦾 SmartBot Navigation Stack (Version 1.0)

A lightweight, multi-layered Simultaneous Localization and Mapping (SLAM) engine built from absolute scratch. 

Designed for both high-speed simulation and physical hardware deployment, this stack combines a C-based mathematical core for low-latency pathfinding with a Python-based OS featuring Voice AI, Computer Vision, and dynamic memory mapping.

---

## 🌟 System Architecture

This repository utilizes a flattened, decoupled architecture. The logic is separated from the interface, and everything is bound together by an agnostic JSON database.

1. **The Core Engine (C):** - Uses a dynamic Wavefront (Breadth-First Search) algorithm.
   - Allocates memory dynamically at runtime to scale seamlessly from 3x3 up to 50x50 matrices without crashing.
   - Built for minimal overhead, ideal for Raspberry Pi / microcontroller integration.

2. **The Command Center OS (Python):**
   - A multi-threaded `tkinter` wrapper that runs the entire software suite from a single, futuristic dashboard.
   - **Computer Vision Mapping:** Import any 2D floorplan (`.png`, `.jpg`, `.webp` - including transparent backgrounds). The OS flattens the image, runs a thresholding algorithm, and converts real-world lines into mathematical arrays via an animated radar sweep.
   - **Live Telemetry & Voice Link:** Uses Google Speech AI to convert natural language into target coordinates, piping the execution logs live to the UI without freezing the main thread.

3. **The Database (`locations.json`):**
   - A "Blank Slate" semantic memory bank. The system assumes nothing. You paint arrays in the UI, name them (e.g., "couch", "wood", "charging_dock"), and the AI adapts its vocabulary to match your custom environment.

---

## 📂 File Roster

```text
SmartBot-NavStack/
│
├── ask_bot.py             # Voice AI to C-Engine Bridge
├── configurator.py        # Hardware C-Code Generator (ToF, Lidar, L298N)
├── locations.json         # Agnostic Core Database
├── map_manager.py         # CV-Enabled Visual Environment Painter
├── pathfinder.c           # High-Speed Dynamic SLAM Engine
├── pathfinder.exe         # Compiled Binary
├── setup.bat              # One-Click Environment Installer
├── smartbot_os.py         # ⚡ The Master GUI Hub
└── README.md              # Documentation
⚙️ Prerequisites
Python 3.x

GCC Compiler (MinGW for Windows) to compile the C-engine.

A working microphone (for the Telemetry Voice Link).

🚀 Installation & Quick Start
1. Clone the Repository:

DOS
git clone [https://github.com/YOUR-USERNAME/SmartBot-NavStack.git](https://github.com/YOUR-USERNAME/SmartBot-NavStack.git)
cd SmartBot-NavStack
2. Run the Auto-Installer (Windows):
Simply double-click setup.bat. This script will:

Install required Python libraries (SpeechRecognition, PyAudio, Pillow).

Compile pathfinder.c into pathfinder.exe.

Verify the integrity of locations.json.

3. Launch the OS:
Open your terminal and boot the Command Center:

DOS
python smartbot_os.py
🕹️ Operating the Stack
Map the Environment: Open the Dashboard tab and click Launch Environment Mapper. Set your matrix size, select blocks to draw custom obstacles, or click Import Floorplan (CV) to let the vision algorithm map an image for you. Hit Commit to save to memory.

Set a Target: While in the Mapper, use the "Place Target" tool to drop a waypoint and give it a name (e.g., "endpoint"). Commit the changes.

Execute via Voice: Open the Telemetry Link tab in the main OS. Click Initiate Voice Link, wait for the green light, and speak your target's name. Watch the C engine execute the pathfinding matrices in real-time.

🔧 Hardware Transition Roadmap
While currently operating as a high-fidelity desktop simulation, this codebase is designed to be pushed to a physical chassis (e.g., Raspberry Pi 4).
Launch the Hardware Bridge Configurator from the main dashboard to automatically generate the specific C-code required to interface this mathematical engine with physical I2C ToF (VL53L0X) sensors and PWM Motor Drivers.

How to Use It on the Robot(deploy_navcore.sh file)



When you actually copy this folder via USB or SSH into your robot's onboard computer (like a Raspberry Pi), it won't be able to run the script immediately for security reasons. You have to grant it execution rights.

Here is what you will type into the robot's terminal:

Make it executable:
chmod +x deploy_navcore.sh

Run the deployment:
./deploy_navcore.sh

The moment you hit enter, the terminal will light up with the giant NAVCORE ASCII logo, quietly configure the Linux environment, and compile the C engine perfectly for the robot's specific processor.