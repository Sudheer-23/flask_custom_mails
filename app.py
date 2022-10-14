from flask import Flask,render_template,request,redirect,url_for
from flask_wtf import FlaskForm
from wtforms import FileField,SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename 
from flaskext.mysql import MySQL
import pymysql
import os
import smtplib  
from email.message import EmailMessage
from datetime import date

app = Flask(__name__)
app.secret_key = "Sudheer"
app.config['UPLOAD_FOLDER'] = "static/attachments"

mysql = MySQL()
# MySQL Configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'sudheer123'
app.config['MYSQL_DATABASE_DB'] = 'college'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

class Upload_attachment(FlaskForm):
    file = FileField("File", validators=[InputRequired()])
    submit = SubmitField("Upload File")

@app.route('/',methods = ['GET','POST'])
def home(): 
    form = Upload_attachment()
    if form.validate_on_submit():
        file = form.file.data # First grab the file
        file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),app.config['UPLOAD_FOLDER'],secure_filename(file.filename))) # Then save the file
        return "File has been uploaded."

    return render_template('draft.html',form = form)
    

@app.route('/send_mail',methods=['GET','POST'])
def send_mail():
    if request.method == 'POST':
        c = request.form['company']
        sam_msg = request.form['message']
        con = mysql.connect()
        cur = con.cursor(pymysql.cursors.DictCursor)
        cur.execute('SELECT email FROM students;')
        data = cur.fetchall()
        cur.close()
         
        email_li = []
        for i in data:
            email_li.append(i['email'])
        
        email_id = "lolday606@gmail.com"
        email_pass = "ztskhwqzmvanmjqn"

        msg = EmailMessage()
        msg['subject'] = "Testing mail feature with smtplib"
        msg['From'] = email_id
        msg['To'] = email_li
        msg.set_content(sam_msg)

        for each_file in os.listdir():
            if(each_file == 'Deltax_circular'):
                with open(each_file, 'rb') as f:
                    file_data = f.read()
                    file_name = f.name
                    msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

        with smtplib.SMTP_SSL("smtp.gmail.com",465) as smtp:
            smtp.login(email_id,email_pass)
            smtp.send_message(msg)
        
        
        
        print(email_li)
        return render_template("output1.html",mails = email_li)
    
if __name__ =='__main__':
    app.run(debug =True)
