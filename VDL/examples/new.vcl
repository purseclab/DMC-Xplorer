from init import *

va1=va("alexa1","alexa", "echo", "livingRoom", "user1")
va2=va("home1","google home", "google home mini", "livingRoom", "user1")
light1=light("light1","kitchen", va1)
light2=light("light2","living room", va2)
setup1=setup(va1,8,2)
time.set("2021:10:01:21:04")
list1=[dim@10,brighten,switchOn]
list2=[switchOff,brighten]
tslt1=[0,1,2]
tslt2=[1,2]
#tslt1=["04:01", "04:03", "04:05"]
#tslt2=["04:07", "04:09"]
lt2=[light1@list1,light2@list2]
time.execute(lt2, [tslt1,tslt2], "m")
prob(lt2,[0.5,0.5])
setup1@lt2

