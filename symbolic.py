import os
import numpy as np
import sys
# This file contains the 4 methods that will allow to go from numerical data to symbolic data

# TODO : New parameter for sax : vary the distance between two horizontal separation in sax/set-based

index_to_attribute = {0:'x', 1:'y', 2:'z', 3:"palm roll", 4:"thumb", 5:"index", 6:"middle", 7:"ring"}

def home_made(input_file, output_file, gap):
	"""
	This "home made" function transform a numerical sequence into a symbolic one. For a value it takes both its previous and next value to calculate the variation
	If this result is greater than a gap defined in the parameters, it will label the value as either I (incrementation) or D (decrementation).
	If this result is lesser than the gap, then the valus is labeled C (constant)

	input_file: file from where the data is read
	output_file: file where the data is written
	gap: value of the gap to consider
	"""
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

def sax(input_file, output_file, height):
	"""
	This function is a simplified use of the SAX method to transform numerical data into symbolic one. 
	See http://cs.gmu.edu/~jessica/SAX_DAMI_preprint.pdf for details
	Right now all separation are equally distant

	input_file: file from where the data is read
	output_file: file where the data is written
	height: number of horizontal separation
	"""
	dict_values = from_file_to_dict(input_file)

	gap = 2/height
	letters = ['A','B','C','D','E','F','G','H','I','J','K']

	for key, values in dict_values.items():
		for idx, value in enumerate(values):
			dict_values[key][idx] = letters[int((value+1)/gap)]

	from_dict_to_file(output_file, dict_values)


def sax_derivate(input_file, output_file, height):
	"""
	This function is similar to the sax one, but here we use SAX on the derivate of the values (for a value, variance between the previous and next values)

	input_file: file from where the data is read
	output_file: file where the data is written
	height: number of horizontal separation
	"""
	dict_values = from_file_to_dict(input_file)

	letters = ['A','B','C','D','E','F','G','H','I','J','K']

	new_dict_values = dict()

	for i in range(0,8):
		new_dict_values[i] = list()

	for key, values in dict_values.items():
		der = []
		if key == 3:
			print(values)
		for idx, value in enumerate(values):
			if idx != 1 and idx != len(values)-1:
				der.append(values[idx+1]-values[idx-1])
		
		if key == 3:
			print(der)
		gap = (max(der)-min(der))/height

		for idx, v in enumerate(der):
			if gap==0: # that's when there is not variation = we don't care about the letter so let's just put a A
				new_dict_values[key].append(letters[0])
			else:
				new_dict_values[key].append(letters[int((abs(min(der))+v)/gap)])

	from_dict_to_file(output_file, new_dict_values)


def set_based(input_file, output_file, height, width):
	"""
	This function is a simplified use of the Set-based method to transform numerical data into symbolic one. 
	See http://dl.acm.org/citation.cfm?id=2882963 for details
	Right now all 'set' have the same height and width

	input_file: file from where the data is read
	output_file: file where the data is written
	height: number of horizontal separation
	width: number of vertical separation
	"""
	dict_values = from_file_to_dict(input_file)

	height_gap = 2/height
	width_gap = 30/width
	letters = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y']

	for key, values in dict_values.items():
		for idx, value in enumerate(values):
			dict_values[key][idx] = letters[int(idx/width_gap)*width + int((value+1)/height_gap)]

	from_dict_to_file(output_file, dict_values)


def from_file_to_dict(input_file):
	"""
	This function take a file in argument and will write its content into a dictionnart to easy the data management

	input_file: name of the file to read the data from
	"""
	file = open(input_file)

	dict_values = {k: [] for k in range(8)}

	for line in file:
		s = line.split(" ")
		s.pop(0) # first column only indicate line's number
		s.remove('\n')
		for idx, a in enumerate(s):
			dict_values[idx].append(float(a))

	file.close

	return dict_values

def from_dict_to_file(output_file, dict_values):
	"""
	This function take a dictionnary of values in argument and will write its content into a file respecting the way the data files are constructed

	output_file: name of the file to write the data into
	dict_values: values to write in the file
	"""
	file = open(output_file, 'w')

	for i in range(0,len(dict_values[0])):
		line = ""

		for key, value in dict_values.items():
			line += str(value[i]) + " "
		file.write(str(i) + " " + line + "\n")

	file.close

if __name__ == "__main__":
	"""
	The script is used as follow : python symbolic.py [sax] [sax_der] [home] [set] depending of whichever kind of method you want to use
	"""
	if len(sys.argv) > 1:
		for file in os.listdir("data"):
			if file.endswith(".dat"):
				for i in range(1,6):
					if "sax" in sys.argv:
						sax("data/" + file, "data/sax/" + file.replace(".dat", "") + "_sax_" + str(i) + ".dat", i)
					if "sax_der" in sys.argv:
						sax_derivate("data/" + file, "data/sax_derivate/" + file.replace(".dat", "") + "_sax_derivate_" + str(i) + ".dat", i)

				if "home" in sys.argv:
					for i in np.arange(0.05,0.5,0.05):
						home_made("data/" + file,  "data/hm/" + file.replace(".dat", "") + "_hm_" + str(i) + ".dat", i)

				if "set" in sys.argv:
					for i in range(1,5):
						for j in range(1,5):
							set_based("data/" + file,  "data/set_based/" + file.replace(".dat", "") + "_setbased_" + str(i) + "_" + str(j) + ".dat", i, j)
	else:
		print("Too few arugments, enter at least one of those : python symbolic.py [sax] [sax_der] [home] [set]")
