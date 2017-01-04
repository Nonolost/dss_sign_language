import sys

#def write_dic(d,filename_out):
#    file = open(filename_out,'w')
#    for i in range(4,11):
#        file.write(str(i)+ " " + str(d[i])+"\n")
#    file.close
   
def read_seq8(d,filename_in):
    file = open(filename_in)
	seq = []
	i = 0
    for line in file:
        s_line = line.split()
		symbol = ""
        for j in s_line:
			symbol += s_line[j]
		seq[i] = symbol
		++i
    file.close
	return seq
	
def read_seq1(d,filename_in):
    file = open(filename_in)
	seq8 = {}
	i = 0
    for line in file:
        s_line = line.split()
        for j in s_line:
			seq[i][j] = s_line[j]
		++i
    file.close
	return seq8
	
def counting(seq,words_grams,word,n_max):
	words_grams[word] = {}
	for i in range(0,n_max):
		words_grams[word][i] = {}
		words_grams[word][i]["nombre"] = 0
		for j in range(0,len(seq)-i):
			gram = ""
			for k in range(0,k):
				gram += seq[j+k]
			if gram in words_grams[word][i]:
				words_grams[word][i][gram] += 1
			else:
				words_grams[word][i][gram] = 1
			words_grams[word][i]["nombre"] +=1
			
def evaluate_word(seq_grams,seq_prefx,words_grams,word,n):
	if i = 1:
		return
	else:
		P = 1
		for i in range(0,len(seq_grams)):
			if (seq_grams[i] in words_grams[word][n]):
				if (seq_prefx[i] in words_grams[word)[n-1]):
					Ps = words_grams[word][n][seq_grams[i]]
					Pp = words_grams[word][n-1][seq_prefx[i]]
				else:
					Pp = 1/words_grams[word][n-1]["nombre"]
			else:
				Ps = 1/words_grams[word][n]["nombre"]
			Pg = Ps/Pp
			P *= Pg
		return P

def evaluating(seq,words_grams,n):
	seq_grams = []
	seq_prefx = []
	for i in range(0,len(seq)-n):
		seq_grams[i] = ""
		seq_prefx[i] = ""
		for j in range(0,n):
			seq_grams[i] += seq[i+j]
			if j != n-1:
				seq_prefx[i] += seq[i+j]
	maxP = 0
	bestW = ""
	for word in words_grams:
		P = evaluate_word(seq_grams,seq_prefx,words_grams,word,n)
		if P > maxP :
			maxP = P
			bestW = word
	return bestW
	
def voting(seq8,words_grams,n):
	words_returned = {}
	for i in range(0,8):
		seq = seq8[i]
		w = evaluating(seq,words_grams,n)
		if w in words_returned:
			words_returned[w] += 1
		else:
			words_returned[w] = 1
	maxC = 0
	bestW = ""
	for word in words_returned:
		if words_returned[word]>maxC:
			maxC = words_returned[word]
			bestW = word
	return bestW
		
		