import random
import sys

random.seed()

def print_dic(d):
	for i in d:
		print(str(i) + " : " + str(d[i]))
	print("\n")


#def write_dic(d,filename_out):
#    file = open(filename_out,'w')
#    for i in range(4,11):
#        file.write(str(i)+ " " + str(d[i])+"\n")
#    file.close
   
def read_seq8(filename_in):
	file = open(filename_in)
	seq = []
	i = 0
	for line in file:
		s_line = line.split()
		symbol = ""
		for j in range(1,9):
			symbol += s_line[j]
		seq[i] = symbol
		i += 1
	file.close
	return seq
	
def read_seq1(filename_in):
	file = open(filename_in)
	seq8 = {}
	for i in range(0,8):
		seq8[i] = {}
	j = 0
	for line in file:
		s_line = line.split()
		i = 0
		for k in range(1,9):
			seq8[i][j] = s_line[k]
			i += 1
		j += 1
	file.close
	return seq8
	
def counting8(seq,words_grams,word,n_max):
	for i in range(0,n_max):
		for j in range(0,len(seq)-i+1):
			gram = ""
			for k in range(0,i):
				gram += seq[j+k]
			if gram in words_grams[word][i]:
				words_grams[word][i][gram] += 1
			else:
				words_grams[word][i][gram] = 1
			words_grams[word][i]["nombre"] +=1
			
def counting1(seq,words_grams,word,n_max,param):
	for i in range(0,n_max):
		for j in range(0,len(seq)-i+1):
			gram = ""
			for k in range(0,i):
				gram += seq[j+k]
			if gram in words_grams[param][word][i]:
				words_grams[param][word][i][gram] += 1
			else:
				words_grams[param][word][i][gram] = 1
			words_grams[param][word][i]["nombre"] +=1

			
def evaluate_word8(seq_grams,seq_prefx,words_grams,word,n):
	if i == 1:
		return
	else:
		P = 1
		for i in range(0,len(seq_grams)):
			if (seq_grams[i] in words_grams[word][n]):
				if (seq_prefx[i] in words_grams[word][n-1]):
					Ps = words_grams[word][n][seq_grams[i]]
					Pp = words_grams[word][n-1][seq_prefx[i]]
					Pg = Ps/Pp
				else:
					Pg = 1/words_grams[word][n-1]["nombre"]
			else:
				Pg = 1/words_grams[word][n]["nombre"]
			P *= Pg
		return P

def evaluate_word1(seq_grams,seq_prefx,words_grams,word,n,param):
	if n == 1:
		return
	else:
		if seq_grams[0] in words_grams[param][word][1]:
			P = words_grams[param][word][1][seq_grams[0]]
		else:
			P = 1/(words_grams[param][word][1]["nombre"])
		Pp = 1
		Ps = 0
		Pg = 0
		for i in range(1,len(seq_grams)):
			#print(str(i) + " " +seq_grams[i])
			l = len(seq_grams[i])
			if (seq_grams[i] in words_grams[param][word][l]):
				Ps = words_grams[param][word][l][seq_grams[i]]+1
				Pp = words_grams[param][word][l-1][seq_prefx[i]]+10
				Pg = Ps/Pp
			else:
				if (seq_prefx[i] in words_grams[param][word][l-1]):
					Pg = 1/(words_grams[param][word][l-1][seq_prefx[i]]+10)
				else:
					Pg = 1/(words_grams[param][word][l-1]["nombre"]+10)
			P *= Pg
		return P

def evaluating8(seq,words_grams,n):
	seq_grams = []
	seq_prefx = []
	for i in range(0,len(seq)-n+1):
		seq_grams.append("")
		seq_prefx.append("")
		for j in range(0,n):
			seq_grams[i] += seq[i+j]
			if j != n-1:
				seq_prefx[i] += seq[i+j]
	maxP = 0
	bestW = ""
	for word in words_grams:
		P = evaluate_word8(seq_grams,seq_prefx,words_grams,word,n)
		if P > maxP :
			maxP = P
			bestW = word
	return bestW

		
