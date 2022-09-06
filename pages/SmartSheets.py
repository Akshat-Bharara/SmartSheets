import streamlit as st
import pandas as pd
import cv2,os
import csv
import numpy as np
from PIL import Image
import datetime
import time
from st_aggrid import GridOptionsBuilder, AgGrid
import plotly.graph_objects as go
import plotly.express as px

############################################# FUNCTIONS ################################################

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def TakeImages():

    global login
    login = False

    columns = ['SERIAL NO.', '','ID','','NAME']
    assure_path_exists("StudentDetails/")
    assure_path_exists("TrainingImage/")
    serial = 0
    exists = os.path.isfile("StudentDetails\StudentDetails.csv")

    if exists:
        with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for l in reader1:
                serial = serial + 1
        serial = serial-1
    else:
        with open("StudentDetails\StudentDetails.csv", 'a+',newline='') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(columns)
            serial = 1
        csvFile1.close()


    row = [int(serial), '', Id, '', name]
    exist = False

    with open('StudentDetails\StudentDetails.csv','r') as file:
        reader = csv.reader(file)

        for i in reader:
            if i[2]==row[2]:
                st.warning('ID is already taken')
                exist = True
            elif i[4] == row[4]:
                st.warning('Name is already present')
                exist = True

    if not exist: 
        login = True
        row = [int(serial), '', Id, '', name]
        with open('StudentDetails\StudentDetails.csv', 'a+',newline='') as csvFile:
            writer = csv.writer(csvFile)
            writer.writerow(row)
        csvFile.close()
        
        col_names = ['Id', 'Name','Date','Time']
        exists = os.path.isfile("D:\\Akshat\\Project\\Attendance\\Attendance_" + date + ".csv")
        if not exists:
            
            with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + date + ".csv", 'w',newline='') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)

        if ((name.isalpha()) or (' ' in name)):
            cam = cv2.VideoCapture(0)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                
                ret, img = cam.read()
                cv2.putText(img, "Press q to close camera", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("TrainingImage\ " + name + "." + str(serial) + "." + Id + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Taken for ID : " + Id
            
        else:
            if (name.isalpha() == False):
                res = "Enter Correct name"
    


########################################################################################

def TrainImages():
    assure_path_exists("TrainingImageLabel/")
    recognizer = cv2.face_LBPHFaceRecognizer.create()
    harcascadePath = "haarcascade_frontalface_default.xml"
    detector = cv2.CascadeClassifier(harcascadePath)
    faces, ID = getImagesAndLabels("TrainingImage")
    try:
        recognizer.train(faces, np.array(ID))
    except:
        return
    recognizer.save("TrainingImageLabel\Trainner.yml")
    res = "Profile Saved Successfully"
    

############################################################################################3

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids

###########################################################################################

def TrackImages():
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    col_names = ['Id', 'Name','Date','Time']
    exists = os.path.isfile("D:\\Akshat\\Project\\Attendance\\Attendance_" + date + ".csv")
    if not exists:
        with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + date + ".csv", 'w',newline='') as csvFile1:
            writer = csv.writer(csvFile1)
            writer.writerow(col_names)

    assure_path_exists("StudentDetails/")
    
    msg = ''
    i = 0
    j = 0
    recognizer = cv2.face.LBPHFaceRecognizer_create()  # cv2.createLBPHFaceRecognizer()
    exists3 = os.path.isfile("TrainingImageLabel\Trainner.yml")
    if exists3:
        recognizer.read("TrainingImageLabel\Trainner.yml")
    else:
        return
    harcascadePath = "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(harcascadePath);

    cam = cv2.VideoCapture(0)
    font = cv2.FONT_HERSHEY_SIMPLEX
    col_names = ['Id', 'Name', 'Date', 'Time']
    exists1 = os.path.isfile("StudentDetails\StudentDetails.csv")
    if exists1:
        df = pd.read_csv("StudentDetails\StudentDetails.csv")
    else:
        cam.release()
        cv2.destroyAllWindows()
    while True:
        ret, im = cam.read()
        cv2.putText(im, "Press q to close camera", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0),2)
        gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, 1.2, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(im, (x, y), (x + w, y + h), (225, 0, 0), 2)
            serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
            if (conf < 50):
                ts = time.time()
                date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                aa = df.loc[df['SERIAL NO.'] == serial]['NAME'].values
                
                ID = df.loc[df['SERIAL NO.'] == serial]['ID'].values
                ID = str(ID)
                
                ID = ID[1:-1]
                
                bb = str(aa)
                
                bb = bb[2:-2]
                
                attendance = [str(ID), bb, str(date),str(timeStamp)]
                
                

            else:
                Id = 'Unknown'
                bb = str(Id)
            cv2.putText(im, str(bb), (x, y + h), font, 1, (255, 255, 255), 2)
        cv2.imshow('Taking Attendance', im)
        if (cv2.waitKey(1) == ord('q')):
            break
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    
    
    
    with open("StudentDetails\StudentDetails.csv", 'r') as csvFile1:
        reader1 = csv.reader(csvFile1)
        i=0
        for lines in reader1:
            if i==0:
                i+=1
                continue
            else:
                i+=1
                if str(lines[4])==str(attendance[1]):
                    attendance[0]=lines[0]
    iidd = str(attendance[0])
    
    with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + date + ".csv", 'r',newline='') as csvFile1:
        reader1 = csv.reader(csvFile1)
        i=0
        for lines in reader1:
            if lines==[]:
                continue
            i = i + 1
            if (i > 1):
                iidd = str(lines[0]) + '   '

    with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + date + ".csv", 'r',newline='') as csvFile1:
        reader=csv.reader(csvFile1)
        flag = True
        for i in reader:
            if i!=[] and attendance!=[] and attendance!=['','','','']:
                if str(i[1])==str(attendance[1]):
                    flag = False
                    break
            else:
                flag = False

        if flag:
            with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + date + ".csv", 'a',newline='') as csvFile1:
                writer1 = csv.writer(csvFile1)
                writer1.writerow(attendance)

    cam.release()
    cv2.destroyAllWindows()


