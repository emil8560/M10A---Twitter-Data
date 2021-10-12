import datetime
import time

first_time = datetime.datetime.now()
print(first_time)
time.sleep(5)
last_time = datetime.datetime.now()
print(last_time)

difference = last_time - first_time
print(difference)

