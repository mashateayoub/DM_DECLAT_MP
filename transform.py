import pandas as pd
from Parser import ParserDiabete as pr
from numpy import nan




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
    20: "NoPregnancie" , 
    21: "MinusFivePreg" , 
    22: "FiveToTenPreg" , 
    23: "PlusTenPreg"
}

# Raw database
data = pd.read_csv(r"diabetes.csv")
# mark zero values as missing or NaN
data[["Glucose",	"BloodPressure","BMI"	]] = data[["Glucose",	"BloodPressure"	,"BMI"]].replace(0, nan)
# fill missing values with mean column values
data.fillna(data.mean(), inplace=True)
parser = pr(data) # Custom Parser

# New Database : Transactional database (non binary) using only the 5 features  
parsedData = pd.DataFrame()
for i in range(0, len(data)):    
    list = data.loc[i]
    line = []
    line.append(Items[parser.checkPregnancies(list.loc["Pregnancies"]) ])
    line.append(Items[parser.checkGlucose(list.loc["Glucose"]) ])
    line.append(Items[parser.checkBloodPressure(list.loc["BloodPressure"]) ])
    line.append(Items[parser.checkBMI(list.loc["BMI"]) ])
    line.append(Items[parser.checkAge(list.loc["Age"]) ])
    line.append(Items[parser.checkOutcome(list.loc["Outcome"]) ])
    new_df = pd.DataFrame([line])
    parsedData = pd.concat([parsedData, new_df], axis=0, ignore_index=True)


parsedData.to_csv(r"DiabetesTransactions.csv")