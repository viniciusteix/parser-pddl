predicates = {}

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
				for k in range(0,count_pred):
					temp_pred.append(name_type)
				name_type_pred = False
				count_pred = 0
				continue
			if pred and line[j][0] == '?':
				count_pred = count_pred + 1
				continue



	

domain_file = 'fond-pddl-problems/doors/domain.pddl'
problem_file = 'fond-pddl-problems/doors/p01.pddl'
parser_file = 'fond-pddl-problems/doors/parser_p01.txt'

readDomain(domain_file)
for i in predicates:
	print(i,': ',predicates[i])