import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import seaborn as sns
import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import threading
import imageio
import os
import time


GRID_SIZE = 50
INITIAL_DENSITY = 0.2
SPEED = 100 
FRAMES = 200

grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
running = False
generation = 0
live_cells_over_time = []
gif_frames = []


def add_glider(grid, x=1, y=1):
    pattern = [(0,1), (1,2), (2,0), (2,1), (2,2)]
    for dx, dy in pattern:
        grid[(x + dx) % GRID_SIZE][(y + dy) % GRID_SIZE] = 1

def add_pulsar(grid, x=15, y=15):
    pattern = [
        (0, 2), (0, 3), (0, 4), (0, 8), (0, 9), (0, 10),
        (2, 0), (3, 0), (4, 0), (8, 0), (9, 0), (10, 0),
        (2, 5), (3, 5), (4, 5), (8, 5), (9, 5), (10, 5),
        (5, 2), (5, 3), (5, 4), (5, 8), (5, 9), (5, 10)
    ]
    for dx, dy in pattern:
        grid[(x + dx) % GRID_SIZE][(y + dy) % GRID_SIZE] = 1


def count_neighbors(g, x, y):
    total = 0
    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            if i == 0 and j == 0:
                continue
            ni, nj = (x + i) % GRID_SIZE, (y + j) % GRID_SIZE
            total += g[ni][nj]
    return total

def update_grid():
    global grid, generation, live_cells_over_time, gif_frames
    new_grid = np.copy(grid)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            n = count_neighbors(grid, i, j)
            if grid[i, j] == 1 and (n < 2 or n > 3):
                new_grid[i, j] = 0
            elif grid[i, j] == 0 and n == 3:
                new_grid[i, j] = 1
    grid = new_grid
    live_cells = np.sum(grid)
    live_cells_over_time.append(live_cells)
    generation += 1
    if save_gif.get():
        gif_frames.append(np.copy(grid))
    return grid


def draw_grid():
    ax.clear()
    ax.imshow(grid, cmap="viridis", interpolation="nearest")
    ax.set_title(f"Geração: {generation} | Vivas: {np.sum(grid)}")
    ax.axis("off")
    canvas.draw()

def toggle_cell(event):
    i = int(event.y / (500 / GRID_SIZE))
    j = int(event.x / (500 / GRID_SIZE))
    grid[i % GRID_SIZE][j % GRID_SIZE] ^= 1
    draw_grid()

def run_simulation():
    global running, generation, live_cells_over_time, gif_frames
    running = True
    live_cells_over_time = []
    gif_frames = []
    generation = 0
    for _ in range(FRAMES):
        if not running:
            break
        update_grid()
        draw_grid()
        time.sleep(SPEED / 1000.0)
    running = False
    plot_stats()
    if save_gif.get():
        export_gif()

def start_thread():
    if not running:
        threading.Thread(target=run_simulation, daemon=True).start()

def stop_simulation():
    global running
    running = False

def reset_grid():
    global grid, generation
    grid = np.zeros((GRID_SIZE, GRID_SIZE), dtype=int)
    generation = 0
    draw_grid()

def randomize_grid():
    global grid
    grid = np.random.choice([0, 1], size=(GRID_SIZE, GRID_SIZE), p=[0.8, 0.2])
    draw_grid()

def plot_stats(show_popup=True):
    if not live_cells_over_time:
        messagebox.showinfo("Aviso", "Nenhum dado de simulação para mostrar.")
        return

    fig2, ax2 = plt.subplots(figsize=(6, 4))
    sns.lineplot(x=range(len(live_cells_over_time)), y=live_cells_over_time, color='blue', ax=ax2)
    ax2.set_title("Células Vivas por Geração")
    ax2.set_xlabel("Geração")
    ax2.set_ylabel("Células Vivas")
    ax2.grid(True, linestyle="--", alpha=0.7)
    fig2.tight_layout()


    fig2.savefig("grafico.png")
    print("📊 Gráfico salvo como 'grafico.png'.")

   
    if show_popup:
        stats_window = tk.Toplevel(root)
        stats_window.title("Gráfico de Células Vivas")
        canvas2 = FigureCanvasTkAgg(fig2, master=stats_window)
        canvas2.draw()
        canvas2.get_tk_widget().pack(fill=tk.BOTH, expand=True)

def export_gif():
    images = []
    for f in gif_frames:
        fig, ax = plt.subplots()
        ax.imshow(f, cmap='viridis', interpolation='nearest')
        ax.axis('off')
        fig.canvas.draw()
        image = np.frombuffer(fig.canvas.tostring_rgb(), dtype='uint8')
        image = image.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        images.append(image)
        plt.close(fig)
    imageio.mimsave("conway_simulation.gif", images, duration=SPEED/1000)
    messagebox.showinfo("GIF Salvo", "GIF salvo como conway_simulation.gif")


root = tk.Tk()
root.title("Jogo da Vida de Conway")


fig, ax = plt.subplots(figsize=(5, 5))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.LEFT)
canvas.mpl_connect("button_press_event", toggle_cell)


frame = tk.Frame(root)
frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

tk.Button(frame, text="▶ Iniciar", command=start_thread).pack(pady=5)
tk.Button(frame, text="⏸ Parar", command=stop_simulation).pack(pady=5)
tk.Button(frame, text="🔁 Reiniciar", command=reset_grid).pack(pady=5)
tk.Button(frame, text="🔀 Aleatório", command=randomize_grid).pack(pady=5)
tk.Button(frame, text="🌀 Adicionar Glider", command=lambda: [add_glider(grid), draw_grid()]).pack(pady=5)
tk.Button(frame, text="🌟 Adicionar Pulsar", command=lambda: [add_pulsar(grid), draw_grid()]).pack(pady=5)
tk.Button(frame, text="📊 Ver Gráfico", command=plot_stats).pack(pady=5)
save_gif = tk.BooleanVar()
tk.Checkbutton(frame, text="Salvar como GIF", variable=save_gif).pack(pady=5)

draw_grid()
root.mainloop()
