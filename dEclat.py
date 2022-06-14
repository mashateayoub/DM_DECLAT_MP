import time
import tracemalloc
import pandas as pd
from Parser import ParserDiabete as pr
from numpy import nan


class dEclat:
    def __init__(self, minsupp: int, data):
        self.minsupp = minsupp
        self.items ={
                1: "NormalGlucose",  # Glucose
                2: "PrediabeteGlucose",
                3: "DiabeteGlucose",
                4: "NormalBloodPressure",  # Blood Pressure
                5: "Hypertension1BloodPressure",
                6: "Hypertension2BloodPressure",
                7: "UnderweightBMI",  # BMI
                8: "HealthyweightBMI",
                9: "OverweightBMI",
                10: "ObesityBMI",
                11: "Childhood",  # Age
                12: "Adolescence",
                13: "EarlyAdulthood",
                14: "Adulthood",
                15: "MiddleAge",
                16: "EarlyElder",
                17: "LateElder",
                18: "OutcomeYes",  # Outcome
                19: "OutcomeNo",
                20: "NoPregnancie" , #pregnancies
                21: "MinusFivePreg" , 
                22: "FiveToTen_preg" , 
                23: "PlusTenPreg"
            }
        self.data = pd.read_csv(data)
        self.data[["Glucose",	"BloodPressure","BMI"	]] = self.data[["Glucose",	"BloodPressure"	,"BMI"]].replace(0, nan)
        self.data.fillna(self.data.mean(), inplace=True)
        self.parser = pr(self.data)
        self.database=pd.DataFrame
        self.tidsetDB = {}
        self.diffsetDB = {}
        self.d={}
        self.frequentItems = []

    def rundEclat(self):
        self.start_timestamp = time.time()
        tracemalloc.start()
        self.database= self.parser.parse(items=self.items);
        self.genTidsets()
        self.genLvl1Diffsets()
        self.genLvl2Diffsets()
        self.freqItems()
        print(" ")
        for i in self.frequentItems:
            print(i)
        _,self.peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.end_timestamp = time.time()
        return 0

    def genTidsets(self):
        tidsetDB = {}
        for j in self.database.columns:
            list = []
            for i in range(0, len(self.database)):
                if self.database.loc[i].loc[j] == 1:
                    list.append(i)
            tidsetDB[j] = list

        self.tidsetDB=tidsetDB

    def genLvl1Diffsets(self):
        diffsetDB = {}
        for j in self.tidsetDB:
            l = []
            for i in range(0, len(self.database)):
                if i not in self.tidsetDB[j]:
                    l.append(i)
            diffsetDB[j] = (l, (j), len(self.database) - len(l))

        self.diffsetDB=diffsetDB

    def genLvl2Diffsets(self):
        d = {}
        m = 1
        for i in self.diffsetDB:
            for j in range(i + 1, len(self.diffsetDB) + 1):
                l = []
                for k in self.diffsetDB[j][0]:
                    if k not in self.diffsetDB[i][0]:
                        l.append(k)
                d[m] = (l, (i, j), self.diffsetDB[i][2] - len(l))
                m = m + 1
        self.d=d


    def freqItems(self):
        n = self.minsupp  / 100
        freq = []
        for i in self.diffsetDB:
            if (self.diffsetDB[i][2]/len(self.database)) >= n:
                obj = (self.items[i], self.diffsetDB[i][2] / len(self.database))
                freq.append(obj)

        for i in self.d:
            if (self.d[i][2]/len(self.database)) >= n:
                a=self.d[i][1]
                obj = ((self.items[a[0]] , self.items[a[1]]), self.d[i][2] / len(self.database))
                freq.append(obj)

        self.frequentItems=freq




    def rundExp(self):
        self.start_timestamp = time.time()
        tracemalloc.start()
        self.database= self.parser.parse(items=self.items);
        self.genTidsets()
        self.genLvl1Diffsets()
        self.genLvl2Diffsets()
        self.freqItems()
        _,self.peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        self.end_timestamp = time.time()
        return 0
