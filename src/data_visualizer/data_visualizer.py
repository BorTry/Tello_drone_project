import pandas as pd
import os

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
        print(self.data["agx"])

    def plot_data(self)
        pass

if __name__ == "__main__":
    testing = vizualizer()

    testing.filter_text()
