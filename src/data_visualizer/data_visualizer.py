import pandas as pd

class data_vizualizer:
    def __init__(self):
        self.path = __file__.replace("/src/data_visualizer/visualizer.py", "")
        
        self.df = pd.read_csv(f"{self.path}/data/.csv")
        pass

    