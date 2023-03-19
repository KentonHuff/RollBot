import random
import re

def roll(output_log, roll_type, multiplier, dice_type):
	if multiplier == 0:
		return output_log, '0'
	
	rolls = []
	for x in range(0, multiplier):
		rollVal = random.randint(1, dice_type)
		rolls.append(rollVal)
		output_log += 'd' + str(dice_type) + ': ' + str(rollVal)+'\n'
	
	if len(rolls) == 1:
		return output_log, str(rolls[0])
	
	char_to_agg_func = {
		'^':'max',
		's':'sum',
		'_':'min'
	}

	replacement = char_to_agg_func[roll_type]+'('+''.join(str(rolls).split())+')'

	return output_log, replacement

def parse_expression(output_log, expression):
	#[\+-]4
	expr_match = re.search(r'^[\+-]((\d+)|(\d+\.\d*)|(\d*\.\d+))$',expression)
	if expr_match:
		expression = 's1d20'+expression
		return parse_expression(output_log,expression)

	#[\^s_]3d12 Full definition
	expr_match = re.search(r'([\^s_])(\d+)d(\d*[1-9]\d*)',expression)
	if expr_match:
		output_log, replacement = roll(output_log,
				 					roll_type=expr_match.group(1),
				 					multiplier=int(expr_match.group(2)),
				 					dice_type=int(expr_match.group(3)))
		
		expression = expression[:expr_match.start()]+replacement+expression[expr_match.end():]
		return parse_expression(output_log,expression)


	#[\^s_]d12
	expr_match = re.search(r'([\^s_])d(\d*[1-9]\d*)',expression)
	if expr_match:
		char_to_num_dice = {
			'^':'2',
			's':'1',
			'_':'2'
		}
		expression = expression[:expr_match.start()]+expr_match.group(1)+char_to_num_dice[expr_match.group(1)]+'d'+expr_match.group(2)+expression[expr_match.end():]
		return parse_expression(output_log,expression)

	#[\^s_]
	expr_match = re.search(r'[\^_]|s(?!u)',expression)
	if expr_match:
		char_to_repl = {
			'^':'^2d20',
			's':'s1d20',
			'_':'_2d20'
		}
		expression = expression[:expr_match.start()]+char_to_repl[expr_match.group(0)]+expression[expr_match.end():]
		return parse_expression(output_log,expression)

	#3d10
	expr_match = re.search(r'\d+d\d*[1-9]\d*',expression)
	if expr_match:
		expression = expression[:expr_match.start()]+'s'+expr_match.group(0)+expression[expr_match.end():]
		return parse_expression(output_log,expression)
	
	#d4
	expr_match = re.search(r'd\d*[1-9]\d*',expression)
	if expr_match:
		expression = expression[:expr_match.start()]+'s1'+expr_match.group(0)+expression[expr_match.end():]
		return parse_expression(output_log,expression)



	return output_log, expression