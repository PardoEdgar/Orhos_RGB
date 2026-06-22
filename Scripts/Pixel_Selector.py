import tkinter as tk
import cv2
from tkinter import filedialog, ttk
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
        self.types = tk.StringVar(value="Type 1")
        self.target = tk.StringVar(value="Red")
        self.zoom_factor = 1
        self.zoom_step = 1.1

        self.text = tk.StringVar(value="Text")

        container = tk.Frame(root, bg=PANEL)
        container.pack(fill="x")
        tk.Label(
            container,
            text="Pixel intensity extraction",
            bg=PANEL,
            fg=ACCENT,
        ).pack(padx=20, pady=20, anchor="w")

        self.notebook = ttk.Notebook(root)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.tab_1 = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_1, text="Pixel Selector")

        self.tab_2 = tk.Frame(self.notebook, bg=BG)
        self.notebook.add(self.tab_2, text="Color Card")

        self.build_tab_1()
        self.build_tab_2()

    def build_tab_1(self):

        btn_frame_1 = tk.Frame(self.tab_1, bg=BG)
        btn_frame_1.pack(side="bottom", fill="x", padx=5, pady=10)

        main_1 = tk.Frame(self.tab_1, bg=BG)
        main_1.pack(fill="both", expand=True, padx=10, pady=10)

        self.h_scroll = tk.Scrollbar(main_1, orient="horizontal")
        self.v_scroll = tk.Scrollbar(main_1, orient="vertical")

        self.canvas_1 = tk.Canvas(
            main_1,
            bg=BG,
            cursor="crosshair",
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set,
        )

        self.v_scroll.config(command=self.canvas_1.yview)
        self.h_scroll.config(command=self.canvas_1.xview)
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        self.canvas_1.pack(side="left", fill="both", expand=True)

        self.btn_1 = tk.Button(
            btn_frame_1,
            text="Load Image",
            bg=ACCENT,
            fg="black",
            relief="flat",
            padx=40,
            pady=5,
            command=self.load_image,
        )
        self.btn_1.pack(side="left", pady=10, padx=40, fill="x")

        self.btn_2 = tk.Button(
            btn_frame_1,
            text="save data",
            bg=ACCENT,
            fg="black",
            relief="flat",
            padx=40,
            pady=5,
            command=self.images_date,
        )
        self.btn_2.pack(side="left", pady=10, padx=40, fill="x")
        self.btn_zoom_in = tk.Button(btn_frame_1, text="+", command=self.zoom_in)
        self.btn_zoom_in.pack(side="left", pady=10, padx=40, fill="x")
        self.btn_zoom_out = tk.Button(btn_frame_1, text="-", command=self.zoom_out)
        self.btn_zoom_out.pack(side="left", pady=10, padx=40, fill="x")

        # Events
        self.canvas_1.bind("<ButtonPress-1>", self.on_click)

        self.pixel_label_1 = tk.Label(btn_frame_1, text="pixel ---", bg=BG, fg="white")
        self.pixel_label_1.pack(side="right", padx=20)

        tk.Label(
            btn_frame_1,
            text="IDs",
            bg=PANEL,
            fg=ACCENT,
        ).pack(anchor="c", pady=(5, 5))

        entry = ttk.Entry(btn_frame_1, textvariable=self.text, state="normal", width=12)
        entry.pack()

        tk.Label(
            btn_frame_1,
            text="Colony Type",
            bg=PANEL,
            fg=ACCENT,
        ).pack(anchor="c", pady=(10, 10))

        ttk.Combobox(
            btn_frame_1,
            textvariable=self.types,
            values=["Type 1", "Type 3"],
            state="readonly",
            width=12,
        ).pack()

    def build_tab_2(self):
        btn_frame_2 = tk.Frame(self.tab_2, bg=BG)
        btn_frame_2.pack(side="bottom", fill="x", padx=5, pady=10)

        main_2 = tk.Frame(self.tab_2, bg=BG)
        main_2.pack(fill="both", expand=True, padx=10, pady=10)

        self.h_scroll = tk.Scrollbar(main_2, orient="horizontal")
        self.v_scroll = tk.Scrollbar(main_2, orient="vertical")

        self.canvas_2 = tk.Canvas(
            main_2,
            bg=BG,
            cursor="crosshair",
            xscrollcommand=self.h_scroll.set,
            yscrollcommand=self.v_scroll.set,
        )

        self.v_scroll.config(command=self.canvas_2.yview)
        self.h_scroll.config(command=self.canvas_2.xview)
        self.v_scroll.pack(side="right", fill="y")
        self.h_scroll.pack(side="bottom", fill="x")

        self.canvas_2.pack(side="left", fill="both", expand=True)

        self.btn_1_tab_2 = tk.Button(
            btn_frame_2,
            text="Load Image",
            bg=ACCENT,
            fg="black",
            relief="flat",
            padx=40,
            pady=5,
            command=self.load_image,
        )
        self.btn_1_tab_2.pack(side="left", pady=10, padx=40, fill="x")
        self.btn_2_tab_2 = tk.Button(
            btn_frame_2,
            text="save data",
            bg=ACCENT,
            fg="black",
            relief="flat",
            padx=40,
            pady=5,
            command=self.images_date,
        )
        self.btn_2_tab_2.pack(side="left", pady=10, padx=40, fill="x")
        self.btn_zoom_in = tk.Button(btn_frame_2, text="+", command=self.zoom_in)
        self.btn_zoom_in.pack(side="left", pady=10, padx=40, fill="x")
        self.btn_zoom_out = tk.Button(btn_frame_2, text="-", command=self.zoom_out)
        self.btn_zoom_out.pack(side="left", pady=10, padx=40, fill="x")

        # Events
        self.canvas_2.bind("<ButtonPress-1>", self.on_click)

        self.pixel_label_2 = tk.Label(btn_frame_2, text="pixel ---", bg=BG, fg="white")
        self.pixel_label_2.pack(side="right", padx=20)

        tk.Label(
            btn_frame_2,
            text="Color target",
            bg=PANEL,
            fg=ACCENT,
        ).pack(anchor="c", pady=(5, 5))

        ttk.Combobox(
            btn_frame_2,
            textvariable=self.target,
            values=["Red", "yellow", "Black"],
            state="readonly",
            width=12,
        ).pack()

    def load_image(self):
        path = filedialog.askopenfilename()

        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.image = img
        self.arr = np.array(img)
        self.hsv_arr = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)
        self.lab_arr = cv2.cvtColor(img, cv2.COLOR_RGB2LAB)

        print("shape:", img.shape)
        self.display_image(img)
        self.path = path
        self.image_path = Path(path)

    def display_image(self, img):
        self.canvas.update_idletasks()
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        h, w = img.shape[:2]

        self.scale = min(canvas_width / w, canvas_height / h)

        self.display_scale = self.scale * self.zoom_factor

        new_w = int(w * self.display_scale)
        new_h = int(h * self.display_scale)

        resized = cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)

        pil_img = Image.fromarray(resized)
        self.tk_image = ImageTk.PhotoImage(pil_img)

        self.canvas.delete("all")
        self.img_canvas_x_position = max(0, (canvas_width - new_w) // 2)
        self.img_canvas_y_position = max(0, (canvas_height - new_h) // 2)
        self.canvas.create_image(
            self.img_canvas_x_position,
            self.img_canvas_y_position,
            anchor="nw",
            image=self.tk_image,
        )

        self.canvas.config(
            scrollregion=(
                0,
                0,
                max(canvas_width, new_w + self.img_canvas_x_position),
                max(canvas_height, new_h + self.img_canvas_y_position),
            )
        )

    def on_click(self, event):
        self.coords = []
        h, w = self.image.shape[:2]

        canvas_x = self.canvas.canvasx(event.x)
        canvas_y = self.canvas.canvasy(event.y)

        relative_x_position = canvas_x - self.img_canvas_x_position
        relative_y_position = canvas_y - self.img_canvas_y_position

        Real_x = int(relative_x_position / self.display_scale)
        Real_y = int(relative_y_position / self.display_scale)

        self.coords.append((Real_x, Real_y))

        for dx in range(-3, 4):
            for dy in range(-3, 4):
                nx = Real_x + dx
                ny = Real_y + dy
                self.coords.append((nx, ny))
        r = self.arr[Real_y, Real_x, 0]
        g = self.arr[Real_y, Real_x, 1]
        b = self.arr[Real_y, Real_x, 2]
        h = self.hsv_arr[Real_y, Real_x, 0]
        s = self.hsv_arr[Real_y, Real_x, 1]
        v = self.hsv_arr[Real_y, Real_x, 2]
        l_lab = self.lab_arr[Real_y, Real_x, 0]
        a_lab = self.lab_arr[Real_y, Real_x, 1]
        b_lab = self.lab_arr[Real_y, Real_x, 2]
        self.pixel_label.config(
            text=f"Pixel ({Real_x}, {Real_y}); R={r},G={g},B={b}; h={h},s={s},v={v}; l={l_lab},a={a_lab},b={b_lab}"
        )
        self.draw_pixels()

    def extract_data(self, output_path=r"C:\Users\jandr\Downloads"):
        records = []
        for x, y in self.coords:
            r = self.arr[y, x, 0]
            g = self.arr[y, x, 1]
            b = self.arr[y, x, 2]

            h = self.hsv_arr[y, x, 0]
            s = self.hsv_arr[y, x, 1]
            v = self.hsv_arr[y, x, 2]

            l_lab = self.lab_arr[y, x, 0]
            a_lab = self.lab_arr[y, x, 1]
            b_lab = self.lab_arr[y, x, 2]

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
                    "x": x,
                    "y": y,
                    "ID": IDs,
                    "R": float(r),
                    "G": float(g),
                    "B": float(b),
                    "h": float(h),
                    "s": float(s),
                    "v": float(v),
                    "l_lab": float(l_lab),
                    "a_lab": float(a_lab),
                    "b_lab": float(b_lab),
                    "Type": self.types.get(),
                    "IDs": self.text.get(),
                }
            )
        df_img = pd.DataFrame(records)
        csv_path = Path(output_path) / "Data_pixels.csv"

        file_exists = csv_path.exists()
        if file_exists:
            mode = "a"
        else:
            mode = "w"
        df_img.to_csv(
            csv_path,
            mode=mode,
            header=not file_exists,
            index=False,
        )

        print(
            f"{len(df_img):,} pixels from {self.image_path.name} were saved in {csv_path}"
        )

    def draw_pixels(self):
        for x, y in self.coords:
            screen_x = x * self.display_scale + self.img_canvas_x_position
            screen_y = y * self.display_scale + self.img_canvas_y_position
            self.canvas.create_oval(
                screen_x - 0.5,
                screen_y - 0.5,
                screen_x + 0.5,
                screen_y + 0.5,
                outline="red",
            )

    def zoom_in(self):
        self.zoom_factor = self.zoom_factor * self.zoom_step
        self.display_image(self.image)
        self.draw_pixels()

    def zoom_out(self):
        self.zoom_factor = self.zoom_factor / self.zoom_step
        self.display_image(self.image)
        self.draw_pixels()

    def images_date(self):
        folder = self.image_path.parent
        for images in folder.iterdir():
            img = cv2.imread(str(images))
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            h, w = img.shape[:2]
            self.image = img
            self.arr = np.array(img)
            self.image_path = images
            self.extract_data()

    @property
    def canvas(self):
        active = self.notebook.index(self.notebook.select())
        if active == 0:
            return self.canvas_1
        else:
            return self.canvas_2

    @property
    def pixel_label(self):
        active = self.notebook.index(self.notebook.select())
        if active == 0:
            return self.pixel_label_1
        else:
            return self.pixel_label_2


if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("1300x700")
    app = Pixel_selector(root)
    root.mainloop()