def view_attendance():
    st.subheader('By date')

    st.write('\n')

    d_input = st.date_input("Choose the date",datetime.date(2022, 1, 1))

    reqd_date = d_input.strftime("%d/%m/%Y")
    reqd_date = str(reqd_date)
    reqd_date = reqd_date.replace("/","-")
    st.subheader(reqd_date)

    d=[]

    try:
        
        with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + reqd_date + ".csv", 'r',newline='') as csvFile1:
            reader = csv.reader(csvFile1)
            for i in reader:
                d.append(i)
            d.pop(0)
            df = pd.DataFrame(d,columns=["ID","Name","Date","Time"])

        total = 0
        with open("StudentDetails\StudentDetails.csv", 'r')as file:
                reader = csv.reader(file)
                for i in reader:
                    total+=1
        total -= 1 

        strength = 0
        with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + reqd_date + ".csv", 'r',newline='') as file:
                reader = csv.reader(file)
                for i in reader:
                    strength+=1
        strength -= 1

        att = strength/total * 100
        att = round(att,2)
        att = str(att) + '%'

        col1, col2, col3 = st.columns(3)
        col1.metric("Number of students present", strength)
        col2.metric("Total no of students", total)
        col3.metric("Overall attendance", att)

        st.write('Table: ')
    
        gb = GridOptionsBuilder.from_dataframe(df)
        gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
        gb.configure_side_bar() #Add a sidebar
        gb.configure_selection('multiple', use_checkbox=True) #Enable multi-row selection
        gb.configure_default_column(enablePivot=False, enableValue=True, enableRowGroup=True)
        gridOptions = gb.build()

        grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode='MODEL_CHANGED', 
        fit_columns_on_grid_load=False,
        theme='blue', #Add theme color to the table
        enable_enterprise_modules=True
        )
    
        data = pd.DataFrame(grid_response["selected_rows"])

        st.subheader("View selected rows below ⬇: ")
        st.text("")
        st.table(data)
        st.text("")

        
    
    except:
        st.write("There is no attendance data of this date as of now")


