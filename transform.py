import pandas as pd
from Parser import ParserDiabete as pr
import numpy as np



# Items utlises
Items = {
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
}

# Raw database
data = pd.read_csv(r"diabetes.csv")
parser = pr(data) # Custom Parser

# New Database : Transactional database (non binary) using only most important 5 features  
parsedData = pd.DataFrame(columns=["Glucose","Blood Pressure","BMI","Age","Outcome"])
for i in range(0, len(data)):    
    list = data.loc[i]
    line = []
    line.append(Items[parser.checkGlucose(list.loc["Glucose"]) ])
    line.append(Items[parser.checkBloodPressure(list.loc["BloodPressure"]) ])
    line.append(Items[parser.checkBMI(list.loc["BMI"]) ])
    line.append(Items[parser.checkAge(list.loc["Age"]) ])
    line.append(Items[parser.checkOutcome(list.loc["Outcome"]) ])
    new_df = pd.DataFrame([line], columns=["Glucose","Blood Pressure","BMI","Age","Outcome"])
    parsedData = pd.concat([parsedData, new_df], axis=0, ignore_index=True)


parsedData.to_csv(r"DiabetesTransactions.csv")