import time
import base64
from string import ascii_letters
from random import choice

import streamlit as st

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
from PIL import Image

from include.mouse import Mouse 
from include.keyboard import Keyboard
from include.keyboard_layouts import us_layout

def st_function(hide_text):
    st.title("1- Generacion de Input")
    if not hide_text:
        st.header("Telegrafistas")
        parrafo_telegraf = '''
        En la primera y segunda guerra mundial la mejor forma de comunicacion a largas distancias era el telegrafo.
        **Los telegrafistas eran capaces de identificar aliados y enemigos**, incluso a individuales **por su cadencia**
        con el telegrafo. **A este concepto se le llamo "Puño del emisor"** ["Fist of the sender"], y es uno de los
        precursores de la biometria del comportamiento *[1]*. 

        Actualmente este estudio de la cadencia ha evolucionado y **se ha convertido en un campo de estudio para la
        autentificacion no intrusiva de usuarios.** Un ejemplo de ello es TypingDNA *[2]*, que complementa a contraseñas
        mirando como los usuarios teclean.
        '''
        st.markdown(parrafo_telegraf)
        st.image("resources/telegrafista.jpeg", "Operador de radio del Ejército de EE.UU. en Nueva Guinea en 1943", use_column_width=True)

        st.header("Keystroke dynamics")
        parrafo_keystroke = '''
        Todos tenemos una letra distinta, **lo mismo ocurre con como escribimos en nuestro teclado**. 
        Posiblemente tu abuela escriba con un dedo buscando las letras, mientras que tú usas diferentes dedos para diferentes teclas.
        Estos cambios generan **variaciones en cuanto tiempo se tarda de tecla a tecla, 
        y cuanto tiempo se aguanta cada tecla pulsada** (así como otros muchos factores). 

        **El estudio de estos tiempos se usa ampliamente en la autenticación de usuarios y la detección de bots** *[3]*.
        '''
        st.markdown(parrafo_keystroke)

        st.header("Sistema propuesto")
        st.subheader("Objetivo")
        st.markdown("Un sistema que teclea con cadencia humana.")
        st.subheader("Funcionamiento")
        parrafo_sistema_key_1 = '''
        **Nuestro sistema genera dos matrices de tiempos**, una entre pares de teclas y otra de tiempos de presionado. 
        Posteriormente toma el texto a teclear, **una semilla que identifica su Puño/Cadencia** (imagínate el dni de cada bot),
        y por ultimo **un valor que simboliza estrés**, que **modifica la velocidad y la cantidad de errores** al teclear.

        Los pasos que sigue es:

         1. Calcula **cuanto tarda entre entre pares de teclas**.
         2. Calcula **cuanto tiempo presiona cada tecla**.
         3. **Genera la secuencia de teclas** dado un *texto* y un valor de *estres*.
         4. **Teclea la secuencia.**
        '''
        st.markdown(parrafo_sistema_key_1)

    # INTERACTIVO
    st.header("Ejemplo interactivo")
    st.markdown("#### Aqui puedes probar el sistema que teclea como un humano")

    text = st.text_input("Texto a escribir")
    seed = st.number_input("Semilla del puño del bot", 0, 2**32-1, 123123, 1)
    stress = st.slider("Estres", 0., 1., 0.2, 0.01)

    keys = get_keys(us_layout, seed, text, stress)

    st.subheader("Teclas y tiempos generados por nuestro sistema:")
    df = pd.DataFrame(
        keys,
        columns=("Tecla", "Mayus", "Tiempo entre teclas", "Tiempo presionada"))

    # Change mayus to true false
    df.loc[df.Mayus == "1", "Mayus"] = "True"
    df.loc[df.Mayus == "0", "Mayus"] = "False"

    # Apply style
    df = df.style.background_gradient(cmap='YlOrRd',subset=['Tiempo presionada', "Tiempo entre teclas"])

    # Transform backspaces to red
    style_backspace = lambda val: "color: red" if val == 'backspace' else ""
    df = df.applymap(style_backspace)

    st.table(df)

    parrafo_sistema_key_2 = '''
    Como podemos ver, **el sistema separa el texto en las teclas que debe pulsar**,
    **el tiempo que espera al pulsar** cada una, y **el tiempo que las mantiene pulsado**.
    Pulsa *Escribir* para ver una simulacion de como lo introduciria un bot.
    '''
    st.markdown(parrafo_sistema_key_2)

    if st.button("Escribir"):
        em = st.empty()
        em.markdown(f"Salida del bot\n\n\t ~")
        time.sleep(2)

        display_text = ""
        for k in keys:
            time.sleep(k[2])
            char = k[0]
            if char == 'space':
                display_text += ' '
            elif char == 'return':
                display_text += '\n'
            elif char == 'tab':
                display_text += '\t'
            elif char == 'backspace':
                display_text = display_text[:-1]
            else:
                display_text += char if not k[1] else char.capitalize()
            time.sleep(k[3])
            em.markdown(f"Salida del bot (escribiendo)\n\n\t{display_text}")
        em.markdown(f"Salida del bot\n\n\t{display_text}")

    st.markdown('---')
    if hide_text:
        citations = {
            1:"https://www.researchgate.net/publication/253642686_The_physiology_of_keystroke_dynamics",
            2:"typingdna.com",
            3:"https://www.tesisenred.net/bitstream/handle/10803/461468/DorcaJosaAleix-Thesis.pdf#section.2.2",
        }

        footer = ""
        for k, v in citations.items():
            footer += f"[{k}] {v}\n"
        st.text(footer)

    st.markdown("#### ⬅️⬅️⬅️ Continua en la proxima seccion  ")

@st.cache
def get_keys(layout, seed, text, stress):
    keyboard = Keyboard(us_layout, seed)
    return keyboard.generate_keys(text, stress)