import streamlit as st
from streamlit_extras.switch_page_button import switch_page
from simulation.trajectory import BodyTrajectory
from simulation.animator import animate_trajectory
from web.interface import render_sidebar, display_information, display_parameters

def main():
    st.set_page_config(page_title="Моделирование", page_icon="📘")

    logo_path = "img/logo.png"
    st.sidebar.image(logo_path)

    page = st.sidebar.selectbox("Выберите страницу:", ["Теория", "Симуляция"])

    if page == "Теория":
        st.title("Теоретическая часть задачи")

        st.markdown(
            """
            ### Условие задачи
            Тело массой $m$, разгоняется в горизонтальной плоскости и попадает на вертикально
            расположенный фрагмент кольца (дугу) радиуса $R$ и угловым размером $a$ ($\\frac{\\pi}{2} \\leq a \\leq \\frac{3\\pi}{2}$).
            Определить скорость тела, необходимую для прохождения всей длины дуги. Изобразить
            траекторию тела после отрыва от дуги. Дуга имеет коэффициент трения $\\mu$.
            """
        )

        st.markdown(
            """
		### Подход к решению
		#### 1. Основная формула для начальной скорости $v_0$

		Начальная скорость $v_0$ рассчитывается с помощью следующего уравнения, основанного на законе сохранения энергии:
		$$
		\\frac{m v_0^2}{2} = E_п + W_{\\text{тр}}
		$$

		Решив это уравнение относительно $v_0$ получаем:
		$$
		v_0 = \sqrt{\\frac{2*(E_п + W_{\\text{тр}})}{m}}
		$$

		#### 2. Потенциальная энергия $E_п$

		Предположим, что начальная точка дуги находится на высоте $h = 0$ (начало координат) и тело поднимается на максимальную высоту на дуге. 
		Для конечной точки дуги высота $h$ будет равна:
		$$
		h = R*(1 - \cos(a))
		$$

		Таким образом, потенциальная энергия $E_п$ на высоте $h$ будет:
		$$
		E_п = m*g*h = m*g*R*(1 - \cos(a))
		$$

		#### 3. Работа силы трения $W_{\\text{тр}}$

		Если сила трения $f = \mu*N$ постоянна на всём пути, то её работа вдоль пути $s$ по дуге будет:
		$$
		W_{\\text{тр}} = f * s
		$$

		Сила реакция опоры $N$ вдоль дуги зависит от массы и угла $a$:
		$$
		N = m * g * \cos(a)
		$$

		Тогда сила трения:
		$$
		f = \mu * m * g * \cos(a)
		$$

		и работа силы трения на всём пути по дуге:
		$$
		W_{\\text{тр}} = \int_0^{a} \mu \, m \, g \, \cos(a) \, R \, da
		$$

		#### 4. Итоговая формула для начальной скорости

		Теперь подставим выражения для $E_п$ и $W_{\\text{тр}}$ в формулу для $v_0$:
		$$
		v_0 = \sqrt{\\frac{2 * (m*g*R*(1 - \cos(a)) + \mu * m * g * \sin(a) * R*a)}{m}}
		$$
    """
        )

    elif page == "Симуляция":
        st.title("Траектория движения тела на дуге и после отрыва")

        mass, radius, friction, angle = render_sidebar()

        display_parameters(mass, radius, friction, angle)

        if st.sidebar.button("Запустить симуляцию"):
            trajectory = BodyTrajectory(mass=mass, radius=radius, friction=friction, angle=angle)
            st.write("Поиск минимальной начальной скорости...")
            try:
                trajectory.find_min_initial_velocity()
                display_information(trajectory.v0_min)

                x_full, y_full, x_flight, y_flight, v_final, start_point, end_point = trajectory.calculate_trajectory()
                st.write("Создание анимации...")
                animate_trajectory(x_full, y_full, x_flight, y_flight, start_point, end_point, trajectory.v0_min)
            except ValueError as e:
                st.error(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
