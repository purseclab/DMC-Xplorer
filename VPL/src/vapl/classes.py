import random
import sys
import numpy as np
import json
from datetime import datetime
from datetime import timedelta


def captureVC(command):
    print(command)



commands=[]
commandTS=[]
deviceList=[]
compareFlag=False
tempLatestTime=""
VaCommands=[]





class timestamp:
    currentTimestamp=""
    def __init__(self, *args):
        if(len(args)==6):
         self.year=args[0]
         self.month=args[1]
         self.day=args[2]
         self.hour=args[3]
         self.minute=args[4]
         self.second=args[5]
         self.actionList=[]
         self.ts=[]
        elif(len(args)==0):
         self.year=0
         self.month=0
         self.day=0
         self.hour=0
         self.minute=0
         self.second=0
         self.actionList=[]
         self.ts=[]





    def set(self, st):
        global globalTimeStamp
        globalTimeStamp=st
        print(type(str(globalTimeStamp)),"gts")
        lt=st.split(":")
        if(len(lt)>0):
         self.year=lt[0]
        if(len(lt)>1):
            self.month=lt[1]
        if(len(lt)>2):
            self.day=lt[2]
        if(len(lt)>3):
            self.hour=lt[3]
        if(len(lt)>4):
            self.minute=lt[4]
        if(len(lt)>5):
            self.second=lt[5]

    def readTimeStamp(self,st):
        lt=st.split(":")
        if(len(lt)==1):
            self.second=lt[0]
        if(len(lt)==2):
            self.second=lt[1]
            self.minute=lt[0]
        if(len(lt)==3):
            self.second=lt[2]
            self.minute=lt[1]
            self.hour=lt[0]
        if(len(lt)==4):
            self.second=lt[3]
            self.minute=lt[2]
            self.hour=lt[1]
            self.day=lt[0]
        if(len(lt)==5):
            self.second=lt[4]
            self.minute=lt[3]
            self.hour=lt[2]
            self.day=lt[1]
            self.month=lt[0]
        if(len(lt)==6):
            self.second=lt[5]
            self.minute=lt[4]
            self.hour=lt[3]
            self.day=lt[2]
            self.month=lt[1]
            self.year=lt[0]
        print(self.year,self.month,self.day,self.hour,self.minute,self.second,"print1")
    def calcTs(self,ts,sm):
        if(str(timestamp.currentTimestamp) is ""):
           if(str(sm) is 'm'):
            gts=str(globalTimeStamp)+":00"
           else:
               gts=globalTimeStamp

        else:
            gts=timestamp.currentTimestamp



        time_str =  str(gts)
        date_format_str = '%Y:%m:%d:%H:%M:%S'
        print(time_str,"time11")
        given_time = datetime.strptime(time_str, date_format_str)
        if(type(ts) is not list):
         if(str(sm) is 's'):
          n = ts
          final_time = given_time + timedelta(seconds=n)

         elif(str(sm) is 'm'):
            n = ts
            final_time = given_time + timedelta(minutes=n)
         final_time_str = final_time.strftime('%Y:%m:%d:%H:%M:%S')
         timestamp.currentTimestamp=final_time_str
         print(final_time_str,"final11")
         print(timestamp.currentTimestamp,"cts")
         return final_time_str
        else:
            tempList=[]
            for i in range(0,len(ts)):

                if(str(sm) is 's'):
                    n = ts[i]
                    final_time = given_time + timedelta(seconds=n)
                elif(str(sm) is 'm'):
                    n = ts[i]
                    print(n,"nn1")
                    final_time = given_time + timedelta(minutes=n)
                given_time=final_time
                final_time=final_time.strftime('%Y:%m:%d:%H:%M:%S')
                tempList.append(final_time)

                print(final_time,"final1")
            timestamp.currentTimestamp=tempList[-1]
            print(timestamp.currentTimestamp,"cts")
            return tempList






    def execute(self, *args):
       if(len(args)==2):
        list1=args[0]
        tsList=args[1]
        print(list1,"list121")
        #print(type(list(list1[0].keys())[0]),"list1111")
        #if(type(list(list1[0].keys())[0]) not in classList):
            #self.actionList.append(list1)
            #self.ts.append(tsList)


        #else:
        if(type(list1) in classList):
            print("I am here..")
            tempTs=str(globalTimeStamp)+":"+str(tsList)
            list1.timestamp.ts.append(tempTs)

        if(type(list1) is dict):
            tempTs=[]
            if(type(tsList) is list):
             for ts in tsList:
                tempTs.append(str(globalTimeStamp)+":"+str(ts))
             list(list1.keys())[0].timestamp.ts=tempTs
            elif(type(tsList) is str):
                tempTs=str(globalTimeStamp)+":"+tsList
                list(list1.keys())[0].timestamp.ts.append(tempTs)



        else:
          print(len(tsList),"tslist11")
          for i in range(0,len(tsList)):
                print(type(tsList[i]),"type1")
                if(tsList[i] is not 'None' and type(tsList[i]) is not list):
                 print(type(list1[i]),"list1111")
                 print(str(globalTimeStamp)," ",str(tsList[i]), "timep1")
                 tempTs=str(globalTimeStamp)+":"+str(tsList[i])
                 print(tempTs, "timep11")
                 if(type(list1[i]) is dict):
                  list(list1[i].keys())[0].timestamp.ts.append(tempTs)
                 elif(type(list1[i]) in classList):
                     list1[i].timestamp.ts.append(tempTs)
                elif(type(tsList[i]) is list):
                    tempTs=[]
                    for ts in tsList[i]:
                        tempTs.append(str(globalTimeStamp)+":"+str(ts))

                    print(str(globalTimeStamp)," ",str(tsList[i]), "timep")
                    if(type(list1[i]) is dict):
                     print("what",list1[i])
                     list(list1[i].keys())[0].timestamp.ts=tempTs
                    elif(type(list1[i]) in classList):
                        list1[i].timestamp.ts=tempTs

                    #print(list(list1[i].keys())[0], tsList[i],i,"alls")
            # list[i].time.actionList=
       elif(len(args)==3):

         list1=args[0]
         tsList=args[1]
         sm=args[2]


           #print(type(list(list1[0].keys())[0]),"list1111")
           #if(type(list(list1[0].keys())[0]) not in classList):
            #self.actionList.append(list1)
            #self.ts.append(tsList)
           #else:
         if(type(list1) in classList):
           print("I am here..")
           calct=self.calcTs(tsList,sm)
           list1.timestamp.ts=calct

         if(type(list1) is dict):
           calct=self.calcTs(tsList,sm)
           if(type(tsList) is list):
               print(calct,"calct11",list(list1.keys())[0])
               list(list1.keys())[0].timestamp.ts=calct
               print(calct,"calct11",list(list1.keys())[0].timestamp.ts)
           elif(type(tsList) is int):
               print(list(list1.keys())[0],"tst1")
               list(list1.keys())[0].timestamp.ts.append(calct)


         else:
           print(len(tsList),"tslist11")
           for i in range(0,len(tsList)):
               print(type(tsList[i]),"type1")
               if(tsList[i] is not 'None' and type(tsList[i]) is not list):
                   print(type(list1[i]),"list1111")
                   calct=self.calcTs(tsList[i],sm)

                   if(type(list1[i]) is dict):
                    list(list1[i].keys())[0].timestamp.readTimeStamp(calct)
                   elif(type(list1[i]) in classList):
                       print(calct,list1[i].timestamp,"tempcalct","ts")
                       list1[i].timestamp.ts.append(calct)
                   tempLatestTime=calct

               elif(type(tsList[i]) is list):
                   calct=self.calcTs(tsList[i],sm)
                   print(calct,"calct1")
                   if(type(list1[i]) is dict):
                    list(list1[i].keys())[0].timestamp.ts=calct
                    print(list(list1[i].keys())[0], calct[i],i,"alls")
                   elif(type(list1[i]) in classList):
                       list1[i].timestamp.ts=calct
                       #print(list(list1[i].keys())[0], calct[i],i,"alls")









