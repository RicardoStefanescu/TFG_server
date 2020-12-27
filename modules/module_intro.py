import streamlit as st

def st_function():
    st.title("Introduccion")

    st.header("2018")
    parrafo_2018 = '''
    En 2018 **decidí que quería hacer algo especial con mi cuenta de Instagram**,
    no soy fan de que haya fotos mias en internet, y me aburría publicar fotos, y escribir comentarios ingeniosos en sus publicaciones.

    Eureka, pensé; “estudio GIC, **podría programar un bot que haga todas esas funciones**, y solo usar Instagram para cotillear las vidas de mis amigos”. 
    En un fin de semana **hice un pequeño bot con python y selenium** que comentaba "🐒🐒🐒" en las fotos de mis mejores amigos.

    Estaba orgulloso y emocionado de descubrir mi nuevo superpoder, tenía ganas de más.

    Pero hubo un percance, no pasaron ni 5 minutos y **instagram bloqueo mi cuenta hasta resolver un captcha**;
    y mi bot, no siendo una obra de arte, encontró un error y paró.

    **“¿Cómo habra detectado instagram mi bot tan rapido?”** me pregunte.
    '''
    st.markdown(parrafo_2018)

    st.header("El problema")
    parrafo_problema = '''
    En Julio de 2020 **los ingenieros de Twitter** escribieron un artículo en su blog *[1]*
     detallando cómo **habían detectado 32,242 cuentas falsas** dedicadas a propagar desinformación.  

    Estas cuentas fueron inhabilitadas por ir contra su política de manipulación de la plataforma *[2]*,
    ya que **constituían una acción coordinada para modificar la opinión pública**.  

    Mientras que **nuestro bot** que comenta monitos **no pretende modificar la opinión de nuestros seguidores**, 
    **las medidas** para detección de bots **complican considerablemente el desarrollo de bots benignos**.
    '''
    st.markdown(parrafo_problema)

    st.header("Este trabajo")
    parrafo_trabajo = '''
    En este trabajo hemos realizado **un estudio de las medidas usadas para detectar bots** en plataformas web y RRSS. Las dividimos en:
    
    1. Aquellas que **observan el input de periféricos** al usar la plataforma.
    2. Aquellas que **observan la huella digital** del dispositivo usado.
    3. Aquellas que **estudian los gustos y patrones temporales**.
    4. **Denuncias de contenido sospechoso** por parte de usuarios
    
    Para cada medida **hemos estudiado su funcionamiento**, y **hemos generado una solución simple en python**, para facilitar el diseño de bots *benignos*.

    Esta página es una demostración visual e interactiva de las contramedidas generadas. 
    
    ⬅️⬅️⬅️ Para continuar selecciona una seccion en el menu de la izquierda.
    '''
    st.markdown(parrafo_trabajo)

    st.markdown('---')
    citations = {
        1:"https://blog.twitter.com/en_us/topics/company/2020/information-operations-june-2020.html",
        2:"https://help.twitter.com/en/rules-and-policies/platform-manipulation"
    }

    footer = ""
    for k, v in citations.items():
        footer += f"[{k}] {v}\n"
    st.text(footer)