from cmath import phase
from flask import render_template
from flask import current_app as app ,redirect
from flask_security import login_required,current_user
from flask import request
from application.models import Card,Phase,Position
from application.database import db
import datetime
import matplotlib.pyplot as plt


@app.route('/',methods=["GET","POST"])
def loginpage():
    return redirect('/home')

@app.route('/home',methods=["GET"])
@login_required
def homepage():
    if request.method == 'GET':
        tasks = Phase.query.all()
        cards = Card.query.all()
        done_all=0
        pending_all = 0
        late_all = 0
        values = {}
        now = str(datetime.datetime.now()).split(' ')[0]
        data = []
        for x in tasks:
            k = Card.query.filter_by(phase_name= x.phase_name)
            done=0
            pending = 0
            late = 0
            for y in k:
                if y.status == 1:
                    done +=1
                elif (now > y.deadline):
                    late +=1
                else:
                    pending+=1
            done_all += done
            late_all +=late
            pending_all += pending
            values[x.phase_name] = (done,pending,late)
            print(values)

            data = [done_all,pending_all,late_all]

            labels = ['Done','Pending','Late']
            c = ['green','yellow','red']
            plt.yticks(range(min(data), max(data)+1, 1))
            plt.bar(labels,data, color=c)
            plt.savefig('static/img.png')

    return render_template("Home.html",user=current_user.username,values = values,total = data)


@app.route('/tasks',methods=['GET','POST'])
@login_required
def tasks():
    if request.method == 'GET':
        tasks = Phase.query.all()
        cards = Card.query.all()
        if(len(tasks)==0):
            return render_template('Tasks.html',user = current_user.username,msg ="No phases found")
        else:
            return render_template('Tasks.html',user = current_user.username,phases = tasks,cards = cards)
    else:
        return render_template('404.html')


@app.route('/addtask',methods=['GET','POST'])
@login_required
def addtask():
    if request.method == 'GET':
        tasks = Phase.query.all()
        cards = Card.query.all()
        return render_template('Tasks.html',phases = tasks,cards = cards,user =  current_user.username,add = 1)
    if request.method == 'POST':
        title = request.form['title']
        Phase.create(title,1,0,0)
        return redirect('/tasks')


@app.route('/delete/<phase_name>',methods=['GET','POST'])
@login_required
def deltask(phase_name):
    Card.query.filter_by(phase_name = phase_name).delete()
    Phase.query.filter_by(phase_name = phase_name).delete()
    db.session.commit()
    return redirect('/tasks')


@app.route('/deletec/<cardid>',methods=['GET','POST'])
@login_required
def delcard(cardid):
    Card.query.filter_by(card_id = cardid).delete()
    db.session.commit()
    return redirect('/tasks')


@app.route('/create/<phase_name>',methods=['GET','POST'])
@login_required
def createtask(phase_name):
    if request.method == 'GET':
        tasks = Phase.query.all()
        cards = Card.query.all()
        return render_template('Tasks.html',phases = tasks,user = current_user.username,addcard = 1,phasename = phase_name,cards = cards)
    if request.method == 'POST':
        ctitle = request.form['title']
        deadline = request.form['deadline']
        status = 0
        content = request.form['content']
        color = request.form['color']
        Card.create(ctitle,deadline,status,content,phase_name,color)
        db.session.commit()
    
        return redirect('/tasks')


@app.route('/carddone/<card_id>',methods=['GET','POST'])
@login_required
def cardid(card_id):
    x = Card.query.filter_by(card_id=card_id).first()
    x.done("green")
    db.session.commit()
    return redirect('/tasks')


@app.route('/changename/<card_id>',methods=['GET','POST'])
@login_required
def namechange(card_id):
    if request.method == 'GET':
        tasks = Phase.query.all()
        cards = Card.query.all()
        card_id = int(card_id)
        return render_template('Tasks.html',user = current_user.username,phases = tasks,cards = cards,namechange= 1,card_id=card_id)
    elif request.method == 'POST':
        name = request.form['newname']
        x = Card.query.filter_by(card_id=card_id).first()
        x.rename(name)
        db.session.commit()
    return redirect('/tasks')


@app.route('/about',methods=['GET'])
@login_required
def about():
    return render_template("About.html",user=current_user.username)

@app.route('/sql',methods=['GET'])
@login_required
def sql():
    return render_template("SQL.html",user=current_user.username)

@app.route('/join',methods=['GET'])
def join():
    result = db.session.query(Card).join(Phase).filter(Card.phase_name == Phase.phase_name)
    for row in result:
            print (row.card_id, row.phase_id, row.description)
