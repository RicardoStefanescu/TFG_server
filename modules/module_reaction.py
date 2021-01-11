import streamlit as st

import pandas as pd
from PIL import Image

from include.reaction import estimate_reaction, Interest


def st_function(hide_text):
    st.title("Reaccion a contenido")
    if hide_text:
        # Ejemplo de mi sobrino
        st.header("El enano")
        parrafo_enano = '''
        **Tengo un sobrino de 5 años**. Es una personita feliz.  \
        
        De vez en cuando **su madre le deja mirar su Instagram**, y **sigue un patron muy simple**, \
        si tiene que ver con **Mario, bomberos o coches, le encanta**.  \
        
        Si tiene que ver con **perros o patos, se asusta** y deja el movil.
        '''
        st.markdown(parrafo_enano)

        # Intro
        st.header("Reactividad")
        parrafo_intro = '''
        El uso normal de redes sociales incluye **interactuar con el contenido publicado por \
        otras cuentas**. Si queremos crear bots parezcan personas, **debemos conseguir \
        que interactuen con cuentas** que publican contenido acorde a sus intereses. \
        
        Para ello **hemos programado un sistema que genera una reaccion a partir de un texto \
        y unos intereses**. 
        '''
        st.markdown(parrafo_intro)

        # Explicacion de interes y reaccion
        st.header("Reacciones e Intereses")
        parrafo_reac = '''
        Para nosotros, **una reaccion tiene dos valores**, **la intensidad**, que representa **como \
        de fuerte es**, y **la polaridad**, que representa si es **buena o mala**.  \
        '''
        st.markdown(parrafo_reac)

        img = Image.open("resources/diagramaemojis.jpg")
        st.image(img, caption="Ejes de una reaccion")

        parrafo_interes = '''
        **Un interes es un prejuicio sobre un tema**, por lo que **tiene los mismos valores que una reaccion**, \
        a los que enlaza con unas **palabras clave**.  \
        '''
        st.markdown(parrafo_interes)

    # INTERACTIVO
    st.header("Ejemplo interactivo")
    parrafo_intro_inter = '''
    **Aqui puedes probar el sistema que calcula la reaccion a un texto dados unos intereses**.  

    A continuacion **exponemos los intereses de mi sobrino**, y un recuadro donde puedes **escribir un texto (en ingles) para estimar su reaccion**. 
    '''
    st.markdown(parrafo_intro_inter)

    # Intereses
    interests = [
        Interest("mario", 0.9, 0.9),
        Interest("firefighter", 0.9, 0.9),
        Interest("fire", 0.9, 0.1),
        Interest("car",0.6, 0.8),
        Interest("trucks",0.6,0.7),
        Interest("dogs",0.9,0),
        Interest("ducks",0.9,0.1)
    ]
    ints = []
    for i in interests:
        ints.append([', '.join(i.get_keywords()), i.get_strenght(), i.get_polarity()])

    df = pd.DataFrame(
        ints,
        columns=("Palabras clave", "Intensidad", "Polaridad"))
    st.table(df)

    parrafo_enano2 = '''
    ##### Estos intereses no han sido simplificados.
    '''
    st.markdown(parrafo_enano2)

    # Ejemplo
    text = st.text_area("Texto al que el enano deberia responder... (en ingles)","I sure enjoy playing Super Mario")

    intensity, polarity = estimate_reaction(text, interests, bayes=False)

    emojis = [
        ['😠', '😒', '🤔','😁', '😆'],
        ['☹️', '🙄', '🤨', '🙂', '😀'],
        ['😐', '😐', '😐', '😐', '😐'],
        ['😶', '😶', '😶', '😶', '😶'],
        ['😶', '😶', '😶', '😶', '😶'],
        ['😶', '😶', '😶', '😶', '😶'],
    ]

    i_strenght = int(polarity*5)
    i_intensity = int((1-intensity)*5)

    result_md = '''
    ### El enano opina: {}
    #### Polaridad:  {}  
    #### Intensidad: {}
    '''.format(emojis[i_intensity][i_strenght], polarity, intensity)

    st.markdown(result_md)
