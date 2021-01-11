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

BG="resources/98desktop.png"

def st_function(hide_text):
    st.title("1- Generacion de Input")
    if hide_text:
        st.header("Runescape")
        parrafo_runescape = '''
        Runescape es un MMORPG [Juego de rol multijugador online] que **anima a sus usuarios a realizar tareas repetitivas** para conseguir recursos, 
        que pueden ser intercambiados con otros jugadores. Todo lo repetitivo atrae a programadores, 
        y **Runescape tuvo que implementar técnicas para parar la avalancha bots en el juego** *[1][2]*.

        Mientras que **las técnicas exactas que usan no son públicas**, 
        los **bots que esquivan la detección suelen implementar técnicas que simulan movimientos de raton humanos** *[2][3]*.
        '''
        st.markdown(parrafo_runescape)
        img_runescape = Image.open("resources/runescape.jpeg")
        st.image(img_runescape, "Cuenta de Runescape controlada por un bot", use_column_width=True)

        ###
        # Mouse
        st.header("Mouse dynamics")
        parrafo_mouse_dyn = '''
        Algo que es muy fácil hacer mal al programar un bot, son los movimientos del cursor.  

        ** *Ninguna persona* pulsa repetidas veces en el mismo píxel**, y mucho menos **mueve el raton en línea recta** como una torre en ajedrez...
        '''
        st.markdown(parrafo_mouse_dyn)

        st.header("Sistema propuesto")
        st.subheader("Objetivo")
        st.markdown("Un sistema que simule como un humano mueve el raton 🖱️.")
        st.subheader("Funcionamiento")
        parrafo_sistema_mouse_1 = '''
        Nuestro sistema se basa **simular las trayectorias de nuestro raton con curvas de bezier** [4],
        a las cuales le **añadimos desperfectos** como **cambios de velocidad** al decelerar,
        **errores de detección** de la superficie por parte del raton, y **pequeñas desviaciones**.
        '''
        st.markdown(parrafo_sistema_mouse_1)

        parrafo_paso1 = '''
         1. Generamos una trayectoria con la fórmula cúbica de las curvas de bézier,
            los dos puntos de anclaje son aleatorios, y están delimitados por la desviación máxima.
            
            La formula para puntos discretos de una curva de Bezier esta dada por la siguiente formula:
        '''

        st.markdown(parrafo_paso1)
        st.latex(r'''
        \mathbf{B}(t)=\mathbf{P}_0(1-t)^3+3\mathbf{P}_1t(1-t)^2+3\mathbf{P}_2t^2(1-t)+\mathbf{P}_3t^3  ,  t \in [0,1].
        ''')

        parrafo_curva ='''
         2. Para simular cambios de velocidad y errores del sensor del raton
            **sacaremos puntos de una distribución triangular aleatoria** *[5]*, 
            por lo que habra más puntos cerca del final, 
            **imitando el el aceleramiento inicial y el ralentizamiento al acabar el movimiento** *[6]*.

            La densidad de una distribucion aleatoria esta dada por la siguiente formula:
        '''
        st.markdown(parrafo_curva)
        st.latex(r'''f(x|a,b,c)= \begin{cases}
            \frac{2(x-a)}{(b-a)(c-a)} & \text{para } a \le x < c, \\[4pt]
            \frac{2}{b-a}             & \text{para } x = c, \\[4pt]
            \frac{2(b-x)}{(b-a)(b-c)} & \text{para } c < x \le b, \\[4pt]
            0                         & \text{para otros casos}
            \end{cases}
        ''')
        st.image("resources/distribucion_triangular.png", 
                "100000 numeros aleatorios sacados de una distribucion triangular con pico en 0 (por numpy.org)",
                use_column_width=False)
        
        parrafo_curva_2 ='''
         3. **Añadimos ruido a la curva**. Para ello **necesitamos una forma de calcular
            desviaciones, sin desviar la curva de su objetivo final**.

            Para ello añadimos desviaciones por pares, es decir, **escogemos parejas de puntos aleatorias**
            y **les añadimos el mismo vector en direcciones opuestas**, por lo que se cancelan. 
        '''
        st.markdown(parrafo_curva_2)

    ## INTERACTIVE
    st.header("Ejemplo interactivo")
    st.markdown("#### Aqui puedes probar el sistema que genera trayectorias de raton realistas")
    
    st.image("resources/mouse_linear.gif", "Movimiento linear como referencia", use_column_width=True)

    max_deviation = st.slider("Desviacion maxima", 0., 1., 0.2, 0.1)
    progre_triangular = st.checkbox("Generar cambios de velocidad")
    ruido = st.checkbox("Añadir ruido")
    seed = st.number_input("Semilla para el generador de numeros aleatorios", 0, (2**32)-1, 1234)


    if st.button("Generar trayectoria"):
        parrafo_notas = '''
        ##### > La conversion a gif puede tardar.
        ##### > Si se sale de la pantalla, es como si empujaramos el cursor contra el borde.
        ##### > Estas animaciones no representan todos los puntos que genera nuestro sistema, son solo ilustrativas.
        '''
        st.markdown(parrafo_notas)

        # Calculate straight line
        fname = get_animation(max_deviation, seed, curve=True, lineal= not progre_triangular, noise=ruido)
        
        # Show animation
        with open(fname, "rb") as f:
            contents = f.read()
        st.image(contents, "Trayectoria generada", use_column_width=True)

    st.markdown('---')

    if hide_text:
        citations = {
            1:"https://oldschool.runescape.wiki/w/Botting",
            2:"https://secure.runescape.com/m=forum/forums?317,318,513,66181144",
            3:"https://github.com/xvol/bezmouse",
            4:"https://es.wikipedia.org/wiki/Curva_de_B%C3%A9zier",
            5:"https://es.wikipedia.org/wiki/Distribuci%C3%B3n_triangular",
            6:"https://arxiv.org/pdf/2005.00890.pdf"
        }

        footer = ""
        for k, v in citations.items():
            footer += f"[{k}] {v}\n"
        st.text(footer)

    st.markdown("#### ⬅️⬅️⬅️ Continua en la proxima seccion  ")