class probDist():
    def __init__(self, typeDist,mean,sd):
        self.typeDist=typeDist
        self.mean=mean
        self.sd=sd
    def normal_dist(self,x,mean ,sd):
        print(type(mean),type(sd),type(x),"types")
        prob_density = (np.pi*sd) * np.exp(-0.5*((x-mean)/sd)**2)
        return prob_density
    def distList(self,totalCommands):
        if(str(self.typeDist) is "normal"):
            x = np.linspace(1,100,totalCommands)
        pdf = self.normal_dist(x,self.mean,self.sd)
        print(totalCommands,"pdf1")
        return pdf







class va:
    counter=0
    def __init__(self, name,type, deviceType, location, userId,id=0):
        self.name=name
        self.type=str(type)
        self.deviceType=deviceType
        self.location=location
        self.userId=userId
        self.id=va.counter
        va.counter=va.counter+1


class setup:
    def __init__(self, vaList, nCommands, distance):
        try:
            if(type(vaList) is list):
                if(type(vaList[0]) is not va):
                    raise Exception("Incorrect type. Object of type VA is required for va attribute of setup instance")
            elif(type(vaList) is not va):
                raise Exception("Incorrect type. Object of type VA is required for va attribute of setup instance")
            elif(type(nCommands) is not int):
                raise Exception("Incorrect type. Integer value is required for nCommands attribute of setup instance")
            elif(type(distance) not in [int, probDist]):
                raise Exception("Incorrect type. Integer value is required for distance attribute of setup instance")


        except Exception as e:
            print(e)
            sys.exit(1)
        else:
         self.vaList=vaList
         self.nCommands=nCommands
         totalCommands=self.nCommands
         print(totalCommands,"tc1")
         self.distance=distance
         self.generatedCommands=[]
