import tkinter as tk
import cv2
from tkinter import filedialog
from PIL import Image, ImageTk
from pathlib import Path
import numpy as np
import pandas as pd

PANEL = "#1D3742"
BG = "#181B1F"
TEXT = "#FFFFFF"
ACCENT = "#FFFFFF"
class Pixel_selector:
    def __init__(self, root):
        self.root = root
        self.root.title("RGB extraction")
        self.image = None
        self.tk_image = None
        self.coords = []
        self.image_path = None

        container = tk.Frame(root, bg=PANEL)
        container.pack(fill="x")
        tk.Label(container, text="Pixel intensity extraction",
            bg=PANEL, fg=ACCENT,
            font=("Segoe UI", 14, "bold")).pack(padx=15, pady=15, anchor="w")

        
        main = tk.Frame(self.root, bg=BG)
        main.pack(fill="both", expand=True, padx=5, pady=5)
        
     
        self.canvas = tk.Canvas(main, bg=BG)
        self.canvas.pack(side="left", fill="both", expand=True)

        btn_frame = tk.Frame(root, bg=BG)
        btn_frame.pack(side="left",fill="x", padx=5, pady=10)

        self.btn = tk.Button(btn_frame, text="Load Image",bg=ACCENT,fg="black",font=("Segoe UI", 10, "bold" ), relief="flat",
                                padx=40, pady=5,cursor="hand2", command=self.load_image)
        self.btn.pack(side="left",pady=10, padx=40, fill="x")

        self.btn_2 = tk.Button(btn_frame, text="save data",bg=ACCENT,fg="black",font=("Segoe UI", 10, "bold" ), relief="flat",
                                padx=40, pady=5,cursor="hand2", command=self.extract_data)
        self.btn_2.pack(side="left",pady=10, padx=40, fill="x")


        # Events
        self.canvas.bind("<ButtonPress-1>", self.on_click)

        self.pixel_label  = tk.Label(btn_frame, text= "pixel ---", bg=BG, fg = "white")
        self.pixel_label.pack(side="right", padx=20)

    def load_image(self):
        path = filedialog.askopenfilename()
        if not path:
            return

        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        print("shape:", img.shape)
        self.image = img
        self.display_image(img)
        self.image_path = Path(path)

        self.arr = np.array(img)


    def display_image(self, img):
        self.canvas.update_idletasks()
        cw = self.canvas.winfo_width()
        ch = self.canvas.winfo_height()
        
        h, w = img.shape[:2]

        scale = min(cw / w, ch / h, 1.0)
        new_w  = int(w * scale)
        new_h  = int(h * scale)

        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
        self.display_scale = scale
        self.rendered_w     = new_w
        self.rendered_h     = new_h
        pil_img = Image.fromarray(resized)
        self.tk_image = ImageTk.PhotoImage(pil_img)

        self.canvas.delete("all")   # limpia antes de redibujar
        self.img_x0 = (cw - new_w) // 2
        self.img_y0 = (ch - new_h) // 2
        self.canvas.create_image(self.img_x0, self.img_y0,
                                 anchor="nw", image=self.tk_image)
    
    def on_click(self, event):
        self.coords = []
        h, w = self.image.shape[:2]
        # Coordenadas relativas al borde de la imagen mostrada
        rx = event.x - self.img_x0
        ry = event.y - self.img_y0

        # Convertir a coordenadas de la imagen original
        cx = int(rx / self.display_scale)
        cy = int(ry / self.display_scale)
        
        h, w = self.image.shape[:2]
        self.coords.append((cx,cy))

        print(
        f"event=({event.x},{event.y})",
        f"img_origin=({self.img_x0},{self.img_y0})",
        f"rx={rx}",
        f"ry={ry}",
        f"scale={self.display_scale}",
        f"cx={cx}",
        f"cy={cy}"
        )
        for dx in range(-3, 3):
            for dy in range(-3, 3):
                nx = max(0, min(cx + dx, w - 1))
                ny = max(0, min(cy + dy, h - 1))
                self.coords.append((nx, ny))
        r = self.arr[cy, cx, 0]
        g = self.arr[cy, cx, 1]
        b = self.arr[cy, cx, 2]
        
        self.pixel_label.config(text=
        f"Pixel ({cx}, {cy}); R={r},G={g},B={b}"
         )    
    def extract_data(self, output_path = "G:\Edgar_workspace\RGB_data.csv"):
        records= []

        for x,y in self.coords:
                r = self.arr[y, x, 0]
                g = self.arr[y, x, 1]
                b = self.arr[y, x, 2]

                datas = self.image_path.stem.split("_")
                IDs = datas[0]
                day = datas[1]
                month = datas[2]
                year = datas[3]
                records.append(
                    {
                        "Filename": self.image_path.stem,
                        "site": self.image_path.parent.parent.name,
                        "year": year,
                        "day": day,
                        "month": month,
                        "x":x,
                        "y":y,
                        "ID": IDs,
                        "R": float(r),
                        "G": float(g),
                        "B": float(b),
                    }
                )
        df_img = pd.DataFrame(records)        
        df_img.to_csv(Path(output_path)/"Data_pixels.csv")
        print(f"Processed {self.image_path.name}: {len(df_img):,} pixels")



if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("900x600")
    app = Pixel_selector(root)
    root.mainloop()
