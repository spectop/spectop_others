# basement of the all supporter
# simulate hand to click and drag, eyes to observe game stage
import copy
import pyautogui
import random
import sys
import time


# call click() to simulate the click operation
# parameter:
# 	area: where should to be clicked, a random point in the give area will be clicked
#		(use a 2*2 list to record it)
#	delay: delay a while before start it
def click(area, delay=0.5):
	
	# delay a random time
	delay_time = random.uniform(0, delay)
	time.sleep(delay_time)

	# caculate the coordinate
	x = random.randint(area[0][0], area[1][0])
	y = random.randint(area[0][1], area[1][1])

	# use moveTo() instead of click directly, avoid anti-cheat
	pyautogui.moveTo(x, y, random.uniform(0,0.5))
	time.sleep(random.uniform(0,0.2))

	pyautogui.mouseDown()
	time.sleep(random.uniform(0,0.5))

	pyautogui.mouseUp()


# call drag() to simulate the drag operation
# parameter:
#	begin_area, end_area: a 2*2 list to tell the start and final position
#	delay: delay a while before start it
#	duraction: how much time it would be cost
def drag(begin_area, end_area, delay=0.5, duraction=0.5):
	
	# delay a random time
	delay_time = random.uniform(0, delay)
	time.sleep(delay_time)

	# caculate the coordinate
	x_begin = random.randint(min(begin_area[0][0], begin_area[1][0]), max(begin_area[0][0], begin_area[1][0]))
	y_begin = random.randint(min(begin_area[0][1], begin_area[1][1]), max(begin_area[0][1], begin_area[1][1]))

	x_end = random.randint(min(end_area[0][0], end_area[1][0]), max(end_area[0][0], end_area[1][0]))
	y_end = random.randint(min(end_area[0][1], end_area[1][1]), max(end_area[0][1], end_area[1][1]))

	# simulation
	pyautogui.moveTo(x_begin, y_begin, random.uniform(0,0.5))
	time.sleep(random.uniform(0,0.5))

	pyautogui.mouseDown()
	time.sleep(random.uniform(0,0.2))

	pyautogui.moveTo(x_end, y_end, random.uniform(0,duraction))
	time.sleep(random.uniform(0,0.2))

	pyautogui.mouseUp()


# call it to find if there exist the give picture on the screen
# parameter:
#	file_location: the Absolute address of the picture
# return:
#	the boolen result, true for found, false for not
#
# It is toooooo slow by this way, remember to upgrade!!!!
def find_picture(file_location):
	ans = pyautogui.locateOnScreen(file_location, grayscale=True)
	if ans != None :
		return True
	return False


#######################################################################
#######################################################################
#						More functions								  #
#######################################################################
#######################################################################


# call it to roll up and down some blocks
# sometimes there exist some activities occupy the first block
# parameter:
#	block_nums: negative number to move down and positive number to move up
#	area: which area is clickable
#	block_height: the height of one block
#	eps, delay, duraction: just what its name means
def roll(block_nums, area, block_height, eps=2, delay=0.5, duraction=0.5):

	# caculate the coordinate
	area_up = copy.deepcopy(area[0])
	area_down = copy.deepcopy(area[1])
	begin_area = copy.deepcopy(area_down)

	if block_nums < 0:
		begin_area = copy.deepcopy(area_up)
	
	end_area = copy.deepcopy(begin_area)
	end_area[0][1] = end_area[0][1] - block_height*block_nums + random.randint(0-eps, 0+eps)
	end_area[1][1] = end_area[1][1] - block_height*block_nums + random.randint(0-eps, 0+eps)

	# drag
	drag(begin_area, end_area, delay, duraction)


# call it to check invatations
# if invatations found, this function will click accept or decline button
# parameter:
#	operation: True for accept and False for decline
#	pic: The symbol of invatation
#	button_accept, button_decline: the position of the button
def check_invatation(operation, pic, button_accept, button_decline):
	
	ans = find_picture(pic)
	if ans :
		if operation :
			click(button_accept)
		else :
			click(button_decline)


# check if you are thhe room owner
def check_roomowner(pic):
	return find_picture(pic)


def check_searching(pic, button):
	ans = find_picture(pic)
	if not ans:
		click(button)



# waiting a symbol
def waiting(symbol, invatation_pic, invatation_operation, roomowner_pic, searching_pic, button_set):

	button_accept = copy.deepcopy(button_set[0])
	button_decline = copy.deepcopy(button_set[1])
	button_search = copy.deepcopy(button_set[2])

	index = 0
	room_status = False
	while(not find_picture(symbol)):
		index = index + 1
		if index % 10 == 0:
			check_invatation(invatation_operation, invatation_pic, button_accept, button_decline)
			room_status = check_roomowner(roomowner_pic)
		if index % 50 == 0:
			check_searching(searching_pic, button_search)
		if room_status:
			return 1
	return 0