####light1.list

    def processList(self, methodsDict):


        print(methodsDict,"1011")

        for i in methodsDict:
            print(i.probability,"methodsDict22")

            nGenCommands=int(i.probability*self.nCommands)
            print(nGenCommands,"ngen1")
            nDoneCommands=0

            if(methodsDict[i]!=None):
                i.list(methodsDict[i],nGenCommands,nDoneCommands)



            else:

                 i.callAll(nGenCommands,nDoneCommands)









        for i in commands:
            self.generatedCommands.append(i)
        commands.clear()









#{<vapl.classes.setup object at 0x104631F0>: [ {<vapl.classes.light object at 0x10463530>:
    # [{'dim': 10}, 'brighten', 'switchOff'], <vapl.classes.light object at 0x10463550>:
    # [{'dim': 10}, 'brighten', 'switchOff'], <vapl.classes.light object at 0x10463570>:
    # [{'dim': 10}, 'brighten', 'switchOff'], <vapl.classes.light object at 0x10463590>:
    # [{'dim': 10}, 'brighten', 'switchOff'], <vapl.classes.light object at 0x10463710>:
    # [{'dim': 10}, 'brighten', 'switchOff']} ]}

#dict [{<vapl.classes.light object at 0x105B2430>: [{'dim': 10}, 'brighten', 'switchOff'],
    # <vapl.classes.light object at 0x105B2450>: [{'dim': 10}, 'brighten', 'switchOff'],
    # <vapl.classes.light object at 0x105B2470>: [{'dim': 10}, 'brighten', 'switchOff'],
    # <vapl.classes.light object at 0x105B2490>: [{'dim': 10}, 'brighten', 'switchOff'],
    # <vapl.classes.light object at 0x105B24B0>: [{'dim': 10}, 'brighten', 'switchOff']}]


    def generate(self, commandRules):
     if(type(commandRules) is not dict):
         commandRules={self:commandRules}

     print("dict",commandRules)
     ls=[]
     #print("generate",commandRules)
     #dict.__setitem__()
     cl=[light, 'messages',thermostat,television,smartLock,fan,airPurifier,smartCamera]
     for i in commandRules:

         #{setup1:({light1:({dim:10},brighten,off)})}
         #{light1:{"dim":10,"brighten":None,"switchOff":None}}

        for j in commandRules[i]:
            #print(type(j))
            if(type(j) is dict):
                #print("in")


                #tempDict[j.keys[0]]={}
                for k1 in list(j.keys()):
                 tempDict={k1:{}}
                 #print("TempDict0",tempDict)
                 for k in j[k1]:
                    #print("k",k)
                    if(type(k) is dict):

                        tempKey=list(k.keys())[0]
                        tempValue=k[list(k.keys())[0]]
                        #print(tempDict[list(j.keys())[0]])
                        #print("list(j.keys())[0]")
                        tempDict[k1].__setitem__(tempKey,tempValue)
                    else:
                        #print(tempDict[list(j.keys())[0]])

                        tempDict[k1].__setitem__(str(k),None)
                 #print("TempcommandRules",tempDict)
                 ls.append(tempDict)
            elif(type(j)  in cl):
                ls.append({j:None})

     print("ls1",len(ls),ls)
     for i in ls:

        self.processList(i)

     for i in range(0,len(self.generatedCommands)):
      updatedCommand=self.addWakeup(self.generatedCommands[i],deviceList[i].connectedVA.type)
      VaCommands.append(voiceCommands(updatedCommand,commandTS[i],deviceList[i],deviceList[i].connectedVA))
      print(deviceList[i].connectedVA,"vaList")
     print(len(self.generatedCommands),self.generatedCommands)
     print(str(globalTimeStamp),"##################Timestamp########################\n",len(commandTS),commandTS)
     if(type(self.distance) is probDist):
         lt=self.distance.distList(self.nCommands)
         print("##################Distance########################\n",lt)
     print("\n##################Output########################\n")
     for i in range(0,len(VaCommands)):
      print(VaCommands[i].voiceCommand,VaCommands[i].timestamp, VaCommands[i].device,VaCommands[i].device.connectedVA)
      #environment='{"VA-Name":VaCommands[i].Va.name,"VA-Type":1,"VA-Location":1,"VA-ID":1,"Device-Name":1,"Device-Type":1,"Device-Location":1,"Device-Manufacturer":1,"Device-ID":1,"Device-ConnectedVA":1}'
     self.convertToJson(VaCommands)

    def addWakeup(self,command,vaType):
        if(vaType.lower()=="alexa"):
            st=command
            st='Alexa, '+ st
            return st
        elif(vaType.lower()=="google home"):
            st=command
            st='Hey Google, '+ st
            return st
    def convertToJson(self, VaCommands):
       vaList=[]
       deviceList=[]
       for i in range(0,len(VaCommands)):
           if(VaCommands[i].Va not in vaList):
               vaList.append(VaCommands[i].Va)
           if(VaCommands[i].device not in deviceList):
               deviceList.append(VaCommands[i].device)


       vaJson={"VA":None}
       tempDictVA={}
       for i in range(0,len(vaList)):

        jsonstr1 = json.dumps(vaList[i].__dict__)
        y = json.loads(jsonstr1)
        idJson = {"id":vaList[i].id}
        y.update(idJson)

        tempDictVA[y['name']]=y

       vaJson["VA"]=tempDictVA
       print(vaJson,"json")
       print(deviceList)
       deviceJson={"Smart Home Device":None}
       tempDictDevice={}
       for i in range(0,len(deviceList)):

        tempDeviceJson={"Device-Name":deviceList[i].name,"Device-Type":type(deviceList[i]).__name__,"Device-Location":deviceList[i].location,"Device-Manufacturer":deviceList[i].manufacturer,"Device-ID":deviceList[i].id,"Device-ConnectedVA":deviceList[i].connectedVA.id}
        y1=json.dumps(tempDeviceJson)
        y1 =json.loads(y1)

        tempDictDevice[y1["Device-Name"]]=y1
        print(tempDictDevice,"dictdevice")
       deviceJson["Smart Home Device"]=tempDictDevice
       print(deviceJson,"json1")

       vcJson={"Voice Command":None}
       tempDictVC={}
       for i in range(0,len(VaCommands)):
           tempVCJson={"command":VaCommands[i].voiceCommand,"timestamp":VaCommands[i].timestamp,"device-id":VaCommands[i].device.id,"va-id":VaCommands[i].Va.id}
           y2=json.dumps(tempVCJson)
           y2 =json.loads(y2)
           tempDictVC[i]=y2
       vcJson["Voice Command"]=tempDictVC
       print(vcJson,"json2")
       json_object_va = json.dumps(vaJson,indent = 4)
       json_object_device = json.dumps(deviceJson,indent = 4)
       json_object_vc = json.dumps(vcJson,indent = 4)
       with open("va.json", "w") as outfile:
        outfile.write(json_object_va)
       with open("devices.json", "w") as outfile:
           outfile.write(json_object_device)
       with open("vc.json", "w") as outfile:
           outfile.write(json_object_vc)
       #print(y1,"json1")










