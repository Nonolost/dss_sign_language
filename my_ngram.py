import random
import os
random.seed()

def from_file_to_list(input_file):
	"""
	This function take a file in argument and will write its content into a dictionnart to easy the data management

	input_file: name of the file to read the data from
	"""
	file = open(input_file)

	dict_values = ["" for k in range(8)]

	for line in file:
		s = line.split(" ")
		s.pop(0) # first column only indicate line's number
		s.remove('\n')
		for idx, a in enumerate(s):
			dict_values[idx] += a


	file.close

	return dict_values

def create_cross_list(protocol):
	filenames = os.listdir("data/" + protocol)
	cross_list = {k: [] for k in range(10)}

	nbParMot = 20
	for i in range(0,10):
		nbApres = 0
		nbAvant = 0
		for j in range(0,10):
			nbApres += nbParMot-1

			pos_word1 = random.randint(nbAvant,nbApres)
			cross_list[i].append((filenames[pos_word1].split("_")[0], filenames.pop(pos_word1)))
			nbApres -= 1
			pos_word2 = random.randint(nbAvant,nbApres)
			cross_list[i].append((filenames[pos_word2].split("_")[0], filenames.pop(pos_word2)))

			nbAvant = nbApres

		nbParMot -= 2

	return cross_list

words = ["come","girl","man","maybe","mine","name","read","right","science","thank"]

def initialize_grams():
	grams = {k: {l: {} for l in words} for k in range(8)}
	return grams

def compting_grams(list_word_file, grams, nb_grams):
	for word, file in list_word_file:
		word_sequences = from_file_to_list("data/sax/" + file)

		for seq_number, sequence in enumerate(word_sequences):
			for i in range(1, nb_grams+1):
				grams[seq_number][word][i] = {}

				for j in range(0, len(sequence)-i+1):
					gram = ""
					for k in range(0, i):
						gram += sequence[j + k]

					if gram not in grams[seq_number][word][i]:
						grams[seq_number][word][i][gram] = 0
					grams[seq_number][word][i][gram] += 1

					if "total" not in grams[seq_number][word][i]:
						grams[seq_number][word][i]["total"] = 0
					grams[seq_number][word][i]["total"] += 1

	return grams

def evaluate_word(sequence_grams, grams, word, n_gram, sequence_number):
	p = 1
	for gram, all_prefix in sequence_grams.items():
		if gram in grams[sequence_number][word][n_gram]:
			p *= grams[sequence_number][word][n_gram][gram]/grams[sequence_number][word][n_gram-1][gram[:-1]]
		else:
			p *= 1/grams[sequence_number][word][n_gram-1]["total"]

		for prefix in all_prefix:
			if prefix in grams[sequence_number][word][len(prefix)]:
				p *= grams[sequence_number][word][len(prefix)][prefix]/grams[sequence_number][word][len(prefix)-1][prefix[:-1]]
			else:
				p *= 1/grams[sequence_number][word][len(prefix)-1]["total"]

	return p

def evaluate_sequence(sequence_number, sequence, grams, n_gram):
	sequence_grams = {}

	for j in range(0, len(sequence)-n_gram+1):
		prefix = []
		gram = ""
		for k in range(0, n_gram):
			gram += sequence[j + k]
			if k < n_gram - 1 and k and j==0:
				prefix.append(gram)

		sequence_grams[gram] = prefix

	print(sequence_grams)
	guessed_word = None
	max_probability = 0

	for word in grams[sequence_number]:
		p = evaluate_word(sequence_grams, grams, word, n_gram, sequence_number)

		if p > max_probability:
			max_probability = p
			guessed_word = word

	return guessed_word

def voting(filename, grams, n_grams):
	word_sequences = from_file_to_list("data/sax/" + filename)

	words_guessed = {}

	for sequence_number in range(0,8):
		sequence = word_sequences[sequence_number]

		guessed_word = evaluate_sequence(sequence_number, sequence, grams, n_grams)
		if guessed_word not in words_guessed:
			words_guessed[guessed_word] = 0

		words_guessed[guessed_word] += 1

	guessed_word = None
	max_guess = 0
	for word in words_guessed:
		if words_guessed[word] > max_guess:
			max_guess = words_guessed[word]
			guessed_word = word

	return guessed_word


def execution_with_vote(protocol, n_gram):
	"""protocol : nom du DOSSIER dans data où y'a la bonne donnée"""
	cpt_res = 0 # TMP

	cross_list = create_cross_list(protocol)

	results = {k: {} for k in range(10)}

	for i in range(0,10):
		print(i, "th cross-validation")
		grams = initialize_grams()

		for j in range(0,10):
			if j != i:
				grams = compting_grams(cross_list[j], grams, n_gram)

		results[i] = {k: {} for k in range(20)}
		for j in range(0, 20):
			word, filename = cross_list[i][j]

			results[i][j]["original"] = word

			best_guess = voting(filename, grams, n_gram) # TODO

			results[i][j]["result"] = best_guess

			if word == best_guess:
				cpt_res+=1

	return cpt_res

#print(create_cross_list("sax"))
print(execution_with_vote("sax", 15)/200*100)
#print(execution_with_vote("sax", 29)[0]["girl"][29])