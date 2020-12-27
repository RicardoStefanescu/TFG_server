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

from include.mouse import Mouse 
from include.keyboard import Keyboard
from include.keyboard_layouts import us_layout

def st_function():
    mouse = Mouse()
    keyboard = Keyboard(us_layout, 123123)

    st.title("1- Generacion de Input")
    st.header("Cadencia al escribir")
    ### 
    # Text
    text = st.text_input("Texto a escribir con cadencia \"humana\"")
    stress = st.slider("Estres", 0., 1., 0.2, 0.01)
    em = st.empty()
    em.markdown(f"Salida del bot\n\n\t")

    if st.button("Escribir"):
        keys = keyboard.generate_keys(text, stress)

        st.subheader("Estas son las teclas que presiona el bot")
        df = pd.DataFrame(
            keys,
            columns=("Tecla", "Mayus", "Tiempo entre teclas", "Tiempo presionada"))
        st.table(df)

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

    ###
    # Mouse
    st.markdown('---')
    st.header("Movimientos de cursor")

    st.markdown("Queremos ser capaces de generar movimientos de mouse imperfectos, y realistas temporalmente entre \
    dos puntos de la pantalla.")
    
    origin_x = 1920
    origin_y = 1080
    dest_x = st.number_input("Objetivo X", 0, 3840, 1000)
    dest_y = st.number_input("Objetivo Y", 0, 2160, 800)
    max_deviation = st.slider("Desviacion maxima", 0., 1., 0.2, 0.01)

    if st.button("Generar animaciones"):
        # Animacion linea recta
        st.subheader("Movimiento en linea recta")
        # Calculate straight line
        p = abs(dest_y-origin_y)/abs(dest_x-origin_x)
        mult_x = np.sign(dest_x-origin_x)
        mult_y = np.sign(dest_y-origin_y)

        points = []
        for step in range(0, abs(origin_x - dest_x), 60):
            points.append((origin_x + mult_x*step, origin_y + mult_y*step*p))
        points = np.array(points)
        
        fname = ''.join([choice(ascii_letters) for _ in range(7)])
        show_animation(points, fname)

        # Animacion curva
        st.subheader("Movimiento en curva")
        p_0 = np.array([origin_x/3840, origin_y/2160])
        p_3 = np.array([dest_x/3840, dest_y/2160])
        np.random.seed(123123)
        points = mouse.generate_cubic_bezier(p_0, p_3, max_deviation=max_deviation, n_steps=30, linear_progression=True)
        np.random.seed()

        points[:, 0] *= 3840
        points[:, 1] *= 2160

        fname = ''.join([choice(ascii_letters) for _ in range(7)])
        show_animation(points, fname)

        # Animacion curva
        st.subheader("Movimiento en curva con cambio de velocidad y errores de sensor")
        np.random.seed(123123)
        points = mouse.generate_cubic_bezier(p_0, p_3, max_deviation=max_deviation, n_steps=40, linear_progression=False)
        np.random.seed()

        points[:, 0] *= 3840
        points[:, 1] *= 2160

        fname = ''.join([choice(ascii_letters) for _ in range(7)])
        show_animation(points, fname)

def show_animation(points, filename):
    def update(i):
        label = f't = {i}'
        ax.set_xlabel(label)
        
        ax.scatter(points[:i-1,0], points[:i-1,1], color="cornflowerblue")
        ax.scatter(points[i,0], points[i,1], color="blue")
        # Plot start and end
        ax.scatter(points[0][0], points[0][1], marker='x', color="yellow")
        ax.scatter(points[-1][0], points[-1][1], marker='x', color="red")
        return ax

    filename = f'/tmp/{filename}.gif'
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)
    
    # Create a Rectangle patch
    rect = patches.Rectangle((0,0),3840,2160, linewidth=2, edgecolor='black', facecolor='none')

    # Add the patch to the Axes
    ax.add_patch(rect)

    anim = FuncAnimation(fig, update, frames=len(points)-1, interval=200)
    anim.save(filename, dpi=80, writer='imagemagick')

    # Show animation
    with open(filename, "rb") as f:
        contents = f.read()
        data_url = base64.b64encode(contents).decode("utf-8")

    st.markdown(
        f'<img src="data:image/gif;base64,{data_url}" alt="animation">',
        unsafe_allow_html=True,
    )
