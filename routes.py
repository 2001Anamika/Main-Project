from flask import Flask, render_template, request, redirect,  flash, abort, url_for, session
from threat import app
from threat import app
from threat.models import *
from flask_login import login_user, current_user, logout_user, login_required
from random import randint
import os
from PIL import Image
from datetime import datetime, timedelta

from flask_mail import Message
from threat import app, db, mail

from datetime import date
from datetime import datetime


from tensorflow import keras
import pandas as pd
import numpy as np


# @app.route('/detection',methods=['GET', 'POST'])
# def detection():
#     # c= Register.query.get_or_404(id)
#     # print(c.id)
#     if request.method == "POST":

#         # c= Register.query.get_or_404(id)
                
#         model_1 = keras.models.load_model('threat/model')

#         THRESHOLD = 71.073

#         threat_labels = {
#             0 :'normal',
#             1 : 'threat'}


#         f = request.files['files']
#         f.save(f.filename)
#         print(f.filename)

#         input_df = pd.read_csv(f.filename)


#         output_list = []

#         for index, rows in input_df.iterrows():
#             input_list =[rows.email_n_pc2,rows.email_send_mail_n_pc2,rows.usb_mean_usb_dur,rows.workhouremail_n_pc2,rows.n_usb,rows.usb_mean_file_tree_len,rows.workhouremail_send_mail_n_pc2,
#                 rows.workhourusb_n_pc0,rows.workhourusb_mean_usb_dur,rows.usb_n_pc0,rows.n_workhourusb,rows.http_leakf_mean_url_len,rows.http_n_pc0,rows.day]
#             numx = np.array(input_list)
#             numx.shape[0]
#             X = np.reshape(numx, (1,14,1))

#             y_pred= model_1.predict(X)

#             reconstruction_loss = np.mean(np.abs(y_pred - X), axis=1)[0][0]
#             # preds = np.max(y_pred, axis=1)


#             if reconstruction_loss >THRESHOLD: 
#                 prediction_class = 1
#             else:
#                 prediction_class = 0

#             prediction_label = threat_labels[prediction_class]

            
#             output_list.append({"user_id": rows.user_id,"result":prediction_label})

#             # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&")
#             # print(rows.user_id)
#             # print("&&&&&&&&&&&&&&&&&&&&&&&&&&&")


#             today = date.today()
#             print(today)
#             now=datetime.now()
#             current_time=now.strftime("%H:%M:%S")
#             print("Current Time=",current_time)
#             my_data = Prediction(user_id=str(rows.user_id),result=prediction_label,det_date=today,time=current_time)
#             db.session.add(my_data) 
#             db.session.commit()


#             print("-----count-----")

#             d=Email.query.first()
#             last_date=d.det_date
#             print (last_date)

#             # cnt=Prediction.query.filter(Prediction.result=="threat",Prediction.det_date > last_date).all()

#             cnt=Prediction.query.filter(Prediction.result=="threat",Prediction.det_date > last_date).all()

            


#             # print(cnt.user_id)
#             print("-----count-----")
#             count1=Prediction.query.filter(Prediction.result=="threat",Prediction.det_date > last_date).count()

            
#             print(count1)
            
#             print("-----coun**---")

           

            
#         print("output user list", output_list,count1,cnt)

#         cnt_mail(count1,cnt)

#         return render_template("file_upload.html",label=output_list)
#         # return render_template("file_upload.html",label=prediction_label,c=c,cnt1=cnt1,cnt2=cnt2)
#     return render_template("file_upload.html")




@app.route('/detection/<int:id>',methods=['GET', 'POST'])
def detection(id):
    c= Register.query.get_or_404(id)
    print(c.id)
    if request.method == "POST":

        c= Register.query.get_or_404(id)

        model_1 = keras.models.load_model('threat/model')
        print("Loaded model from disk")

        threat_labels = {
            0 :'NORMAL',
            1 :'THREAT'}

        #threat example
        email_n_pc2 = request.form['data1']
        email_send_mail_n_pc2 = request.form['data2']
        usb_mean_usb_dur = request.form['data3']
        workhouremail_n_pc2 = request.form['data4']
        n_usb = request.form['data5']
        usb_mean_file_tree_len = request.form['data6']
        workhouremail_send_mail_n_pc2 = request.form['data7']
        workhourusb_n_pc0 = request.form['data8']
        workhourusb_mean_usb_dur = request.form['data9']
        usb_n_pc0 = request.form['data10']
        n_workhourusb = request.form['data11']
        http_leakf_mean_url_len = request.form['data12']
        http_n_pc0 = request.form['data13']
        day = request.form['data14']


        input_list = [float(email_n_pc2),float(email_send_mail_n_pc2),float(usb_mean_usb_dur),float(workhouremail_n_pc2),float(n_usb),float(usb_mean_file_tree_len),float(workhouremail_send_mail_n_pc2),
                float(workhourusb_n_pc0),float(workhourusb_mean_usb_dur),float(usb_n_pc0),float(n_workhourusb),float(http_leakf_mean_url_len),float(http_n_pc0),float(day)]

        numx = np.array(input_list)
        numx.shape[0]
        X = np.reshape(numx, (1,14,1))

        y_pred= model_1.predict(X)

        preds = np.max(y_pred, axis=1)


        if preds[0][0] >0.007: 
            prediction_class = 1
        else:
            prediction_class = 0

        prediction_label = threat_labels[prediction_class]

        print(prediction_label)



        today = date.today()
        print(today)
        now=datetime.now()
        current_time=now.strftime("%H:%M:%S")
        print("Current Time=",current_time)
        my_data = Prediction(user_id=c.id,result=prediction_label,det_date=today,time=current_time)
        db.session.add(my_data) 
        db.session.commit()



        # d=Email.query.first()
        # last_date=d.det_date
        # print (last_date)

        # cnt=Prediction.query.filter(Prediction.result=="threat",Prediction.det_date > last_date).all()

        # count1=Prediction.query.filter(Prediction.result=="threat",Prediction.det_date > last_date).count()
        # if prediction_label=="THREAT":
        #     cnt_mail(id)

        # print(count1)
        # print(cnt)

        return render_template("detection.html",label=prediction_label,c=c)
    return render_template("detection.html")



