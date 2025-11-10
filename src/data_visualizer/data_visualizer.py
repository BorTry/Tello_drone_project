import pandas as pd
import os
import matplotlib.pyplot as plt
import numpy as np

class vizualizer:
    def __init__(self):
        self.path = __file__.replace("/src/data_visualizer/data_visualizer.py", "")
        print(self.path)

        self.filename = [i for i in os.listdir(f"{self.path}/data/") if i.endswith(".csv")]
        print(f"Reading: {self.filename}")

        self.text = pd.read_csv(f"{self.path}/data/{self.filename[-1]}") #leser nyeste csv-fila

        self.data = pd.DataFrame(self.text) 
        
        #print(self.text)

        # self.text = pd.read_csv(f"{self.path}/data/{"insert filename.csv"}") # csv override 
        # print(self.text)

    def clean_text(self):
        self.cleaned_text = self.text.iloc[0, 0].strip() 
        print(self.cleaned_text)
        #return self.clean_text

    def filter_text(self):
        print(self.data)
        #print(self.data["agx"])

    def plot_data(self, cols = ("agx", "agy", "agz"), magnitude=False, title=None, ylabel="Value"):

        df = self.data.copy()

        # if isinstance(cols, str):
        #     cols = [c.strip() for c in cols.split(",") if c.strip()]
        # else:
        #     cols = list(cols)

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

        use_cols = [c for c in cols if c in df.columns]
        for c in use_cols:
            df[c] = pd.to_numeric(df[c], errors="coerce")

        plot_cols = use_cols[:]
        if magnitude and len(use_cols) >= 2:
            df["magnitude"] = np.sqrt(sum(df[c]**2 for c in use_cols))
            plot_cols.append("magnitude")

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
        plt.ylabel(ylabel)
        plt.legend()
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    testing = vizualizer()

    testing.filter_text()

testing = vizualizer()

testing.plot_data(("height"))