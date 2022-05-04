from Parser import ParserDiabete as pr
import pandas as pd

from dEclat import dEclat

# Items utlises
Items = {
    1: "NormalGlucose",
    2: "PrediabeteGlucose",
    3: "DiabeteGlucose",
    4: "NormalBloodPressure",
    5: "Hypertension1BloodPressure",
    6: "Hypertension2BloodPressure",
    7: "UnderweightBMI",
    8: "HealthyweightBMI",
    9: "OverweightBMI",
    10: "ObesityBMI",
    11: "Childhood",
    12: "Adolescence",
    13: "EarlyAdulthood",
    14: "Adulthood",
    15: "MiddleAge",
    16: "EarlyElder",
    17: "LateElder",
    18: "OutcomeYes",
    19: "OutcomeNo",
}


data = pd.read_csv(r"diabetes.csv")
parser = pr(data)
transactionsDataframe = parser.parse(items=Items)
# transactionsDataframe.to_csv(r"Transactions.csv")
# print(transactionsDataframe.loc[100])


# dEclat tests :

d = dEclat(minsupp=5, binaryTransactionsDB=transactionsDataframe)
# diff = d.genLvl1Diffsets()
# lvl2 = d.genLvl2Diffsets()

print(d.diffsetDB[18][1] - len(d.genLvl2Diffsets()[171][0]))