class googleDevices():
    pass

class amazonAlexa():
    pass

class voiceCommands():
    def __init__(self, voiceCommand,timestamp, device, Va):
        self.voiceCommand=voiceCommand
        self.timestamp=timestamp
        self.Va=Va
        self.device=device







class cc():
    def __init__(self, timestamp):
        self.timestamp=timestamp
    def convertStr(self,methodsDict):
        dict={}
        for i in methodsDict:
            key=i
            if('function' in key):

                key=key.split(" ")[1]
                print("KEY",key)
            dict.__setitem__(key,methodsDict[i])
        print("DICT",dict)
        return dict
    def list(self, methodsDict,nGenCommands,nDoneCommands):
        print("list111",self, methodsDict)
        #print(methodsDict,"3")
        methodsDict=self.convertStr(methodsDict)
        while (nDoneCommands<nGenCommands):
         k=0
         for i in methodsDict:

          if(nDoneCommands>=nGenCommands):
              break
            #print(i,"4")
          try:
            if(methodsDict[i]!=None):
                print("methods11", methodsDict, self.timestamp.ts[k])
                class_method = getattr(type(self), i)
                class_method(self,methodsDict[i])

                commandTS.append(self.timestamp.ts[k])
                deviceList.append(self)

                #self.i(methodsDict[i])
            else:
                class_method = getattr(type(self), i)
                print("methods112", methodsDict, self.timestamp.ts[k])
                class_method(self)
                commandTS.append(self.timestamp.ts[k])
                deviceList.append(self)
            nDoneCommands=nDoneCommands+1
            k=k+1
          except AttributeError as e:
              print(e)

