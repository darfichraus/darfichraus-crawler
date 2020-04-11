from crawlers import *

f = BadenW()
nrw = Nrw()
by = Bayern()

f.parse_feed()
nrw.parse_feed()
by.parse_feed()


print("--------------------------------------------")
print("--------------------------------------------")


#print(nrw.parse_feed()[0])