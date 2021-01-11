import time
import base64
from string import ascii_letters
from random import choice
import os

import streamlit as st

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from PIL import Image
from skimage.transform import resize
import cv2

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
    st.header("Auto edicion")
    parrafo_intro = '''
    Una de las funcionalidades mas utiles que le podemos dar a nuestros bots \
    para que pasen desapercibidos, es la capacidad de generar contenido que parezca\
    humano. Hemos implementado una funcionalidad para que puedan subir\
    fotos donde salen ellos. Utiliza las tecnicas descritas por Aliaksandr Siarohin [1]\
    para segmentar las caras en zonas, y despues sustituye las partes.\
    '''
    if hide_text:
        st.markdown(parrafo_intro)

    work = False

    # Ask for images
    st.markdown("#### Usa las fotos por defecto, o sube fotos tu")
    source_img_b = st.file_uploader("Cara a usar", ['png', 'jpg', 'jpeg'])
    target_img_b = st.file_uploader("Imagen objetivo", ['png', 'jpg', 'jpeg'])

    if st.button("Usar imagenes por defecto"):
        source_path = default_face_path
        source_img_arr = np.array(Image.open(source_path))
        target_path = default_group_path
        target_img_arr = np.array(Image.open(target_path))
        work = True

    elif source_img_b and target_img_b:
        source_img = np.array(Image.open(source_img_b).convert('RGB'))
        target_img = np.array(Image.open(target_img_b).convert('RGB'))

        max_val = 1080
        # Resize them before working with them
        w_mult = source_img.shape[0] / max(source_img.shape[:2])
        h_mult = source_img.shape[1] / max(source_img.shape[:2])
        resized_source_img = cv2.resize(source_img, (int(h_mult*max_val), int(w_mult*max_val)))
        w_mult = target_img.shape[0] / max(target_img.shape[:2])
        h_mult = target_img.shape[1] / max(target_img.shape[:2])
        resized_target_img = cv2.resize(target_img, (int(h_mult*max_val), int(w_mult*max_val)))

        # Convert to cv2 img
        source_img_arr = np.array(resized_source_img)
        target_img_arr = np.array(resized_target_img)
        print(target_img_arr)

        # Save
        source_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(source_path, source_img_arr)

        target_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(target_path, target_img_arr)

        work = True

    if work:
        st.image(source_img_arr, caption="Cara de nuestro bot", use_column_width=True)

        with st.spinner("Calculando la similitud de las caras"):
            all_faces = find_similar_faces(source_path, target_path)
            if not all_faces:
                st.image(target_img_arr, caption="Imagen objetivo", use_column_width=True)
                st.error("El sistema no pudo encontrar caras en esta foto (quizas llevan gafas).")
                st.stop()
            display_target = target_img_arr.copy()

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
        
        #result_img = cv2.cvtColor(result_img, cv2.COLOR_BGR2RGB)
        correction = st.checkbox("La imagen sale azul")
        st.image(result_img, "Imagen resultante", channels="RGB" if correction else "BGR", use_column_width=True)

@st.cache(suppress_st_warning=True)
def segment(path, face_location=None):
    if not face_location:
        return visualize_segmentation(path)
    else:
        return visualize_segmentation(path, face_location=face_location)

@st.cache(suppress_st_warning=True)
def get_result(source_path, target_path, face_location, gpu=False):
    return replace_face(source_path, target_path, face_location, gpu=False)