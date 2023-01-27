import csv
import dEclat
from pyECLAT import ECLAT
import pandas as pd
import matplotlib.pyplot as plt
from mlxtend.frequent_patterns import apriori
import time
import tracemalloc
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px
from mlxtend.frequent_patterns import fpgrowth
from mlxtend.preprocessing import TransactionEncoder

# Experience :
print(" ")
print("============== Test & experiments : Declat, Eclat, Apriori and Fp-growth ==========================")

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


# Declat
FreqItemsD = []
MinSuppsD = []
TimesD = []
MemUsageD = []
for i in [20, 30, 40, 50, 60, 70]:
    fitems, mem, t = dEclat.declat(data, (i*767)/100)
    FreqItemsD.append(len(fitems)-1)
    MinSuppsD.append(i)
    TimesD.append(t)
    MemUsageD.append(mem)


# ECLAT
dataframe = pd.read_csv("DiabetesTransactions.csv", header=None)
eclat_instance = ECLAT(data=dataframe, verbose=True)

# generate a binary dataframe, that can be used for other analyzes.
eclat_instance.df_bin
eclat_instance.uniq_  # a list with all the names of the different items


MinSupps = []
Times = []
MemUsage = []
FreqItems = []
for i in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    start_timestamp = time.time()
    tracemalloc.start()
    get_ECLAT_indexes, get_ECLAT_supports = eclat_instance.fit(
        min_support=i,
        separator=" , ",
        verbose=True,
    )

    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_timestamp = time.time()
    FreqItems.append(len(get_ECLAT_supports))
    MinSupps.append(i * 100)
    Times.append(end_timestamp - start_timestamp)
    MemUsage.append(peak_memory / 1024)

# Apriori
dataframe = pd.read_csv("BinaryData.csv", header=None)
MinSuppsA = []
TimesA = []
MemUsageA = []
FreqItemsA = []
for i in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    start_timestamp = time.time()
    tracemalloc.start()
    frequent_itemsets = apriori(dataframe, min_support=i).sort_values(
        by=["support"], ascending=False
    )
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_timestamp = time.time()
    FreqItemsA.append(len(frequent_itemsets))
    MinSuppsA.append(i * 100)
    TimesA.append(end_timestamp - start_timestamp)
    MemUsageA.append(peak_memory / 1024)


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


# running the fpgrowth algorithm
TimesF = []
MemUsageF = []
FreqItemsF = []
for i in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    tp1 = time.time()
    tracemalloc.start()
    res = fpgrowth(dataset, min_support=i, use_colnames=True)
    w, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    MemUsageF.append(peak_memory / 1024)
    tp2 = time.time()
    tp3 = tp2 - tp1
    TimesF.append(tp3)
    FreqItemsF.append(len(res))

# Scatter Plot : Memory usage  / min supports
fig, ax = plt.subplots()
ax.plot(np.array(MinSuppsD), np.array(MemUsageD),
        label="DEclat", color="blue")
ax.plot(np.array(MinSupps), np.array(MemUsage), label="Eclat", color="orange")
ax.plot(np.array(MinSuppsA), np.array(MemUsageA),
        label="Apriori", color="red")
ax.plot(
    np.array(MinSuppsA), np.array(MemUsageF), label="Fp-Growth", color="green"
)


ax.set(
    xlabel="Minimum Supports (%)",
    ylabel="Memory usage (Kb)",
    title="Memory usage variation in function of minimum supports ",
)
ax.legend()
ax.grid(True)

fig.savefig("Memory variation.png")
plt.show()

# Scatter Plot : freq items number / min supports
fig, ax = plt.subplots()
ax.scatter(np.array(MinSuppsA), np.array(FreqItemsA),
           marker="o", color="blue", label="Apriori")
ax.scatter(np.array(MinSupps), np.array(FreqItems),
           marker="*", color="orange", label="Eclat")
ax.scatter(np.array(MinSuppsD), np.array(FreqItemsD),
           marker="+", color="red", label="DEclat")
ax.scatter(np.array(MinSuppsD), np.array(FreqItemsF),
           marker="|", color="green", label="Fp-Growth")


ax.set(
    xlabel="Minimum Supports (%)",
    ylabel="Frequent items number",
    title="Freq items variation in function of minimum supports ",
)
ax.legend()
ax.grid(True)

fig.savefig("Frequent items number variation.png")
plt.show()

# Scatter Plot : running time number / min supports
fig, ax = plt.subplots()
ax.scatter(np.array(MinSuppsA), np.array(TimesA),
           marker="o", color="blue", label="Apriori")
ax.scatter(np.array(MinSupps), np.array(Times),
           marker="*", color="orange", label="Eclat")
ax.scatter(np.array(MinSuppsD), np.array(TimesD),
           marker="+", color="red", label="DEclat")
ax.scatter(np.array(MinSuppsD), np.array(TimesF),
           marker="|", color="green", label="Fp-Growth")


ax.set(
    xlabel="Minimum Supports (%)",
    ylabel="running time (s)",
    title="Time variation in function of minimum supports ",
)
ax.legend()
ax.grid(True)

fig.savefig("time.png")
plt.show()


# # Presentation :-----------------------------------------------------------------------------------------------------------------------------------
# # temps :
# print("time : ")
# print("Eclat : \n", Times)
# print("DEclat : \n", TimesD)
# print("Apriori : \n", TimesA)
# print("Fp-Growth : \n", TimesF)
# print("\n")

# # Memoire :
# print("Memory : \n")
# print("Eclat : \n", MemUsage)
# print("DEclat : \n", MemUsageD)
# print("Apriori : \n", MemUsageA)
# print("Fp-Growth : \n", MemUsageF)
# print("\n")

# # Freq items
# print("nb Freq items : \n")
# print("Eclat : \n", FreqItems)
# print("DEclat : \n", FreqItemsD)
# print("Apriori : \n", FreqItemsA)
# print("Fp-Growth : \n", FreqItemsF)
# print("\n")
