# -*- coding: utf-8 -*-
import serial
import time
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import queue

# --- Configuración del puerto serial ---
ser = None
try:
    # Adjust 'COMx' (on Windows) or '/dev/ttyACMx' (on Linux/macOS)
    # to your Micro:bit's port.
    ser = serial.Serial('COM3', 112500, timeout=1)
    print(f"Conectado al puerto serial: {ser.name}")
except serial.SerialException as e:
    print(f"Error al abrir el puerto serial: {e}")
    print("Asegúrate de que la Micro:bit esté conectada y que ningún otro programa (como el Monitor Serial) esté utilizando el puerto.")
    exit()

# --- Queue to communicate between threads ---
data_queue = queue.Queue()

def serial_reader():
    """Reads data from the serial port and puts it into the queue."""
    while ser.is_open:
        try:
            if ser.in_waiting > 0:
                # Read until a newline character is found
                linea_recibida = ser.read_until(b'\r\n').decode('utf-8').strip()
                if linea_recibida:
                    data_queue.put(linea_recibida)
        except serial.SerialException as e:
            print(f"Error de comunicación serial: {e}")
            try:
                ser.close()
                time.sleep(1)
                ser.open()
                print("Puerto serial reconectado.")
            except serial.SerialException as re:
                print(f"Fallo la reconexión: {re}")
                break
        except Exception as e:
            print(f"Error inesperado en el hilo de lectura serial: {e}")
        time.sleep(0.05) # Small delay to prevent high CPU usage

# Start the serial reading thread
serial_thread = threading.Thread(target=serial_reader, daemon=True)
serial_thread.start()

# --- Configuración del gráfico con estilo ---
# Use a specific style for a modern look.
plt.style.use('default')

# Create the figure and axes for the graph.
fig, ax = plt.subplots(figsize=(10, 6), facecolor='#ebebeb')  # Background color of the graph area.
fig.patch.set_facecolor('#ebebeb')  # Background color of the graph's border.

# Initialize data for the four bars with different initial values below 30%.
stress = 25
ansiedad = 15
cansancio_cognitivo = 20
falta_concentracion = 30

# Store initial values to reset later
initial_values = {
    'stress': stress,
    'ansiedad': ansiedad,
    'cansancio_cognitivo': cansancio_cognitivo,
    'falta_concentracion': falta_concentracion
}

# Names for the graph columns.
nombres_columnas = ['Stress', 'Ansiedad', 'Cansancio Cognitivo', 'Falta de Concentración']

# Initialize bar colors based on initial values.
def get_initial_colors():
    colors = []
    values = [initial_values['stress'], initial_values['ansiedad'], initial_values['cansancio_cognitivo'], initial_values['falta_concentracion']]
    for value in values:
        if value < 10:
            colors.append('#28a745') # Green
        elif value > 85:
            colors.append('#dc3545') # Red
        else:
            colors.append('#ff6384') # Default pink
    return colors

bar_colors = get_initial_colors()

# Create the initial bars with personalized colors.
barras = ax.bar(nombres_columnas, [stress, ansiedad, cansancio_cognitivo, falta_concentracion], color=bar_colors)

# Configure the title and Y-axis limits.
ax.set_title('Reporte de Bienestar Interactivo', fontsize=20, color='#333333', fontweight='bold', pad=20)
ax.set_ylabel('Nivel de Impacto', color='#555555')
ax.set_ylim(0, 100)
ax.set_facecolor('#e3e3e3') # Background of the plot area.

# Configure axis labels with darker colors.
ax.tick_params(axis='x', colors='#555555')
ax.tick_params(axis='y', colors='#555555')

# Remove spines (graph borders) for a cleaner look.
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_color('#555555')
ax.spines['left'].set_color('#555555')
ax.grid(axis='y', linestyle='--', alpha=0.7)


# Add percentage labels above the bars.
def autolabel(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height:.0f}%',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points of vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom',
                    fontsize=12, color='#333333', fontweight='bold')

autolabel(barras)

# Global variable to track the last action
ultima_accion = None

