import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn import preprocessing

class PVPredictor:

    def __init__(self):
        # linear regression model
        self.model = LinearRegression()

    def preprocess(self, weather_record, electricity_record):
        electricity_raw = pd.read_csv(electricity_record)
        weather_raw = pd.read_csv(weather_record)

        # accumulate solar production within a day
        date = '0000-00-00 00:00:00'
        accumulated_solar = 0.
        accumulated_solar_records = []
        for index, row in electricity_raw.iterrows():
            if date != row['DateTime'].split(' ')[0]:
                accumulated_solar_records.append(int(accumulated_solar))
                date = row['DateTime'].split(' ')[0]
                accumulated_solar = 0
            accumulated_solar += row['solar']
        accumulated_solar_records.append(int(accumulated_solar))
        # eliminate first record
        self.solar_records = pd.DataFrame(data=accumulated_solar_records[1:],    # values
                                     index=[i+1 for i in range(len(accumulated_solar_records)-1)],    # 1st column as index
                                     columns=['Solar'])  # 1st row as the column names

        # eliminate useless data
        self.weather_records = weather_raw[['MaxTemperature', 'AvgTemperature', 'MinTemperature', 'MaxHumidity', 'AvgHumidity', 'MinHumidity', 'MaxWindspeed', 'AvgWindspeed', 'MinWindspeed', 'Precipitation']]

        # normalization
        self.weather_records = preprocessing.scale(self.weather_records)

        print("Finish preprocessing")
        print("weather record size: ", self.weather_records.shape)
        print("solar record size: ", self.solar_records.shape)

    def train(self, weather_record='../Data/weather/weather_record.csv', electricity_record='../Data/electricity/electricity_record.csv', toPrint=False):
        self.preprocess(weather_record, electricity_record)
        train_X, test_X, train_y, test_y = train_test_split(self.weather_records[:], self.solar_records[:], train_size=0.8)

        if toPrint:
            print('Train X size: ', train_X.shape)
            print('Train y size: ', train_y.shape)
            print('Test X size: ', test_X.shape)
            print('Test y size: ', test_y.shape)

        self.model.fit(train_X, train_y)
        if toPrint:
            print("Score: ", self.model.score(test_X, test_y))
            print("Finish training\n")

    def predict(self, input_weather):
        input_weather = preprocessing.scale(input_weather)
        return self.model.predict(input_weather)