def find_specific_attendance():
    st.subheader("Specific student")
    name = st.text_input('Enter the name of the student:')
    temp = False

    if name:

        with open("StudentDetails\StudentDetails.csv", 'r')as file:
                reader = csv.reader(file)
                for i in reader:
                    if i[4].lower() == name.lower():
                        temp = True

        present = 0
        files = os.listdir ('D:\\Akshat\\Project\\Attendance')
        total = len(files)
        present_dates=[]
        absent_dates=[]

        for i in files:
            flag = False
            with open("D:\\Akshat\\Project\\Attendance\\"+i, 'r',newline='') as file:
                reader = csv.reader(file)
                for j in reader:
                    if j[1].lower() == name.lower():
                        present+=1
                        present_dates.append(j)
                        flag = True
                        break
            if not flag:
                absent_dates.append(i)

                

        with st.spinner('Loading...'):
            time.sleep(0.5)

        if temp:
            att = present/total*100
            att = round(att,2)
            att = str(att) + '%'
            absent = total - present

            col1, col2, col3 = st.columns(3)
            col1.metric("No of days present", present)
            col2.metric("Total no of days", total)
            col3.metric("Attendance", att)

            fig = go.Figure(
            go.Pie(
            labels = ["Present","Absent"],
            values = [present,absent],
            hoverinfo = "value",
            textinfo = "label+percent"
            ))

            st.write("Pie chart")
            st.plotly_chart(fig)

           
            with st.expander("Present on 🅿:", expanded=False):
                for i in present_dates:
                    st.write(i[2])

            with st.expander("Absent on 🅰:", expanded=False):
                for i in absent_dates:
                    st.write(i.lstrip('Attendance_').rstrip('.csv'))

        else:
            st.write("There is no such student")


def manual():
    name = st.text_input('Enter the student name: ')
    date = st.date_input('Enter the date: ',datetime.date(2022, 1, 1))
    time_input = st.time_input('Enter the time: ',datetime.time(00,00))
    id=''
    
    if st.button('Enter attendance'):

        if name:

            with open('StudentDetails\StudentDetails.csv','r') as file:
                reader = csv.reader(file)
                exist = False

                for i in reader:
                    if i[4]==name:
                        id = i[2]
                        exist = True
                        break

                if exist:

                    

                    reqd_date = date.strftime("%d/%m/%Y")
                    reqd_date = str(reqd_date)
                    reqd_date = reqd_date.replace("/","-")

                    try:
                        present = False
                        with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + reqd_date + ".csv", 'r',newline='') as file:
                            reader = csv.reader(file)
                            for i in reader:
                                if i[1]==name:
                                    present = True

                        if present:
                            
                            st.warning("The student's attendance is already present")

                        else:
                            my_bar = st.progress(0)

                            for percent_complete in range(100):
                                time.sleep(0.01)
                                my_bar.progress(percent_complete + 1)

                            with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + reqd_date + ".csv", 'a',newline='') as file:
                                writer = csv.writer(file)
                                writer.writerow([id,name,reqd_date,time_input])
                            st.success("Profile saved succesfully! 🎉")
                    
                    except:
                        my_bar = st.progress(0)
                        for percent_complete in range(100):
                                time.sleep(0.01)
                                my_bar.progress(percent_complete + 1)
                        col_names = ['Id', 'Name','Date','Time']
                        with open("D:\\Akshat\\Project\\Attendance\\Attendance_" + reqd_date + ".csv", 'w',newline='') as file:
                            writer = csv.writer(file)
                            writer.writerow(col_names)
                            writer.writerow([id,name,reqd_date,time_input])
                            st.success("Profile saved succesfully! 🎉")
                        

                else:
                    st.warning('There is no such student')

        else:
            st.warning('Enter the student name first')

