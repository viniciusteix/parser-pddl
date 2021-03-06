predicates = {}
objects = {}

state_initial = []
state_goal = []
list_predicates = []
final_predicates = []
list_actions = []

types_objects = set()
conj_predicates = set()

def readDomain(domain_file):
	file_object = open(domain_file,'r')
	count_par = 0
	pred = False

	temp_pred = []
	name_pred = ''
	count_pred = 0

	action = False
	name_action = ''
	list_param = []
	param = False
	type_param = False
	pre = []
	pos = []

	for i in file_object.readlines():
		line = i.split()
		n = len(line)
		name_type_pred = False

		for j in range(0,n):
			if line[j] == '(':
				if pred and count_par == 2:
					name_pred = line[j+1]
				count_par = count_par + 1
				continue
			if line[j] == ')':
				if action and count_par == 2:
					action = False
					action_ = []
					action_.append(name_action)
					action_.append(list_param)
					action_.append(pre)
					action_.append(pos)
					list_actions.append(action_)
					name_action = ''
					list_param = []
				if param:
					param = False
				if pred and count_par == 2:
					pred = False
				if pred and count_par == 3:
					predicates[name_pred] = temp_pred
					temp_pred = []
				count_par = count_par - 1
				continue
			if line[j] == ':predicates':
				pred = True
				continue
			if line[j] == ':action':
				action = True
				name_action = line[j+1]
				continue
			if line[j] == ':parameters':
				param = True
				continue
			if pred and line[j] == '-':
				name_type_pred = True
				continue
			if param and line[j] == '-':
				type_param = True
				continue
			if name_type_pred:
				name_type = line[j]
				types_objects.add(name_type)
				for k in range(0,count_pred):
					temp_pred.append(name_type)
				name_type_pred = False
				count_pred = 0
				continue
			if type_param:
				name_type_param = line[j]
				list_param.append(name_type_param)
				type_param = False
				continue
			if pred and line[j][0] == '?':
				count_pred = count_pred + 1
				continue

def readProblem(problem_file):
	file_object = open(problem_file,'r')
	count_par = 0
	obj = False

	temp_obj = []
	name_obj = ''
	count_obj = 0

	initial = False
	prop_initial = ''

	goal = False
	prop_goal = ''

	for i in file_object.readlines():
		line = i.split()
		n = len(line)
		name_type_obj = False

		for j in range(0,n):
			if line[j] == '(':
				count_par = count_par + 1
				continue
			if line[j] == ')':
				count_par = count_par - 1
				if count_par == 1 and obj:
					obj = False
				if count_par == 1 and initial:
					initial = False
				if count_par == 1 and goal:
					goal = False
				if initial and count_par == 2:
					prop_initial = prop_initial[1:]
					state_initial.append(prop_initial)
					prop_initial = ''
				if goal and count_par == 2:
					prop_goal = prop_goal[1:]
					state_goal.append(prop_goal)
					prop_goal = ''
				continue
			if line[j] == ':objects':
				obj = True
				continue
			if line[j] == ':init':
				initial = True
				continue
			if line[j] == ':goal':
				goal = True
				continue
			if obj and line[j] == '-':
				name_type_obj = True
				continue
			if name_type_obj:
				name_type = line[j]
				for k in temp_obj:
					objects[name_type].append(k)
				name_type_obj = False
				temp_obj = []
				continue
			if obj:
				temp_obj.append(line[j])
				continue
			if initial:
				prop_initial = prop_initial + '_' + line[j]
				continue
			if goal:
				prop_goal = prop_goal + '_' + line[j]
				continue

def initializeConjPredicates():
	aux = []
	for i in predicates:
		temp = []
		temp.append(i)
		for j in predicates[i]:
			temp.append(j)
		list_predicates.append(temp)

def calculateConjPredicates():
	for i in objects:
		for j in objects[i]:
			new_conj = []
			for k in list_predicates:
				one = k
				new_one = []
				for l in one:
					if l == i:
						new_one.append(j)
					else:
						new_one.append(l)
				new_conj.append(new_one)
			for k in new_conj:
				list_predicates.append(k)

def conjToSetPredicates():
	for i in list_predicates:
		temp = i[0]
		flag = True
		for j in range(1,len(i)):
			if i[j] in objects:
				flag = False
				continue
			temp = temp + '_' + i[j]
		if flag:
			conj_predicates.add(temp)

	aux = list(conj_predicates)
	aux.sort()
	for i in aux:
		final_predicates.append(i)


def initializeTypes():
	for i in types_objects:
		objects[i] = []

def writePredicates(parser_file):
	file = open(parser_file,'w')
	file.write('<predicates>\n')
	n = len(final_predicates)-1
	for i in range(0,n):
		temp = final_predicates[i] + ','
		file.write(temp)
	temp = final_predicates[n] + '\n'
	file.write(temp)
	file.write('<\\predicates>\n')

def writeStateInitial(parser_file):
	file = open(parser_file,'a+')
	file.write('<initial>\n')
	n = len(state_initial)-1
	for i in range(0,n):
		temp = state_initial[i] + ','
		file.write(temp)
	temp = state_initial[n] + '\n'
	file.write(temp)
	file.write('<\\initial>\n')

def writeStateGoal(parser_file):
	file = open(parser_file,'a+')
	file.write('<goal>\n')
	n = len(state_goal)-1
	for i in range(0,n):
		temp = state_goal[i] + ','
		file.write(temp)
	temp = state_goal[n] + '\n'
	file.write(temp)
	file.write('<\\goal>\n')

def writeActions(parser_file):
	file = open(parser_file,'a+')
	file.write('<actionsSet>\n')
	for i in list_actions:
		file.write('<action>\n')

		file.write('<\\action>\n')
	file.write('<\\actionsSet>\n')

domain_file = 'fond-pddl-problems/doors/domain.pddl'
problem_file = 'fond-pddl-problems/doors/p01.pddl'
parser_file = 'fond-pddl-problems/doors/parser_p01.txt'


readDomain(domain_file)
initializeTypes()
readProblem(problem_file)
initializeConjPredicates()
calculateConjPredicates()
conjToSetPredicates()
writePredicates(parser_file)
writeStateInitial(parser_file)
writeStateGoal(parser_file)
writeActions(parser_file)
print(list_actions)
print()
print()
print(objects)

# print(state_initial)
# print(state_goal)
# for i in final_predicates:
# 	print(i)