class skills(cc):
    def __init__(self,name,timestamp):
        self.name=name
        self.timestamp=timestamp
    def skillOpen(self):
        commands.append("Open "+ self.name)

class smartDevice(cc):
    counter=0
    def __init__(self, name,state, location, connectedVA, manufacturer, probability, timestamp,id):
        self.name=name
        self.state=state
        self.location=location
        self.connectedVA=connectedVA
        self.manufacturer=manufacturer
        self.probability=probability
        self.timestamp=timestamp
        self.id=smartDevice.counter
        smartDevice.counter=smartDevice.counter+1


class light(smartDevice):
    def __init__(self, name, location, connectedVA, manufacturer="default", probability=0):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of light instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of light instance")



        except Exception as e:
            print(e)
            sys.exit(1)
        else:
            timestamp1=timestamp(0,0,0,0,0,0)
            smartDevice.__init__(self,name, 0, location, connectedVA,manufacturer,probability,timestamp1,0)



    #### list (methods of light1) handling

    def switchOn(self):

        commands.append("Turn on the lights in the "+ self.location)

    def switchOff(self):

        commands.append("Turn off the lights in the "+ self.location)


        #print(commands)

    def brighten(self,*args):
        if(len(args)==0):
            commands.append("Brighten the lights in the "+self.location +" to "+ str(random.randrange(0,100,5)))
        try:
         if(len(args)==1):
            if(type(args[0]) is int):
             commands.append("Brighten the lights in the "+self.location +" to "+ str(args[0]))
            else:
                raise ValueError("Wrong data type. Integer value is required for brighten method. Ignoring this method call")
        except ValueError as ve:
            print(ve)


    def dim(self,*args):
       #print("is it heres")
       # print(len(args))
       if(len(args)==0):
            commands.append("Dim the lights in the "+self.location +" to "+ str(random.randrange(0,100,5)))



       try:
           if(len(args)==1):
               if(type(args[0]) is int):
                   commands.append("Dim the lights in the "+self.location +" to "+ str(args[0]))
               else:
                   raise ValueError("Wrong data type. Integer value is required for dim method. Ignoring this method call")
       except ValueError as ve:
           print(ve)

    def color(self,*args):
        colors=["Red", "Pink", "Orange","Yellow","Green","Blue","Purple","White","Warmer","Cooler"]
        if(len(args)==0):
            commands.append("Turn my "+self.location +" lights "+ str(random.choice(colors)))


        try:
            if(len(args)==1):
                if(type(args[0]) is str):
                    commands.append("Turn my "+self.location +" lights "+ str(args[0]))
                else:
                    raise ValueError("Wrong data type. String value is required for color method. Ignoring this method call")
        except ValueError as ve:
          print(ve)

    def callAll(self,nGenCommands,nDoneCommands):
       while (nDoneCommands<nGenCommands):
        if(nDoneCommands<nGenCommands):
         self.switchOn()
         nDoneCommands=nDoneCommands+1

         commandTS.append(self.timestamp.ts[0])
         deviceList.append(self)
        if(nDoneCommands<nGenCommands):
         self.switchOff()
         nDoneCommands=nDoneCommands+1
         commandTS.append(self.timestamp.ts[0])
         deviceList.append(self)
        if(nDoneCommands<nGenCommands):
         self.brighten()
         nDoneCommands=nDoneCommands+1
         commandTS.append(self.timestamp.ts[0])
         deviceList.append(self)
        if(nDoneCommands<nGenCommands):
         self.dim()
         nDoneCommands=nDoneCommands+1
         commandTS.append(self.timestamp.ts[0])
         deviceList.append(self)
        if(nDoneCommands<nGenCommands):
         self.color()
         nDoneCommands=nDoneCommands+1
         commandTS.append(self.timestamp.ts[0])
         deviceList.append(self)

