from flask import Flask
from flask import render_template
from flask import request
import random
import re
app = Flask(__name__)
# def huoquSimiA():
# 	return
# def huoquSimiB():
# 	return
def cal_accuracy(drugid,ATCid):
	a=1
	return a
	a=a+1
def cal(x):	
	# huoquSimiA(x)
	# huoquSimiB(x)
	# sys.shell("java -cp vaka.jar asdasdad -asdsd ")
	# return p[0]
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