def evaluating1(seq,words_grams,n,param):
	seq_grams = []
	seq_prefx = []
	gram = seq[0]
	prefx = ""
	seq_grams.append(gram)
	seq_prefx.append(prefx)
	i=0
	for i in range(1,n-1):
		gram += seq[i]
		prefx += seq[i-1]
		#print(str(i) + " " +gram + " " + prefx)
		seq_grams.append(gram)
		seq_prefx.append(prefx)
	for k in range(0,len(seq)-n+1):
		seq_grams.append("")
		seq_prefx.append("")
		for j in range(0,n):
			seq_grams[k+i+1] += seq[k+j]
			if j != n-1:
				seq_prefx[k+i+1] += seq[k+j]
	maxP = 0
	bestW = ""
	for word in words_grams[0]:
		P = evaluate_word1(seq_grams,seq_prefx,words_grams,word,n,param)
		#print(str(P)+" "+word)
		if P > maxP :
			maxP = P
			bestW = word
	#print(bestW)
	#print(str(maxP))
	return bestW
	
def voting(seq8,words_grams,n):
	words_returned = {}
	for i in range(0,8):
		seq = seq8[i]
		w = evaluating1(seq,words_grams,n,i)
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
		elif words_returned[word]==maxC:
			bestW = "eq " + bestW + " " + word
	return bestW
		
def reset_grams8(words,n):
	words_grams8	= {}
	for word in words:
		words_grams8[word] = {}
		for i in range(0,n+1):
			words_grams8[word][i] = {}
			words_grams8[word][i]["nombre"] = 0
	return words_grams8
		
def reset_grams(words,n):
	words_grams	= {}
	for j in range(0,8):
		words_grams[j] = {}
		for word in words:
			words_grams[j][word] = {}
			for i in range(0,n+1):
				words_grams[j][word][i] = {}
				words_grams[j][word][i]["nombre"] = 0
	return words_grams

def create_filenames(words,protocol,k):
	filenames = []
	filename_in = ""
	for word in words:
		for i in range(1,21):
			if protocol == "sax":
				filename_in = "sax/" + word + "_" + str(i) + "_" + "sax" + "_" + k + ".dat"
			if protocol == "hm":
				filename_in = "hm/"+ word + "_" + str(i) + "_" + "hm" + "_" + k + ".dat"
			if protocol == "set_based":
				filename_in = "set_based/" + word + "_" + str(i) + "_" + "set_based" + "_" + k + ".dat"
			filenames.append((filename_in,word))
			filename_in = ""
	return filenames
	
def exe(words,k,n,protocol):
	filenames = create_filenames(words,protocol,k)
	cross_list = {}
	for i in range(0,10):
		cross_list[i] = []
		for j in range(0,20):
			pos = random.randrange(200 - i*20 - j)
			(file,word) = filenames.pop(pos)
			cross_list[i].append((file,word))
	words_grams	= {}
	filenames = create_filenames(words,protocol,k)
	words_grams = reset_grams(words,n)
	results = {}
	for i in range(0,10):
		results[i] = {}
		for j in range(0,200):
			if filenames[j] not in cross_list[i]:
				(filename,word) = filenames[j]
				seq8 = read_seq1(filename)
				for l in range(0,8):
					counting1(seq8[l],words_grams,word,n+1,l)
		for j in range(0,20):
			results[i][j] = {}
			(filename,word)= cross_list[i][j]
			results[i][j]["original"] = word
			seq8 = read_seq1(filename)
			for l in range(0,8):
				bestW = evaluating1(seq8[l],words_grams,n,l)
				results[i][j][l] = bestW			
		reset_grams(words,n)
	return results
	

	