class thermostat(smartDevice):
    def __init__(self, connectedVA, location="default", manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of thermostat instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of thermostat instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)

    def switchOn(self):
        print("this")
        commands.append("Turn on the thermostat")

    def switchOff(self):

        commands.append("Turn off the thermostat")
        #print(commands)

    def setTemp(self,*args):
        if(len(args)==0):
            commands.append("set the thermostat" +" to "+ str(random.randrange(50,90,1)))
        try:
            if(len(args)==1):
                if(type(args[0]) is int):
                    if(args[0]  in range(50,90)):
                     commands.append("set the thermostat" +" to "+ str(args[0]))
                    else:
                        raise ValueError("Incorrect paramter for set method. Temperature should in range 50-90")

                else:
                    raise ValueError("Wrong data type. Integer value is required for set method. Ignoring this method call")
        except ValueError as ve:
            print(ve)


    def increase(self,*args):
        # print("is it heres")
        # print(len(args))
        if(len(args)==0):
            commands.append("Increase the thermostat by "+ str(random.randrange(1,20,1)))

        try:
            if(len(args)==1):
                if(type(args[0]) is int):
                    commands.append("Increase the thermostat " + "by "+ str(args[0]))
                else:
                    raise ValueError("Wrong data type. Integer value is required for increase method. Ignoring this method call")
        except ValueError as ve:
            print(ve)
    def decrease(self,*args):
        # print("is it heres")
        # print(len(args))
        if(len(args)==0):
            commands.append("Decrease the thermostat by "+ str(random.randrange(1,20,1)))

        try:
            if(len(args)==1):
                if(type(args[0]) is int):
                    commands.append("Decrease the thermostat " + "by "+ str(args[0]))
                else:
                    raise ValueError("Wrong data type. Integer value is required for decrease method. Ignoring this method call")
        except ValueError as ve:
            print(ve)

    def currentTemp(self):
        commands.append("What is the current temperature")


    def callAll(self):
        self.switchOn()
        self.switchOff()
        self.setTemp()
        self.increase()
        self.decrease()
        self.currentTemp()

class television(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)

    def switchOn(self):

        commands.append("Turn on the television in the "+ self.location)

    def switchOff(self):

        commands.append("Turn off the television in the "+ self.location)

    def volUp(self,*args):
        if(len(args)==0):
            commands.append("Increase the volume of television in the" + self.location)
    def volDown(self,*args):
        if(len(args)==0):
            commands.append("Decrease the volume of television in the" + self.location)
    def setVolume(self,*args):

        if(len(args)==0):
            commands.append("set the volume of television in the" + self.location+ "to"+ str(random.randrange(1,100,1)))

        try:
            if(len(args)==1):
                if(type(args[0]) is int):
                    commands.append("Decrease the thermostat " + "by "+ str(args[0]))
                else:
                    raise ValueError("Wrong data type. Integer value is required for setVolume method. Ignoring this method call")
        except ValueError as ve:
            print(ve)

    def mute(self):
        commands.append("Mute the television in" + self.location)
    def unmute(self):
        commands.append("Unmute the television in" + self.location)
    def play(self):
        commands.append("Play the television in" + self.location)
    def pause(self):
        commands.append("Pause the television in" + self.location)
    def changeInput(self,*args):
        inputs=["HDMI 1","HDMI 2","HDMI 3","HDMI 4","Cable"]
        if(len(args)==0):
            commands.append("Set the input of the television in" + self.location+ "to"+ str(random.choice(inputs)))

        try:
            if(len(args)==1):
                if(type(args[0]) is str):
                    commands.append("Set the input of the television in" + self.location+ "to"+ str(args[0]))
                else:
                    raise ValueError("Wrong data type. String value is required for changeInput method. Ignoring this method call")
        except ValueError as ve:
            print(ve)
    def openApp(self,*args):
        inputs=["Youtube","Netflix","Prime Video"]
        if(len(args)==0):
            commands.append("Open"+ str(random.choice(inputs)) +"on television in"+ self.location)

        try:
            if(len(args)==1):
                if(type(args[0]) is str):
                    commands.append("Open"+ str(args[0]) +"on television in"+ self.location)
                else:
                    raise ValueError("Wrong data type. String value is required for openApp method. Ignoring this method call")
        except ValueError as ve:
            print(ve)
    def callAll(self):
        self.volUp()
        self.volDown()
        self.setVolume()
        self.mute()
        self.unmute()
        self.changeInput()
        self.openApp()
        self.play()
        self.pause()

