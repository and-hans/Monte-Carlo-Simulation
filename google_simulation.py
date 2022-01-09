import pandas as pd
from math import log
from math import sqrt
from math import exp
from random import uniform
from statistics import NormalDist


GOOGL = pd.read_csv("GOOGL.csv", index_col=0)

closing = []

for stock in GOOGL["Adj Close"]:
    closing.append(stock)


def periodicDailyReturn():
    periodicDailyReturn = []
    for i in range(0, len(closing)):
        if (i+1) != 253:
            periodicDailyReturn.append(log(closing[i+1]/closing[i]))
    return periodicDailyReturn


averagePeriodicDailyReturn = sum(periodicDailyReturn())/len(periodicDailyReturn())  # noqa: E501


def variance():
    mean = 0
    for i in range(0, len(periodicDailyReturn())):
        mean += (periodicDailyReturn()[i] - averagePeriodicDailyReturn)**2
    return mean/len(periodicDailyReturn())


drift = averagePeriodicDailyReturn - (variance()/2)

standard_deviation = sqrt(variance())


def randomValues():
    randList = []
    for i in range(0, 253):
        rand = uniform(0, 1)
        randList.append(standard_deviation * NormalDist().inv_cdf(rand))
    return randList


def predictedPrices():
    predictedPricesList = []
    for i in range(len(periodicDailyReturn())):
        predictedPricesList.append(closing[i] * exp(drift+randomValues()[i]))
    return predictedPricesList


def percentDifference():
    differenceList = []
    for i in range(len(periodicDailyReturn())):
        numerator = abs(predictedPrices()[i] - closing[i])

        denominator = (predictedPrices()[i] + closing[i])/2

        total = (numerator/denominator)*100

        differenceList.append(round(total, 2))
    return differenceList