@app.route("/cnt_mail")
def cnt_mail():

    d=Email.query.first()
    last_date=d.det_date
    print (last_date)

    cnt=Prediction.query.filter(Prediction.result=="THREAT",Prediction.det_date > last_date).all()

    count1=Prediction.query.filter(Prediction.result=="THREAT",Prediction.det_date > last_date).count()
    # if prediction_label=="THREAT":
    #     cnt_mail(id)

    print(count1)
    print(cnt)



    msg = Message('Count ',
                  recipients=["anamikapradeep6@gmail.com"])
    msg.body = f'''Threat detected user ID  - {id} '''

    msg.html = render_template('email.html',count1=count1,cnt=cnt)


    mail.send(msg)

    today = date.today()
    print(today)
    now=datetime.now()
    current_time=now.strftime("%H:%M:%S")
    print("Current Time=",current_time)
    a=Email.query.all()
    for i in a:

        i.det_date = today
        i.time = current_time
        db.session.commit()
        return redirect('/admin_index')


  




# @app.route('/edit_staff/<int:id>',methods=["GET","POST"])
# def edit_staff(id):
#     c= Register.query.get_or_404(id)
#     if request.method == 'POST':
#         c.name =  request.form['name']
#         c.email =  request.form['email']
#         c.contact =  request.form['contact']
#         c.password =  request.form['password']
       
#         db.session.commit()
#         return redirect('/view_staff')
#     else:
#         return render_template('edit_staff.html',c=c)







@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template("index.html")



@app.route('/admin_index',methods=['GET', 'POST'])
def admin_index():
    return render_template("admin_index.html")






@app.route('/layout')
def layout():
    return render_template("layout.html")

@app.route('/admin_layout')
def admin_layout():
    return render_template("admin_layout.html")





@app.route('/about')
def about():
    return render_template("about.html")







@app.route('/add_staff',methods=['GET','POST'])
def add_staff():
    if request.method == 'POST':

        name = request.form['name']
        email = request.form['email']
        
        address= request.form['address']
        contact= request.form['contact'] 
        my_data = Register(name=name,email=email,contact=contact,address=address,usertype="staff")
        db.session.add(my_data) 
        db.session.commit()
        return redirect('/add_staff')
    return render_template("add_staff.html")


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method=="POST":
        email=request.form['email']
        password=request.form['password']
        admin =Register.query.filter_by(email=email, password=password,usertype= 'admin').first()
        
               
        if admin:
            login_user(admin)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect('/admin_index') 
        
       
        else:
            d="Invalid Username or Password!"
            return render_template("login.html",d=d)
    return render_template("login.html")




@app.route('/view_staff')
def view_staff():
    obj = Register.query.filter_by(usertype="staff").all()
    return render_template("view_staff.html",obj=obj)



@app.route('/edit_staff/<int:id>',methods=["GET","POST"])
def edit_staff(id):
    c= Register.query.get_or_404(id)
    if request.method == 'POST':
        c.name =  request.form['name']
        c.email =  request.form['email']
        c.contact =  request.form['contact']
        c.address =  request.form['address']
       
        db.session.commit()
        return redirect('/view_staff')
    else:
        return render_template('edit_staff.html',c=c)



@app.route('/delete_staff/<int:id>', methods = ['GET','POST'])
def delete_staff(id):

    delet = Register.query.get_or_404(id)
    try:
        db.session.delete(delet)
        db.session.commit()
        return redirect('/view_staff')
    except:
        return 'There was a problem deleting that task'


# @app.route('/file_upload',methods=['GET','POST'])
# def file_upload():
#     if request.method == 'POST':

#         file= request.files['file']

#         file.save(os.path.join(app.config['UPLOAD_FOLDER'],file.filename))
#         print(file.filename)
       
#         my_data = Prediction(file=file.filename)
#         db.session.add(my_data) 
#         db.session.commit()
#         return redirect('/file_upload')
#     return render_template("file_upload.html")


@login_required
@app.route("/logout")
def logout():
    logout_user()
    return redirect('/')


def save_picture(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/uploads', picture_fn)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn

def save_pictures(form_picture):
    random_hex = random_with_N_digits(14)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = str(random_hex) + f_ext
    picture_path = os.path.join(app.root_path, 'static/upload', picture_fn)
    output_size = (500, 500)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    return picture_fn


def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

