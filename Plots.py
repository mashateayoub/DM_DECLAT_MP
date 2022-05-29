from jinja2 import PrefixLoader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


data=pd.read_csv("DiabetesTransactions.csv")
AgeItems=["Childhood",  "Adolescence","EarlyAdulthood", "Adulthood","MiddleAge", "EarlyElder", "LateElder",] 
AgeCounts=[0,0,0,0,0,0,0]
BloodPressureItems=["NormalBloodPressure", "Hypertension1BloodPressure", "Hypertension2BloodPressure" ]
BloodPressureCounts=[0,0,0]
BMIItems =["UnderweightBMI", "HealthyweightBMI", "OverweightBMI", "ObesityBMI"] 
BMICounts=[0,0,0,0]
GlucoseItems=[  "NormalGlucose",  "PrediabeteGlucose", "DiabeteGlucose"]
GlucoseCounts=[0,0,0]
OutcomeClass=["OutcomeYes", "OutcomeNo"]
OutcomeCounts=[0,0]
PregClass=[ "NoPregnancie" , "MinusFivePreg" ,"FiveToTen_preg" , "PlusTenPreg"]
PregCounts=[0,0,0,0]

for i in data:
    j=0
    for k in data[i]:
        for m in AgeItems:
            if m==k:
                AgeCounts[AgeItems.index(m)]+=1
        for m in BloodPressureItems:
            if m==k:
                BloodPressureCounts[BloodPressureItems.index(m)]+=1

        for m in BMIItems:
            if m==k:
                BMICounts[BMIItems.index(m)]+=1
        
        for m in GlucoseItems:
            if m==k:
                GlucoseCounts[GlucoseItems.index(m)]+=1
        for m in OutcomeClass:
            if m==k:
                OutcomeCounts[OutcomeClass.index(m)]+=1
        for m in PregClass:
            if m==k:
                PregCounts[PregClass.index(m)]+=1

        
# Outcome counts plot 
plt.bar(OutcomeClass, OutcomeCounts)
plt.title('Outcome counts')
plt.xlabel('Outcome')
plt.ylabel('counts')
plt.savefig("OutcomeCounts.png")
plt.show()

# Glucose counts plot 
plt.bar(GlucoseItems, GlucoseCounts)
plt.title('Glucose counts')
plt.xlabel('Glucose categories')
plt.ylabel('Counts')
plt.savefig("GlucoseCounts.png")
plt.show()

# Blood Pressure counts plot 
plt.bar(BloodPressureItems, BloodPressureCounts)
plt.title('BloodPressure counts')
plt.xlabel('BloodPressure categories')
plt.ylabel('Counts')
plt.savefig("BloodPressureCounts.png")
plt.show()

# Age counts plot 
plt.bar(AgeItems, AgeCounts)
plt.title('Age counts')
plt.xlabel('Age categories')
plt.ylabel('Counts')
plt.savefig("AgeCounts.png")
plt.show()

# BMI counts plot 
plt.bar(BMIItems, BMICounts)
plt.title('BMI counts')
plt.xlabel('BMI categories')
plt.ylabel('Counts')
plt.savefig("BMICounts.png")
plt.show()

# Preg counts plot 
plt.bar(PregClass, PregCounts)
plt.title('Pregnancies counts')
plt.xlabel('Pregnancies Classes')
plt.ylabel('Counts')
plt.savefig(r"PregCounts.png")
plt.show()