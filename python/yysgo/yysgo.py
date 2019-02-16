import order
import sys
import time
import random

if __name__ == '__main__':
	# python yysgo.py user_name what_to_do times code
	# user_name: same with the picture name in ./usr, the screen shot of your name in game
	# what_to_do: the dungeon, use the first letter of pinyin, eg:gsh - gui shi hei
	# times: how many times you want to play
	# code: a number in range of 0 - 7, (XXX)B
	#	the first bit : whether you want to accpet the invatation
	#	the second bit: willing to be the room owner?
	#	the last bit: is there any special activities make the button move to the other place?
	# 
	# for example:
	# ~/yysgo > python yysgo.py smm ekn 100 5
	# this means : use ./smm.png to locate the screen, 
	#				play er kou nv dungeon 100 times, 
	#				accept it when someone invite me, 1
	#				if the room owner leave the room make me become a new one, i will leave also,0
	#				there exist some special activities, the button is not at the origin position.1
	count = int(sys.argv[3])
	auto_function = sys.argv[2]
	user_name = sys.argv[1]
	offset = int(sys.argv[4])

	invitation_op = (offset & 4) >> 2
	roomowner_op = (offset & 2) >> 1
	special_activities = offset & 1

	if auto_function == 'gsh':
		order.guishihei(count, invitation_op, roomowner_op, user_name, special_activities)
	if auto_function == 'ekn':
		order.erkounv(count, invitation_op, roomowner_op, user_name, special_activities)