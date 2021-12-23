import pandas as pd
import matplotlib.pyplot as plt

# df = pd.read_csv('PlaysPerDay.csv', parse_dates=['Date'], index_col='Date')
# df.plot()
# plt.show()

df = pd.read_csv('AllTimeTopArtists.csv')
# print(df)
df.plot(x='Artists', kind='bar')

df = pd.read_csv('AllTimeTopAlbums.csv')
# print(df)
df.plot(x='Albums', kind='bar')

df = pd.read_csv('AllTimeTopTracks.csv')
# print(df)
df.plot(x='Tracks', kind='bar')


plt.show()
