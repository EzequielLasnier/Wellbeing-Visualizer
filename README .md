# **Interactive Wellbeing Reporter (IoT \+ Python Data Viz)**

## **Description**

This project is a real-time data visualization system that utilizes a distributed **Micro:bit** hardware architecture and asynchronous **Python** processing. The system monitors emotional wellbeing indicators (stress, anxiety, fatigue) based on two key factors: blue light exposure from screens and physical activity levels.

## **Project Architecture**

The system is divided into three main layers for a continuous Live Streaming data flow:

1. **Micro:bit Wristband (Transmitter):** Uses the accelerometer to detect movement. It sends physical activity data via radio to the receiving Micro:bit.  
2. **Micro:bit Receiver (Hub \+ Sensor):** Permanently connected to the PC. it receives data from the wristband and uses an integrated color sensor to detect the blue light spectrum from screens. It transmits all consolidated information via Serial to the computer.  
3. **Computer (Visualization):** Runs a Python script that processes the data and generates an interactive dynamic chart.

## **Project Spirit**

The central objective is to promote **Digital Balance**. Through the visual metaphor of the bars, the user can see how positive physical actions compensate for the exhaustion caused by technological overexposure, encouraging active awareness of mental health in the digital age.

## **Tech Stack**

* **Hardware:**  
  * 1x Micro:bit (Receiver connected to PC \+ Color Sensor).  
  * 1x Micro:bit (Wristband with acceleration sensor).  
* **Language:** Python 3.x.  
* **Communication:** Radio (between Micro:bits) and Serial Protocol (PySerial to PC).  
* **Visualization:** Matplotlib for real-time dynamic charts.  
* **Data Management:** Threading & Queue architecture to avoid UI latency.

## **Repository Files**

* /src/grafico\_dinamico.py: Main Python script for visualization.  
* /firmware/microbit-Feria-Ciencias-Gráfico.hex: Firmware for the receiver Micro:bit.  
* /firmware/microbit-Pulsera-Actividad-Fisica.hex: Firmware for the wristband Micro:bit.  
* /assets/: Images and visual resources of the project.

## **Configuration & Installation**

1. **Flash Firmware:** Flash the .hex files onto the corresponding Micro:bits.  
2. **Connection:** Connect the receiver Micro:bit to the PC via USB.  
3. **Install Dependencies:**  
   pip install \-r requirements.txt

4. **Run:**  
   python src/grafico\_dinamico.py

*Project developed for Science Fair \- IoT and Health Integration.*