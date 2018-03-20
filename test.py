from logg import Logfile
import time

l=Logfile()
try:

    z = 0
    for y in range(0, 10):

        summa = z/y
        l.log(summa)

        time.sleep(1)
except Exception as err:
    l.log_err(err)
finally:
    l.end()