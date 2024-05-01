import pandas as pd
import openpyxl as px
import math


class Data:
    def __init__(self):
        pass

    def load_data(self, data):

        self.alldata = data

    def get_productivity_count(self, data, key):
        keys = ["ST80", "ST90", "ST100", "ST110", "ST120"]
        model1 = [
            "ST20A",
            "ST20B",
            "ST30A",
            "ST30B",
            "ST40A",
            "ST40B",
            "ST50A",
            "ST50B",
            "ST60A",
            "ST60B",
            "ST71",
            "ST72",
            "ST91",
            "ST92",
        ]

        data.dropna(inplace=True)

        # GETTING START TIME
        startime = data.iloc[0, 0]

        # GETTING END TIME
        endtime = data.iloc[len(data) - 1, 0]

        # FUNCTION TO COUNT PRODUCTIVITY CODE WITHIN GIVEN SPECIFIED TIME
        def countproductivity(startime, secondtime):
            return len(
                data[
                    (data[1] >= startime)
                    & (data[1] < secondtime)
                    & (data[3] == "1 - Productive")
                ]
            )

        # INITIALIZING AN ARRAY
        self.productivityarray = []
        self.timearray = []

        while startime < endtime:

            # if not (ignorestart.time() < startime.time() < ignoreend.time()):
            # SECOND TIME IS STARTIME + 1 HOUR
            secondtime = startime + pd.Timedelta(hours=0.5)
            # USING THE FUNCTION TO GET THE COUNT

            # checkdate is a function that checks whether the startime falls in the break period or not but it has not been implemented properly
            # a  = self.checkdate(startime)

            # if a:
            count = countproductivity(startime, secondtime)
            # INCREMENTING STARTIME BY 1 HOUR
            # # IF COUNT ==0 THEN SKIP
            if key not in model1:
                if key in keys:
                    count = math.ceil((count / 265) * 100)
                    count = min(100, count)
                else:
                    count = math.ceil((count / 132) * 100)
                    count = min(100, count)

            self.productivityarray.append(count)
            self.timearray.append(secondtime)
            startime += pd.Timedelta(hours=0.5)

        return [self.productivityarray, self.timearray]

    global dfs

    def createDictionary(self, sheet_names):

        return self.alldata

    def create_dataframeforsinglemachine(self, key):
        # selecting particular machine
        machinedata = self.alldata[key]
        # getting productivity and time arrays
        a, b = self.get_productivity_count(machinedata, key)
        # creating a dataframe
        machinedataframe = pd.DataFrame(a, b)
        # resetting the index
        machinedataframe.reset_index(inplace=True)
        # setting appropriate column names
        machinedataframe.columns = ["index", "Value"]
        # returning df
        return machinedataframe

    def dataforml(self):
        # used for extracting data for machine learning
        return [self.productivityarray, self.timearray]

    def getstartandenddate(self):
        data = self.alldata["ST10A"]
        data.dropna(inplace=True)

        startime = data.iloc[0, 0]

        # GETTING END TIME
        endtime = data.iloc[len(data) - 1, 0]

        return [startime, endtime]
    def validlengthforprediction(self):
        self.get_productivity_count(self.alldata["ST10A"], "ST10A")

        return len(self.productivityarray)>48
