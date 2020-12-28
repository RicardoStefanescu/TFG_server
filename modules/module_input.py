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

def st_function():
    st.title("1- Generacion de Input")
    st.header("Runescape")
    parrafo_runescape = '''
    Runescape es un MMORPG [Juego de rol multijugador online] que **anima a sus usuarios a realizar tareas repetitivas** para conseguir recursos, 
    que pueden ser intercambiados con otros jugadores. Todo lo repetitivo atrae a programadores, 
    y **Runescape tuvo que implementar técnicas para parar la avalancha bots en el juego** *[1][2]*.

    Mientras que **las técnicas exactas que usan no son públicas**, 
    los **bots que esquivan la detección suelen implementar técnicas que simulan movimientos de mouse,
    y pulsacion de teclas parecidas a las de un usuario legítimo** *[3]*.
    '''
    st.markdown(parrafo_runescape)
    img_runescape = Image.open("resources/runescape.jpeg")
    st.image(img_runescape, "Cuenta de Runescape controlada por un bot", use_column_width=True)

    st.header("Keystroke dynamics")
    parrafo_keystroke = '''
    Todos tenemos una letra distinta, **lo mismo ocurre con como escribimos en nuestro teclado****. 
    Posiblemente tu abuela escriba con un dedo buscando las letras, mientras que tú usas diferentes dedos para diferentes teclas.
    Estos cambios generan **variaciones en cuanto tiempo se tarda de tecla a tecla, 
    y cuanto tiempo se aguanta cada tecla pulsada** (así como otros muchos factores). 

    **El estudio de estos tiempos se usa ampliamente en la detección de bots** y en autenticación de usuarios *[4]*.
    No es nada nuevo, los telegrafistas eran capaces de reconocer con quién estaban hablando por su cadencia escribiendo puntos y líneas *[5]*.
    '''
    st.markdown(parrafo_keystroke)

    st.header("Sistema propuesto")
    parrafo_sistema_key_1 = '''
    **Proponemos un sistema que genera una matriz de tiempos** entre pares de teclas, y tiempos de presionado. 
    A parte de el texto a teclear, **el sistema toma una semilla que identifica la cadencia del bot** (imagínate el dni de cada bot),
    y **un valor que simboliza estrés**, que **modifica la velocidad y la cantidad de errores** al teclear este determinado texto.
    '''
    st.markdown(parrafo_sistema_key_1)

    seed = st.number_input("Semilla", 0, 2**32-1, 123123, 1)
    stress = st.slider("Estres", 0., 1., 0.2, 0.01)
    text = st.text_input("Texto a escribir con cadencia \"humana\"")

    keyboard = Keyboard(us_layout, seed)
    np.random.seed(seed)
    keys = keyboard.generate_keys(text, stress)
    np.random.seed()

    st.subheader("Estas son las teclas que presionaria el bot")
    df = pd.DataFrame(
        keys,
        columns=("Tecla", "Mayus", "Tiempo entre teclas", "Tiempo presionada"))
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
    ###
    # Mouse
    st.header("Mouse dynamics")
    parrafo_mouse_dyn = '''
    Algo que es muy fácil hacer mal al programar un bot, son los movimientos del cursor. 
    ** *Ninguna persona* pulsa repetidas veces en el mismo píxel**, y mucho menos **mueve el mouse en línea recta** como una torre en ajedrez.
    Como la cadencia de tecleo, **la forma de mover el mouse es usada para discernir entre usuarios legítimos y bots** [6].
    '''
    st.markdown(parrafo_mouse_dyn)

    st.header("Sistema propuesto")
    parrafo_sistema_mouse_1 = '''
    Nuestro sistema se basa **simular las trayectorias de nuestro mouse con curvas de bezier** [7],
    a las cuales le **añadimos desperfectos** como **cambios de velocidad** al decelerar,
    **errores de detección** de la superficie por parte del mouse, y **pequeñas desviaciones**.

    Nuestro cursor se encuentra en el centro de la pantalla. 
    Antes de continuar, por favor **elige a donde queremos moverlo, así como la desviación máxima** de nuestra trayectoria.
    '''
    st.markdown(parrafo_sistema_mouse_1)

    mouse = Mouse((3840, 2160))

    origin_x = 1920
    origin_y = 1080
    dest_x = st.number_input("Objetivo X", 0, 3840, 1000)
    dest_y = st.number_input("Objetivo Y", 0, 2160, 800)
    max_deviation = st.slider("Desviacion maxima", 0., 1., 0.2, 0.01)

    if st.button("Continuar"):
        st.markdown("##### Estas animaciones no representan todos los puntos que genera nuestro sistema, son solo ilustrativas")
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

        parrafo_linea_recta ='''
        Como podemos ver una línea recta perfecta no engaña a nadie, vamos a ver que podemos mejorar.  
        Vamos a generar una trayectoria con la fórmula cúbica de las curvas de bézier,
        los dos puntos de anclaje son aleatorios, y están delimitados por la desviación máxima.

        Una curva de bezier esta dada por la siguiente formula:
        '''
        st.markdown(parrafo_linea_recta)
        st.latex(r'''
        \mathbf{B}(t)=\mathbf{P}_0(1-t)^3+3\mathbf{P}_1t(1-t)^2+3\mathbf{P}_2t^2(1-t)+\mathbf{P}_3t^3  ,  t \in [0,1].
        ''')

        # Animacion curva
        curve_seed = np.random.randint(0,2**32-1)

        st.subheader("Movimiento en curva")
        p_0 = np.array([origin_x/3840, origin_y/2160])
        p_3 = np.array([dest_x/3840, dest_y/2160])
        np.random.seed(curve_seed)
        points = mouse.generate_cubic_bezier(p_0, p_3, max_deviation=max_deviation, n_steps=30, linear_progression=True)
        np.random.seed()

        points[:, 0] *= 3840
        points[:, 1] *= 2160

        fname = ''.join([choice(ascii_letters) for _ in range(7)])
        show_animation(points, fname)

        parrafo_curva ='''
        Mientras que la curva es una gran mejora, esta trayectoria **mantiene la misma velocidad y carece de errores**. 
        Para mejorar el diseño, en vez de tomar una serie de puntos igualmente espaciados en la curva, 
        **sacaremos puntos de una distribución triangular aleatoria** *[8]*, 
        por lo que habra más puntos al llegar a nuestro objetivo, 
        **imitando el el aceleramiento inicial y el ralentizamiento al acabar el movimiento** *[9]*.

        La distribucion aleatoria esta dada por la siguiente formula:
        '''
        st.markdown(parrafo_curva)
        st.latex(r'''f(x|a,b,c)= \begin{cases}
            \frac{2(x-a)}{(b-a)(c-a)} & \text{para } a \le x < c, \\[4pt]
            \frac{2}{b-a}             & \text{para } x = c, \\[4pt]
            \frac{2(b-x)}{(b-a)(b-c)} & \text{para } c < x \le b, \\[4pt]
            0                         & \text{para otros casos}
            \end{cases}
        ''')

        # Animacion curva
        st.subheader("Movimiento en curva con cambio de velocidad y errores de sensor")
        np.random.seed(curve_seed)
        points = mouse.generate_cubic_bezier(p_0, p_3, max_deviation=max_deviation, n_steps=40, linear_progression=False)
        np.random.seed()

        points[:, 0] *= 3840
        points[:, 1] *= 2160

        fname = ''.join([choice(ascii_letters) for _ in range(7)])
        show_animation(points, fname)

        parrafo_curva_2 ='''
        Acabamos de conseguir un movimiento con cambios de velocidad, y errores en el sensor. 
        El siguiente paso es añadir pequeñas desviaciones.
        # WIP
        '''
        st.markdown(parrafo_curva_2)

    st.markdown('---')
    citations = {
        1:"https://oldschool.runescape.wiki/w/Botting",
        2:"https://secure.runescape.com/m=forum/forums?317,318,513,66181144",
        3:"https://github.com/xvol/bezmouse",
        4:"https://en.wikipedia.org/wiki/Telegraph_key#%22Fist%22",
        5:"https://www.tesisenred.net/bitstream/handle/10803/461468/DorcaJosaAleix-Thesis.pdf#section.2.2",
        6:"https://www.researchgate.net/publication/336270420_A_Deep_Learning_Approach_to_Web_Bot_Detection_Using_Mouse_Behavioral_Biometrics",
        7:"https://es.wikipedia.org/wiki/Curva_de_B%C3%A9zier",
        8:"https://es.wikipedia.org/wiki/Distribuci%C3%B3n_triangular",
        9:"https://arxiv.org/pdf/2005.00890.pdf"
    }

    footer = ""
    for k, v in citations.items():
        footer += f"[{k}] {v}\n"
    st.text(footer)

def show_animation(points, filename, bg="resources/windows_bg.jpeg", cursor="resources/cursor.svg"):
    def update(i):
        label = f't = {i}'
        ax.set_xlabel(label)

        ax.scatter(points[:i-1,0], points[:i-1,1], color="moccasin")
        ax.scatter(points[0][0], points[0][1], marker='x', color="yellow")
        ax.scatter(points[i,0], points[i,1], color="darkorange")
        # Plot start and end
        return ax

    filename = f'/tmp/{filename}.gif'
    fig, ax = plt.subplots()
    fig.set_tight_layout(True)

    ax.set_facecolor('black')
    img = plt.imread(bg)
    ax.imshow(img, extent=[0, 3840, 0, 2160])
    ax.scatter(points[-1][0], points[-1][1], marker='x', color="red")

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
