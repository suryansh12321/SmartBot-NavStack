import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, filedialog
import json
import os

# Try to import Pillow for Computer Vision, handle gracefully if missing
try:
    from PIL import Image
    HAS_PIL = True
except ImportError:
    HAS_PIL = False

DB_FILE = 'locations.json'

class AgnosticMapManager:
    def __init__(self, root):
        self.root = root
        self.root.title("🦾 SMARTBOT DYNAMIC MAPPER (CV ENABLED)")
        self.root.geometry("1050x800") 
        self.root.configure(bg="#0A0F1D")

        self.load_db()
        self.active_mode = "select" 
        self.current_selection = [] 
        self.buttons = {}

        # --- HEADER ---
        header = tk.Label(root, text="⚡ NEURAL MAP & VISION CONFIGURATOR ⚡", font=("Consolas", 18, "bold"), bg="#0A0F1D", fg="#00F0FF")
        header.pack(pady=15)

        # --- MAIN LAYOUT ---
        main_frame = tk.Frame(root, bg="#0A0F1D")
        main_frame.pack(expand=True, fill="both", padx=20)

        left_panel = tk.Frame(main_frame, bg="#0A0F1D")
        left_panel.pack(side="left", expand=True, fill="both")

        right_panel = tk.Frame(main_frame, bg="#112244", bd=2, relief="groove", width=250)
        right_panel.pack(side="right", fill="y", padx=(20, 0))

        # --- LEFT PANEL: DIMENSIONS, TOOLS & GRID ---
        
        # 1. Dimension Controls
        dim_frame = tk.Frame(left_panel, bg="#112244", bd=2, relief="groove")
        dim_frame.pack(fill="x", pady=(0, 10))
        
        tk.Label(dim_frame, text="MATRIX CONFIG:", font=("Consolas", 10, "bold"), bg="#112244", fg="#00F0FF").grid(row=0, column=0, padx=10, pady=8)
        self.width_var = tk.StringVar(value=str(self.width))
        self.height_var = tk.StringVar(value=str(self.height))
        tk.Entry(dim_frame, textvariable=self.width_var, width=4, bg="#0A0F1D", fg="#39FF14", font=("Consolas", 10)).grid(row=0, column=1)
        tk.Label(dim_frame, text="x", bg="#112244", fg="#00F0FF").grid(row=0, column=2, padx=5)
        tk.Entry(dim_frame, textvariable=self.height_var, width=4, bg="#0A0F1D", fg="#39FF14", font=("Consolas", 10)).grid(row=0, column=3)
        tk.Button(dim_frame, text="REGENERATE GRID", command=self.resize_grid, bg="#0A0F1D", fg="#00F0FF", font=("Consolas", 9, "bold")).grid(row=0, column=4, padx=15)
        
        # CV IMPORT BUTTON
        tk.Button(dim_frame, text="👁️ IMPORT FLOORPLAN (CV)", command=self.import_floorplan, bg="#39FF14", fg="black", font=("Consolas", 9, "bold")).grid(row=0, column=5, padx=20)

        # 2. Tools
        tools = tk.Frame(left_panel, bg="#0A0F1D")
        tools.pack(pady=5)
        
        tk.Button(tools, text="1. SELECT CELLS", bg="#E1AD01", fg="black", font=("Consolas", 9, "bold"), command=lambda: self.set_mode("select"), width=16).grid(row=0, column=0, padx=5)
        tk.Button(tools, text="2. NAME OBSTACLE", bg="#FF0055", fg="white", font=("Consolas", 9, "bold"), command=self.save_obstacle, width=18).grid(row=0, column=1, padx=5)
        tk.Button(tools, text="CLEAR SELECT", bg="#112244", fg="white", font=("Consolas", 9), command=self.clear_selection, width=14).grid(row=0, column=2, padx=5)
        tk.Button(tools, text="📍 PLACE TARGET", bg="#00F0FF", fg="black", font=("Consolas", 9, "bold"), command=lambda: self.set_mode("target"), width=18).grid(row=0, column=3, padx=5)

        # 3. Grid
        self.grid_container = tk.Frame(left_panel, bg="#0A0F1D")
        self.grid_container.pack(expand=True, fill="both", pady=10)
        self.build_grid_ui()

        # --- RIGHT PANEL: LIVE DATABASE SIDEBAR ---
        tk.Label(right_panel, text="LIVE JSON MEMORY", font=("Consolas", 12, "bold"), bg="#112244", fg="#39FF14").pack(pady=10)
        
        tk.Label(right_panel, text="📍 TARGETS:", font=("Consolas", 10, "underline"), bg="#112244", fg="#00F0FF").pack(anchor="w", padx=10, pady=(10,0))
        self.targets_list = tk.Listbox(right_panel, bg="#0A0F1D", fg="#00F0FF", font=("Consolas", 9), height=8, bd=0, highlightthickness=0)
        self.targets_list.pack(fill="x", padx=10, pady=5)

        tk.Label(right_panel, text="🛑 OBSTACLES:", font=("Consolas", 10, "underline"), bg="#112244", fg="#FF0055").pack(anchor="w", padx=10, pady=(10,0))
        self.obstacles_list = tk.Listbox(right_panel, bg="#0A0F1D", fg="#FF0055", font=("Consolas", 9), height=12, bd=0, highlightthickness=0)
        self.obstacles_list.pack(fill="x", padx=10, pady=5)

        self.update_sidebar()

        # --- FOOTER ---
        footer = tk.Frame(root, bg="#0A0F1D")
        footer.pack(fill="x", side="bottom", pady=15)
        tk.Button(footer, text="💾 COMMIT TO LOCATIONS.JSON", bg="#39FF14", fg="black", font=("Consolas", 12, "bold"), command=self.save_and_sync, width=40).pack()

    def load_db(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r') as f:
                    self.db = json.load(f)
            except:
                self.db = {"metadata": {"width": 10, "height": 10}, "targets": {}, "obstacles": {}}
        else:
            self.db = {"metadata": {"width": 10, "height": 10}, "targets": {}, "obstacles": {}}
        
        self.width = self.db["metadata"].get("width", 10)
        self.height = self.db["metadata"].get("height", 10)

    # === NEW ANIMATION: HOVER STATES ===
    def on_enter(self, e, btn, r, c):
        if btn.cget('bg') == "#0D1527":
            btn.config(bg="#1A2E5A") 

    def on_leave(self, e, btn, r, c):
        if btn.cget('bg') == "#1A2E5A":
            btn.config(bg="#0D1527")

    # === NEW ANIMATION: RADAR SWEEP ===
    def animated_reveal(self, walls, index=0):
        chunk_size = 3
        end_index = min(index + chunk_size, len(walls))
        
        for i in range(index, end_index):
            y, x = walls[i]
            if (y, x) in self.buttons:
                self.buttons[(y, x)].config(bg="#FFFFFF")
                self.root.after(50, lambda r=y, c=x: self.buttons[(r, c)].config(bg="#FF0055", text="██" if self.width <= 20 else ""))

        if end_index < len(walls):
            self.root.after(10, self.animated_reveal, walls, end_index)
        else:
            self.update_sidebar()
            messagebox.showinfo("CV Scan Complete", f"Vision algorithm extracted {len(walls)} blocks.")

    # === UPGRADED COMPUTER VISION MODULE ===
    def import_floorplan(self):
        if not HAS_PIL:
            messagebox.showerror("Dependencies Missing", "Pillow library not found.\nRun: pip install Pillow")
            return

        filepath = filedialog.askopenfilename(title="Select 2D Map/Floorplan", filetypes=[("All Files", "*.*"), ("Image Files", "*.png *.jpg *.jpeg *.bmp *.webp")])
        if not filepath: return

        try:
            # 1. Open the raw image file
            img = Image.open(filepath)

            # 2. THE FIX: Handle Transparent PNGs and Alpha Channels
            if img.mode in ('RGBA', 'LA') or (img.mode == 'P' and 'transparency' in img.info):
                alpha = img.convert('RGBA').split()[-1] 
                bg = Image.new("RGB", img.size, (255, 255, 255)) 
                bg.paste(img, mask=alpha) 
                img = bg 

            # 3. Convert to grayscale and compress to matrix size
            img = img.convert('L')
            img = img.resize((self.width, self.height))

            auto_walls = []
            
            # 4. Scan pixels (Darker than 128 = Wall)
            for y in range(self.height):
                for x in range(self.width):
                    if img.getpixel((x, y)) < 128:
                        auto_walls.append([y, x])

            if auto_walls:
                if "auto_scan" in self.db["obstacles"]:
                    del self.db["obstacles"]["auto_scan"]
                
                self.db["obstacles"]["auto_scan"] = auto_walls
                self.redraw_matrix() 
                
                self.animated_reveal(auto_walls)
            else:
                messagebox.showwarning("Scan Empty", "No dark areas detected. Ensure your map has dark lines.")
        
        except Exception as e:
            messagebox.showerror("CV Processing Error", f"Failed to parse visual data. Ensure it is a valid image file.\nError: {e}")

    # === STANDARD LOGIC ===
    def set_mode(self, mode): self.active_mode = mode

    def clear_selection(self):
        self.current_selection = []
        self.redraw_matrix()

    def resize_grid(self):
        try:
            new_w, new_h = int(self.width_var.get()), int(self.height_var.get())
            if new_w < 3 or new_h < 3 or new_w > 50 or new_h > 50:
                raise ValueError
            self.width, self.height = new_w, new_h
            self.db["metadata"]["width"], self.db["metadata"]["height"] = self.width, self.height
            self.build_grid_ui()
        except ValueError:
            messagebox.showerror("DIMENSION ERROR", "Keep limits between 3 and 50.")

    def build_grid_ui(self):
        for widget in self.grid_container.winfo_children(): widget.destroy()
        self.buttons = {}
        grid_frame = tk.Frame(self.grid_container, bg="#0A0F1D")
        grid_frame.place(relx=0.5, rely=0.5, anchor="center")

        btn_width = 4 if self.width <= 20 else 2
        font_size = 8 if self.width <= 20 else 5

        for r in range(self.height):
            for c in range(self.width):
                btn = tk.Button(grid_frame, text="·" if self.width <= 20 else "", width=btn_width, height=1, font=("Consolas", font_size),
                                bg="#0D1527", fg="#00F0FF", relief="flat", command=lambda row=r, col=c: self.handle_click(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                
                btn.bind("<Enter>", lambda e, b=btn, row=r, col=c: self.on_enter(e, b, row, col))
                btn.bind("<Leave>", lambda e, b=btn, row=r, col=c: self.on_leave(e, b, row, col))
                
                self.buttons[(r, c)] = btn
        self.redraw_matrix()

    def redraw_matrix(self):
        for (r, c), btn in self.buttons.items():
            btn.config(text="·" if self.width <= 20 else "", bg="#0D1527", fg="#00F0FF")
            
        for r, c in self.current_selection:
            self.buttons[(r, c)].config(text="[ ]" if self.width <= 20 else "", bg="#E1AD01", fg="black")

        for obs_name, coords_list in self.db["obstacles"].items():
            for r, c in coords_list:
                if (r, c) in self.buttons:
                    self.buttons[(r, c)].config(text=obs_name[:2].upper() if self.width <= 20 else "", bg="#FF0055", fg="white")

        for name, coords in self.db["targets"].items():
            r, c = coords
            if (r, c) in self.buttons:
                self.buttons[(r, c)].config(text=name[:2].upper() if self.width <= 20 else "", bg="#39FF14", fg="black")

    def update_sidebar(self):
        self.targets_list.delete(0, tk.END)
        for name, coords in self.db["targets"].items():
            self.targets_list.insert(tk.END, f" {name} [{coords[0]},{coords[1]}]")

        self.obstacles_list.delete(0, tk.END)
        for obs_name, coords in self.db["obstacles"].items():
            self.obstacles_list.insert(tk.END, f" {obs_name} ({len(coords)} blocks)")

    def handle_click(self, r, c):
        if self.active_mode == "select":
            for obs_name, coords_list in list(self.db["obstacles"].items()):
                if [r, c] in coords_list:
                    if messagebox.askyesno("DELETE", f"Erase '{obs_name}'?"):
                        del self.db["obstacles"][obs_name]
                        self.update_sidebar()
                    self.redraw_matrix()
                    return

            if [r, c] in self.current_selection:
                self.current_selection.remove([r, c])
            else:
                self.current_selection.append([r, c])
            self.redraw_matrix()
            
        elif self.active_mode == "target":
            name = simpledialog.askstring("NEW TARGET", "Enter target name:")
            if name:
                self.db["targets"][name.strip().lower()] = [r, c]
                self.update_sidebar()
            self.redraw_matrix()

    def save_obstacle(self):
        if not self.current_selection: return messagebox.showwarning("NO CELLS", "Select grid cells first!")
        name = simpledialog.askstring("DEFINE OBSTACLE", "What is this obstacle?")
        if name:
            self.db["obstacles"][name.strip().lower()] = self.current_selection.copy()
            self.current_selection = []
            self.update_sidebar()
            self.redraw_matrix()

    def save_and_sync(self):
        with open(DB_FILE, 'w') as f: json.dump(self.db, f, indent=4)
        messagebox.showinfo("SYNCED", "Memory committed to locations.json.")

if __name__ == "__main__":
    root = tk.Tk()
    app = AgnosticMapManager(root)
    root.mainloop()
    