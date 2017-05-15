from flask import Flask, redirect, url_for, request, render_template
from flask_mail import Mail, Message
import os
import urllib
import subprocess
from multiprocessing import Process
import sys
sys.path.append('../')
import question_detection

class processClass:

    def __init__(self, qtype, chapNum, question, email):
        p = Process(target=self.run, args=(qtype, chapNum, question, email))
        p.daemon = True                       # Daemonize it
        p.start()                             # Start the execution

    def run(self, qtype, chapNum, question, email):

         #
         # This might take several minutes to complete
         answer_process(qtype, chapNum, question, email)

app = Flask(__name__)
mail = Mail(app)

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'dsac.automatic.qa@gmail.com'
app.config['MAIL_PASSWORD'] = 'dsackesitare'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)

@app.route('/success/<question>/<email>')
def success(question, email):
	try:
		os.chdir("../node_modules/qtypes/test/")
		qtype = int(subprocess.Popen(["node", "question_classify.js", question], stdout=subprocess.PIPE).communicate()[0])
		print "qtype:", qtype
		os.chdir("../../../webApp")
		print question_detection.detect_question_main(question)
		begin = processClass(qtype, question_detection.detect_question_main(question), question, email)
	except:
		abort(500)
	return render_template('success.html')

def answer_process(qtype, chapNum, question, email):
	if int(qtype) == 0:
		os.chdir("../factoid_qa/NLP-Question-Answer-System/stanford-corenlp-python/")
		answer = subprocess.Popen(["python", "new_factoid.py", str(chapNum), question], stdout=subprocess.PIPE)
		answer.wait()
		answer = answer.communicate()[0].strip("\n")
		os.chdir("../../../webApp")
	elif int(qtype) == 1:
		os.chdir("../")
		answer = subprocess.Popen(["python", "answer_desc.py", str(chapNum), question], stdout=subprocess.PIPE)
		answer = answer.communicate()[0].split("\n")
		answer = answer[2:]
		answer = "\n".join(answer)
		os.chdir("./webApp")
	msg = Message(question, sender = 'dsac.automatic.qa@gmail.com', recipients = [email])
	msg.body = answer
	mail.send(msg)
	print answer

@app.route('/input',methods = ['POST', 'GET'])
def login():
	if request.method == 'POST':
		question = request.form['question']
		email = request.form['email']
		#return redirect("autoQA/success/"+urllib.urlencode(question)+"/"+urllib.urlencode(email))
		return redirect("autoQA"+url_for('success',question = question, email = email))
	else:
		question = request.args.get('question')
		email = request.args.get('email')
		#return redirect("autoQA/success/"+urllib.urlencode(question)+"/"+urllib.urlencode(email))
		return redirect("autoQA"+url_for('success',question = question, email = email))

@app.route("/", methods=["GET", "POST"])
def home():
	return render_template('home.html')
if __name__ == '__main__':
	app.run('0.0.0.0', debug = True)
