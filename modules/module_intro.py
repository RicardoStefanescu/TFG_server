import streamlit as st
from PIL import Image

def st_function(hide_text):
    st.title("Introduccion")

    if not hide_text:
        st.header("2018")
        parrafo_2018 = '''
        En 2018 **decidí que quería hacer algo especial con mi cuenta de Instagram**,
        no soy fan de que haya fotos mias en internet, y me aburría publicar fotos y escribir comentarios en publicaciones.
        Eureka, pensé; “estudio GIC, **podría programar un bot que haga todas esas funciones**, y solo usar Instagram para cotillear las vidas de mis amigos”. 
        En un fin de semana **hice un pequeño bot con python y selenium** que comentaba "🐒🐒🐒" en las fotos de mis mejores amigos.

        Estaba orgulloso y emocionado de descubrir mi nuevo superpoder, tenía ganas de más.

        Pero hubo un percance, no pasaron ni 5 minutos y **instagram bloqueo mi cuenta hasta que resolvera un captcha**;
        y mi bot, muy lejos de ser una obra de arte, encontró un error y paró.

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
        
        network_img = Image.open("resources/intro_bot_network.jpeg")
        network_caption = "La difusión de un artículo que afirmaba que 3 millones de inmigrantes ilegales votaron en las elecciones presidenciales de EE.UU. de 2016. (por phys.org)"
        st.image(network_img, caption=network_caption, use_column_width=True)

        st.header("Verificacion Intrusiva")
        parrafo_intrusiva = '''
        Un captcha es una prueba de turing automatizada, es decir, 
        una prueba que **un humano puede realizar fácilmente, pero que a un ordenador le es casi imposible**. 

        Las últimas versiones de **ReCaptcha *[3]* usan detección de objetos en imágenes**, un problema que a las máquinas aún le cuesta mucho.
        Mientras que es una solución casi infalible, 
        **presentar a todos los usuarios con puzzles cada vez que quieren usar nuestro servicio es una forma asegurada de aburrirlos**.

        A estas pruebas de verificación que suponen una interrupción del servicio habitual se llaman **pruebas de verificación intrusivas**.
        '''
        st.markdown(parrafo_intrusiva)

        st.header("Verificacion no Intrusiva")
        parrafo_no_intrusiva = '''
        Si fuésemos una red social, **nuestro objetivo es que nuestros usuarios pasen el mayor tiempo posible usando nuestros servicios**, 
        por lo que nos interesan medidas de detección de bots que sean **invisibles a nuestros usuarios**.  
        Esto se llama **verificación no intrusiva**.

        **En este trabajo trataremos sólo con verificación no intrusiva**. Dividiremos las diferentes técnicas en:

        1. Aquellas que **observan el input de periféricos** al usar la plataforma.
        2. Aquellas que **observan la huella digital** del dispositivo usado.
        3. Aquellas que **estudian los gustos y patrones temporales**.
        4. **Denuncias de contenido sospechoso** por parte de usuarios

        Para cada medida **hemos estudiado su funcionamiento**, y **hemos generado una solución simple en python**, para facilitar el diseño de bots *benignos*.

        Esta página es una demostración visual e interactiva de las contramedidas generadas. 

        ⬅️⬅️⬅️ Para continuar selecciona una seccion en el menu de la izquierda.
        '''
        st.markdown(parrafo_no_intrusiva)

        st.markdown('---')
        citations = {
            1:"https://blog.twitter.com/en_us/topics/company/2020/information-operations-june-2020.html",
            2:"https://help.twitter.com/en/rules-and-policies/platform-manipulation",
            3:"https://www.google.com/recaptcha/about/"
        }

        footer = ""
        for k, v in citations.items():
            footer += f"[{k}] {v}\n"
        st.text(footer)
    
    else:
        parrafo_continuar = '''
        ##### Para que me curro tanto texto...
        
        ⬅️⬅️⬅️ Selecciona una seccion en el menu de la izquierda para continuar.
        '''
        st.markdown(parrafo_continuar)