class smartLock(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)
    def lock(self):
        commands.append("Lock the" + self.location+" lock")
    def unlock(self):
        commands.append("Unlock the" + self.location+" lock")
    def status(self):
        commands.append("Get the status of " + self.location+" lock")
    def callAll(self):
        self.lock()
        self.unlock()
        self.status()

class fan(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)
    def setSpeed(self,*args):

        if(len(args)==0):
            commands.append("set the fan speed in the" + self.location+ "to"+ str(random.randrange(1,10,1)))

        try:
            if(len(args)==1):
                if(type(args[0]) is int):
                    commands.append("set the fan speed in the" + self.location+ "to"+ str(args[0]))
                else:
                    raise ValueError("Wrong data type. Integer value is required for setSpeed method. Ignoring this method call")
        except ValueError as ve:
            print(ve)
    def incSpeed(self,*args):
        if(len(args)==0):
            commands.append("Increase the fan speed in the" + self.location)
    def decSpeed(self,*args):
        if(len(args)==0):
            commands.append("Decrease the fan speed in the" + self.location)
    def callAll(self):
        self.setSpeed()
        self.incSpeed()
        self.decSpeed()

class airPurifier(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)

    def setMode(self,*args):
        inputs=["Auto","Whisper","Speed 1","Speed 2","Speed 3","Turbo"]
        if(len(args)==0):
            commands.append("Set the mode of air purifier in "+self.location + "to" + str(random.choice(inputs)))

        try:
            if(len(args)==1):
                if(type(args[0]) is str):
                    commands.append("Set the mode of air purifier in "+self.location + "to" + str(args[0]))
                else:
                    raise ValueError("Wrong data type. String value is required for setMode method. Ignoring this method call")
        except ValueError as ve:
            print(ve)
    def setTimer(self,*args):

        if(len(args)==0):
            commands.append("set a timer for" + str(random.randrange(1,10,1)) +"minutes in air purifier at"+ self.location)

        try:
            if(len(args)==1):
                if(type(args[0]) is int):
                    commands.append("set a timer for" + str(args[0]) +"minutes in air purifier at"+ self.location)
                else:
                    raise ValueError("Wrong data type. Integer value is required for setTimer method. Ignoring this method call")
        except ValueError as ve:
            print(ve)
    def nightModeOn(self):
        commands.append("Switch on the night mode of air purifier in"+self.location)
    def nightModeOff(self):
        commands.append("Switch off the night mode of air purifier in"+self.location)
    def uvOn(self):
        commands.append("Switch on the UV mode of air purifier in"+self.location)
    def uvOff(self):
        commands.append("Switch off the UV mode of air purifier in"+self.location)
    def callAll(self):
        self.setMode()
        self.setTimer()
        self.nightModeOn()
        self.nightModeOff()
        self.uvOn()
        self.uvOff()

class smartCamera(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)

    def answer(self):
            commands.append("Answer the" + self.location+ "camera")
    def show(self):
            commands.append("Show the" + self.location+ "camera")
    def hide(self):
            commands.append("Hide the" + self.location+ "camera")
    def callAll(self):
        self.answer()
        self.show()
        self.hide()

