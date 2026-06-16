from tkinter import filedialog
from PIL import Image
import numpy as np
import tkinter as tk
from pathlib import Path
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq


def file_selection():
    root = tk.Tk()
    root.withdraw()
    folder = filedialog.askdirectory(title="files")
    return Path(folder)


def image(folder, output_path = r"G:\Edgar_workspace\MogoMogo_2023\RGB_data.csv"):

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
           # mean_rgb = (0.299 * r.astype(float)+ 0.587 * g.astype(float)      + 0.114 * b.astype(float)   )

            datas = file.stem.split("_")
            IDs = datas[0]
            Date = datas[2]
            df_img = pd.DataFrame(
                {
                    "Filename": file.stem,
                    "site": site,
                    "Date": Date,
                    "ID": IDs,
                    "R": r.flatten(),
                    "G": g.flatten(),
                    "B": b.flatten(),
                }
            )
            
            table = pa.Table.from_pandas(df_img, preserve_index=False)

            pq.write_to_dataset(
            table,
            root_path="dataset_pixels",
             partition_cols=["ID"]
            )
            print(f"Processed {file.name}: {len(df_img):,} pixels")



def main():
    folder = file_selection()
    image(folder)


main()
