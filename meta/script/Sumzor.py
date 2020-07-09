########################
#
# Authour: Daniel Laden
# 	@:	   dthomasladen@gmail.com
#
########################

########################
# Libraries used
from nltk.corpus import stopwords 
from nltk.tokenize import sent_tokenize, word_tokenize 

# sw contains the list of stopwords 
sw = stopwords.words('english')  


#the plan is to use word simularity between abstract and intro/results/conclusion

#We need full texts and stuff in an easier 

# /Libraries used
########################

########################
# Function Declaration

def load_file(file):
	f = open(file, 'r')

	text = ""
	for line in f:
		line = line.replace("\n", " ")
		text = text + line

	return text

# X: Abstract sentence		Y: Full sentence
def cosine_simulator(X, Y): #Using simple cosine simularity to compare abstract sentences to sentences in the full text
	# tokenization 
	X_list = word_tokenize(X)  
	Y_list = word_tokenize(Y) 
	  
	l1 =[];l2 =[] 
	  
	# remove stop words from string 
	X_set = {w for w in X_list if not w in sw}  
	Y_set = {w for w in Y_list if not w in sw} 
	  
	# form a set containing keywords of both strings  
	rvector = X_set.union(Y_set)  
	for w in rvector: 
	    if w in X_set: l1.append(1) # create a vector 
	    else: l1.append(0) 
	    if w in Y_set: l2.append(1) 
	    else: l2.append(0) 
	c = 0
	  
	# cosine formula  
	for i in range(len(rvector)): 
	        c+= l1[i]*l2[i] 
	cosine = c / float((sum(l1)*sum(l2))**0.5) 
	#print("similarity: ", cosine) 

	return cosine

#X: Is the sentence being parsed in from the introduction/conclusions/results 	
#Y: Is the abstract sentences being put in to iterated through
#section: this is where the location of the sentence occurs
def most_related_sentence(X, Y, section):
	maxV = 0
	overall_max = 0
	best_sent = []
	overall_best_sent = []

	for y in Y:
		n = cosine_simulator(X, y)
		if n > maxV:
			maxV = n
			best_sent = [X, y]

	if maxV > overall_max:
		overall_max = maxV
		overall_best_sent =  best_sent

	return [overall_max, overall_best_sent, section]

#This function goes through and deletes the section header in each part returns a String
def clean_section(section):
	section = section.split("\n")
	while "section:\t" in section[0]:
		section = section[1:]
	full_section = ""
	for paragraph in section:
		full_section = full_section + paragraph

	return full_section
	

# /Function Declaration
########################

#these have been made based on survey responses on important sections
# ignored_sections = ["materials and methods", "author contributions", "acknowledgments", "supplementary material"]
# listening_sections =["introduction", "results", "conclusion", "discussion"]
listening_sections =["introduction", "results", "conclusion", "discussion", "materials and methods", "author contributions", "acknowledgments", "supplementary material"]

f = open("text-cleanup-humanities.txt", "r")

full_text = ""
for line in f:
	full_text = full_text + line

full_text = full_text.split("\n\n\n")
#print(full_text[0])
# print(len(full_text))

listener = True #Flipping between listening to sections or not
abstract = False

full_text_cleaned = []
sent_abstract = ""
holder = "" #holding text inside subsections
holder_header = ""

for section in full_text:
	full_header = section.split("\n")
	full_header = full_header[0]
	full_header = full_header.split("\t")
	header = full_header[1].replace("\n", "")
	num_of_sections = section.split("section:\t")
	#print(header)
	if "abstract" in section and not abstract:
		abstract = True
		sent_abstract = clean_section(section)
	elif listener:
		if len(num_of_sections) > 2: #This detects that there is a nested section aka a subsection triggering the listener
			listener = False
			holder = holder + clean_section(section)
			holder_header = header
		else:
			full_text_cleaned.append([header, clean_section(section)])
	elif not listener:
		if any(word in listening_sections for word in full_header):
			# print("in")
			full_text_cleaned.append([holder_header, holder])
			holder = ""
			if len(num_of_sections) > 2: #This if if there is another nested section right after a nested section
				listener = False
				holder = holder + clean_section(section)
				holder_header = header
			else:
				full_text_cleaned.append([header, clean_section(section)])
				listener = True
		else: #if we're still in the subsections this keeps adding to the holder
			# print("out") 
			holder = holder + clean_section(section)

