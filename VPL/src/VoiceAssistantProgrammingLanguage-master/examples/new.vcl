from init import *
​
va1=va("alexa1","alexa", "echo", "livingRoom", "user1")
va2=va("home1","google home", "google home mini", "livingRoom", "user1")
light1=light("light1","kitchen", va1)
light2=light("light2","living room", va1)
light3=light("light3","bathroom", va1)
#tv3=television(va1, "living room")
#smartlock4=smartLock(va1, "corridor")
setup1=setup(va1,8,2)
time.set("2021:10:01:21:04")
list1=[dim@10,brighten,switchOn]
list2=[switchOff,brighten]
list3=[switchOff,brighten]
tslt1=[0,1,2]
tslt2=[1,2]
tslt3=[1,2]
#tslt1=["04:01", "04:03", "04:05"]
#tslt2=["04:07", "04:09"]
#tslt3=["04:07", "04:09"]
lt2=[light1@list1,light2@list2,light3@list3]
time.execute(lt2, [tslt1,tslt2,tslt3], "m")
prob(lt2,[0.5,0.4,0.1])
setup1@lt2