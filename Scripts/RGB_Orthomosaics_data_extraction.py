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


def image(folder, output_path = r"C:\Users\PardoEA\Downloads\RGB_data"):

    for i in folder.iterdir():
        site = i.parent.name
        for file in i.iterdir():
            img = Image.open(file).convert("RGB")
            arr = np.array(img)

            r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
            # Distribución de cada canal
           # mean_rgb = (0.299 * r.astype(float)+ 0.587 * g.astype(float)      + 0.114 * b.astype(float)   )

            datas = file.stem.split("_")
            IDs = datas[0]
            month = datas[2]
            year = datas[3]
            df_img = pd.DataFrame(
                {
                    "Filename": file.stem,
                    "site": site,
                    "month": month,
                    "year": year,
                    "ID": IDs,
                    "R": r.flatten(),
                    "G": g.flatten(),
                    "B": b.flatten(),
                }
            )
            
            table = pa.Table.from_pandas(df_img, preserve_index=False)

            pq.write_to_dataset(
            table,
            output_path,
             partition_cols=["ID"]
            )
            print(f"Processed {file.name}: {len(df_img):,} pixels")

 

def main():
    folder = file_selection()
    image(folder)


main()


main()
