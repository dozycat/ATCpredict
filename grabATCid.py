#coding=utf-8
import re
fr=open('br08303.keg','r')
outfile=open('ATCid.txt','w')
p=[]
for st in fr:
	st=st.rstrip('\n')
	match=re.compile(r'[A-Z]{1}\d{2}[A-Z]{2}\d{2}').search(st)
	if match:
		#p.append(match.group())
		outfile.write(match.group()+'\n')
fr.close()
