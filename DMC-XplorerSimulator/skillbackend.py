import sys

#f = open(sys.argv[1], 'rw')

print("Devices to add:")
user_req = input()
while(user_req != "q"):

	f = open(sys.argv[1], 'a')
	text = f.write(user_req + "\n")
	#print(text)
	f.close()

	print("Devices to add:")
	user_req = input()