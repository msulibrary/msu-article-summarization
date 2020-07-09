########################
#
# Authour: Daniel Laden
# 	@:	   dthomasladen@gmail.com
#
########################

########################
# Libraries used

import re

# /Libraries used
########################

########################
# Function Declaration

#this function will be called anytime to extract text between p it returns [all occurrences found][1; the occurance]
def extract_paragraph_text(text):
	all_paragraphs = []
	paragraphs = text.split("<p>")
	for paragraph in paragraphs:
		p = paragraph.split("</p>")
		all_paragraphs.append(p[0])

	return all_paragraphs

#works as the fuction above but grabs the text between the abstract tag
def extract_abstract_text(full_text):
	
	abstract = full_text.split("<abstract>")
	abstract = abstract[1].split("</abstract>")
	abstract = abstract[0]

	abstract = extract_paragraph_text(abstract)
	abstract = abstract[1]

	#print(abstract)
	return abstract

#This function go through and divides the paper into invidual sections from the cerminexml
def extract_all_sections(full_text):
	all_sections = []

	section = re.split(r"<sec(.*)>", full_text) #since section areas have unique ids we need a re
	for sec in section:
		if "</sec>" in sec:
			local_section = sec.split("</sec>")
			all_sections.append(local_section[0])

	#print(abstract)
	return all_sections

#here we get all the paragraph text inside of a section and clean it up
def extract_paragraphs_in_section(section):
	raw_paragraphs = extract_paragraph_text(section)
	#print(len(raw_paragraphs))
	#print(raw_paragraphs)
	cleaned_section = "" #for all the cleaned paragraphs in a section
	section_title = ""
	i = 0
	for p in raw_paragraphs:
		i += 1
		cleaned_text = "" #for the cleaned text of the paragraph
		if "<xref" in p: #removing the reference links in the paragraph (unnecessary for the text mining)
			holder = p.replace("\n        ","")
			holder = holder.split("<xref")
			for t in holder:
				if "</xref>" in t:
					t = t.split("</xref>")
					t = t[1]
				cleaned_text = cleaned_text + t
			#print(cleaned_text)
		elif "<title" in p:
			#print(p)
			p = p.split(">")
			p = p[1].split("<")
			section_title = p[0].lower()
		else:
			cleaned_text = p
		cleaned_text = cleaned_text.replace("\n", " ") #this is to fix \n created by columns in papers
		cleaned_text = cleaned_text.replace("       ", " ")
		#print(cleaned_text)
		if not cleaned_section: #first paragraph so we don't add an extra \n at the start
			cleaned_section = cleaned_text
		else:
			cleaned_section = cleaned_section + "\n" + cleaned_text
	#print(cleaned_section)
	return([cleaned_section, section_title])

	



# /Function Declaration
########################

########################
# Main Code

f = open("test-cleanup-humanities.cermxml", 'r')

full_text = ""
for l in f:
	full_text = full_text+l

#print(full_text)

ab = extract_abstract_text(full_text)
#print(ab)

sections = extract_all_sections(full_text)
#print(len(sections))
cleaned_paper = []
for section in sections:
	cleaned_paper.append(extract_paragraphs_in_section(section))

#print(cleaned_paper)

f = open("text-cleanup-humanities.txt", 'w')
f.write("section:\tabstract\n")
f.write(ab+"\n\n\n")
stop = len(cleaned_paper)
i = 0
for section in cleaned_paper:
	i +=1
	f.write("section:\t"+section[1]+"\n")
	if not section[0]:
		#print(section[1])
		continue
	elif i < stop:
		f.write(section[0]+"\n\n\n")
	else:
		f.write(section[0])

f.close()


# /Main Code
########################


######################
# Code Resources
#
# https://note.nkmk.me/en/python-split-rsplit-splitlines-re/
# https://stackoverflow.com/questions/8703017/remove-sub-string-by-using-python/8703078
# https://stackoverflow.com/questions/1185524/how-do-i-trim-whitespace
# https://pythex.org/
######################