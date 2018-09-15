import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression


stock = "AMD"
url = "https://api.iextrading.com/1.0/stock/"+stock+"/chart/5y?filter=date,close"
urlInfo = "https://api.iextrading.com/1.0/stock/"+stock+"/company"
closingprices = []
dates = []
data = pd.DataFrame(pd.read_json(url, orient="columns"))
for i in data:
    dates.append(data["date"])
    closingprices.append(data["close"])

cp = list(reversed(closingprices))

scores = []
with open("trends.txt") as f:
    data = f.readlines()
    scores = str(data).split(",")
    scores[0] = scores[0][2:]
    scores[-1] = scores[-1][:2]
    int_scores = []

    for score in scores:
        int_scores.append(int(score))




print(len(scores))
DATES = np.array(dates)
CLOSINGPRICES = np.array(cp)
TRENDSCORES = np.array(int_scores)
DatesDF = pd.DataFrame(data=DATES.T)
pricesDF = pd.DataFrame(data=CLOSINGPRICES.T)
trendsDF = pd.DataFrame(data=TRENDSCORES.T)

completeDF = pd.DataFrame()
completeDF = completeDF.assign(Date=DATES[0])
completeDF = completeDF.assign(ClosingPrice=CLOSINGPRICES[0])
completeDF = completeDF.assign(GoogleTrendsScore=trendsDF[0])
print(completeDF)
##### THIS IS TEMPORARY, GOOGLE TRENDS API ONLY RETRIEVES 260 RECENT QUERIES
tempDF = completeDF.loc[0:260]
lm = LinearRegression()
train_x = [tempDF["ClosingPrice"][:-52]]
test_x = [tempDF["ClosingPrice"][-52:]]
train_y = [tempDF["GoogleTrendsScore"][:-52]]
test_y = [tempDF["GoogleTrendsScore"][-52:]]

## Original Graph
plt.scatter(train_x, train_y, color="black")
plt.ylabel("Stock Price")
plt.xlabel("Google Trend Score")
plt.show()

## MACHINE LEARNING
lm.fit(train_x, train_y)
m = lm.coef_
b = lm.intercept_
print(m, b)

## MACHINE LEARNING GRAPH
plt.scatter(train_x, train_y, color="black")
lm.fit(train_x, train_y)
plt.plot(np.unique(tempDF["ClosingPrice"]), np.poly1d(np.polyfit(tempDF["ClosingPrice"], tempDF["GoogleTrendsScore"], 1))(np.unique(tempDF["ClosingPrice"])))
plt.ylabel("Stock Price")
plt.xlabel("Google Trend Score")
plt.show()
# plt.scatter()




# print('Mean Absolute Error:', metrics.mean_absolute_error(y_test, y_pred))
# print('Mean Squared Error:', metrics.mean_squared_error(y_test, y_pred))
# print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, y_pred)))