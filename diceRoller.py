import random

def roll(mult, die):
	total = 0
	for x in range(0, mult):
		rollVal = random.randint(1, die)
		total += rollVal
		print('d' + str(die) + ': ' + str(rollVal))
	return total


def parseRoll(string):
	isNegative = False
	if string[0] == '-':
		string = string.replace('-','')
		isNegative = True
	
	multiplier = 1
	die = 1
	array = string.split('d')
	array = [x for x in array if x != '']
	if len(array) == 1:
		die = int(array[0])
	else:
		multiplier = int(array[0])
		die = int(array[1])
	
	result = roll(multiplier, die)
	if isNegative:
		return -1 * result
	else:
		return result
	

def execute(active):
	active = active.replace(' ','')
	active = active.replace('-', '+-')
	array = active.split('+')
	array = [x for x in array if x != '']
	
	total = 0
	
	for index in range(0, len(array)):
		if 'd' in array[index]:
			array[index] = parseRoll(array[index])
			
		total += int(array[index])
		
		
	return 'Result: ' + str(total)


inp = input('Roll: ')

while inp != 'quit':
	output = execute(inp)
	print(output)
	inp = input('Roll: ')