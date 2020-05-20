# Data Read Script

import os
from enum import Enum

class chara:
	def __init__(self, name):
		self.name = name
		self.raw = [''] * 21
		self.format = [''] * 21


	  
	def __setitem__(self, index, value):
		self.raw[index] = value

class stats:
	def __init__(self, move):
		self.move_name = move
		self.start = 0
		self.end = 0
		self.total = 0
		self.iasa = 0
		self.ld_fl_spec = 0
		self.stun = 0
		self.percent = 0
		self.percent_weak = 0
		self.notes = ""

		self.auto_cancel_s = 0
		self.auto_cancel_e = 0
		self.land_lag = 0
		self.cancel_lag = 0

	def print(self):
		print("Move Name:", self.move_name)
		print("Start:", self.start)
		print("End:", self.end)
		print("Total Frames:", self.total)
		print("IASA", self.iasa)
		print("Land Fall Special:", self.ld_fl_spec)
		print("Shield Stun:", self.stun)
		print("Percent:", self.percent)
		print("Percent Weak:", self.percent_weak)
		print("Notes:", self.notes)
		print("Auto Cancel Start:", self.auto_cancel_s)
		print("Auto Cancel End:", self.auto_cancel_e)
		print("Landing Lag:", self.land_lag)
		print("L_Cancel_Lag:", self.cancel_lag)

    #char = db.Column(db.String(20))
    #move = db.Column(db.String(20))
    #start = db.Column(db.Integer())
    #end = db.Column(db.Integer())
    #total = db.Column(db.Integer())
    #iasa = db.Column(db.Integer())
    #ld_fl_spec = db.Column(db.Integer())
    #stun = db.Column(db.Integer())
    #percent = db.Column(db.Float())
    #percent_weak = db.Column(db.Float())
    #notes = db.Column(db.String(200))

    #auto_cancel_s = db.Column(db.Integer())
    #auto_cancel_e = db.Column(db.Integer())
    #land_lag = db.Column(db.Integer())   aerials only
    #cancel_lag = db.Column(db.Integer()) 

    # we have char, move
    # first line is total_frames
    # second line is IASA
    # thrid line is Auto Cancel Frames
    # fourth line is Landing Lag
    # fifth line is L-cancelled

all_raw_data = []

characters = ["bowser", "peach", "captain_falcon", "donkey_kong",
"dr._mario", "falco", "fox", "game_&_watch", "ganondorf", "jigglypuff",
"kirby", "link", "luigi", "mario", "marth", "mewtwo", 
"ness", "peach", "pichu", "pikachu", "roy", "samus", 
"sheik", "yoshi", "young_link", "zelda" ]

for i in characters:
	all_raw_data.append(chara(i))

moves = ("bair", "fair", "dair", "nair",
"uair", "fsmash_m", "dsmash",
"usmash", "dtilt", "ftilt_m", "utilt",
"dashattack", "jab1", "jab2", "jab3", 
"fthrow", "bthrow", "dthrow", "uthrow", 
"grab", "dashgrab")


for subdir, dirs, files in os.walk("frame_data"):
    for file in files:
        #print os.path.join(subdir, file)
        filepath = subdir + os.sep + file
        if filepath[:-4].endswith(moves):
        	start = filepath.find('/') 
        	end = filepath.find('/', 11)
        	curr_name = filepath[start+1:end]
        	curr_move = filepath[end+1:-4]
        	for x in all_raw_data:
        		if x.name == curr_name:
        			with open(filepath, 'r') as f:
        				data = f.read()
        			x[moves.index(curr_move)] = data
        				

#for j in range(len(characters)):
#	for i in range(21):
#		print(all_raw_data[j].raw[i])
        			
#print(all_raw_data[5].raw[3])

go_over = (">", " ", ",", "<")

terms = ["Total Frames", "IASA", "Auto-Cancel", "Landing Lag",
	"L-cancelled"]

data = []


items = all_raw_data[5].raw[2].splitlines()



for i in items:
	stat_name = ""
	for l in terms:
		if i.startswith(l):
			stat_name = l
	current = ""
	for j in i:				
		if j.isdigit():
			current += j
		elif j == ',' or j == '-':
			if current != "":
				current += '-'
	st = [stat_name, current]
	data.append(st)

cur_num = 0
for i in data:
	if i[0] == '' and i[1] != "":
		i[0] = cur_num
		cur_num += 1


hitboxes = []
length = data[len(data)-1][0] + 1
for i in range(len(data)):
	if data[i][0] == length / 3:
		index = i

hitbox = 1
row = 1
for i in range(index, len(data)):
	if data[i][0] == "":
		hitbox += 0.5
	elif row == 1:
		num = data[i][1].find('-')
		dmg = data[i][1][:num]
		row += 1
	elif row == 2:
		num = data[i][1].find('-')
		shield_stun = data[i][1][num+1:]
		for j in range(len(data)):
			if data[j][0] == hitbox - 1:
				rge = data[j][1]
				break
		bk = rge.find('-')
		start = rge[:bk]
		end = rge[bk+1:]
		hitboxes.append([int(hitbox), start, end, dmg,shield_stun])
		row = 1

for i in data:
	print(i)

for i in hitboxes:
	print(i)

temp = stats("temp move name")
temp.start = hitboxes[0][1]
temp.end = hitboxes[len(hitboxes)-1][2]
temp.total = data[0][1]
if data[1][1] != '':
	temp.iasa = data[1][1]

#ld_fl_spec

cur_max = 0
for i in hitboxes:
	if int(i[4]) > cur_max:
		cur_max = int(i[4])
temp.stun = cur_max
				
cur_max = 0
for i in hitboxes:
	if int(i[3]) > cur_max:
		cur_max = int(i[3])
temp.percent = cur_max

cur_min = 100
for i in hitboxes:
	if int(i[3]) < cur_min:
		cur_min = int(i[3])
temp.percent_weak = cur_min	

for i in data:
	
	if i[0] == "Auto-Cancel":
		bk = i[1].find('-')
		temp.auto_cancel_s = i[1][:bk]
		temp.auto_cancel_e = i[1][bk+1:]

	elif i[0] == "Landing Lag":
		temp.land_lag = i[1]

	elif i[0] == "L-cancelled":
		temp.cancel_lag = i[1]

	elif i[0] == '':
		break

temp.print()

		
#for i in range(5):
#	current = ''
#	for k in reversed(items[i]):
#		if k.isdigit(): 
#			current = k + current
#		elif k in go_over:
#			print(current)
#			current = ''
#		else:
#			break

#	print(current)
            