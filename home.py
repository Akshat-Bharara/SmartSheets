import streamlit as st
from PIL import Image

st.header('Project')
st.sidebar.header('Home 🏡')
image = Image.open('D:\Akshat\Project\SmartSheets2.jpeg')
st.image(image)

st.write(
    '''
    
    '''
)

txt = st.text_area('Registration: ', 
'''To register a new student, go to the register page.
If already registered, then go to the SmartSheets page to take and view attendance.
You can also view the About page for more information.
''')

st.write('''

''')

