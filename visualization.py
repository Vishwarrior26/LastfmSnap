import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('PlaysPerDay.csv', parse_dates=['Date'], index_col='Date')
df.plot()
plt.show()

# df = pd.read_csv('AllTimeTopArtists.csv')
# df.plot()
# plt.show()
