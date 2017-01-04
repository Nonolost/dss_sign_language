import os
import numpy as np
# This file contains the three methods that will allow to go from numerical data to symbolic data

# TODO : lets make sax on derivate to get something looking like the home-made
# New parameter for sax : vary the distance between two horizontal separation in sax/set-based
# TODO : function that call every function with different parameters
# TODO : SAX pour les doigts faire avec le nb de valeurs différentes, pour x y z essayer de trouver des positions clés pour séparer là, et orientation main?



# The home made function take into argument a file with numerical data and will convert it into symbolic data in an output file
# In this version, we will take values 3 by 3 and if these values varied outside of a defined threshold, we apply the I (incrementation), D (decrementation).
# If not, we label it C (Constant)
def home_made(input_file, output_file, gap):
	dict_values = from_file_to_dict(input_file)

	new_dict_values = dict()

	for key, values in dict_values.items():
		new_dict_values[key] = []
		for idx, value in enumerate(values):
			if idx != 1 and idx != len(values)-1:
				diff = values[idx+1]-values[idx-1]
				if abs(diff) < gap:
					new_dict_values[key].append('C')
				elif diff > 0:
					new_dict_values[key].append('I')
				else:
					new_dict_values[key].append('D')


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
	letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']

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

if __name__ == "__main__":
    # Here we're going to generate all the data for sax, derivated sax, set-based and home-made for all our dataset and for different parameters

    # sax :	
	for file in os.listdir("data"):
		if file.endswith(".dat"):
			for i in range(1,6):
				sax("data/" + file, "data/sax/" + file.replace(".dat", "") + "_sax_" + str(i) + ".dat", i)

			for i in np.arange(0.05,0.5,0.05):
				home_made("data/" + file,  "data/hm/" + file.replace(".dat", "") + "_hm_" + str(i) + ".dat", i)

			for i in range(1,5):
				for j in range(1,5):
					set_based("data/" + file,  "data/set_based/" + file.replace(".dat", "") + "_setbased_" + str(i) + "_" + str(j) + ".dat", i, j)
