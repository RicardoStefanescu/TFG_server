import streamlit as st

from modules.module_intro import st_function as st_intro
from modules.module_input import st_function as st_input
from modules.module_imggen import st_function as st_imggen


def todo():
    st.title("🚧 WIP 🚧")

st.set_page_config(page_title='TFG - Ricardo S.', page_icon = "🤖", initial_sidebar_state = 'auto')

st.sidebar.title("Contramedidas para técnicas de detección de bots en RRSS.")
st.sidebar.text("TFG GIC UAH - Ricardo S.\nTutor: Manuel Sanchez Rubio")

hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            footer:after {
                content:'Contramedidas para técnicas de detección de bots en RRSS. - Ricardo S. | Tutor: Manuel Sanchez Rubio'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 2px;
            }
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


modules = {'0- Introduccion 🤖' : st_intro,
            '1- Input 🖐️': st_input,
            '2- Fingerprinting 🔍': todo,
            '3- Generacion de imagenes 🖼️': st_imggen, 
            '4- Generacion de texto 📖': todo, 
            '5- Reaccion a texto 🤔': todo}

selection = st.sidebar.selectbox("Seccion", list(modules.keys()))

func = modules.get(selection)
func()