# --- Function to update the graph ---
def actualizar_grafico(i):
    """
    This function is called on each "frame" of the animation.
    It reads the serial port, updates the data, and redraws the graph.
    """
    global stress, ansiedad, cansancio_cognitivo, falta_concentracion, barras, bar_colors, ultima_accion
    
    try:
        # Get data from the queue without blocking
        linea_recibida = data_queue.get(block=False)
        
        if "Uso de Pantalla" in linea_recibida:
            stress = min(100, stress + 8)
            ansiedad = min(100, ansiedad + 6)
            cansancio_cognitivo = min(100, cansancio_cognitivo + 7)
            falta_concentracion = min(100, falta_concentracion + 5)
            ultima_accion = "aumentar"
            print(f"Mensaje recibido: '{linea_recibida}'. Aumentando valores.")
        elif "Actividad Fisica" in linea_recibida:
            stress = max(0, stress - 4)
            ansiedad = max(0, ansiedad - 3)
            cansancio_cognitivo = max(0, cansancio_cognitivo - 5)
            falta_concentracion = max(0, falta_concentracion - 2)
            ultima_accion = "disminuir"
            print(f"Mensaje recibido: '{linea_recibida}'. Disminuyendo valores.")
    except queue.Empty:
        # If the queue is empty, do nothing
        pass
    except Exception as e:
        print(f"Error al procesar datos de la cola: {e}")

    # Update the bar heights.
    barras[0].set_height(stress)
    barras[1].set_height(ansiedad)
    barras[2].set_height(cansancio_cognitivo)
    barras[3].set_height(falta_concentracion)
    
    # Update the bar colors based on new heights and last action.
    valores_actuales = [stress, ansiedad, cansancio_cognitivo, falta_concentracion]
    for j in range(len(barras)):
        valor = valores_actuales[j]
        if valor < 10:
            barras[j].set_color('#28a745') # Green
        elif valor > 85:
            barras[j].set_color('#dc3545') # Red
        else:
            # Color based on the last action
            if ultima_accion == 'aumentar':
                barras[j].set_color('#ff6384') # Default pink for increase
            elif ultima_accion == 'disminuir':
                barras[j].set_color('#36a2eb') # Default blue for decrease
            else:
                # Keep initial color if no action has been registered yet
                barras[j].set_color(get_initial_colors()[j])

    # Update the text labels for the bars.
    for text in ax.texts:
        text.remove()
    autolabel(barras)

# --- Function to handle key presses ---
def on_key(event):
    """
    Handles keyboard events.
    If the 'a' key is pressed, it resets the graph to its initial values.
    """
    global stress, ansiedad, cansancio_cognitivo, falta_concentracion, barras, ultima_accion
    print(f"Tecla presionada: {event.key}")
    if event.key == 'a':
        print("Reseteando el gráfico a los valores iniciales...")
        stress = initial_values['stress']
        ansiedad = initial_values['ansiedad']
        cansancio_cognitivo = initial_values['cansancio_cognitivo']
        falta_concentracion = initial_values['falta_concentracion']
        
        # Update bar heights and redraw the canvas
        barras[0].set_height(stress)
        barras[1].set_height(ansiedad)
        barras[2].set_height(cansancio_cognitivo)
        barras[3].set_height(falta_concentracion)

        # Reset colors to initial state and reset last action
        initial_colors = get_initial_colors()
        for j in range(len(barras)):
            barras[j].set_color(initial_colors[j])
        ultima_accion = None
        
        # Update text labels
        for text in ax.texts:
            text.remove()
        autolabel(barras)

        fig.canvas.draw()
    
# Connect the key press event to the `on_key` function
fig.canvas.mpl_connect('key_press_event', on_key)
    
# --- Start the main loop ---
# The FuncAnimation function calls `actualizar_grafico` repeatedly.
ani = animation.FuncAnimation(fig, actualizar_grafico, interval=50, cache_frame_data=False)

# Show the graph in a window.
plt.show()

# Close the serial port on application exit.
try:
    if ser and ser.is_open:
        ser.close()
        print("Puerto serial cerrado.")
except Exception as e:
    print(f"Error al cerrar el puerto serial: {e}")
