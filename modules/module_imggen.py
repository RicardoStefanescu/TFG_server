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

def st_function():
    st.title("Generacion de imagenes")
    st.header("Mystique de X-Men")
    parrafo_intro = '''
    Una de las funcionalidades mas utiles que le podemos dar a nuestros bots \
    para que pasen desapercibidos, es la capacidad de generar contenido que parezca\
    humano. Hemos implementado una funcionalidad para que nuestros bots puedan subir\
    fotos normales donde salen ellos. Utiliza las tecnicas descritas por Aliaksandr Siarohin [1]\
    para segmentar las caras en zonas, y despues sustituye las partes.\
    
    Puedes subir tu propia foto, o jugar con las por defecto.
    '''
    st.markdown(parrafo_intro)

    # Ask for images
    st.markdown("#### Sube una foto de una cara, y una foto de un grupo")
    source_img_b = st.file_uploader("Cara a usar", ['png', 'jpg', 'jpeg'])
    target_img_b = st.file_uploader("Imagen objetivo", ['png', 'jpg', 'jpeg'])

    if source_img_b is None:
        source_path = default_face_path
        source_img_arr = np.array(Image.open(source_path))
    
    else:
        source_img = Image.open(source_img_b)
        source_img_arr = np.array(source_img)
        source_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(source_path, source_img_arr)

    
    if target_img_b is None:
        target_path = default_group_path
        target_img_arr = np.array(Image.open(target_path))

    else:
        target_img = Image.open(target_img_b)
        target_img_arr = np.array(target_img)
        target_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(target_path, target_img_arr)

    st.image(source_img_arr, caption="Tu careto", use_column_width=True)

    with st.spinner("Calculando la similitud de las caras"):
        all_faces = find_similar_faces(source_path, target_path)
        display_target = target_img_arr.copy()

        for i, face in enumerate(all_faces):
            sim = face[0]
            y_0, x_1, y_1, x_0 = face[1]

            cv2.rectangle(display_target, (x_0, y_0), (x_1, y_1), (0, 255, 60), 10)
            cv2.putText(display_target, f'Cara {i}', (x_0, (y_1 - y_0)//6+y_0), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 60), 4)
            cv2.putText(display_target, 'Similitud: {:.2f}'.format(sim), (x_0, 2*(y_1 - y_0)//6+y_0), cv2.FONT_HERSHEY_DUPLEX, 2, (0, 255, 60), 4)

        st.image(display_target, caption="Imagen objetivo", use_column_width=True)

    st.markdown('---\n Elije que cara sustituir')
    i = st.slider("Que cara sustituimos?", min_value=0, max_value=len(all_faces) - 1, value=2)

    parrafo_segmentacion = '''
    Usamos el codigo de Motion co-seg para segmentar las caras en zonas. \
    A continuacion podemos ver las dos caras segmentadas:
    '''
    st.markdown(parrafo_segmentacion)

    with st.spinner("Calculando segmentacion"):
        seg_source_path = visualize_segmentation(source_path)
        seg_target_path = visualize_segmentation(target_path, face_location=all_faces[i])

    st.image([Image.open(seg_source_path), Image.open(seg_target_path)], ["Cara del bot segmentada", f"Cara {i} segmentada"])

    parrafo_result = '''
    Por ultimo, movemos las zonas de la cara de nuestro bot a la cara final.
    '''
    st.markdown(parrafo_result)

    with st.spinner("Calculando transformacion"):
        result_img = replace_face(source_path, target_path, all_faces[i][1], gpu=False)
    
    #cv2.cvtColor(, cv2.COLOR_BGR2RGB)
    st.subheader("Resultado")
    st.image(result_img, "Imagen resultante", channels="BGR", use_column_width=True)
