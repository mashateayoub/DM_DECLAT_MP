import csv
import dEclat
from pyECLAT import ECLAT
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
import time
import tracemalloc
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from mlxtend.preprocessing import TransactionEncoder

# Experience :
print(" ")
print("============== Test & experiments : Declat, Eclat, Apriori and Fp-growth (Association rules) ==========================")

# data
with open('DiabetesTransactions.csv', newline='') as file:
    reader = csv.reader(file, delimiter=',')
    # store the headers in a separate variable,
    # move the reader object to point on the next row
    headings = next(reader)
    # data list to store all rows
    data = []
    data.append(headings)
    for row in reader:
        data.append(row[:])

fitems, mem, t = dEclat.declat(data, 300)
print(len(fitems), " f items found")
a = dEclat.generate_association_rules(fitems, data, 0, 0)
print(len(a), " association rules found")
print("     Antecedent,            Consequent,     Support,   Confidence,           Lift")
for i in a:
    print(i)


# fpGrowth
# importation de la base de donnée
dataset = pd.read_csv("DiabetesTransactions.csv")
transaction = []
for i in range(0, dataset.shape[0]):
    for j in range(0, dataset.shape[1]):
        transaction.append(dataset.values[i, j])
# convertir en un tableau numpy
transaction = np.array(transaction)
#  ensuite transformer en dataframe
df = pd.DataFrame(transaction, columns=["items"])
# Put 1 to Each Item For Making Countable Table, to be able to perform Group By
df["incident_count"] = 1
#  supprimer les items ayant des valeurs nulle de la dataset
indexNames = df[df["items"] == "nan"].index
df.drop(indexNames, inplace=True)
# Transform Every Transaction to Seperate List & Gather Them into Numpy Array
transaction = []
for i in range(dataset.shape[0]):
    transaction.append([str(dataset.values[i, j])
                       for j in range(dataset.shape[1])])
#  creation d'un tableau numpy pour les transactions
transaction = np.array(transaction)
te = TransactionEncoder()
te_ary = te.fit(transaction).transform(transaction)
dataset = pd.DataFrame(te_ary, columns=te.columns_)


print(len(fpgrowth(dataset, min_support=300/767, use_colnames=True)))
arule = association_rules(
    fpgrowth(dataset, min_support=300/767, use_colnames=True), "confidence", 0)
print(arule)
