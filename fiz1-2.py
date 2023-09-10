import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
import PySimpleGUI as sg
import math
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
m = 10
k = 1
dt = 0.01
MODE = 1

class Canvas(FigureCanvasTkAgg):
  """
    Create a canvas for matplotlib pyplot under tkinter/PySimpleGUI canvas
    """

  def __init__(self, figure=None, master=None):
    super().__init__(figure=figure, master=master)
    self.canvas = self.get_tk_widget()
    self.canvas.pack(side='top', fill='both', expand=1)


def cm_to_inch(value):
  return value / 2.54


def p(t, v0, a, xr, yr, h, w):
  g = 9.80665
  for i in t:
    if (v0 * np.cos(math.radians(a)) * i) >= xr and (v0 * np.cos(math.radians(a)) *
                                                  i) <= (xr + w):
      if not (((v0 * np.sin(math.radians(a)) * i - g * (i**2) / 2) >=
               (yr + h)) and ((v0 * np.sin(math.radians(a)) * i - g *
                               (i**2) / 2) <= (yr + h + z))):
        return False
  return True
def plot_figure_hard_wing(a, v0, y0, x0, m, k, dt):
    g = 9.80665
    ax.cla()
    vx = [v0*math.cos(math.radians(a))]
    vy = [v0*math.sin(math.radians(a))]
    x = [0]
    y = [0]
    i = 0
    while True:
        vx.append(vx[i] - ( k/m*((vx[i]*vx[i]+vy[i]*vy[i])**0.5) *vx[i]*dt) )
        vy.append(vy[i] - (g + k/m*((vx[i]*vx[i]+vy[i]*vy[i])**0.5) *vy[i])*dt )
        x.append(x[i]+vx[i]*dt)
        y.append(y[i]+vy[i]*dt)
        if y[i+1] <= 0:
            break
        i = i + 1
    plt.figure(figsize=(cm_to_inch(h), cm_to_inch(w)))
    ax.set_xlim(0, x0)
    ax.set_ylim(0, y0)
    ax.set_title(r'${V}_0$'+f' = {v0}, α = {a}', fontsize=32)
    ax.set_xlabel(f'H = {np.max(x)} - Максимальная дальность полёта')
    ax.set_ylabel(f'H = {np.max(y)} - Максимальная высота')
    ax.plot(x, y, color='g')
    canvas.draw()
def plot_figure_wing(a, v0, y0, x0, m, k):
    g = 9.80665
    t0 = 0.01
    ax.cla()
    if k == 0:
        k = 0.00001
    while True:
            yt = (v0*math.sin(math.radians(a))+m*g/k)*(1-(math.exp(-k*t0/m)))-g*t0
            if yt <= 0:
                break
            t0 = t0 + 0.01
    t = np.linspace(0, t0, 1000)
    l = v0 * math.cos(math.radians(a))*m/k*(1-(math.exp(-k*t0/m)))
    x = v0 * np.cos(math.radians(a))*m/k*(1-(np.exp(-k*t/m)))
    y = (m/k)*((v0*np.sin(math.radians(a))+m*g/k)*(1-(np.exp(-k*t/m)))-g*t)
    plt.figure(figsize=(cm_to_inch(h), cm_to_inch(w)))
    ax.set_xlim(0, x0)
    ax.set_ylim(0, y0)
    ax.set_title(r'${V}_0$'+f' = {v0}, α = {a}', fontsize=32)
    if l == np.max(x):
      ax.set_xlabel(f'L = {l} - Максимальная дальность полёта')
    else:
      ax.set_xlabel(f'L = {l}')
    ax.set_ylabel(f'H = {np.max(y)} - Максимальная высота')
    ax.plot(x, y, color='g')
    canvas.draw()