def exe_vote(words,k,n,protocol):
	filenames = create_filenames(words,protocol,k)
	cross_list = {}
	for i in range(0,10):
		cross_list[i] = []
		for j in range(0,20):
			pos = random.randrange(200 - i*20 - j)
			(file,word) = filenames.pop(pos)
			cross_list[i].append((file,word))
	words_grams	= {}
	filenames = create_filenames(words,protocol,k)
	words_grams = reset_grams(words,n)
	results = {}
	for i in range(0,10):
		results[i] = {}
		for j in range(0,200):
			if filenames[j] not in cross_list[i]:
				(filename,word) = filenames[j]
				seq8 = read_seq1(filename)
				for l in range(0,8):
					counting1(seq8[l],words_grams,word,n+1,l)
#		print(words_grams[1]["girl"][27])
		for j in range(0,20):
			results[i][j]= {}
			(filename,word)= cross_list[i][j]
			results[i][j]["original"] = word
			seq8 = read_seq1(filename)
			bestW = voting(seq8,words_grams,n)
			results[i][j]["resultat"] = bestW			
		words_grams = reset_grams(words,n)
	return results
	
words = ["come","girl","man","maybe","mine","name","read","right","science","thank"]
		
		
#res = exe_vote(words,"0",2,"sax")

def print_votes(res):
	for i in range(0,10):
		print ("beginning of cross test " + str(i))
		for j in range(0,20):
			print ("\n" + res[i][j]["original"])
			print (str(res[i][j]["resultat"]))
		
def print_results(res):
	for i in range(0,10):
		print ("beginning of cross test " + str(i))
		for j in range(0,20):
			print ("\norigine: "+ res[i][j]["original"]+ " ::::::: ", end="")
			for l in range(0,8):
				print (str(res[i][j][l]) + " - ", end="")
				
def compute_success(res):
	total = 200
	good = 0
	bad = 0
	for i in range(0,10):
		for j in range(0,20):
			if res[i][j]["original"] == res[i][j]["resultat"]:
				good += 1
			else :
				bad +=1
	return (good/total)*100
	
def compute_success_rates(words,k,protocol):
	success_rate = {}
	for i in range (2,21):
		success = compute_success(exe_vote(words,k,i,protocol))
		success_rate[i] = success
	print_dic(success_rate)
	return success_rate
	
	
	
	
def find_best_param(words,n,protocol,numb_param):
	results = {}
	for i in range(1,numb_param+1):
		results[i] = exe(words,str(i),n,protocol)		
	res = {}
	for i in range(0,8):
		bestP = -1
		bestG = 0
		bestB = 0
		for j in range(1,numb_param+1):
			good = 0
			bad = 0
			for ii in range(0,10):
				for jj in range(0,20):
					if results[j][ii][jj]["original"] == results[j][ii][jj][i]:
						good += 1
					else:
						bad += 1
			if 	good > bestG:
				bestP = j
				bestG = good
				bestB = bad
		res[i] = (bestP,bestG,bestB)
	return res

	
	
def create_confusion_matrix(words,results):
	cm = {}
	for wordi in words:
		cm[wordi] = {}
		for wordj in words:
			cm[wordi][wordj] = 0
	for i in range(0,10):
		for j in range(0,20):
			cm[results[i][j]["original"]][results[i][j]["resultat"]] += 1
	return cm
	
	
def print_cm(words,cm):
	first_line = "     "
	for word in words:
		first_line += word +  " "
	print(first_line)
	for wordi in words:
		line = word
		for wordj in words:
			line += "  " + cm[wordi][wordj] +"  "
		print(line)

			
res = exe_vote(words,"2",29,"sax")
#print_votes(res)
#print_votes(res)
print(compute_success(res))

#print_dic(find_best_param(words,10,"sax",9))
#print_dic(find_best_param(words,15,"hm",7))

#res = exe_vote(words,"1",10,"hm")
#print(compute_success(res))
#cm = create_confusion_matrix(words,res)
#print_cm(words,cm)


#compute_success_rates(words,"0","sax")
#compute_success_rates(words,"0","hm")