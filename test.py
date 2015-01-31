import numpy as np
import urllib,urllib2,cookielib,socket  
from bs4 import BeautifulSoup
import re
import sys


# def huoquSim_drug(a,b):
# 	return 1
# def huoquSim_ATC(c,d):
# 	return 1

# train=open('chemfingerprint_cath_pfam.csv','r')
# drugID=open('drugID.txt','r')
# ATCID=open('ATCID.txt','r')
# drugid='D00001'
# ATCid='A01AB02'
# trainfile=[]
# testfile=[]
# for st in train:
# 	st=st.strip('\n').split(',')
# 	a=[float(x) for x in st]
# 	trainfile.append(a)
# trainfile=np.array(trainfile)
# 	# tra=np.vstack(tra,b)
# sim_drug=[]
# sim_ATC=[]
# for st1 in drugID:
# 	st1=st1.strip('\n\r').split(' ')
# 	sim_drug.append(huoquSim_drug(drugid,st1))
# sim_drug=np.array(sim_drug)
# for st2 in ATCID:
# 	st2=st2.strip('\n\r').split(' ')
# 	sim_ATC.append(huoquSim_ATC(ATCid,st2))
# sim_ATC=np.array(sim_ATC)
# for i in range(trainfile.shape[0]):
# 	testfile.append(sim_drug[i]*sim_ATC[i])
# testfile=np.array(testfile)
def crawl(url):
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	webpage= urllib2.urlopen(req)
	html=webpage.read()
	soup= BeautifulSoup(html, "html.parser")
	div=soup.find(attrs={'class':'target well well-sm bonds'})
	anchor=div.findAll("a")
	res=[]
	for a in anchor:
		pattern = re.compile(r'^http://www.uniprot.org/uniprot/.*$')
		if pattern.match(a['href']):
			 res.append(a['href'])
	return res

def crawl2(url):
	req = urllib2.Request(url, headers={'User-Agent' : "Magic Browser"})
	webpage= urllib2.urlopen(req)
	html=webpage.read()
	soup= BeautifulSoup(html, "html.parser")
	p1 = re.compile(r'^http://pfam.xfam.org/family/.*$')
	p0 = re.compile(r'^http://www.cathdb.info/superfamily/.*$')
	trs=[1,2,3]
	soup=soup.find("table","databaseTable DOMAIN")
	trs=soup.find_all("tr")
	res=[]
	res.append([])
	res.append([])
	for tr in trs:
		try:
			acronym=(str)(tr.find("span","context-help tooltipped-click").contents[1])
			# print acronym
			if (acronym=="Gene3D"):
				anchors=tr.findAll("a")
				for a in anchors:
					if (p0.search(a['href'])):
						res[0].append(re.sub(r'[^(\d{1}.\d{2}.\d{3}.\d{2})]','',(str)(a.contents[0])))
			if (acronym=="Pfam"):
				anchors=tr.findAll("a")
				for a in anchors:
					if (p1.search(a['href'])):
						res[1].append(re.sub(r'[^A-Z0-9+]','',(str)(a.contents[0])))
		except Exception, e:
			print e
		else:
			pass
		finally:
			pass
	return res

url='D00225'
req = urllib2.Request("http://www.genome.jp/dbget-bin/www_bget?dr:"+url, headers={'User-Agent' : "Magic Browser"})
webpage= urllib2.urlopen(req)
html=webpage.read()
soup= BeautifulSoup(html, "html.parser")
p = re.compile(r'[^0-9]+')
temp=url+"\t"
trs=soup.find_all("tr")

# print len(trs)

for tr in trs:
	nobr=tr.find("nobr")
	key=""
	try:
		key=(str)(nobr.contents[0])
	except Exception,e:
		pass
	if (key=="Other DBs"):
		anchor=None
		try:
			anchor=tr.findAll("a")
		except Exception,e:
			pass
		
		if (anchor!=None):
			for a in anchor:
				pattern = re.compile(r'^http://www.drugbank.ca/drugs/.*$')
				if pattern.match(a['href']):
					 temp=a['href']
line=temp
urls = {}
p = re.compile(r'[A-Z0-9]+')
key=""
name = line.strip('\n')
match = p.match(name)
if match:
	pass
else:
	if (len(name)>4):
		urls[name]=[]
		nameList=name.split(" ")
		for nameTemp in nameList:
			try:
				listContent=crawl(nameTemp)
				for c in listContent:
					urls[name].append(c)	
			except Exception, e:
				pass

for u in urls:
	line2=",".join(urls[u])
urls2 = {}
p2 = re.compile(r'[A-Z0-9]+')
key2=""
key2=url
urls2[key2]={}
urls2[key2]['Gene3D']={}
urls2[key2]['Pfam']={}
nameList2=line2.strip().split(",")
for nameTemp2 in nameList2:
	try:
		listContent2=crawl2(nameTemp2)
		for x in listContent2[0]:
			if not (x in urls2[key2]['Gene3D']):
				urls2[key2]['Gene3D'][x]=1
			else:
				urls2[key2]['Gene3D'][x]=urls2[key2]['Gene3D'][x]+1
		for x in listContent2[1]:
			if not (x in urls2[key2]['Pfam']):
				urls2[key2]['Pfam'][x]=1
			else:
				urls2[key2]['Pfam'][x]=urls2[key2]['Pfam'][x]+1
	except Exception,e:
		print e		

cathID=open('GPCRFinal.txt.Gene3D.ID','r')
pfamID=open('GPCRFinal.txt.Pfam.ID','r')	
list_cath=[]	
list_pfam=[]
for i in cathID:
	i=i.strip('\n\r').split(' ')[1]
	val=0
	if i in urls2[key2]['Gene3D']:
		val=urls2[key2]['Gene3D'][i]
	list_cath.append(val)
print list_cath
for i in pfamID:
	i=i.strip('\n\r').split(' ')[1]
	val=0
	if i in urls2[key2]['Pfam']:
		val=urls2[key2]['Pfam'][i]
	list_pfam.append(val)
print list_pfam
	
