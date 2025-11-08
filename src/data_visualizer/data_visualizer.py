import pandas as pd
import os

class vizualizer:
    def __init__(self):
        self.path = __file__.replace("/src/data_visualizer/data_visualizer.py", "")
        print(self.path)

        self.filename = [i for i in os.listdir(f"{self.path}/data/") if i.endswith(".csv")]
        print(self.filename)

        self.df = pd.read_csv(f"{self.path}/data/{self.filename[0]}")
        print(self.df)

testing = vizualizer()
vizualizer()