from tkinter import filedialog
from PIL import Image
import numpy as np
import tkinter as tk
from pathlib import Path
import pandas as pd


def file_selection():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="files")
    return Path(folder)


def image(folder):
    images_data = []
    for i in folder.iterdir():
        site = i.parent.name
        for file in i.iterdir():
            img = Image.open(file).convert("RGB")
            arr = np.array(img)

            arr = arr / 255.0

            arr = np.power(arr, 2.2)

            arr = (arr * 255.0).clip(0, 255)

            r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
            # Distribución de cada canal
            mean_rgb = (
                0.299 * r.astype(float)
                + 0.587 * g.astype(float)
                + 0.114 * b.astype(float)
            )

            datas = file.stem.split("_")
            IDs = datas[0]
            Date = datas[2]
            df_img = pd.DataFrame(
                {
                    "Filename": file.stem,
                    "site": site,
                    "Date": Date,
                    "ID": IDs,
                    "meanRGB": mean_rgb.flatten(),
                    "R": r.flatten(),
                    "G": g.flatten(),
                    "B": b.flatten(),
                }
            )
            images_data.append(df_img)

    return pd.concat(images_data, ignore_index=True)


def save_data(images_data):
    output_path = r"C:\Users\jandr\Downloads\RGB_data.csv"
    images_data.to_csv(output_path, index=False)
    print(images_data)


def main():
    folder = file_selection()
    images_data = image(folder)
    save_data(images_data)


main()
