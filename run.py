import streamlit as st

from modules.module_intro import st_function as st_intro
from modules.module_mouse import st_function as st_mouse
from modules.module_keyboard import st_function as st_keyboard
from modules.module_reaction import st_function as st_reaction
from modules.module_scheduling import st_function as st_scheduling
from modules.module_imggen import st_function as st_imggen
from modules.module_textgen import st_function as st_textgen


def todo():
    st.title("🚧 WIP 🚧")

st.set_page_config(page_title='TFG - Ricardo S.', page_icon = "🤖", initial_sidebar_state = 'auto')

st.sidebar.title("Resumen interactivo de TFG")
st.sidebar.header('"Contramedidas para técnicas de detección de bots en RRSS."')
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
            p {
                text-align: justify;
            } 
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True) 


modules = {'0- Introduccion 🤖' : st_intro,
            '1- Raton humano 🖱️': st_mouse,
            '2- Cadencia humana ⌨️': st_keyboard,
            '3- Activaciones 💤': st_scheduling,
            '4- Reaccion a texto 🤔': st_reaction,
            '5- Sintesis de imagenes 📷': st_imggen, 
            '6- Sintesis de texto 📖': st_textgen,}
            #'7- Conclusion 📜': todo}


selection = st.sidebar.selectbox("Seccion", list(modules.keys()))
hide_text = st.sidebar.checkbox("Solo quiero jugar con las herramientas, no que me cuentes tu vida.")

func = modules.get(selection)
func(hide_text)
