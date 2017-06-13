from requests import get
import urllib.request
from tkinter import *
from PIL import Image, ImageTk
from os import remove

def removeSpaces(string):
	return ''.join(x for x in string if x is not " ")

def removeApostrophes(string):
	return ''.join(x for x in string if x is not "\'")

#edit the string such that all characters EXCEPT THE FIRST are lowercase
def headCase(string):
	return removeApostrophes(string[0] + string[1:].lower())

window = Tk()
window.title("Free Champion Rotation")
w, h = window.winfo_screenwidth(), window.winfo_screenheight()
header = Label(window, text = "Here are this week's free champions.", font = ("Helvetica", 20)).grid(row = 0, column = 0, columnspan = 10)

key = #INSERT YOUR OWN API KEY HERE

freeChampList = get("https://na.api.riotgames.com/api/lol/NA/v1.2/champion?freeToPlay=true&api_key="+key).json()["champions"]#list, not dict
allChampsDict = get("https://global.api.riotgames.com/api/lol/static-data/NA/v1.2/champion?api_key="+key).json()["data"]

i=0
photoArr = []
dbNames = []

for eachChamp in freeChampList:
	champID = eachChamp["id"]

	for n, info in allChampsDict.items():
		if info["id"] == champID:
			champInfo = info
			break

	dbName = champInfo["name"]

	if "\'" in dbName or dbName == "LeBlanc": #triggers for void champs khazix, chogath, and velkoz, as well as that troublemaker LB
		dbName = headCase(dbName)
		if dbName == "Kogmaw":
			dbName = "KogMaw"     #yay inconsistency
		elif dbName == "Reksai":
			dbName = "RekSai"
	
	if " " in dbName:
		dbName = removeSpaces(dbName) #triggers for champs with spaces in their names like Twisted Fate, Miss Fortune, Tahm Kench, etc
		if dbName == "Dr.Mundo":
			dbName = "DrMundo"	
	
	elif dbName == "Wukong":
		dbName = "MonkeyKing" #why

	try:
		urllib.request.urlretrieve("http://ddragon.leagueoflegends.com/cdn/img/champion/loading/"+dbName+"_0.jpg", dbName+".jpg")
	except urllib.error.HTTPError:
		print("Image retrieval failed on " + dbName + ".")
		exit()

	dbNames.append(dbName)	
	
	urllib.request.urlretrieve("http://ddragon.leagueoflegends.com/cdn/img/champion/loading/"+dbName+"_0.jpg", dbName+".jpg")
	img = Image.open(dbName+".jpg").resize((154, 280))#(int(w/10 + 10), 400)
	photo = ImageTk.PhotoImage(img)
	photoArr.append(photo)
	
	rowLength = int(len(freeChampList)/2)

	if i - rowLength < 0: #top row
		Label(window, width = 14, wraplength = 90, text = champInfo["name"]+", "+champInfo["title"], font = ("Helvetica", 10)).grid(row = 1, column = i)
		Label(window, width = 154, image = photo).grid(row = 2, column = i)
	else:
		Label(window, width = 14, wraplength = 90, text = champInfo["name"]+", "+champInfo["title"], font = ("Helvetica", 10)).grid(row = 3, column = i-rowLength)
		Label(window, width = 154, image = photo).grid(row = 4, column = i-rowLength)
	i+=1
	
window.mainloop()
for i in dbNames:
	remove(i+".jpg")