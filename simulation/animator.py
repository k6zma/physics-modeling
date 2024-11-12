import matplotlib.pyplot as plt
import matplotlib.animation as animation
import tempfile
import numpy as np
from scipy.interpolate import interp1d
import streamlit as st
from stqdm import stqdm


def animate_trajectory(
    x_full,
    y_full,
    x_flight,
    y_flight,
    start_point,
    end_point,
    v0_min,
    total_frames=200,
    fps=24,
):
    fig, ax = plt.subplots(figsize=(6, 4))

    fig.patch.set_facecolor("none")
    ax.set_facecolor("none")

    ax.plot(x_full, y_full, label="Движение по дуге", color="purple")
    ax.plot(
        x_flight,
        y_flight,
        label="Траектория после отрыва",
        linestyle="--",
        color="orange",
    )
    ax.axhline(y=0, color="black", linestyle="-", linewidth=2)
    ax.set_xlabel("X, м")
    ax.set_ylabel("Y, м")
    ax.set_title("Анимация движения тела на дуге и движение после отрыва")

    ax.legend(
        [
            "Движение по дуге",
            "Траектория после отрыва",
            f"Минимальная скорость: {v0_min:.2f} м/с",
        ]
    )

    ax.plot(
        start_point[0],
        start_point[1],
        "o",
        color="#ABDF21",
        markersize=8,
        label="Начало дуги",
    )
    ax.plot(
        end_point[0],
        end_point[1],
        "o",
        color="#ABDF21",
        markersize=8,
        label="Конец дуги",
    )

    ax.grid(True)
    ax.axis("equal")
    ax.set_ylim(bottom=-2, top=10)
    ax.set_xlim(left=-15, right=5)

    x_all = np.concatenate((x_full, x_flight))
    y_all = np.concatenate((y_full, y_flight))

    total_time = np.linspace(0, 1, len(x_all))
    time_uniform = np.linspace(0, 1, total_frames)

    x_interp = interp1d(total_time, x_all, kind="linear")
    y_interp = interp1d(total_time, y_all, kind="linear")

    x_uniform = x_interp(time_uniform)
    y_uniform = y_interp(time_uniform)

    (ball,) = ax.plot([], [], "ro", markersize=8)

    def init():
        ball.set_data([], [])
        return (ball,)

    def update(frame):
        ball.set_data([x_uniform[frame]], [y_uniform[frame]])
        return (ball,)

    with tempfile.NamedTemporaryFile(suffix=".gif", delete=False) as temp_file:
        writer = animation.PillowWriter(fps=fps)
        with stqdm(total=total_frames) as pbar:
            ani = animation.FuncAnimation(
                fig,
                update,
                frames=total_frames,
                init_func=init,
                blit=True,
                repeat=False,
            )
            ani.save(
                temp_file.name,
                writer=writer,
                progress_callback=lambda i, n: pbar.update(1),
            )
        temp_file.seek(0)
        gif_data = temp_file.read()

    st.image(gif_data)
