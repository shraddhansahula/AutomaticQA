import re

file = open("/home/shraddhan/Honors/Dataset_NCERT/Dataset-txt/iess301.txt")
sentences = file.read()
file.close()
sentences = re.split(r'(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s', sentences)
for i, s in enumerate(sentences):
	s = s.replace("\n", " ")
	sentences[i] = s
print sentences