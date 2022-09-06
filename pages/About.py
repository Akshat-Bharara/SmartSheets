import streamlit as st

def about():

    st.header('Attendance Monitoring system')

    with st.expander("ℹ️ - About this project", expanded=True):

        st.write(
            """     
    -   This project is an Attendance monitoring system that is built for the benefit of teachers.
    -   The students register their faces through the **Register** tab.
    -   The students have to take their attendance for each day through the **Take Attendance** tab . 
        Attendance of a particular student is marked only once for each day.
    -   The teachers can view the attendance of the students for each day through the **View Attendance** tab.
        The attendance is shown in the form of a table. 
        The attendance of each day is also stored in the attendance folder in the form of a csv file.
    -   To check the individual attendance of a student, go to the **Find Specific Attendance** tab.
        Here, you can view the attendance of a student, the number of days he/she is present.
        A **pie chart** is also provided for a quick glance. 
    -The attendance of an existing student can also be added manually from the **Add Attendance Manually** tab.
            """
        )

    st.image('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSxnzi46iH9e4g55C9Yx20pDlfTIYM0Qq4JuNxY_xthTobIZzzAiQLlgcjjtW0AS5wyQrw&usqp=CAU')
    st.subheader('Developers')
    st.markdown(
        '''
        This project has been developed by **Akshat Bharara**.
        '''
    )

about()