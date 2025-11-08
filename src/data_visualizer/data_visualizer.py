import pandas as pd

class data_vizualizer:
    def __init__(self):
        self.df = pd.read_csv(f"{self.path}/data/.csv")
        pass

    