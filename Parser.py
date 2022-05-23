from ast import Dict
import pandas as pd
import numpy as np


class ParserDiabete:
    def __init__(
        self,
        raw: pd.DataFrame,
    ):self.raw = raw

    def parse(self, items: Dict):
        data = self.raw
        parsedData = pd.DataFrame(columns=items.keys())
        for i in range(0, len(data)):
            list = data.loc[i]
            line = np.zeros(19, dtype=int)
            line[self.checkBloodPressure(list.loc["BloodPressure"]) - 1] = 1
            line[self.checkAge(list.loc["Age"]) - 1] = 1
            line[self.checkBMI(list.loc["BMI"]) - 1] = 1
            line[self.checkGlucose(list.loc["Glucose"]) - 1] = 1
            line[self.checkOutcome(list.loc["Outcome"]) - 1] = 1
            new_df = pd.DataFrame([line], columns=items.keys())
            parsedData = pd.concat([parsedData, new_df], axis=0, ignore_index=True)

        return parsedData

    def getFeatures(self):
        data = self.raw
        i = 1
        features = {}
        for feature in data.columns.values:
            features[i] = feature
            i = i + 1
        return features

    def checkGlucose(self, glucose: float):
        i = 0
        if glucose <= 140:
            i = 1
        elif glucose < 200:
            i = 2
        else:
            i = 3
        return i

    def checkBloodPressure(self, mesure: float):
        i = 0
        if mesure < 80:
            i = 4
        elif 80 <= mesure < 90:
            i = 5
        else:
            i = 6
        return i

    def checkBMI(self, bmi: float):
        i = 0
        if bmi < 18.5:
            i = 7
        elif bmi <= 24.9:
            i = 8
        elif bmi <= 29.9:
            i = 9
        else:
            i = 10
        return i

    def checkAge(self, age: int):
        i = 0
        if age < 10:
            i = 11
        elif age < 20:
            i = 12
        elif age < 30:
            i = 13
        elif age < 40:
            i = 14
        elif age < 60:
            i = 15
        elif age < 80:
            i = 16
        else:
            i = 17
        return i

    def checkOutcome(self, var: float):
        i = 0
        if var == 1:
            i = 18
        else:
            i = 19
        return i


