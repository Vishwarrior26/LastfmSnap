import eyed3
duration = eyed3.load('D:\\Music\\29 Snow.mp3').info.time_secs
print(duration)
