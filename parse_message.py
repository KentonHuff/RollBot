import random

def roll(mult, die):
	total = 0
	str_result = ''
	for x in range(0, mult):
		rollVal = random.randint(1, die)
		total += rollVal
		str_result += 'd' + str(die) + ': ' + str(rollVal)+'\n'
	return str_result, total


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
	
	output, roll_total = roll(multiplier, die)
	if isNegative:
		return -1 * roll_total
	else:
		return output, roll_total
	

def execute(active):
	active = active.replace(' ','')
	active = active.replace('-', '+-')
	array = active.split('+')
	array = [x for x in array if x != '']
	
	total = 0

	output = ''
	
	for index in range(0, len(array)):
		if 'd' in array[index]:
			roll_out, array[index] = parseRoll(array[index])
			output += roll_out
			
		total += int(array[index])
		
		
	return output+'Result: ' + str(total)

def parse_message(msg):
	return execute(msg)

#print(eval('min([1,2,3])'))
#print(str([1,2,3]))