def student_details():

    d=[]
    with open("StudentDetails\StudentDetails.csv", 'r')as file:
        reader = csv.reader(file)
        for i in reader:
            i.pop(1)
            i.pop(2)
            d.append(i)
        d.pop(0)

    df = pd.DataFrame(d,columns=["SERIAL NO.","ID","NAME"])

        
    gb = GridOptionsBuilder.from_dataframe(df)
    gb.configure_pagination(paginationAutoPageSize=True) #Add pagination
    gb.configure_side_bar() #Add a sidebar
    gb.configure_default_column(enablePivot=False, enableValue=True, enableRowGroup=True)
    gridOptions = gb.build()

    grid= AgGrid(
    df,
    gridOptions=gridOptions,
    data_return_mode='AS_INPUT', 
    update_mode='MODEL_CHANGED', 
    fit_columns_on_grid_load=False,
    theme='light', 
    enable_enterprise_modules=True
    )

def overall_attendance():    

    names=[]
    data=dict()

    with open("StudentDetails\StudentDetails.csv", 'r')as file:
        reader = csv.reader(file)
        for i in reader:
            names.append(i[4])
    names.pop(0)
    data = dict.fromkeys(names,0)
    

    files = os.listdir('D:\\Akshat\\Project\\Attendance')

    for i in files:
        with open("D:\\Akshat\\Project\\Attendance\\"+i, 'r',newline='') as file:
            reader = csv.reader(file)
            for j in reader:
                for k in data.keys():
                    
                    if j[1] == k:
                        data[k]+=1
    d={}

    d['Name'] = data.keys()
    d['No of days present'] = data.values()

    df = pd.DataFrame.from_dict(d) 

    tab1, tab2 = st.tabs(["Table", "Chart 📊"])

    with tab1:
        
        st.subheader('Overall Attendance table')

        with st.container():
            st.write(df)
        

    with tab2:
        st.subheader('Overall Attendance chart')

        with st.container():
            fig = px.bar(df, x='Name', y='No of days present',
             color='Name',
             title="Class Attendance",
             labels={'pop':'Attendance'}, height=500)
            st.plotly_chart(fig) 
            

#################################################################################################################################

def main_code():
    global date
    global time
    global month
    global year
    ts = time.time()
    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
    day,month,year=date.split("-")
    st.sidebar.header('DASHBOARD ')
    menu = ['<Select>','Register','View Student Details','Take Attendance','View Attendance','Add Attendance Manually ✍']
    choice = st.sidebar.selectbox('MENU',menu)  

    if choice == '<Select>':
        st.subheader('WELCOME 👋')
        st.write('Select the options from the Menu')


    elif choice == 'Register':
        st.image('https://blog.langlion.com/en/wp-content/uploads/2014/10/register-button.jpg')
        global Id
        global name
        Id,name='',''
        Id = st.text_input('Enter ID: ')
        name = st.text_input('Enter name: ')
        train_save = st.button('Train images and Save profile')
        taken = False

        if train_save:
            if Id!='' and name!='':
                

                TakeImages()

                if login:
                    st.success("Images taken ")
                    TrainImages()

                    my_bar = st.progress(0)

                    for percent_complete in range(100):
                        time.sleep(0.01)
                        my_bar.progress(percent_complete + 1)

                    st.success("Profile saved succesfully!")
                    

            else:
                st.warning('Please fill in the ID and name first')    
        

    elif choice == 'Take Attendance':

        st.subheader('Take Attendance ')
        st.image('https://static.thenounproject.com/png/7792-200.png')
        with st.spinner('Opening camera...'):
            time.sleep(1)
        TrackImages()
        st.info("Camera closed ")

    elif choice == 'View Attendance':
        st.subheader('View Attendance 🔎')
        option = st.selectbox(
        'Options:',
        ('<Select>','By date', 'By student','Overall attendance'))

        if option == 'By date':

            view_attendance()

        elif option == 'By student':

            find_specific_attendance()
        
        elif option == 'Overall attendance':
            overall_attendance()      

        


    elif choice == 'Add Attendance Manually ✍':
        st.subheader('Add Attendance Manually')

        st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSPKhr4qdUgIRxwC5rfQhQWq8D7zTxPuxnhGlXOyZ1OTKtCfHIhf9Lc2_mxITsEU-GsUlU&usqp=CAU')
        
        manual()
    elif choice == 'View Student Details':
        st.image('https://electricalworkbook.com/wp-content/uploads/2018/09/c_stu-1024x440.png')
        student_details()


    
login = False

main_code()