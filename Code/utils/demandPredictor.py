from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np

class demandPredictor:

    def __init__(self):
        self.model = LinearRegression()

    def train(self, file='../Data/electricity/electricity_record.csv'):
        df = pd.read_csv(file)
        df['year'] = ''
        df['month'] = ''
        df['date'] = ''
        df['day'] = ''
        day = 3
        date = '2018/11/1'

        for index, row in df.iterrows():
            if date != row['DateTime'].split(' ')[0]:
                date = row['DateTime'].split(' ')[0]
                day += 1
                day %= 7
            y, m, d = df.at[index, 'DateTime'].split(' ')[0].split('/')
            df.at[index, 'year'] = int(y)
            df.at[index, 'month'] = int(m)
            df.at[index, 'date'] = int(d)
            df.at[index, 'day'] = day
    
        df.drop(['DateTime'], axis=1, inplace=True)
        df = df.groupby(['year', 'month', 'date', 'day']).sum()
        df['demand'] = ''

        for index, row in df.iterrows():
            df.at[index, 'demand'] = (df.at[index, 'grid'] + df.at[index, 'solar'])
        
        _, _, _, d = zip(*df.index.values)

        meanDemand = df.groupby(['day'])['demand'].apply(lambda x: sum(x)/len(x))
        monthly_mean = df.groupby(['month'])['demand'].apply(lambda x: sum(x)/len(x))
        
        self.monthly_mean = monthly_mean
        self.meanDemand = meanDemand

        def base_mean(month, day, month_mean, day_mean):
            return month_mean[month], day_mean[day]

        _, month, _, day = zip(*df.index.values)
        month_base, day_base = zip(*[base_mean(index[1], index[3], monthly_mean, meanDemand) for index, row in df.iterrows()])
        data = list(map(lambda x: list(x), zip(month, day, month_base, day_base)))
        trainX, testX, trainY, testY = train_test_split(data, list(df[['demand']].demand))
        self.model.fit(trainX, trainY)
        print("Score: {:.2f}%".format(self.model.score(testX, testY)*100))
    
    def predict(self, input):
        # input => [month, day]
        month, day = input
        input.append(self.monthly_mean[month-1])
        input.append(self.meanDemand[(day-1+7)%7])
        return self.model.predict([input])