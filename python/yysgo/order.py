import pyautogui
import copy
import time
import random
import sys
import baseFunction

block_height_l1 = 128
block_height_l2 = 118

BASE = [542,350]

ACCEPT = [[1480,770], [1550,840]]
DECLINE = [[1480,960], [1550,1020]]
BACK = [[50,90], [95,140]]
START = [[1720,1090], [1990,1170]] # start as room omner

MATCH = [[1230,1140], [1510, 1220]]
PREPARE = [[2000,1000], [2100,1100]]
FINISH = [[500,800], [1800,1100]]

TEAM = [[420,1170], [500,1270]]

DEMON_SEAL = [[260,1060], [640,1150]]

GUI_SHI_HEI = [[720,780], [1000,830]]
ER_KOU_NV = [[740,990], [970, 1010]]


AREA = [
[], # da shen me   up///down
[[[700,340], [1030,460]], [[700,1095], [1030,975]]], # shen me yao qi  
]


PIC_READY = './pic/back.png'
PIC_FINISH = './pic/finished.png'
PIC_INVATATION = './pic/invite.png'
PIC_ROOMOWNER = './pic/roomowner.png'
PIC_IS_SEARCHING = './pic/searching.png'
USER_BASE = './usr/'



def get_start_symbol(user_name):
	st = USER_BASE + user_name + '.png'
	return st


def get_button(butt):
	ans = copy.deepcopy(butt)
	ans[0][0] = ans[0][0] + BASE[0]
	ans[1][0] = ans[1][0] + BASE[0]
	ans[0][1] = ans[0][1] + BASE[1]
	ans[1][1] = ans[1][1] + BASE[1]
	return ans


def guishihei(count, invitation_op, roomowner_op, user_name, activities=False):
	
	index = 0
	button_set = [get_button(ACCEPT), get_button(DECLINE), get_button(MATCH)]
	interupt = 0
	while(count - index > 0):

		# begin information
		print 'Gui Shi Hei' ########
		print '----------------------------'

		pyautogui.moveTo(1, 1, 0.3)
		print '\tSearching start signal:  '

		baseFunction.waiting(get_start_symbol(user_name), PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set)
		print '\tStart signal found, excute matching operating!'
		
		baseFunction.click(get_button(TEAM))
		time.sleep(1.5)

		if activities:
			baseFunction.roll(1, get_button(AREA[0]), block_height)

		baseFunction.click(get_button(DEMON_SEAL)) ##### below
		drag_area = [get_button(AREA[1][0]), get_button(AREA[1][1])] #####
		baseFunction.roll(8, drag_area, block_height_l2) #####
		baseFunction.click(get_button(GUI_SHI_HEI)) #####
		baseFunction.click(get_button(MATCH))
		pyautogui.moveTo(1, 1, 0.3)
		print '\tFinished, waiting the battle!'

		interupt = baseFunction.waiting(PIC_READY, PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set)
		if interupt == 1:
			if roomowner_op:
				baseFunction.click(get_button(START))
				pyautogui.moveTo(1, 1, 0.3)
				if baseFunction.waiting(PIC_ROOMOWNER, PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set) == 0:
					baseFunction.click(get_button(START))
					pyautogui.moveTo(1, 1, 0.3)
					baseFunction.waiting(PIC_READY, PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set)
			else:
				baseFunction.click(get_button(BACK))
				countinue
		print '\tBattle signal found, press prepare button!'

		baseFunction.click(get_button(PREPARE))
		pyautogui.moveTo(1, 1, 0.3)
		print '\tPrepared, waiting the finish signal'

		baseFunction.waiting(PIC_FINISH, PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set)
		baseFunction.click(get_button(FINISH))
		print '\tFinished'
		print '----------------------------'
		index = index + 1
		print 'Gui Shihei: ', index  #####
		print '\n\n'



def erkounv(count, invitation_op, roomowner_op, user_name, activities=False):
	
	index = 0
	button_set = [get_button(ACCEPT), get_button(DECLINE), get_button(MATCH)]
	interupt = 0
	while(count - index > 0):

		# begin information
		print 'Er Kou Nv' ########
		print '----------------------------'

		pyautogui.moveTo(1, 1, 0.3)
		print '\tSearching start signal:  '

		baseFunction.waiting(get_start_symbol(user_name), PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set)
		print '\tStart signal found, excute matching operating!'
		
		baseFunction.click(get_button(TEAM))
		time.sleep(1.5)

		if activities:
			baseFunction.roll(1, get_button(AREA[0]), block_height)

		baseFunction.click(get_button(DEMON_SEAL)) ##### below
		# drag_area = [get_button(AREA[1][0]), get_button(AREA[1][1])] #####
		# baseFunction.roll(8, drag_area, block_height_l2) #####
		baseFunction.click(get_button(ER_KOU_NV)) #####
		baseFunction.click(get_button(MATCH))
		pyautogui.moveTo(1, 1, 0.3)
		print '\tFinished, waiting the battle!'

		interupt = baseFunction.waiting(PIC_READY, PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set)
		if interupt == 1:
			if roomowner_op:
				baseFunction.click(get_button(START))
				pyautogui.moveTo(1, 1, 0.3)
				if baseFunction.waiting(PIC_ROOMOWNER, PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set) == 0:
					baseFunction.click(get_button(START))
					pyautogui.moveTo(1, 1, 0.3)
					baseFunction.waiting(PIC_READY, PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set)
			else:
				baseFunction.click(get_button(BACK))
				countinue
		print '\tBattle signal found, press prepare button!'

		baseFunction.click(get_button(PREPARE))
		pyautogui.moveTo(1, 1, 0.3)
		print '\tPrepared, waiting the finish signal'

		baseFunction.waiting(PIC_FINISH, PIC_INVATATION, invitation_op, PIC_ROOMOWNER, PIC_IS_SEARCHING, button_set)
		baseFunction.click(get_button(FINISH))
		print '\tFinished'
		print '----------------------------'
		index = index + 1
		print 'Er Kounv: ', index  #####
		print '\n\n'


