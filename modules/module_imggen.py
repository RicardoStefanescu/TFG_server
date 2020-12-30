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
from matplotlib.animation import FuncAnimation
from PIL import Image

import cv2

from include.content_generation import find_similar_faces, replace_face


base_path = '/tmp/'

def st_function():
    st.title("Generacion de imagenes")
    st.subheader("Funcionalidad que sustituye cabeza")
    # Ask for images
    st.markdown("Sube una foto de DNI, y una foto de un grupo o persona")
    source_img_b = st.file_uploader("Cara a usar", ['png', 'jpg', 'jpeg'])
    target_img_b = st.file_uploader("Imagen objetivo", ['png', 'jpg', 'jpeg'])

    if source_img_b is not None and target_img_b is not None:
        # Open images
        source_img = Image.open(source_img_b)
        source_img_arr = np.array(source_img)
        source_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(source_path, source_img_arr)

        target_img = Image.open(target_img_b)
        target_img_arr = np.array(target_img)
        target_path = os.path.join(base_path, ''.join([choice(ascii_letters) for _ in range(7)]) + '.jpg')
        cv2.imwrite(target_path, target_img_arr)

        st.image(source_img_arr, caption="Tu careto", use_column_width=True)
        st.image(target_img_arr, caption="Imagen objetivo", use_column_width=True)

        st.markdown('---\n Elije que cara sustituir')
        

        all_faces = find_similar_faces(source_path, target_path)

        target_img_arr = cv2.imread(target_path)
        imgs = []
        captions = []
        for i, x in enumerate(all_faces):
            sim, rect = x
            y_0, x_1, y_1, x_0 = rect
            captions.append(f"Cara {i} | Similaridad: {sim}")
            imgs.append(target_img_arr[y_0:y_1,x_0:x_1])

        st.image(imgs, caption=captions)

        i = st.slider("Que cara sustituimos?", min_value=0, max_value=len(imgs) - 1)

        result_img = replace_face(source_path, target_path, all_faces[i][1], gpu=False)
        #cv2.cvtColor(, cv2.COLOR_BGR2RGB)
        st.subheader("Resultado")
        st.image(result_img, "Imagen resultante", channels="BGR", use_column_width=True)