if not sent_abstract:
	print("No Abstract Error, terminating program")
	quit()


sent_abstract = sent_tokenize(sent_abstract)

sent_introduction = ""
sent_results = ""
sent_conclusion = ""

extra_text = ""

for text in full_text_cleaned:
	if "introduction" in text[0]:
		sent_introduction = sent_tokenize(text[1])
	elif "results" in text[0]:
		sent_results = sent_tokenize(text[1])
	elif "conclusion" in text[0] or "discussion" in text[0]:
		sent_conclusion = sent_tokenize(text[1])
	else:
		extra_text = extra_text+text[1]+"\n"
		continue


if not sent_introduction or not sent_results or not sent_conclusion:
	if not sent_results:
		sent_results = sent_tokenize(extra_text)
	else:
		print("Critical Paper Parts Missing, terminating program")
		quit()






### NOTES ###
# Word Embeddings like GloVE? cosine simularity by
# itself?


##############
# Cosine Simularity

overall_top_sent = []

# most_related_sentence(X, Y, Section) sections numbers are as follows Introduction:1, Results:2, Conclusions:3

########### Introduction ###########

top_sent = []
for intro in sent_introduction:
	top_sent.append(most_related_sentence(intro, sent_abstract, 1))

top_sent.sort(key = lambda x: x[0])
top_sent.reverse()
top_sent = top_sent[:3]
print(top_sent)
overall_top_sent = overall_top_sent + top_sent

########### Results ###########

top_sent = []
for results in sent_results:
	top_sent.append(most_related_sentence(results, sent_abstract, 2))

top_sent.sort(key = lambda x: x[0])
top_sent.reverse()
top_sent = top_sent[:3]
print(top_sent)
overall_top_sent = overall_top_sent + top_sent

########### Conclusion ###########

top_sent = []
for conclusion in sent_conclusion:
	top_sent.append(most_related_sentence(conclusion, sent_abstract, 3))

top_sent.sort(key = lambda x: x[0])
top_sent.reverse()
top_sent = top_sent[:3]
print(top_sent)
overall_top_sent = overall_top_sent + top_sent

#to get the highest similarity
overall_top_sent.sort(key = lambda x: x[0])
overall_top_sent.reverse()
overall_top_sent = overall_top_sent[:5]
#then to sort by where they occur
overall_top_sent.sort(key = lambda x: x[2])
overall_top_sent.reverse()


f = open("top-sentence-humanities.txt", 'w')
for top in overall_top_sent:
		sent = top[1]
		if len(sent[0]) > len(sent[1]):
			print(sent[0])
			sent = sent[0]
		else:
			print(sent[1])
			sent = sent[1]

		f.write("similarity:\t"+str(top[0])+"\n"+sent+"\n\n\n")
		print("similarity: ", top[0])

f.close()

quit()

##################################

# /Cosine Simularity
######################

######################
# Code Resources
# https://www.geeksforgeeks.org/python-measure-similarity-between-two-sentences-using-cosine-similarity/
# https://pythonspot.com/tokenizing-words-and-sentences-with-nltk/
# https://medium.com/analytics-vidhya/basics-of-using-pre-trained-glove-vectors-in-python-d38905f356db
# https://stackoverflow.com/questions/3121979/how-to-sort-a-list-tuple-of-lists-tuples-by-the-element-at-a-given-index
# https://stackoverflow.com/a/3271485
#
######################
