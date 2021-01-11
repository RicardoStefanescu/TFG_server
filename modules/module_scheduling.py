import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

from include.scheduling import calcular_tiempos, generate_scheduling_function, calcular_probabilidades

def st_function(hide_text):
    st.title("Tiempos de activacion")
    if hide_text:
        # Insomnia y bots
        st.header("Ritmos circadianos")
        parrafo_alicebob = '''
        Los ritmos circadianos, del latín circa ("alrededor de") y dies ("día"),
        son los ciclos sueño-vigilia de 24 horas por los que pasamos todas las personas.

        A parte del ciclo de sueño, la mayoría de los humanos tenemos una ocupación que ronda las 8 horas,
        nos gusta tomarnos un café por las mañanas, y tenemos la mayoría de nuestro tiempo libre por la tarde noche. 

        Si estos patrones temporales se ven reflejados en nuestro uso de redes sociales, ¿por qué no en el de nuestros bots?
        '''
        st.markdown(parrafo_alicebob)

        # Tiempos humanos
        st.header("La importancia de los horarios")
        parrafo_horarios = '''
        Una forma de detectar bots dedicados a spamear contenido, es observar sus patrones temporales.

        Es fácil para sistemas automáticos y moderadores detectar las cuentas que publican contenido sin descanso,
        como aquellas dedicadas a publicar noticias o anuncios.

        Si nuestro objetivo es crear bots que se hacen pasar por humanos, tenemos que tener
        en cuenta que tengan ritmos de tiempo humanos.
        '''
        st.markdown(parrafo_horarios)


        # Sistema propuesto
        st.header("Sistema propuesto")
        # Objetivo
        st.subheader("Objetivo")
        parrafo_objetivo = '''
        Crear un sistema que genera tiempos de activacion que parecen humanos.
        '''
        st.markdown(parrafo_objetivo)

        parrafo_sistema = '''
        
        '''
        st.markdown(parrafo_sistema)

    # Ejemplo interactivo
    st.header("Ejemplo interactivo")
    st.markdown("#### Aqui puedes probar el sistema que genera tiempos de activacion de un bot")
    seed_bot = st.number_input("Semilla del bot", 0, 2**32-1, 123123, 1)
    sleep_time, work_time, chore_time, free_time = calcular_tiempos(seed_bot)
    
    parrafo_times = '''
    ### Este bot suele tener:
     - **{:.2f}** horas de sueño.
     - **{:.2f}** horas de trabajo.
     - **{:.2f}** horas de tiempo para sus hobbies.
     - **{:.2f}** horas de descansos.
    '''.format(sleep_time, work_time, chore_time, free_time)
    st.markdown(parrafo_times)

    n_days = st.slider("Cuantos dias simular", 1, 31, 10, 1)
    min_acts, max_acts = st.slider("Activaciones por dia", 1, 25, (3,15), 1)

    scheduling_func = generate_scheduling_function(seed_bot)
    activations = []
    for i in range(n_days):
        seed_c = 1
        activations_c = np.random.randint(min_acts, max_acts)
        activations.append(scheduling_func(seed_c, activations_c))
    activations = np.array(activations)

    probabilities = calcular_probabilidades(seed_bot)

    fig, ax = plt.subplots(figsize=(12,3))
    ax.set_xlim(0, 24)
    ax.set_ylim(-1,len(activations))
    ax.set_xlabel("Hora")
    ax.set_ylabel("Dia")

    ax.pcolorfast(ax.get_xlim(), ax.get_ylim(),
              np.array([p for p in probabilities])[np.newaxis],
              cmap='YlOrRd', alpha=0.4)

    for i, acts in enumerate(activations):
        ax.scatter(np.array(acts)/60, [i]*len(acts), color='black')

    st.subheader("Activaciones generadas")
    st.pyplot(fig)
    st.markdown('''
    ##### Cada punto representa una activacion.
    ##### El color (de amarillo a rojo) corresponde con la probabilidad de activacion (de menos a mas).
    ''')