class vacuumCleaner(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)

    def pause(self):
        commands.append("Pause the vacuum cleaner in "+ self.location)
    def resume(self):
        commands.append("Resume the vacuum cleaner in "+ self.location)
    def returnBase(self):
        commands.append("Make my vacuum cleaner in"+ self.location +"to return to base")
    def status(self):
        commands.append("what is the status of my vacuum cleaner in" +self.location)
    def schedule(self,*args):
        inputs=["Living Room", "Kitchen", "Bedroom", "Dining Room", "Balcony"]
        if(len(args)==0):
            commands.append("Schedule a vacuum in" + str(random.choice(inputs)) + "at" + str(random.randrange(1,23,1)) + "hrs")

        try:
            if(len(args)==2):
                if(type(args[0]) is int and type(args[1]) is str):
                    commands.append("Schedule a vacuum in" + str(args[1]) + "at" + str(args[0]) + "hrs")
                else:
                    raise ValueError("Wrong data type. Integer and String value is required for schedule method. Ignoring this method call")
        except ValueError as ve:
            print(ve)

    def callAll(self):
       self.pause()
       self.resume()
       self.returnBase()
       self.status()
       self.schedule()

class washingMachine(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)

    def pause(self):
        commands.append("Pause the washing machine in "+ self.location)
    def resume(self):
        commands.append("Resume the washing machine in "+ self.location)
    def status(self):
        commands.append("what is the status of my washine machine in " +self.location)
    def setSpin(self):
        commands.append("Set the washing machine in "+self.location + "to spin")
    def setTemp(self,*args):
        inputs=["hot","cold","mild"]
        if(len(args)==0):
            commands.append("Set the wash temperature of washing machine in "+self.location+" to"+ str(andom.choice(inputs)))

        try:
            if(len(args)==1):
                if(type(args[0]) is str):
                    commands.append("Set the wash temperature of washing machine in "+self.location+" to"+ str(args[0]))
                else:
                    raise ValueError("Wrong data type. String value is required for setTemp method. Ignoring this method call")
        except ValueError as ve:
            print(ve)

    def callAll(self):
        self.status()
        self.pause()
        self.resume()
        self.setTemp()
        self.setTemp()

class refrigerators(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)

    def checkTemp(self):
        commands.append("what is the temperature of refrigerator in "+ self.location)
    def doorStatus(self):
        commands.append("What is the door status of the refrigerator in"+ self.location)
    def setTemp(self,*args):

        if(len(args)==0):
            commands.append("Set the temperature of refrigerator in "+self.location +" to "+ str(random.randrange(-10,25,1)))

        try:
            if(len(args)==1):
                if(type(args[0]) is int):
                    commands.append("Set the temperature of refrigerator in "+self.location +" to "+ str(args[0]))
                else:
                    raise ValueError("Wrong data type. Integer value is required for setTemp method. Ignoring this method call")
        except ValueError as ve:
            print(ve)

    def callAll(self):
        self.setTemp()
        self.checkTemp()
        self.doorStatus()

class microwave(smartDevice):
    def __init__(self, connectedVA, location, manufacturer="a"):
        try:
            if(type(location) is not str):
                raise Exception("Incorrect type. String value is required for location attribute of television instance")
            elif(type(connectedVA) is not va):
                raise Exception("Incorrect type. Object of type VA is required for connectedVA attribute of television instance")

        except Exception as e:
            print(e)
            sys.exit(1)
        else:

            smartDevice.__init__(self, 0, location, connectedVA,manufacturer)

    def pause(self):
        commands.append("Pause the microwave oven in"+ self.location)
    def resume(self):
        commands.append("Resume the microwave oven in"+ self.location)
    def addTime(self,*args):

        if(len(args)==0):
            commands.append("Add"+ str(random.randrange(1,60,1)) + " minutes to microwave in "+ self.location)

        try:
            if(len(args)==1):
                if(type(args[0]) is int):
                    commands.append("Add"+ str(args[0]) + " minutes to microwave in "+ self.location)
                else:
                    raise ValueError("Wrong data type. Integer value is required for addTime method. Ignoring this method call")
        except ValueError as ve:
            print(ve)

    def callAll(self):
        self.setTemp()
        self.checkTemp()
        self.doorStatus()

classList=[light,thermostat,television,smartLock,fan,airPurifier,smartCamera]





