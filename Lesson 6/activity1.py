import os

import calendar
yy=2025
mm=9

print(calendar.month(yy,mm))

file=open('D://cal.txt','w')
file.write(calendar.calendar(2025))
file.close()


# os.system('print /d:"HP Ink Tank 310 series" "D://cal.txt"')
os.startfile("D://cal.txt", "print")