def plot_figure(a, v0, y0, x0, pr):
  g = 9.80665
  ax.cla()
  l = v0**2 * math.sin(2 * math.radians(a)) / g
  # time to max height
  tp = 2 * v0 * np.sin(math.radians(a)) / g

  # converting to time range
  t = np.linspace(0, tp, 1000)

  # x axis
  x = v0 * np.cos(math.radians(a)) * t

  # y axis
  y = v0 * np.sin(math.radians(a)) * t - g * (t**2) / 2
  plt.figure(figsize=(cm_to_inch(h), cm_to_inch(w)))
  ax.set_xlim(0, x0)
  ax.set_ylim(0, y0)
  ax.set_title(r'${V}_0$'+f' = {v0}, α = {a}', fontsize=32)
  if a == 45:
    ax.set_xlabel(f'L = {l} - Максимальная дальность полёта')
  else:
    ax.set_xlabel(f'L = {l}')
  ax.set_ylabel(f'H = {np.max(y)} - Максимальная высота')
  if pr:
    ax.add_patch(Rectangle((xr, yr), w, h))
    ax.add_patch(Rectangle((xr, yr + h + z), w,
                           y0 + 5))  #z - зазор между препятствиями
    # x from xr to xr+w and y from yr+h to yr+h+z
    # for i in t:
    #     if (v0 * np.cos(m.radians(a)) * i) >= xr and (v0 * np.cos(m.radians(a)) * i) <= (xr+w):
    #         if not (((v0 * np.sin(m.radians(a)) * i - g * (i**2) / 2) >= (yr+h)) and ((v0 * np.sin(m.radians(a)) * i - g * (i**2) / 2) <= (yr+h+z))):
    #             ax.plot(x, y,color='r')
    if p(t, v0, a, xr, yr, h, w):
      ax.plot(x, y, color='g')
    else:
      ax.plot(x, y, color='r')
  else:
    ax.plot(x, y, color='g')

  # change size for figure

  #можно #87a3cc
  # plt.xlim([0, np.max(x) * 1.1])
  #
  # # ylim

  # plt.ylim([0, np.max(y) * 1.1])
  # ax.plot(x0, y0*var)
  canvas.draw()  # Rendor figure into canvas


# 3. Initial Values
#
# var = 5
# x0, y0 = np.array([-1, 0, 1]), np.array([1, 3, -1])

# 4. create PySimpleGUI window
sg.theme('DefaultNoMoreNagging')
krange = []
for i in range(0,1000):
    krange.append(i/10)
trange = []
for i in range(1,1000000):
    trange.append(i/1000)
layout = [
    [sg.Canvas(size=(640, 480), key='Canvas')],
    [
        sg.Radio('F_c = 0',"RD1", default = True, enable_events = True, k='-FCZ-'),
        sg.Radio('F_c = -kv', "RD1", enable_events = True, k='-FCK-'),
        sg.Radio('F_c = -k |v| v', "RD1", enable_events = True, k='-FCC-'),
        sg.Text(text="xm"),
        sg.Spin([i for i in range(1, 100)],
                initial_value=50,
                enable_events=True,
                k='-X-'),
        sg.Text(text="ym"),
        sg.Spin([i for i in range(1, 100)],
                initial_value=50,
                enable_events=True,
                k='-Y-'),
        sg.pin(sg.Text(text="m",k='-MT-',visible=False)),
        sg.pin(sg.Spin([i for i in range(1, 100)],
                visible=True,
                initial_value=10,
                enable_events=True,
                k='-M-')),
        sg.pin(sg.Text(text="k",k='-KT-',visible=False)),
        sg.pin(sg.Spin(krange,
                visible=True,
                initial_value=krange[10],
                enable_events=True,
                k='-K-')),
        sg.pin(sg.Text(text="∆t",k='-DT-',visible=False)),
        sg.pin(sg.Spin(trange,
                visible=True,
                initial_value=0.01,
                enable_events=True,
                k='-D-')),
    ],
    [
        sg.Text(text="α"),
        sg.Slider(range=(0, 90),
                  default_value=a,
                  size=(10, 20),
                  expand_x=True,
                  enable_events=True,
                  orientation='h',
                  key='Slider')
    ],
    [
        sg.Text(text="v0"),
        sg.Slider(range=(0, 100),
                  default_value=v0,
                  size=(10, 20),
                  expand_x=True,
                  enable_events=True,
                  orientation='h',
                  key='v')
    ],
    [sg.Checkbox('Препятствие', default=False, enable_events=True, k='-P-'),
    sg.Text(text="h",enable_events=True,k='-HT-'),
    sg.Spin([i for i in range(1, 70)],
            initial_value=12,
            enable_events=True,
            k='-H-'),
    sg.Text(text="w",k='-WT-'),
    sg.Spin([i for i in range(1, 30)],
            initial_value=2,
            enable_events=True,
            k='-W-'),
    sg.Text(text="z",k='-ZT-'),
    sg.Spin([i for i in range(1, 30)],
            initial_value=2,
            enable_events=True,
            k='-Z-'),
    sg.Text(text="xr",k='-XRT-'),
    sg.Spin([i for i in range(1, 100)],
            initial_value=24,
            enable_events=True,
            k='-XR-')
    ],

    # здесь нужен радио определяющий определённое сопротивление воздуха (для F=0 программа фактически уже сделана)
  #При выбранном радио с сопротивлением воздуха  вызвать другую функцию вывода и использовать другой список элементов интерфейса (чтобы убрать лишние)
    [sg.Push(), sg.Button('Exit'), sg.Push()],
]
# def win_call(title,lt,finalize, resizable):
#     return sg.Window(title,lt,finalize,resizable)
# window = win_call('Движение тела в поле тяжести',layout,True,True)
window = sg.Window('Движение тела в поле тяжести',
                   layout,
                   finalize=True,
                   resizable=True)

