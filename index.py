from flask import Flask
from flask import render_template
from flask import request
import urllib,urllib2,cookielib,socket  
from bs4 import BeautifulSoup
import sys
import random
import re
import numpy as np

app = Flask(__name__)
def huoquSim_drug():
	return
def huoquSim_ATC():
	return

drugID=open('drugID.txt','r')
ATCID=open('ATCID.txt','r')
cathID=open('GPCRFinal.txt.Gene3D.ID','r')
pfamID=open('GPCRFinal.txt.Pfam.ID','r')

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
	
def grab_domain(url):
	req = urllib2.Request("http://www.genome.jp/dbget-bin/www_bget?dr:"+url, headers={'User-Agent' : "Magic Browser"})
	webpage= urllib2.urlopen(req)
	html=webpage.read()
	soup= BeautifulSoup(html, "html.parser")
	p = re.compile(r'[^0-9]+')
	# temp=p.sub(url,"1")+"\t"
	temp=url+"\t"
	# print html
	trs=soup.find_all("tr")
	# print soup.get_text()
	for tr in trs:
		nobr=tr.find("nobr")
		# for no in nobr:
		# 	print no
		# print nobr.string
		key=""
		try:
			key=(str)(nobr.contents[0])
		except Exception,e:
			pass
		if (key=="Other DBs"):
			# print "find Other DBs"
			anchor=None
			try:
				anchor=tr.findAll("a")
			except Exception,e:
				pass
			
			if (anchor!=None):
				for a in anchor:
					pattern = re.compile(r'^http://www.drugbank.ca/drugs/.*$')
					if pattern.match(a['href']):
						 temp=temp+a['href']
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
				# print nameTemp
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
	


def cal_accuracy(drugid,ATCid):
	train=open('chemfingerprint_cath_pfam.csv','r')
	trainfile=[]
	testfile=[]
	for st in train:
		st=st.strip('\n').split(',')
		a=[float(x) for x in st]
		trainfile.append(a)
	trainfile=np.array(trainfile)
		# tra=np.vstack(tra,b)
	sim_drug=[]
	sim_ATC=[]
	for st1 in drugID:
		st1=st1.strip('\n\r').split(' ')
		# np.array(st1)
		sim_drug.append(huoquSim_drug(drugid,st1))
	sim_drug=np.array(sim_drug)
	for st2 in ATCID:
		st2=st2.strip('\n\r').split(' ')
		# np.array(st2)
		sim_ATC.append(huoquSim_ATC(ATCid,st2))
	sim_ATC=np.array(sim_ATC)
	for i in range(trainfile.shape[0]):
		testfile.append(sim_drug[i]*sim_ATC[i])
	testfile=np.array(testfile)
	grab_domain(drugid)
	# sys.shell("java -cp vaka.jar asdasdad -asdsd ")
	# return p[0]


def cal(x):	
	fr=open('ATCid.txt','r')
	dic={}
	for st in fr:
		dic[st]=cal_accuracy(x,st)
	dic=sorted(dic.iteritems(),key=lambda asd:asd[0],reverse=True)	
	return ' '.join([dic[i][0] for i in range(0,5)])
		
@app.route('/',methods=['GET','POST'])
def hello():
	
	return render_template("index.html",title=cal(request.args.get("a","A01AC02")))

	# return "hello"
if __name__ == "__main__" :
	app.run(debug=True)