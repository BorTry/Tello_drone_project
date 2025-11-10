import datetime
import os

import pandas as pd

# The logger that gets passed when trying to get a logger
class sub_logger:
    def __init__(self, root, logger_name):
        self.root = root
        self.name = logger_name

    def get_curr_time(self):
        return self.root.get_curr_time()
    
    def log(self, string:str):
        """
        appends a string into a txt file
        """
        self.root.csv(f"{self.name} -> {string}")

    def log_csv(self, data:object):
        """
        Writes a row to a csv file 
        """
        self.root.log_csv(data)

class logger:
    def __init__(self):
        date = datetime.datetime.now()
        self.formatted_date = f"{date.year}-{date.month}-{date.day}"

        self.path = __file__.replace("/src/drone/logger.py", "") # get the project path

    def get_curr_time(self):
        curr_time = datetime.datetime.now().time()
        return f"{curr_time.hour}:{curr_time.minute}:{curr_time.second}"
    
    def log_csv(self, data:object):
        """
        Writes a row to a csv file 
        """

        formatted_path = f"{self.path}/data/{self.formatted_date}.csv"

        df = pd.DataFrame(data)

        df["time"] = self.get_curr_time()

        if not os.path.exists(formatted_path):
            # fix the data if the file already exists
            df.to_csv(formatted_path, mode="x", index=False)
        else:
            df.to_csv(formatted_path, mode="a", header=False, index=False)

    def log(self, string:str):
        """
        appends a string into a txt file
        """

        formatted_path = f"{self.path}/logs/{self.formatted_date}.txt"

        if not os.path.exists(formatted_path):
            open(formatted_path, "x").close()

        with open(formatted_path, "a") as file:
            file.write(f"[{self.get_curr_time()}] : {string}\n")

        file.close()

    def get_logger(self, logger_name):
        return sub_logger(self, logger_name)

LOGGER = logger() # The variable that should be imported

LOGGER.log_csv("asdaf")