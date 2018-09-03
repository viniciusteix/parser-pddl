predicates = {}
objects = {}
types_objects = set()
list_predicates = []
conj_predicates = set()
final_predicates = []

def readDomain(domain_file):
	file_object = open(domain_file,'r')
	count_par = 0
	pred = False

	temp_pred = []
	name_pred = ''
	count_pred = 0

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
			if pred and line[j] == '-':
				name_type_pred = True
				continue
			if name_type_pred:
				name_type = line[j]
				types_objects.add(name_type)
				for k in range(0,count_pred):
					temp_pred.append(name_type)
				name_type_pred = False
				count_pred = 0
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
				continue
			if line[j] == ':objects':
				obj = True
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
# for i in final_predicates:
# 	print(i)