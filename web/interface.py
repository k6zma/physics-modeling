import streamlit as st
import numpy as np

def render_sidebar():
    mass = st.sidebar.number_input("Масса тела (кг)", value=3.0)
    radius = st.sidebar.number_input("Радиус дуги (м)", value=3.0)
    friction = st.sidebar.number_input("Коэффициент трения", value=0.03)
    
    angle_selection = st.sidebar.radio("Выберите угол дуги:", [
        "π", "π + π/3", "π + π/6", "π/2 + π/3", "π/2 + π/6"
    ])
    angle_values = {
        "π": np.pi,
        "π + π/3": np.pi + np.pi / 3,
        "π + π/6": np.pi + np.pi / 6,
        "π/2 + π/3": np.pi / 2 + np.pi / 3,
        "π/2 + π/6": np.pi / 2 + np.pi / 6
    }
    angle = angle_values[angle_selection]

    return mass, radius, friction, angle

def display_information(v0_min):
    st.markdown(
        f"""
        <div style="background-color: #f0f8e2; padding: 15px; border-radius: 10px; border: 2px solid #d4edda;">
            <h3 style="color: #2f5d62;">📈 Минимальная начальная скорость для успешного прохождения дуги:</h3>
            <p style="font-size: 24px; color: #4CAF50; font-weight: bold; text-align: center;">{v0_min:.2f} м/с</p>
            <p style="font-size: 16px; color: #6c757d; text-align: center;">Эта скорость рассчитана на основе выбранных вами параметров массы, радиуса и трения.</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.write(" ")
    st.write(" ")

def display_parameters(mass, radius, friction, angle):
    st.markdown(
        f"""
        <div style="background-color: #e6f7ff; padding: 15px; border-radius: 10px; border: 2px solid #cceeff;">
            <h3 style="color: #007acc;">🔍 Параметры для расчета:</h3>
            <p style="font-size: 18px; color: #333333;"><strong>Масса:</strong> {mass:.2f} кг</p>
            <p style="font-size: 18px; color: #333333;"><strong>Радиус дуги:</strong> {radius:.2f} м</p>
            <p style="font-size: 18px; color: #333333;"><strong>Коэффициент трения:</strong> {friction:.2f}</p>
            <p style="font-size: 18px; color: #333333;"><strong>Угол дуги:</strong> {angle:.2f} радиан</p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    st.write(" ")
    st.write(" ")