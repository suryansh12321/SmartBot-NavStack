import tkinter as tk
from tkinter import ttk, scrolledtext

def generate_code():
    # Get the user's selections from the dropdowns
    sensor_choice = sensor_var.get()
    motor_choice = motor_var.get()
    
    # Start building the C code string
    c_code = "/* ==========================================\n"
    c_code += "   SmartBot Auto-Generated Hardware Bridge\n"
    c_code += "   Copy and paste this into your C Engine\n"
    c_code += "========================================== */\n\n"
    
    c_code += "#include <stdio.h>\n"
    c_code += "#include <wiringPi.h> // Standard Raspberry Pi GPIO library\n\n"
    
    # Inject Sensor Code
    if sensor_choice == "3x ToF Sensors (VL53L0X - I2C)":
        c_code += "// --- SENSOR SETUP: I2C Time-of-Flight ---\n"
        c_code += "#include <wiringPiI2C.h>\n"
        c_code += "int fd_tof;\n"
        c_code += "void init_sensors() {\n"
        c_code += "    printf(\"Initializing I2C Bus for VL53L0X...\\n\");\n"
        c_code += "    fd_tof = wiringPiI2CSetup(0x29); // Default I2C address\n"
        c_code += "}\n\n"
    elif sensor_choice == "RPLidar A1 (UART)":
        c_code += "// --- SENSOR SETUP: UART Lidar ---\n"
        c_code += "#include <wiringSerial.h>\n"
        c_code += "int fd_lidar;\n"
        c_code += "void init_sensors() {\n"
        c_code += "    printf(\"Initializing Serial Port for RPLidar...\\n\");\n"
        c_code += "    fd_lidar = serialOpen(\"/dev/ttyUSB0\", 115200);\n"
        c_code += "}\n\n"

    # Inject Motor Code
    if motor_choice == "L298N Motor Driver (PWM)":
        c_code += "// --- MOTOR SETUP: L298N ---\n"
        c_code += "#define ENA 1  // PWM Pin for Speed\n"
        c_code += "#define IN1 2  // Direction Pin 1\n"
        c_code += "#define IN2 3  // Direction Pin 2\n"
        c_code += "void init_motors() {\n"
        c_code += "    printf(\"Setting up PWM pins for L298N...\\n\");\n"
        c_code += "    pinMode(ENA, PWM_OUTPUT);\n"
        c_code += "    pinMode(IN1, OUTPUT);\n"
        c_code += "    pinMode(IN2, OUTPUT);\n"
        c_code += "}\n\n"

    # Main bridging function
    c_code += "void init_hardware_bridge() {\n"
    c_code += "    wiringPiSetup(); // Boot up Raspberry Pi GPIO\n"
    c_code += "    init_sensors();\n"
    c_code += "    init_motors();\n"
    c_code += "    printf(\"Hardware Bridge Online. Ready for SLAM.\\n\");\n"
    c_code += "}\n"

    # Push the generated code to the text box in the UI
    output_box.delete('1.0', tk.END)
    output_box.insert(tk.END, c_code)

# --- GUI SETUP ---
root = tk.Tk()
root.title("SmartBot Hardware Configurator")
root.geometry("600x500")
root.configure(padx=20, pady=20)

# Title Label
title_label = tk.Label(root, text="Hardware Bridge Configurator", font=("Arial", 16, "bold"))
title_label.pack(pady=(0, 10))

# Sensor Dropdown
tk.Label(root, text="Select Vision Sensor:", font=("Arial", 10)).pack(anchor="w")
sensor_var = tk.StringVar()
sensor_dropdown = ttk.Combobox(root, textvariable=sensor_var, state="readonly", width=40)
sensor_dropdown['values'] = ("3x ToF Sensors (VL53L0X - I2C)", "RPLidar A1 (UART)")
sensor_dropdown.current(0)
sensor_dropdown.pack(pady=(0, 15), anchor="w")

# Motor Dropdown
tk.Label(root, text="Select Motor Driver:", font=("Arial", 10)).pack(anchor="w")
motor_var = tk.StringVar()
motor_dropdown = ttk.Combobox(root, textvariable=motor_var, state="readonly", width=40)
motor_dropdown['values'] = ("L298N Motor Driver (PWM)", "Direct ESCs (PWM)")
motor_dropdown.current(0)
motor_dropdown.pack(pady=(0, 20), anchor="w")

# Generate Button
generate_btn = tk.Button(root, text="Generate C Code", bg="#0078D7", fg="white", font=("Arial", 10, "bold"), command=generate_code)
generate_btn.pack(pady=(0, 10))

# Output Text Box
tk.Label(root, text="Generated C Code (Copy/Paste into pathfinder.c):", font=("Arial", 10)).pack(anchor="w")
output_box = scrolledtext.ScrolledText(root, width=70, height=15, font=("Consolas", 9), bg="#1E1E1E", fg="#D4D4D4")
output_box.pack()

# Run the application
root.mainloop()