
import pandas as pd
df = pd.read_csv(r"C:\Users\admin\OneDrive\Desktop\LP5\1_boston_housing.csv")

 
df 
df.head(n=10)   
df.isnull().sum()

from sklearn.model_selection import train_test_split

X = df.loc[:, df.columns != 'MEDV'] # all columns except price are feature
y = df.loc[:, df.columns == 'MEDV']  # price clm is target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=123)

from sklearn.preprocessing import MinMaxScaler
mms = MinMaxScaler()
mms.fit(X_train)
X_train = mms.transform(X_train)
X_test = mms.transform(X_test)

from keras.models import Sequential
from keras.layers import Dense
# build neural network 
model = Sequential()

model.add(Dense(128, input_shape=(13, ), activation='relu', name='dense_1'))
model.add(Dense(64, activation='relu', name='dense_2'))
model.add(Dense(1, activation='linear', name='dense_output'))

model.compile(optimizer='adam', loss='mse', metrics=['mae'])
model.summary()
# adam = adjust weights smartly 
history = model.fit(X_train, y_train, epochs=100, validation_split=0.05, verbose = 1)
# epoch = 100  learn from data 100 times          5% monitor overfitting 
mse_nn, mae_nn = model.evaluate(X_test, y_test)
# Tests model on unseen data (30% we kept aside)

print('Mean squared error on test data: ', mse_nn)
print('Mean absolute error on test data: ', mae_nn)

y1 = model.predict(X_test[:])
y_test
ps=[]
for i in y1:
    ps.append(list(i)[0])

d = pd.DataFrame({'actual':y_test['MEDV'],'predicted':ps})
print(d)