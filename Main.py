from Parser import ParserDiabete as pr
import pandas as pd

from dEclat import dEclat

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


data = pd.read_csv(r"diabetes.csv")
parser = pr(data)
transactionsDataframe = parser.parse(items=Items)
transactionsDataframe.to_csv(r"Transactions.csv")


# dEclat  : 300 transaction (minsup=39,0625%)
d = dEclat(minsupp=10, binaryTransactionsDB=transactionsDataframe, Items=Items)
for i in d.frequentItems:
    print(i)
