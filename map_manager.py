import tkinter as tk
from tkinter import simpledialog, messagebox
import json
import os

# Define the grid size to match your C engine
GRID_WIDTH = 10
GRID_HEIGHT = 10
DB_FILE = 'locations.json'

class MapManager:
    def __init__(self, root):
        self.root = root
        self.root.title("SmartBot Map Manager")
        self.root.geometry("500x600")
        self.root.configure(padx=20, pady=20)
        
        self.locations = self.load_database()
        self.buttons = {}

        # Title
        tk.Label(root, text="Visual Map Editor", font=("Arial", 16, "bold")).pack(pady=(0, 10))
        tk.Label(root, text="Click a cell to set a target location.", font=("Arial", 10)).pack(pady=(0, 20))

        # Create the visual grid
        self.grid_frame = tk.Frame(root)
        self.grid_frame.pack()

        for r in range(GRID_HEIGHT):
            for c in range(GRID_WIDTH):
                btn = tk.Button(self.grid_frame, text=".", width=4, height=2, 
                                command=lambda row=r, col=c: self.on_cell_click(row, col))
                btn.grid(row=r, column=c, padx=1, pady=1)
                self.buttons[(r, c)] = btn

        self.refresh_grid()

        # Save Button
        tk.Button(root, text="Save & Exit", bg="#28A745", fg="white", font=("Arial", 10, "bold"), 
                  command=self.root.destroy).pack(pady=20)

    def load_database(self):
        if os.path.exists(DB_FILE):
            try:
                with open(DB_FILE, 'r') as file:
                    return json.load(file)
            except Exception:
                return {}
        return {}

    def save_database(self):
        with open(DB_FILE, 'w') as file:
            json.dump(self.locations, file, indent=4)

    def refresh_grid(self):
        # Reset all buttons
        for (r, c), btn in self.buttons.items():
            btn.config(text=".", bg="SystemButtonFace")

        # Highlight saved locations
        for name, coords in self.locations.items():
            if len(coords) == 2:
                r, c = coords
                if (r, c) in self.buttons:
                    self.buttons[(r, c)].config(text=name[:3].upper(), bg="#0078D7", fg="white")

    def on_cell_click(self, row, col):
        # Check if a location already exists here
        existing_name = None
        for name, coords in self.locations.items():
            if coords == [row, col]:
                existing_name = name
                break

        if existing_name:
            # Ask if they want to delete it
            if messagebox.askyesno("Delete Location", f"'{existing_name}' is here. Delete it?"):
                del self.locations[existing_name]
                self.save_database()
                self.refresh_grid()
        else:
            # Ask for a new location name
            new_name = simpledialog.askstring("New Location", f"Name for coordinate [{row}, {col}]:")
            if new_name:
                new_name = new_name.strip().lower()
                self.locations[new_name] = [row, col]
                self.save_database()
                self.refresh_grid()

if __name__ == "__main__":
    root = tk.Tk()
    app = MapManager(root)
    root.mainloop()