fig = Figure(figsize=(cm_to_inch(16), cm_to_inch(10)))

ax = fig.add_subplot()
canvas = Canvas(fig, window['Canvas'].Widget)

# plot_figure(a, v0, y0, x0, pr)

def mode_conf():
    if MODE == 1:
        window["-P-"].update(visible=True)
    if pr:
        window["-HT-"].update(visible=True)
        window["-H-"].update(visible=True)
        window["-WT-"].update(visible=True)
        window["-W-"].update(visible=True)
        window["-ZT-"].update(visible=True)
        window["-Z-"].update(visible=True)
        window["-XRT-"].update(visible=True)
        window["-XR-"].update(visible=True)
    else:
        window["-H-"].update(visible=False)
        window["-HT-"].update(visible=False)
        window["-W-"].update(visible=False)
        window["-WT-"].update(visible=False)
        window["-Z-"].update(visible=False)
        window["-ZT-"].update(visible=False)
        window["-XR-"].update(visible=False)
        window["-XRT-"].update(visible=False)
    if MODE == 1:
        # window["-P-"].update(visible=True)
        window["-MT-"].update(visible=False)
        window["-M-"].update(visible=False)
        window["-KT-"].update(visible=False)
        window["-K-"].update(visible=False)
        window["-DT-"].update(visible=False)
        window["-D-"].update(visible=False)
        return plot_figure(a, v0, y0, x0, pr)
    elif MODE == 2:
        window["-P-"].update(visible=False)
        window["-MT-"].update(visible=True)
        window["-M-"].update(visible=True)
        window["-KT-"].update(visible=True)
        window["-K-"].update(visible=True)
        window["-DT-"].update(visible=False)
        window["-D-"].update(visible=False)
        # print('MODE 2')
        return plot_figure_wing(a, v0, y0, x0, m, k)
    elif MODE == 3:
        window["-P-"].update(visible=False)
        window["-MT-"].update(visible=True)
        window["-M-"].update(visible=True)
        window["-KT-"].update(visible=True)
        window["-K-"].update(visible=True)
        window["-DT-"].update(visible=True)
        window["-D-"].update(visible=True)
        return plot_figure_hard_wing(a, v0, y0, x0, m, k, dt)
mode_conf()
while True:

  event, values = window.read()
  # print(event)
  if event in (sg.WIN_CLOSED, 'Exit'):
    break
  elif event == '-FCZ-':
      MODE = 1
      mode_conf()
  elif event == '-FCK-':
      MODE = 2
      mode_conf()
  elif event == '-FCC-':
      MODE = 3
      mode_conf()
  elif event == 'Slider':
    a = values[event]
    mode_conf()
  elif event == 'v':
    # print(values)
    v0 = values[event]
    mode_conf()
  elif event == '-Y-':
    # print(values)
    y0 = values[event]
    mode_conf()
  elif event == '-X-':
    # print(values)
    x0 = values[event]
    mode_conf()
  elif event == '-P-':
    # print(values)
    pr = values[event]
    mode_conf()
  elif event == '-H-':
    # print(values)
    h = values[event]
    mode_conf()
  elif event == '-W-':
    # print(values)
    w = values[event]
    mode_conf()
  elif event == '-Z-':
    # print(values)
    z = values[event]
    mode_conf()
  elif event == '-XR-':
    # print(values)
    xr = values[event]
    mode_conf()
  elif event == '-K-':
     # print(values)
     k = values[event]
     mode_conf()
  elif event == '-M-':
     # print(values)
     m = values[event]
     mode_conf()
  elif event == '-DT-':
     # print(values)
     dt = values[event]
     mode_conf()

#если выбрано диф сопрт воздуха, то вызвать отдельную функцию
# 8. Close window to exit

window.close()
