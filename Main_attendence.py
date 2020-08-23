import tkinter as tk
from tkinter import *
import cv2
import csv
import os
import numpy as np
from PIL import Image,ImageTk
import pandas as pd
import datetime
import time

####GUI for manually fill attendance

##For clear textbox
def clear():
    txt.delete(first=0, last=22)

def clear1():
    txt2.delete(first=0, last=22)

def clear2():
    sub.delete(first=0, last=22)

def clear3():
    phn.delete(first=0, last=22)
def del_sc1():
    sc1.destroy()
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry('300x100')
    sc1.title('Warning!!')
    sc1.configure(background='snow')
    Label(sc1,text='Enrollment & Name required!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc1,text='OK',command=del_sc1,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

##Error screen2
def del_sc2():
    sc2.destroy()
def err_screen1():
    global sc2
    sc2 = tk.Tk()
    sc2.geometry('300x100')
    sc2.title('Warning!!')
    sc2.configure(background='snow')
    Label(sc2,text='Please enter your subject name!!!',fg='red',bg='white',font=('times', 16, ' bold ')).pack()
    Button(sc2,text='OK',command=del_sc2,fg="black"  ,bg="lawn green"  ,width=9  ,height=1, activebackground = "Red" ,font=('times', 15, ' bold ')).place(x=90,y= 50)

###For take images for datasets
def take_img():
    l1 = txt.get()
    l2 = txt2.get()
    if l1 == '':
        err_screen()
    elif l2 == '':
        err_screen()
    else:
        try:
            cam = cv2.VideoCapture(0)
            detector = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
            Enrollment = txt.get()
            Name = txt2.get()
            subject = sub.get()
            phone = phn.get()
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder
                    cv2.imwrite("TrainingImage/ " + Name + "." + Enrollment + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    cv2.imshow('Frame', img)
                # wait for 100 miliseconds
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 200:
                    break
            cam.release()
            cv2.destroyAllWindows()
            ts = time.time()
            Date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
            Time = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                        
            row = [Enrollment, Name, subject, Time, Date, phone]
            with open('StudentDetails/StudentDetails.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile, delimiter=',')
                writer.writerow(row)
                csvFile.close()
            res = "Images Saved \nEnrollment : " + Enrollment 
            Notification.configure(text=res, bg="lavender",fg="green", width=40, font=('times', 17, 'bold'))
            Notification.place(x=60, y=420)
        except FileExistsError as F:
            f = 'Student Data Already Exists..!!'
            Notification.configure(text=f, bg="lavender",fg="red", width=21,font=('times', 17, 'bold'))
            Notification.place(x=80, y=420)


###for choose subject and fill attendance
def subjectchoose():
    def Fillattendances():
        import csv
        import tkinter

        sub=tx.get()
        now = time.time()  ###For calculate seconds of video
        future = now + 20
        if time.time() < future:
            if sub == '':
                err_screen1()
            else:
                recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
                try:
                    recognizer.read("TrainingImageLabel/Trainner.yml")
                except:
                    e = 'Model not found, Please train model'
                    Notifica.configure(text=e, bg="red", fg="black", width=33, font=('times', 15, 'bold'))
                    Notifica.place(x=100, y=160)

                harcascadePath = "haarcascade_frontalface_default.xml"
                faceCascade = cv2.CascadeClassifier(harcascadePath)
                df = pd.read_csv("StudentDetails/StudentDetails.csv")
                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX
                col_names = ['Enrollment', 'Name','Subject', 'Time', 'Date']
                attendance = pd.DataFrame(columns=col_names)
                checkdict={}
                css='StudentDetails/StudentDetails.csv'
                with open(css, newline="") as file:
                    reader = csv.reader(file)
                    if reader:
                        for row in reader:
                            checkdict[row[0]]=[row[2],row[3],row[4]]
                
                while True:
                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
                    faces = faceCascade.detectMultiScale(gray, 1.2, 5)
                    for (x, y, w, h) in faces:
                        global Id

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])
                        Id=str(Id)
                        if (conf <70):
                            global Subject
                            global aa
                            global date
                            global timeStamp
                            Subject = tx.get()
                            ts = time.time()
                            date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                            enr=[str(i) for i in df['Enrollment'].values]
                            if Id in enr:
                                if checkdict[Id][0] == Subject:
                                    aa = df.loc[df['Enrollment']==int(Id)]['Name'].values[0]
                                    global tt
                                    
                                    tt = Id+ " " + aa
                                    attendance.loc[len(attendance)] = [Id, aa, Subject, timeStamp,date]
                                    cv2.rectangle(im, (x, y), (x + w, y + h), (0, 260, 0), 7)
                                    cv2.putText(im, tt, (x + h, y), font, 1, (255, 255, 0,), 4)
                                else:
                                    Id = 'Other'
                                    tt = Id
                                    cv2.rectangle(im, (x, y), (x + w, y + h), (90, 25, 255), 7)
                                    cv2.putText(im, tt, (x + h, y), font, 1, (100, 25, 255), 4)                            
                            else:
                                Id = 'Unknown'
                                tt = Id
                                cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                                cv2.putText(im, tt, (x + h, y), font, 1, (0, 25, 255), 4)                            
                        else:
                            Id = 'Unknown'
                            tt = Id
                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 25, 255), 7)
                            cv2.putText(im, tt, (x + h, y), font, 1, (0, 25, 255), 4)
                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                    cv2.imshow('Filling attedance..', im)
                    key = cv2.waitKey(30) & 0xff
                    if key == 27:
                        break

                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                
                fileName = "Attendance/"+Subject + "_" + date + ".csv"
                attendance = attendance.drop_duplicates(['Enrollment'], keep='first')
                attendance.to_csv(fileName, index=False)

                
                M = 'Attendance filled Successfully'
                Notifica.configure(text=M, bg="lavender", fg="green", width=33, font=('times', 17, 'bold'))
                Notifica.place(x=100, y=160)

                cam.release()
                cv2.destroyAllWindows()

                root = tkinter.Tk()
                root.title("Attendance of " + Subject)
                root.configure(background='snow')
                cs="/root/Desktop/Attendace_management_system-master/"+fileName
                with open(cs,'a+') as file:
                    reader = csv.reader(file)
                    for col in reader:
                        for row in col:
                            writer = csv.writer(file, delimiter=',')
                            writer.writerow(row)
                
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            # i've added some styling
                            label = tkinter.Label(root, width=15, height=2, fg="black", font=('times', 15, ' bold '),
                                                  bg="lavender", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                    
                root.mainloop()

    ###windo is frame for subject chooser
    windo = tk.Tk()
    windo.title("Enter subject name")
    windo.geometry('580x320')
    windo.configure(background='lavender')
    Notifica = tk.Label(windo, text="Attendance filled Successfully", bg="lavender", fg="green", width=33,
                            height=2, font=('times', 15, 'bold'))
    sub1 = tk.Label(windo, text="Attendance", width=20, height=2, fg="black", bg="lavender", font=('times', 23, ' bold '))
    sub1.place(x=170, y=20)
    sub = tk.Label(windo, text="Enter Subject", width=20, height=2, fg="black", bg="lavender", font=('times', 17, ' bold '))
    sub.place(x=30, y=100)

    tx = tk.Entry(windo, width=20, bg="snow", fg="red", font=('times', 20, ' bold '))
    tx.place(x=250, y=105)

    fill_a = tk.Button(windo, text="Submit", fg="white",command=Fillattendances, bg="gray80", width=15, height=1,
                       activebackground="gray60", font=('times', 15, ' bold '))
    fill_a.place(x=200, y=230)
    windo.mainloop()

def admin_panel():
    win = tk.Tk()
    win.title("LogIn")
    win.geometry('800x420')
    win.configure(background='lavender')

    def log_in():
        username = un_entr.get()
        password = pw_entr.get()

        if username == 'admin' :
            if password == 'admin':
                win.destroy()
                import csv
                import tkinter
                root = tkinter.Tk()
                root.title("Student Details")
                root.configure(background='snow')

                cs = "/root/Desktop/Attendace_management_system-master/StudentDetails/StudentDetails.csv"
                with open(cs, newline="") as file:
                    reader = csv.reader(file)
                    r = 0
                    for col in reader:
                        c = 0
                        for row in col:
                            label = tkinter.Label(root, width=15, height=2, fg="black", font=('ms serif', 15, ' bold '),
                                                  bg="lavender", text=row, relief=tkinter.RIDGE)
                            label.grid(row=r, column=c)
                            c += 1
                        r += 1
                root.mainloop()
            else:
                valid = 'Incorrect ID or Password'
                Nt.configure(text=valid, bg="lavender", fg="red", width=38, font=('times', 19, 'bold'))
                Nt.place(x=120, y=250)

        else:
            valid ='Incorrect ID or Password'
            Nt.configure(text=valid, bg="lavender", fg="red", width=38, font=('times', 19, 'bold'))
            Nt.place(x=120, y=250)


    Nt = tk.Label(win, text="Attendance filled Successfully", bg="lavender", fg="green", width=40,
                  height=2, font=('times', 19, 'bold'))
    u1n = tk.Label(win, text="Admin LogIn", width=15, height=2, fg="black", bg="lavender",
                   font=('times', 24, ' bold '))
    u1n.place(x=330, y=30)
    un = tk.Label(win, text="Enter username: ", width=15, height=2, fg="black", bg="lavender",
                   font=('times', 18, ' bold '))
    un.place(x=50, y=150)

    pw = tk.Label(win, text="Enter password:", width=15, height=2, fg="black", bg="lavender",
                  font=('times', 18, ' bold '))
    pw.place(x=50, y=200)

    def c00():
        un_entr.delete(first=0, last=22)

    un_entr = tk.Entry(win, width=22, bg="snow", fg="red", font=('times', 23, ' bold '))
    un_entr.place(x=250, y=155)

    def c11():
        pw_entr.delete(first=0, last=22)

    pw_entr = tk.Entry(win, width=22,show="*", bg="snow", fg="red", font=('times', 23, ' bold '))
    pw_entr.place(x=250, y=205)

    c0 = tk.Button(win, text="Clear", command=c00, fg="black", bg="gray80", width=10, height=1,
                            activebackground="gray60", font=('times', 15, ' bold '))
    c0.place(x=650, y=155)

    c1 = tk.Button(win, text="Clear", command=c11, fg="black", bg="gray80", width=10, height=1,
                   activebackground="gray60", font=('times', 15, ' bold '))
    c1.place(x=650, y=205)

    Login = tk.Button(win, text="LogIn", fg="black", bg="gray80", width=20,
                       height=2,activebackground="gray60",command=log_in, font=('times', 15, ' bold '))
    Login.place(x=290, y=330)
    win.mainloop()


###For train the model
def trainimg():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    global detector
    detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")
    try:
        global faces,Id
        faces, Id = getImagesAndLabels("TrainingImage")
    except Exception as e:
        l='please make "TrainingImage" folder & put Images'
        Notification.configure(text=l, bg="lavender",fg="red", width=30, font=('times', 15, 'bold'))
        Notification.place(x=150, y=420)

    recognizer.train(faces, np.array(Id))
    try:
        recognizer.save("TrainingImageLabel/Trainner.yml")
    except Exception as e:
        q='Please make "TrainingImageLabel" folder'
        Notification.configure(text=q, bg="lavender",fg="red", width=70, font=('times', 18, 'bold'))
        Notification.place(x=150, y=420)

    res = "Model Trained\nEnrollment No.: "+str(Id[0])
    Notification.configure(text=res, bg="lavender",fg="green", width=70, font=('times', 18, 'bold'))
    Notification.place(x=100, y=420)

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empth face list
    faceSamples = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image

        Id = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces = detector.detectMultiScale(imageNp)
        # If a face is there then append that in the list as well as Id of it
        for (x, y, w, h) in faces:
            faceSamples.append(imageNp[y:y + h, x:x + w])
            Ids.append(Id)
    return faceSamples, Ids

#####Window is our Main frame of system
window = tk.Tk()
window.title("Face Recognition Attendance System")

window.geometry("1200x625")
window.configure(background='lavender')

window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

def on_closing():
    from tkinter import messagebox
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        window.destroy()
window.protocol("WM_DELETE_WINDOW", on_closing)

message = tk.Label(window, text="Face Recognition Attendance System", bg="lavender", fg="black", width=50,
                   height=3, font=('times new roman', 32, 'bold '))

message.place(x=80, y=15)

Notification = tk.Label(window, text="All things good", bg="Green", fg="white", width=15,
                      height=3, font=('times', 17, 'bold'))

lbl = tk.Label(window, text="Enrollment Number: ", width=30, height=2, fg="black", bg="lavender", font=('ms serif', 21, ' bold '))
lbl.place(x=100, y=160)


def testVal(inStr,acttyp):
    if acttyp == '1': #insert
        if not inStr.isdigit():
            return False
    return True

txt = tk.Entry(window, validate="key", width=30, bg="gray95", fg="red", font=('times', 20, ' bold '))
txt['validatecommand'] = (txt.register(testVal),'%P','%d')
txt.place(x=450, y=170)

clearButton = tk.Button(window, text="Clear",command=clear,fg="black"  ,bg="gray80"  ,width=10  ,height=1 ,activebackground = "gray60" ,font=('times', 15, ' bold '))
clearButton.place(x=950, y=170)

lbl2 = tk.Label(window, text="Student Name: ", width=25, fg="black", bg="lavender", height=2, font=('ms serif', 21, ' bold '))
lbl2.place(x=165, y=230)

txt2 = tk.Entry(window, width=30, bg="gray95", fg="red", font=('times', 20, ' bold '))
txt2.place(x=450, y=240)


clearButton1 = tk.Button(window, text="Clear",command=clear1,fg="black"  ,bg="gray80"  ,width=10 ,height=1, activebackground = "gray60" ,font=('times', 15, ' bold '))
clearButton1.place(x=950, y=240)

lb = tk.Label(window, text="Subject: ", width=25, fg="black", bg="lavender", height=2, font=('ms serif', 21, ' bold '))
lb.place(x=165, y=300)

sub = tk.Entry(window, width=30, bg="gray95", fg="red", font=('times', 20, ' bold '))
sub.place(x=450, y=310)

clearButton1 = tk.Button(window, text="Clear",command=clear2,fg="black"  ,bg="gray80"  ,width=10 ,height=1, activebackground = "gray60" ,font=('times', 15, ' bold '))
clearButton1.place(x=950, y=310)

lb = tk.Label(window, text="Phone No.: ", width=25, fg="black", bg="lavender", height=2, font=('ms serif', 21, ' bold '))
lb.place(x=165, y=360)


phn = tk.Entry(window, validate="key", width=30, bg="gray95", fg="red", font=('times', 20, ' bold '))
phn['validatecommand'] = (phn.register(testVal),'%P','%d')
phn.place(x=450, y=370)

clearButton1 = tk.Button(window, text="Clear",command=clear3,fg="black"  ,bg="gray80"  ,width=10 ,height=1, activebackground = "gray60" ,font=('times', 15, ' bold '))
clearButton1.place(x=950, y=370)


takeImg = tk.Button(window, text="Take Images",command=take_img,fg="white"  ,bg="deep sky blue"  ,width=17  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
takeImg.place(x=90, y=500)

trainImg = tk.Button(window, text="Train Images",fg="white",command=trainimg ,bg="deep sky blue"  ,width=17  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
trainImg.place(x=320, y=500)

FA = tk.Button(window, text="Automatic Attendace",fg="white",command=subjectchoose  ,bg="springgreen2"  ,width=19  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
FA.place(x=600, y=500)

quitWindow = tk.Button(window, text="Check Register students", command=admin_panel  ,fg="white"  ,bg="springgreen2"  ,width=21  ,height=2, activebackground = "Red" ,font=('times', 15, ' bold '))
quitWindow.place(x=850, y=500)

window.mainloop()