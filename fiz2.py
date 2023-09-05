import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import PySimpleGUI as sg
import math as m
import matplotlib as mt
mt.use('agg')
a = 45
v0 = 22
h = 12
w = 2
x0 = 50
y0 = 50
pr = False
xr = 24
yr = 0
z = 1
class Canvas(FigureCanvasTkAgg):
    """
    Create a canvas for matplotlib pyplot under tkinter/PySimpleGUI canvas
    """
    def __init__(self, figure=None, master=None):
        super().__init__(figure=figure, master=master)
        self.canvas = self.get_tk_widget()
        self.canvas.pack(side='top', fill='both', expand=1)

def cm_to_inch(value):
    return value/2.54

def p(t,v0,a,xr,yr,h,w):
    g=9.80665
    for i in t:
        if (v0 * np.cos(m.radians(a)) * i) >= xr and (v0 * np.cos(m.radians(a)) * i) <= (xr+w):
            if not (((v0 * np.sin(m.radians(a)) * i - g * (i**2) / 2) >= (yr+h)) and ((v0 * np.sin(m.radians(a)) * i - g * (i**2) / 2) <= (yr+h+z))):
                return False
    return True

def plot_figure(a,v0,y0,x0,pr):
    g=9.80665
    ax.cla()
    l = v0**2 * m.sin(2*m.radians(a))/g
 # time to max height
    tp = 2 * v0 * np.sin(m.radians(a)) / g

    # converting to time range
    t = np.linspace(0, tp, 1000)

    # x axis
    x = v0 * np.cos(m.radians(a)) * t

    # y axis
    y = v0 * np.sin(m.radians(a)) * t - g * (t**2) / 2
    plt.figure(figsize=(cm_to_inch(h),cm_to_inch(w)))
    ax.set_xlim(0,x0)
    ax.set_ylim(0,y0)
    ax.set_title(f'v_0 = {v0}, α = {a}', fontsize=32)
    if a == 45:
        ax.set_xlabel(f'L = {l} - Максимальная дальность полёта')
    else:
        ax.set_xlabel(f'L = {l}')
    ax.set_ylabel(f'H = {np.max(y)} - Максимальная высота')
    if pr:
        ax.add_patch (Rectangle((xr, yr), w, h))
        ax.add_patch (Rectangle((xr, yr+h+z), w, y0+5)) #z - зазор между препятствиями
        # x from xr to xr+w and y from yr+h to yr+h+z
        # for i in t:
        #     if (v0 * np.cos(m.radians(a)) * i) >= xr and (v0 * np.cos(m.radians(a)) * i) <= (xr+w):
        #         if not (((v0 * np.sin(m.radians(a)) * i - g * (i**2) / 2) >= (yr+h)) and ((v0 * np.sin(m.radians(a)) * i - g * (i**2) / 2) <= (yr+h+z))):
        #             ax.plot(x, y,color='r')
        if p(t,v0,a,xr,yr,h,w):
            ax.plot(x, y,color='g')
        else:
            ax.plot(x, y,color='r')
    else:
        ax.plot(x, y,color='g')


    # change size for figure

     #можно #87a3cc
    # plt.xlim([0, np.max(x) * 1.1])
    #
    # # ylim

    # plt.ylim([0, np.max(y) * 1.1])
    # ax.plot(x0, y0*var)
    canvas.draw()               # Rendor figure into canvas

# 3. Initial Values
#
# var = 5
# x0, y0 = np.array([-1, 0, 1]), np.array([1, 3, -1])

# 4. create PySimpleGUI window
sg.theme('DefaultNoMoreNagging')

layout = [
    [sg.Canvas(size=(640, 480), key='Canvas')],
    [sg.Text(text="xm"),sg.Spin([i for i in range(1,100)], initial_value=50,enable_events=True, k='-X-'),
    sg.Text(text="ym"),sg.Spin([i for i in range(1,100)], initial_value=50,enable_events=True, k='-Y-'),
    sg.Text(text="h"),sg.Spin([i for i in range(1,70)], initial_value=12,enable_events=True, k='-H-'),
    sg.Text(text="w"),sg.Spin([i for i in range(1,30)], initial_value=2,enable_events=True, k='-W-'),
    sg.Text(text="z"),sg.Spin([i for i in range(1,30)], initial_value=2,enable_events=True, k='-Z-'),
    sg.Text(text="xr"),sg.Spin([i for i in range(1,100)], initial_value=24,enable_events=True, k='-XR-')],
    [sg.Text(text="α"),
     sg.Slider(range=(0, 90), default_value=a, size=(10, 20), expand_x=True, enable_events=True, orientation='h', key='Slider')],
    [sg.Text(text="v0"),
     sg.Slider(range=(0, 100), default_value=v0, size=(10, 20), expand_x=True, enable_events=True, orientation='h', key='v')],
     [sg.Checkbox('Препятствие', default=False,enable_events=True, k='-P-')],
# здесь нужен радио определяющий определённое сопротивление воздуха (для F=0 программа фактически уже сделана)
    [sg.Push(), sg.Button('Exit'), sg.Push()],
]
window = sg.Window('Движение тела в поле тяжести', layout, finalize=True, resizable=True)



fig = Figure(figsize=(cm_to_inch(15),cm_to_inch(10)))

ax = fig.add_subplot()
canvas = Canvas(fig, window['Canvas'].Widget)



plot_figure(a,v0,y0,x0,pr)




while True:

    event, values = window.read()

    if event in (sg.WIN_CLOSED, 'Exit'):
        break
    elif event == 'Slider':
        # print(values)
        a = values[event]
        plot_figure(a,v0,y0,x0,pr)
    elif event == 'v':
        # print(values)
        v0 = values[event]
        plot_figure(a,v0,y0,x0,pr)
    elif event == '-Y-':
        # print(values)
        y0 = values[event]
        plot_figure(a,v0,y0,x0,pr)
    elif event == '-X-':
        # print(values)
        x0 = values[event]
        plot_figure(a,v0,y0,x0,pr)
    elif event == '-P-':
        # print(values)
        pr = values[event]
        plot_figure(a,v0,y0,x0,pr)
    elif event == '-H-':
        # print(values)
        h = values[event]
        plot_figure(a,v0,y0,x0,pr)
    elif event == '-W-':
        # print(values)
        w = values[event]
        plot_figure(a,v0,y0,x0,pr)
    elif event == '-Z-':
        # print(values)
        z = values[event]
        plot_figure(a,v0,y0,x0,pr)
    elif event == '-XR-':
        # print(values)
        xr = values[event]
        plot_figure(a,v0,y0,x0,pr)
	#если выбрано диф сопрт воздуха, то вызвать отдельную функцию
# 8. Close window to exit

window.close()
