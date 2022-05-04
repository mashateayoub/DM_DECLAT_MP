from ast import Dict, Set
from tokenize import Double
import pandas as pd
import numpy as np


class dEclat:
    def __init__(self, minsupp: int, binaryTransactionsDB: pd.DataFrame):
        self.minsupp = minsupp
        self.database = binaryTransactionsDB
        self.tidsetDB = self.genTidsets()
        self.diffsetDB = self.genLvl1Diffsets()

    def genTidsets(self):
        tidsetDB = {}
        for j in self.database.columns:
            list = []
            for i in range(0, len(self.database)):
                if self.database.loc[i].loc[j] == 1:
                    list.append(i)
            tidsetDB[j] = list

        return tidsetDB

    def genLvl1Diffsets(self):
        self.tidsetDB = self.genTidsets()
        diffsetDB = {}
        for j in self.tidsetDB:
            l = []
            for i in range(0, len(self.database)):
                if i not in self.tidsetDB[j]:
                    l.append(i)
            diffsetDB[j] = (l, len(self.database) - len(l))

        return diffsetDB

    def genLvl2Diffsets(self, n=2):
        self.tidsetDB = self.genTidsets()
        self.diffsetDB = self.genLvl1Diffsets()
        d = {}
        m = 1
        for i in self.diffsetDB:
            for j in range(i + 1, len(self.diffsetDB) + 1):
                l = []
                for k in self.diffsetDB[j][0]:
                    if k not in self.diffsetDB[i][0]:
                        l.append(k)
                d[m] = (l, i, j, self.diffsetDB[i][1] - len(l))
                m = m + 1
        return d
