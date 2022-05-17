
from dEclat import dEclat
import numpy as np
import os
import time
import tracemalloc
from pyECLAT import ECLAT
import pandas as pd
import matplotlib.pyplot as plt

# dEclat  : minsupp=20%
# Test :
print("==================== dEclat: (min_comb=1 & max_comb=2) ==========================")

d = dEclat(minsupp=20, data="diabetes.csv")
d.rundEclat()


print(" ")
print("=========================== Statistiques : ============================")
print("Minimum support: "+str(d.minsupp)+"%")
file_size = os.path.getsize(r'diabetes.csv') 
print("Database Size: ", file_size/1024, "Kb")
print("Transactions count from database :"+str(len(d.data)))
print("Frequent itmsets count :"+str(len(d.frequentItems)))
print("Total Time ~ "+str((d.end_timestamp - d.start_timestamp))+" s")
print("Maximum Memory usage ~ "+str(d.peak_memory/1024 )+" Kb")



#Experience : 

# DECLAT
print(" ")
print("==============dEclat: Test & experience ==========================")
FreqItemsD=[]
MinSuppsD=[]
TimesD=[]
MemUsageD=[]
for i in [20,30, 40,50,60, 70  ]:
    d = dEclat(minsupp=i, data="diabetes.csv")
    d.rundExp()
    FreqItemsD.append(len(d.frequentItems))
    MinSuppsD.append(i)
    TimesD.append(d.end_timestamp - d.start_timestamp)
    MemUsageD.append(d.peak_memory/1024)


# ECLAT 
dataframe = pd.read_csv('DiabetesTransactions.csv', header=None) 
eclat_instance = ECLAT(data=dataframe, verbose=True)

eclat_instance.df_bin   #generate a binary dataframe, that can be used for other analyzes.
eclat_instance.uniq_    #a list with all the names of the different items

MinSupps=[]
Times=[]
MemUsage=[]
FreqItems=[]
for i in [0.2, 0.3, 0.4, 0.5, 0.6, 0.7]:
    start_timestamp = time.time()
    tracemalloc.start()
    get_ECLAT_indexes, get_ECLAT_supports = eclat_instance.fit(min_support=i,
                                                            min_combination=1,
                                                            max_combination=2,
                                                            separator=' & ',
                                                            verbose=True)
    
    _,peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    end_timestamp = time.time()
    FreqItems.append(len(get_ECLAT_supports))
    MinSupps.append(i*100)
    Times.append(end_timestamp - start_timestamp)
    MemUsage.append(peak_memory/1024)



# Scatter Plot : Memory usage  / min supports
fig, ax = plt.subplots()
ax.plot(np.array(MinSuppsD), np.array(MemUsageD),label="diffeclat")
ax.plot(np.array(MinSupps), np.array(MemUsage), label="eclat", linestyle='dashed')

ax.set(xlabel='Minimum Supports (%)', ylabel='Memory usage (Kb)',
       title='Memory usage variation in function of min supports ')
ax.grid()

fig.savefig("Memory variation.png")
plt.show()



# Scatter Plot : freq items number / min supports
fig, ax = plt.subplots()
ax.scatter(np.array(MinSupps), np.array(FreqItems) , marker = '*', color = 'green')
ax.scatter(np.array(MinSuppsD), np.array(FreqItemsD) , marker = '+', color = 'red')

ax.set(xlabel='Minimum Supports (%)', ylabel='Frequent items number',
       title='Freq items variation in function of min supports ')
ax.grid()

fig.savefig("Freq items number variation.png")
plt.show()




