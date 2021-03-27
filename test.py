import time
from datetime import datetime


time = int(datetime.now().time().strftime("%M"))
if 55 <= time & time <= 5:
    print('asdasd')