@st.cache(suppress_st_warning=True)
def get_animation(max_deviation, seed, 
                curve=True,
                lineal=False, 
                noise=False):
    background = plt.imread(BG)
    bg_h = background.shape[0]
    bg_w = background.shape[1]

    origin = (bg_w//4, bg_h//2)
    dest = (3*bg_w//4, bg_h//2)

    if not curve:
        p = abs(dest[1]-origin[1])/abs(dest[0]-origin[0])
        mult_x = np.sign(dest[0]-origin[0])
        mult_y = np.sign(dest[1]-origin[1])

        points = []

        for step in range(0, abs(origin[0] - dest[0]), 30):
            points.append((origin[0] + mult_x*step, origin[1] + mult_y*step*p))
        points = np.array(points)

    else:
        # Get curve params
        p_0 = np.array([origin[0]/bg_w, origin[1]/bg_h])
        p_3 = np.array([dest[0]/bg_w, dest[1]/bg_h])
        mouse = Mouse((bg_w, bg_h))
        np.random.seed(seed)
        points = mouse.generate_cubic_bezier(p_0, p_3, max_deviation=max_deviation, n_steps=40, linear_progression=lineal)
        np.random.seed()

        points[:, 0] *= bg_w
        points[:, 1] *= bg_h

        if noise:
            np.random.seed(seed)
            points = mouse.add_noise(points, 0.3, 1)
            np.random.seed()

    # Create animation
    def update(i):
        ax.scatter(points[:i-1,0], points[:i-1,1], color="moccasin")
        ax.scatter(points[0][0], points[0][1], marker='x', color="yellow")
        ax.scatter(points[i,0], points[i,1], color="darkorange")
        # Plot start and end
        return ax

    # Get bg proportions
    fig, ax = plt.subplots(figsize=(bg_w/100, bg_h/100))
    fig.set_tight_layout(True)
    ax.axis("off")

    ax.set_facecolor('black')
    ax.imshow(background)
    ax.plot(points[:,0], points[:,1], color="moccasin")
    ax.scatter(points[-1][0], points[-1][1], marker='x', color="red")

    filename = ''.join([choice(ascii_letters) for _ in range(7)])
    filename = f'/tmp/{filename}.gif'

    anim = FuncAnimation(fig, update, frames=len(points)-1, interval=200)
    anim.save(filename, writer='imagemagick')

    return filename
