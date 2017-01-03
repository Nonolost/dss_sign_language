# This file contains the three methods that will allow to go from numerical data to symbolic data

# The home made function take into argument a file with numerical data and will convert it into symbolic data in an output file
# In this version, we will take values 3 by 3 and if these values varied outside of a defined threshold, we apply the I (incrementation), D (decrementation).
# If not, we label it C (Constant)
def home_made(input_file, output_file, gap, nb):
	dict_values = from_file_to_dict(input_file)

	new_dict_values = dict()

	for key, values in dict_values.items():
		new_dict_values[key] = []
		last = []
		for idx, value in enumerate(values):
			last.append(value)
			if len(last) == nb:
				diff = last[nb-1]-last[0]
				if abs(diff) < gap:
					new_dict_values[key].append('C')
				elif diff > 0:
					new_dict_values[key].append('I')
				else:
					new_dict_values[key].append('D')

				del last[:]

	from_dict_to_file(output_file, new_dict_values)

# Follozwing SAX method
def sax(input_file, output_file, height):
	dict_values = from_file_to_dict(input_file)

	gap = 2/height
	letters = ['A','B','C','D','E','F','G','H','I','J','K']

	for key, values in dict_values.items():
		for idx, value in enumerate(values):
			dict_values[key][idx] = letters[int((value+1)/gap)]

	from_dict_to_file(output_file, dict_values)

# Following set based method
def set_based(input_file, output_file, height, width):
	dict_values = from_file_to_dict(input_file)

	height_gap = 2/height
	width_gap = 30/width
	letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R']

	for key, values in dict_values.items():
		for idx, value in enumerate(values):
			dict_values[key][idx] = letters[int(idx/width_gap)*width + int((value+1)/height_gap)]

	from_dict_to_file(output_file, dict_values)

# This function take into argument a file, will read its content and transfer data into a dictionnary
def from_file_to_dict(input_file):
	file = open(input_file)

	dict_values = dict()

	for i in range(0,8):
		dict_values[i] = list()

	for line in file:
		s = line.split(" ")
		for idx, a in enumerate(s):
			if idx != 0 and idx<9:
				try:
					dict_values[idx-1].append(float(a))
				except ValueError:
					pass
	file.close

	return dict_values
# This function take into argument a dictionnary and will write its content into a file
def from_dict_to_file(output_file, values):
	file = open(output_file, 'w')

	for i in range(0,len(values[0])):
		line = ""
		for key, value in values.items():
			line += str(value[i]) + " "
		file.write(str(i) + " " + line + "\n")

	file.close

set_based("data/girl_10.dat", "data/test_set.dat", 4, 3)
home_made("data/girl_10.dat", "data/test_hm.dat", 0.2, 3)
sax("data/girl_10.dat", "data/test_sax.dat", 4)