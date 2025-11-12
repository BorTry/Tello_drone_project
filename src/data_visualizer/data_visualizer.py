import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

class vizualizer:
    def __init__(self, file_name):
        if file_name is None:
            print(f"No file with name {file_name}")
            return
        
        self.path = __file__.replace("/src/data_visualizer/data_visualizer.py", "")
        self.file_path = f"{self.path}/data/{file_name}.csv"

        print(f"Reading data from: {self.file_path}")

        self.text = pd.read_csv(self.file_path) #leser nyeste csv-fila

        self.data = pd.DataFrame(self.text) 

    def clean_text(self):
        self.cleaned_text = self.text.iloc[0, 0].strip() 
        print(self.cleaned_text)
        #return self.clean_text

    def filter_text(self):
        print(self.data)
        #print(self.data["agx"])

    def plot_data(self, cols, title=None, y_label="Value", x_label="index"):
        if isinstance(cols, list):
            self.__plot_multiple_points(cols, title, y_label, x_label)
        else:
            self.__plot_single_point(cols, title, y_label, x_label)

    def __plot_single_point(self, col_name, title, y_label, x_label):
        df = self.data.copy()

        coloumn = df[col_name]
        time_col = df["time"]

        plt.figure(figsize=(10, 6))
        plt.plot(time_col, coloumn)

        if title is None:
            title = f"{col_name} over {x_label}"

        plt.title(title)

        plt.xlabel(x_label)
        plt.ylabel(y_label)

        plt.xticks(time_col[::20], rotation=45)

        plt.legend()
        plt.grid(True, alpha=0.3)

    def __plot_multiple_points(self, cols, title, y_label, x_label):
        df = self.data.copy()

        if "time" in df.columns:
            t_parsed = pd.to_datetime(df["time"], errors="coerce", infer_datetime_format=True)

            if t_parsed.notna().mean() > 0.8:
                t = (t_parsed - t_parsed.iloc[0]).dt.total_seconds()
                x_label = "Flight Time (s)"
            else:
                t_num = pd.to_numeric(df["time"], errors="coerce")

                if t_num.notna().mean() > 0.8:
                    t = t_num - t_num.iloc[0]
                    x_label = "Flight Time"
                else:
                    t = df.index
                    x_label = "Index"
        else:
            t = df.index
            x_label = "Index"

        use_cols = []

        for col_name in cols:
            if col_name in df.columns:
                use_cols.append(col_name)

        for c in use_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        plot_cols = use_cols[:]

        if not plot_cols:
            print("No column")
            return

        plt.figure(figsize=(10, 6))
        for c in plot_cols:
            plt.plot(t, df[c], label=c)

        if title is None:
            title = f"{', '.join(plot_cols)} over {x_label}"

        plt.title(title)
        plt.xlabel(x_label)
        plt.ylabel(y_label)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

    def show_plots(self):
        plt.show()
if __name__ == "__main__":
    testing = vizualizer("2025-11-12[17:1:34]")

    testing.plot_data(["vgx", "vgy", "vgz"])
    testing.plot_data(["agx", "agy", "agz"])

    testing.plot_data("agz")
    testing.plot_data("bat")

    testing.show_plots()