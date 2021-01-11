import streamlit as st
import re

from include.text_generation import GPT2

#model_path = "/home/workingman/Studies/TFG/3-ContentGeneration/TextGeneration/gpt-2-finetuning/models/simple_gen"
model_path = "/home/user/TFG_server/include/resources/models/gpt_simple_gen"

def st_function(hide_text):
    prompt = st.text_input("Input: (Sustantivos en ingles separados por comas)")

    if not prompt:
        st.warning("Escribe algunos sustantivos")
    elif st.button('Generar texto "natural"'):
        # Start model
        m = GPT2(model_path)

        prompt = prompt.lower()
        if bool(re.match(r"([a-z]*, *)*[a-z]+", prompt)):
            prompt = re.sub(r" *, *", ', ', prompt)
            output = m.prompt_model(prompt)

            st.markdown('''
            #### Input: {}   
            #### Output: {}
            '''.format(prompt, output))

        else:
            st.warning("Input invalido")


        