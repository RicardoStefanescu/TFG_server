import time
import base64
from string import ascii_letters
from random import choice
import os
from datetime import datetime

import streamlit as st

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image
from skimage.transform import resize
import cv2

from include.resources.tweet_image_generator.generate_tweet_image import gen
from include.content_generation import find_similar_faces, replace_face, visualize_segmentation

# Intro text
# Explain file uploads or face
# Show images
# Select faces
# Explain segmentation
# Show segmentation
# Talk about next step
# Show 

base_path = '/tmp/'
default_face_path = "resources/default_face.jpeg"
default_group_path = "resources/default_group.jpg"

def st_function(hide_text):
    st.title("Generacion de imagenes")
    
    if not hide_text:
        st.header("Alberto Saiz")
        parrafo_saiz = '''
        *Alberto Saiz* fue el director del CNI de 2004 hasta 2009, cuando **dimitio por acusaciones \
        de haber usado recursos del centro para irse de caza y pesca.** *[1]* \
        Cuando empezó a sentir la presión, **ordeno a un grupo del CNI en Dakar a borrar \
        pruebas incriminatorias**.
        
        Algunas de ellas eran las **fotos subidas a la pagina de una de las agencias de pesca**.  \
        **Decidieron editar las imágenes** de tal forma que *Saiz* pareciese otra persona, \
        en este caso el agente que tenia a su lado. 

        No le salió muy bien la jugada, ya que la prensa se dio cuenta y se le echó encima.
        '''
        st.markdown(parrafo_saiz)
        st.image("resources/albertosaiz.jpeg", caption="Foto editada por el CNI, *Alberto Saiz* va vestido de negro.", use_column_width=True)
        st.header("Auto edicion")
        parrafo_intro = '''
        Para evadir deteccion de por otros usuarios, **queremos crear un sistema para generar \
        imagenes realistas donde salga nuestro bot**. Para ello le copiaremos la idea a *Alberto Saiz*.
        '''
        st.markdown(parrafo_intro)

        st.header("Sistema propuesto")
        st.subheader("Objetivo")
        st.markdown("Sistema que añade a nuestro Bot a fotos de personas ajenas.")
        st.subheader("Funcionamiento")
        parrafo_func = '''
        Nuestro sistema **toma una foto de perfil** (nos valen las generadas por StyleGAN2 *[2]*), \
        **y una foto de un grupo de personas** en la que queramos que aparezca nuestro bot.
        Para ello **utilizamos una red neuronal entrenada para segmentar caras \
        en zonas**, creada por Aliaksandr Siarohin *[3]*. Una vez \
        tenemos las caras segmentadas, **sustituimos las zonas de la cara de nuestro \
        bot a la cara de la imagen objetivo**. 
        '''
        st.markdown(parrafo_func)

    st.header("Ejemplo interactivo")
    work = False
    correction = False
    st.markdown("**Aqui puedes probar el sistema que edita cabezas en fotos de manera automatica.**")
    st.markdown("#### Usa las fotos por defecto, o sube fotos tu")
    # Ask for images
    source_img_b = st.file_uploader("Cara a usar", ['png', 'jpg', 'jpeg'])
    target_img_b = st.file_uploader("Imagen objetivo", ['png', 'jpg', 'jpeg'])

    if source_img_b is None and target_img_b is None:
        source_path = default_face_path
        with open(default_face_path, 'rb') as f:
            source_img = np.array(Image.open(f).convert('RGB'))

        target_path = default_group_path
        with open(default_group_path, 'rb') as f:
            target_img = np.array(Image.open(f).convert('RGB'))
        correction = True
        work = True

    elif source_img_b and target_img_b:
        source_img = np.array(Image.open(source_img_b).convert('RGB'))
        target_img = np.array(Image.open(target_img_b).convert('RGB'))

        max_val = 1080
        # Resize them before working with them
        if max(source_img.shape[:2]) > max_val:
            w_mult = source_img.shape[0] / max(source_img.shape[:2])
            h_mult = source_img.shape[1] / max(source_img.shape[:2])
            source_img = cv2.resize(source_img, (int(h_mult*max_val), int(w_mult*max_val)))
        if max(target_img.shape[:2]) > max_val:
            w_mult = target_img.shape[0] / max(target_img.shape[:2])
            h_mult = target_img.shape[1] / max(target_img.shape[:2])
            target_img = cv2.resize(target_img, (int(h_mult*max_val), int(w_mult*max_val)))

        # If source image is not a square make it into one
        if source_img.shape[0] != source_img.shape[1]:
            source_img = source_img[0:min(source_img.shape[:2])-1,0:min(source_img.shape[:2])-1]

        # Save
        source_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(source_path, source_img)

        target_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(target_path, target_img)

        correction = False
        work = True

    if work or correction:
        st.image(source_img, caption="Cara de nuestro bot", use_column_width=True)

        with st.spinner("Calculando la similitud de las caras"):
            all_faces = find_similar_faces(source_path, target_path)
            if not all_faces:
                st.image(target_img, caption="Imagen objetivo", use_column_width=True)
                st.error("El sistema no pudo encontrar caras en esta foto (quizas llevan gafas).")
                st.stop()
            display_target = target_img.copy()

            for i, face in enumerate(all_faces):
                sim = face[0]
                y_0, x_1, y_1, x_0 = face[1]

                cv2.rectangle(display_target, (x_0, y_0), (x_1, y_1), (255, 0, 0), 8)
                cv2.putText(display_target, 'Sim: {:.2f}'.format(sim), (x_0, 2*(y_1 - y_0)//8+y_1), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 0, 0), 3)
            
            for i, face in enumerate(all_faces):
                y_0, x_1, y_1, x_0 = face[1]
                cv2.putText(display_target, f'{i}', (x_0, 2*(y_1 - y_0)//8+y_0), cv2.FONT_HERSHEY_DUPLEX, 1, (255, 255, 0), 3)

            st.image(display_target, caption="Imagen objetivo", use_column_width=True)

        st.markdown('---\n Elije que cara sustituir')
        i = st.number_input("Que cara sustituimos?", min_value=0, max_value=len(all_faces) - 1, value=0)

        parrafo_segmentacion = '''
        Usamos el codigo de Motion co-seg para segmentar las caras en zonas. \
        A continuacion podemos ver las dos caras segmentadas:
        '''
        if hide_text:
            st.markdown(parrafo_segmentacion)

        with st.spinner("Calculando segmentacion"):
            seg_source_path = segment(source_path)
            seg_target_path = segment(target_path, face_location=all_faces[i][1])

        st.image([Image.open(seg_source_path), Image.open(seg_target_path)], ["Cara del bot segmentada", f"Cara {i} segmentada"], use_column_width=True)

        parrafo_result = '''
        #### Por ultimo, movemos las zonas de la cara de nuestro bot a la cara final.
        '''
        st.markdown(parrafo_result)

        with st.spinner("Calculando transformacion"):
            result_img = get_result(source_path, target_path, all_faces[i][1], gpu=False)
        
        if correction:
            result_img = cv2.cvtColor(np.float32(result_img), cv2.COLOR_BGR2RGB)
        
        #result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        #st.image(result_img, "Imagen resultante", channels="RGB" if correction else "BGR", use_column_width=True)

        st.markdown('---')
        st.subheader("Resultado")

        result_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(result_path, result_img*255)
        tweet = get_img(source_path, result_path)
        st.image(tweet, "Sugerencia de presentacion", use_column_width=True)
    
    st.markdown('---')
    if not hide_text:
        citations = {
            1:"https://www.elmundo.es/elmundo/2009/06/16/espana/1245121096.html",
            2:"https://thispersondoesnotexist.com/",
            3:"https://arxiv.org/abs/2004.03234",
        }

        footer = ""
        for k, v in citations.items():
            footer += f"[{k}] {v}\n"
        st.text(footer)

@st.cache(suppress_st_warning=True)
def segment(path, face_location=None):
    if not face_location:
        return visualize_segmentation(path)
    else:
        return visualize_segmentation(path, face_location=face_location)

@st.cache(suppress_st_warning=True)
def get_result(source_path, target_path, face_location, gpu=False):
    return replace_face(source_path, target_path, face_location, gpu=False)


@st.cache
def get_img(profileImg, img):
    date_format = "%I:%M %p · %d %b. %Y"
    date = datetime.now().strftime(date_format)
    name = "Hugh Jass"
    username = "@totallynotabot"
    text = "Adjunto una imagen con mis amigos. Soy capaz de disfrutar conversaciones complejas en \
            lenguaje natural sin motivo aparente como cualquier otro humano"
    verified = True
    return gen(name, username, text, profileImg, date, verified, images=img)
