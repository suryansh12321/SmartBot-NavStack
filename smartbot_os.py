import tkinter as tk
from tkinter import ttk, scrolledtext
import subprocess
import threading
import os
import sys

class SmartBotOS:
    def __init__(self, root):
        self.root = root
        self.root.title("🦾 SMARTBOT OS - MISSION CONTROL")
        self.root.geometry("900x600")
        self.root.configure(bg="#050814") # Ultra deep space black

        # Styles
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Sidebar.TFrame', background='#0A0F1D')
        self.style.configure('Main.TFrame', background='#050814')

        # --- LAYOUT ---
        self.sidebar = ttk.Frame(root, style='Sidebar.TFrame', width=200)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        self.main_area = ttk.Frame(root, style='Main.TFrame')
        self.main_area.pack(side="right", expand=True, fill="both")

        # --- SIDEBAR NAVIGATION ---
        tk.Label(self.sidebar, text="SYSTEM\nNEXUS", font=("Consolas", 18, "bold"), bg="#0A0F1D", fg="#00F0FF").pack(pady=20)
        
        tk.Button(self.sidebar, text="1. DASHBOARD", bg="#112244", fg="#00F0FF", font=("Consolas", 11, "bold"), relief="flat", command=lambda: self.show_frame(self.frame_dash)).pack(fill="x", pady=5, padx=10)
        tk.Button(self.sidebar, text="2. TELEMETRY LINK", bg="#112244", fg="#39FF14", font=("Consolas", 11, "bold"), relief="flat", command=lambda: self.show_frame(self.frame_telemetry)).pack(fill="x", pady=5, padx=10)
        tk.Button(self.sidebar, text="3. DIAGNOSTICS", bg="#112244", fg="#FF0055", font=("Consolas", 11, "bold"), relief="flat", command=self.run_diagnostics).pack(fill="x", pady=5, padx=10)

        # --- FRAMES ---
        self.frame_dash = tk.Frame(self.main_area, bg="#050814")
        self.frame_telemetry = tk.Frame(self.main_area, bg="#050814")
        self.frame_diag = tk.Frame(self.main_area, bg="#050814")

        self.setup_dashboard()
        self.setup_telemetry()
        self.setup_diagnostics()

        # Show Dashboard by default
        self.show_frame(self.frame_dash)

    def show_frame(self, frame):
        for f in (self.frame_dash, self.frame_telemetry, self.frame_diag):
            f.pack_forget()
        frame.pack(expand=True, fill="both")

    # === TAB 1: DASHBOARD (LAUNCHERS) ===
    def setup_dashboard(self):
        tk.Label(self.frame_dash, text="COMMAND CENTER OVERVIEW", font=("Consolas", 16, "bold"), bg="#050814", fg="#FFFFFF").pack(pady=30)
        
        btn_frame = tk.Frame(self.frame_dash, bg="#050814")
        btn_frame.pack(pady=20)

        # Map Manager Launcher (Flat Architecture)
        tk.Button(btn_frame, text="🗺️ LAUNCH ENVIRONMENT MAPPER\n(Configure Matrix & CV Vision)", 
                  bg="#0A0F1D", fg="#00F0FF", font=("Consolas", 12), width=35, height=3, relief="groove", bd=2,
                  command=lambda: subprocess.Popen(["python", "map_manager.py"])).grid(row=0, column=0, padx=15, pady=15)

        # Configurator Launcher
        tk.Button(btn_frame, text="⚙️ LAUNCH HARDWARE BRIDGE\n(Generate C-Code for Sensors)", 
                  bg="#0A0F1D", fg="#E1AD01", font=("Consolas", 12), width=35, height=3, relief="groove", bd=2,
                  command=lambda: subprocess.Popen(["python", "configurator.py"])).grid(row=0, column=1, padx=15, pady=15)

    # === TAB 2: LIVE TELEMETRY (VOICE LINK) ===
    def setup_telemetry(self):
        tk.Label(self.frame_telemetry, text="LIVE NEURAL TELEMETRY", font=("Consolas", 16, "bold"), bg="#050814", fg="#39FF14").pack(pady=(20, 5))
        
        self.term_box = scrolledtext.ScrolledText(self.frame_telemetry, bg="#0A0F1D", fg="#39FF14", font=("Consolas", 10), height=22)
        self.term_box.pack(fill="both", expand=True, padx=20, pady=10)
        self.term_box.insert(tk.END, ">>> SYSTEM STANDBY. Awaiting neural voice link initialization...\n")
        self.term_box.config(state=tk.DISABLED)

        tk.Button(self.frame_telemetry, text="🎙️ INITIATE VOICE LINK", bg="#39FF14", fg="#050814", font=("Consolas", 12, "bold"), width=30,
                  command=self.start_voice_thread).pack(pady=15)

    def start_voice_thread(self):
        self.term_box.config(state=tk.NORMAL)
        self.term_box.insert(tk.END, "\n>>> [SYSTEM] Spawning subprocess for ask_bot.py...\n")
        self.term_box.see(tk.END)
        self.term_box.config(state=tk.DISABLED)
        # Run in a separate thread to prevent UI freezing
        threading.Thread(target=self.run_voice_bot, daemon=True).start()

    def run_voice_bot(self):
        try:
            # We use Popen to capture the console output in real-time, enforcing UTF-8 for emojis
            process = subprocess.Popen(["python", "ask_bot.py"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, bufsize=1, encoding='utf-8')
            
            for line in process.stdout:
                self.root.after(0, self.append_telemetry, line)
                
            process.wait()
            self.root.after(0, self.append_telemetry, ">>> [SYSTEM] Voice link terminated.\n")
        except Exception as e:
            self.root.after(0, self.append_telemetry, f">>> [ERROR] {e}\n")

    def append_telemetry(self, text):
        self.term_box.config(state=tk.NORMAL)
        self.term_box.insert(tk.END, text)
        self.term_box.see(tk.END)
        self.term_box.config(state=tk.DISABLED)

    # === TAB 3: DIAGNOSTICS ===
    def setup_diagnostics(self):
        tk.Label(self.frame_diag, text="SYSTEM HEALTH DIAGNOSTICS", font=("Consolas", 16, "bold"), bg="#050814", fg="#FFFFFF").pack(pady=20)
        self.diag_text = tk.Label(self.frame_diag, text="", font=("Consolas", 12), bg="#050814", fg="#00F0FF", justify="left")
        self.diag_text.pack(pady=20)

    def run_diagnostics(self):
        self.show_frame(self.frame_diag)
        status = ""
        
        # Check Database
        if os.path.exists("locations.json"): status += "✅ locations.json ... ONLINE\n"
        else: status += "❌ locations.json ... MISSING\n"
            
        # Check C Engine
        if os.path.exists("pathfinder.exe"): status += "✅ pathfinder.exe ... COMPILED\n"
        else: status += "❌ pathfinder.exe ... MISSING (Run setup.bat)\n"
            
        # Check Python Modules
        try:
            import speech_recognition
            status += "✅ SpeechRecognition ... INSTALLED\n"
        except ImportError:
            status += "❌ SpeechRecognition ... MISSING\n"
            
        try:
            import PIL
            status += "✅ Pillow (CV Engine) ... INSTALLED\n"
        except ImportError:
            status += "❌ Pillow (CV Engine) ... MISSING\n"

        self.diag_text.config(text=status)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartBotOS(root)
    root.mainloop()