import streamlit as st
import re
from datetime import datetime

from include.resources.tweet_image_generator.generate_tweet_image import gen
from include.text_generation import GPT2

model_path = "include/resources/models/gpt_simple_gen"

def st_function(hide_text):
    st.title("Generacion de lenguaje natural")

    if not hide_text:
        st.header("Lenguaje natural")
        parrafo_nl = '''
        El **lenguaje natural es el lenguage creado espontaneamente por los seres
        vivos con el objetivo de comunicarse** *[1]*. Al haber sido creado sobre la marcha
        **es ambiguo, y depende del contexto**. Esta complejidad causa que procesarlo con
        lenguajes formales, como los usados por los ordenadores, sea extremadamente dificil.
        '''
        st.markdown(parrafo_nl)

        st.header("Como afecta a los bots")
        parrafo_afecta = '''
        La dificultad de procesar lenguaje natural supone que **es muy dificil hacer bots que 
        puedan generar texto dado un contexto**, por ejemplo aquellos que se unan a cadenas
        de tweets, o respondan a otros. Como ultima seccion en este trabajo, queremos crear 
        un sistema que genere texto dados unos temas.
        '''
        st.markdown(parrafo_afecta)

        st.header("GPT")
        parrafo_gpt = '''
        **GPT (Generative Pre-trained Transformer) es una red neuronal creada y pre-entrenada
        por OpenAI [2], usada para tareas de procesamiento de lenguaje natural**. La ultima
        version, GPT-3, aun no ha sido publicada abiertamente. La version **GPT-2 es capaz
        de generar texto dado un contexto**, tiene cuatro tamaños, el mas pequeño teniendo
        117 millones de parametros.
        '''
        st.markdown(parrafo_gpt)

        st.header("Sistema propuesto")
        st.subheader("Objetivo")
        st.markdown("Crear un sistema que genere texto dado un/os tema/s")
        st.subheader("Funcionamiento")
        parrafo_func = '''
        Para generar texto **hemos re-entrenado GPT-2 sobre un dataset de 30000 tweets**.
        Para poder tener una estructura por la cual introducir y extraer
        texto, **los formateamos de la siguiente foma**:
        ```
        Input: baked, cake, @mention
        Output: @mention I baked you a cake but I ate it 
        <|endtext|>
        [...]
        ```

        Para generar texto, **introducimos a GPT-2**:
        ```
        Input: baked, cake, @mention
        ```
        **y el modelo completa la estructura**.

        La salida **no suele ser coherente**, ya que el set de datos usado para
        el entrenamiento era de solo 30000 tweets, usamos el modelo mas pequeño de GPT-2,
        y lo entrenamos solo una noche en un portatil.

        A pesar de ello, **el modelo ha comprendido la estructura de entrada salida**, y sirve \
        como prueba de concepto.
        
        ---
        '''
        st.markdown(parrafo_func)

    st.header("Ejemplo interactivo")
    parrafo_ejemplo = '''
    **Aqui puedes probar el sistema que genera texto natural dados unos temas.**

    ** Usamos GPT-2 con 117 millones de parametros en un servidor de 5 euros, tarda mucho en 
    generar texto...**

    A continuacion puedes introducir un input a nuestro sistema y ver su output.
    **El input debe ser en Ingles**, y estar formado por **palabras separadas por comas**.
    **La temperatura controla la aleatoriedad** de la salida de GPT-2.
    '''
    st.markdown(parrafo_ejemplo)
    prompt = st.text_input("Input", "bite, shiny, metal, buttocks").lower()
    temp = st.slider("Temperatura", 0.01, 1.0, 1., step=0.01)
    st.markdown("##### > A bajas temperaturas, el modelo suele pedir perdon (por alguna razon???)  ")

    if not prompt:
        st.info("Escribe algunos sustantivos")
        st.stop()

    elif not bool(re.match(r"([a-z]+, *)*[a-z]+", prompt)) or re.match(r"([a-z]+, *)*[a-z]+", prompt).span()[1] != len(prompt):
        st.error("Input invalido")
        st.stop()

    elif st.button('Generar texto "natural"'):
        prompt = re.sub(r" *, *", ', ', prompt)
        parrafo_espera ='''
        Quiero que pienses en que tal te fue el fin de semana.
        Que tal pasaste tu tiempo, y si dormiste bien.
        La razon para esto es que el modelo de GPT-2 que usamos tiene 117 millones de 
        parametros (Es el mas pequeño!), y estoy ejecutando esta demo en un servidor 
        de 5 euros/mes.
        Esto quiere decir que sacar una salida de GPT puede tardar hasta 20 min...
        Asi que rememora tu finde. :)
        '''
        st.text(parrafo_espera)

        with st.spinner("Ten paciencia"):
            output = prompt_gpt(prompt, temp)

        st.balloons()

        st.markdown('''
        #### Input: 
        ```{}```
        #### Output: 
        ```{}```
        '''.format(prompt, output))

        st.markdown("---")
        st.header("Souvenir")
        parrafo_fin ='''
        Como premio por aguantar todo este tiempo, aqui tienes un souvenir. Espero que te guste.
        '''
        st.markdown(parrafo_fin)
        tweet_img = get_img(output)
        st.image(tweet_img, "Tu souvenir personalizado [3]", use_column_width=True)

    st.markdown('---')
    if not hide_text:
        citations = {
            1:"https://es.wikipedia.org/wiki/Lengua_natural",
            2:"https://openai.com/blog/better-language-models",
            3:"Gracias a https://github.com/fedejordan/tweet-image-generator"
        }

        footer = ""
        for k, v in citations.items():
            footer += f"[{k}] {v}\n"
        st.text(footer)

    st.header("- Fin -")

@st.cache
def prompt_gpt(prompt, temperature):
    m = GPT2(model_path)
    return m.prompt_model(prompt, temperature=temperature)

@st.cache
def get_img(text):
    date_format = "%I:%M %p · %d %b. %Y"
    date = datetime.now().strftime(date_format)
    name = "Hugh Jass"
    username = "@totallynotabot"
    profileImg = "resources/bender.png"
    img = "resources/lousyImg.png"
    verified = True
    return gen(name, username, text, profileImg, date, verified, images=img)
