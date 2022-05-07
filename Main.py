
from dEclat import dEclat
import os

# dEclat  : minsupp=10%
print("==============dEclat: Version Beta :==========================")

d = dEclat(minsupp=25, data="diabetes.csv")
d.rundEclat()


print(" ")
print("===========================Stats: ============================")
print("Minimum support: "+str(d.minsupp)+"%")
file_size = os.path.getsize(r'diabetes.csv') 
print('Database Size:', file_size/1024, ' Kb')
print("Transactions count from database :"+str(len(d.data)))
print("Frequent itmsets count :"+str(len(d.frequentItems)))
print("Total Time ~ "+str((d.end_timestamp - d.start_timestamp)*100)+" ms")
print("Maximum Memory usage ~ "+str(d.peak_memory/1024 )+" Ko")

