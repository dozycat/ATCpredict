cathID=open('GPCRFinal.txt.Gene3D.ID','r')
pfamID=open('GPCRFinal.txt.Pfam.ID','r')
for i in cathID:
	i=i.strip('\n\r').split(' ')[1]
	print i