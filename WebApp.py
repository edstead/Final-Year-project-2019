from flask import Flask, render_template, request, url_for, redirect, session
from Project import MainProject2018
import mysql.connector
import jinja2
import pygal
import os

app = Flask(__name__)

app.secret_key=os.urandom(24)
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir))

searchterm =""
noofterms = 0
# positive=""
# negative=""
# neutral=""

def appRun():
    flag = MainProject2018.runfunc(searchterm, noofterms)


@app.route("/", methods=["GET", "POST"])
def homepage():
    error = None
    #return render_template("Compare.html", user=user)
    if request.method == 'POST':
        searchterm = request.form['keyword']
        print(searchterm)
        noofterms = request.form['number']
        print(noofterms)

        flag = MainProject2018.runfunc(searchterm, noofterms)
        #MainProject2018.theflag(passedbool)

        ##use an if statment
        #return redirect(url_for("SecondPage"))
        return redirect(url_for("DisplayPage"))



    return render_template("Homepage.html", error=error)

@app.route("/")
@app.route("/Database/")
def Database():
    mydb = mysql.connector.connect(
        host="edstead.mysql.pythonanywhere-services.com",
        port=3306,
        user="edstead",
        passwd="Eddyiscool123",
        database="edstead$project"
    )
    items=[]
    mycursor = mydb.cursor()

    mycursor.execute("SELECT * FROM project")

    myresult = mycursor.fetchall()


    for x in myresult:
        print(x)
        items.append(x)

    items.reverse()
    template = jinja_env.get_template('Database.html')
    return template.render(items=items)

@app.route("/Compare", methods=["GET", "POST"])
def Compare():
    error = None
    if request.method == 'POST':
        firstKeyword = request.form['keyword1']
        #print(firstKeyword)
        session["firstKeyword"] = firstKeyword
        secondKeyword = request.form['keyword2']
        #print(secondKeyword)
        session["secondKeyword"] = secondKeyword
        return redirect(url_for("CompareGraph"))

    return render_template("Compare.html", error=error)

@app.route("/CompareGraph")
def CompareGraph():
    kwordone = session.get("firstKeyword", None)
    print(kwordone)
    kwordtwo = session.get("secondKeyword", None)
    print(kwordtwo)

    mydb = mysql.connector.connect(
        host="edstead.mysql.pythonanywhere-services.com",
        port=3306,
        user="edstead",
        passwd="Eddyiscool123",
        database="edstead$project"
    )
    mycursor = mydb.cursor()


    mysql_result= "SELECT * FROM project WHERE Keyword = %s"

    mycursor.execute(mysql_result, (kwordone,))

    result1 = mycursor.fetchall()
    #  print(result1)


    pos1= (sum(x.count('Positive') for x in result1))
    neg1=(sum(x.count('Negative') for x in result1))
    neut1=(sum(x.count('Neutral') for x in result1))

    print(pos1)
    print(neg1)
    print(neut1)

    mysql_result2= "SELECT * FROM project WHERE Keyword = %s"

    mycursor.execute(mysql_result, (kwordtwo,))

    result2 = mycursor.fetchall()
    #print(result2)

    pos2 = (sum(y.count('Positive') for y in result2))
    neg2 = (sum(y.count('Negative') for y in result2))
    neut2 = (sum(y.count('Neutral') for y in result2))

    print(pos2)
    print(neg2)
    print(neut2)

    line_chart = pygal.Line()
    line_chart.title = 'Comparison of your two choosen keywords' +str(kwordone) +'&' +str(kwordtwo)
    line_chart.x_labels =('Negitive', 'Neutral', 'Positive')
    line_chart.add(kwordone, [neg1, neut1, pos1])
    line_chart.add(kwordtwo, [neg2, neut2, pos2])
    compare_data= line_chart.render_data_uri()
    return render_template("CompareGraph.html", compare_data= compare_data)

@app.route("/")
@app.route("/DisplayPage/")
def DisplayPage():
    positive = float(MainProject2018.pos)
    print (positive)
    negative = float(MainProject2018.neg)
    print(negative)
    neutral = float(MainProject2018.neut)
    print(neutral)
    pie_chart = pygal.Pie()
    pie_chart.title = 'How many people are reacting the keyword' +str(searchterm)
    pie_chart.add('Positive', positive)
    pie_chart.add('Negative', negative)
    pie_chart.add('Neutral', neutral)
    #pie_chart.add('Safari', 4.5)
    #pie_chart.add('Opera')
    graph_data= pie_chart.render_data_uri()
    return render_template("DisplayPage.html", graph_data= graph_data )


@app.route("/")
@app.route("/LoadingPage/")
def LoadingPage():
    return render_template("LoadingPage.html")



if __name__== "__main__":
    app.run()