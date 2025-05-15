import matplotlib.pyplot as plt
import matplotlib as mpl
import plotly.graph_objects as go
import numpy as np
from function import fittingCircles
import scipy.interpolate as scint
from matplotlib.ticker import LinearLocator

def profiling_plot(arr, method):
    fig = plt.figure(figsize = (20, 12), constrained_layout = True)
    gs = fig.add_gridspec(2, 3)
    fax_main = fig.add_subplot(gs[:, :-1])
    plt.tick_params(axis = 'both', which = 'major', labelsize = 20, 
                    direction = 'inout', length = 10, pad = 15) # настройка обозначений значений
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which = 'major', color = '#aaa', linewidth = 1) # настройка сетки
    plt.grid (which = 'minor', color = '#aaa', ls = ':')

    fax_main.set_title("Геометрия профиля", size = 25)
    plt.xlabel('x, мм', fontsize = 20, loc = 'center')
    plt.ylabel('y, мм', fontsize = 20, loc = 'center')
    plt.axis("equal")

    if method == 'sopl':
        col = "red"
    if method == 'rab':
        col = "blue"

    # Входная кромка визуализация
    circle_inl = plt.Circle((arr['point_O1'].x, arr['point_O1'].y), arr['r_inl'], fill = False, ls = "-", linewidth = 5, color = col)  
    fax_main.add_artist(circle_inl)
    circle_inl_copy = plt.Circle((arr['point_O1copy'].x, arr['point_O1copy'].y), arr['r_inl'], fill = False, ls = "-", linewidth = 5, color = col)
    fax_main.add_artist(circle_inl_copy)
    plt.scatter(arr['point_O1'].x, arr['point_O1'].y, color = col, s = 15, marker = "o")
    plt.scatter(arr['point_O1copy'].x, arr['point_O1copy'].y, color = col, s = 15, marker = "o")
    ###################################   

    # Выходная кромка визуализация
    circle_out = plt.Circle((arr['point_O2'].x, arr['point_O2'].y), arr['r_out'], fill = False, ls = "-", linewidth = 5, color = col)
    fax_main.add_artist(circle_out)
    circle_out_copy = plt.Circle((arr['point_O2copy'].x, arr['point_O2copy'].y), arr['r_out'], fill = False, ls = "-", linewidth = 5, color = col)
    fax_main.add_artist(circle_out_copy)
    ###################################

    # Сплайн выпуклой спинки профиля
    plt.plot(arr['spline_1'].x, arr['spline_1'].y, ls = "-", linewidth = 5, color = col)
    plt.plot(arr['spline_2'].x, arr['spline_2'].y, ls = "-", linewidth = 5, color = col)
    plt.plot(arr['spline_1copy'].x, arr['spline_1copy'].y, ls = "-", linewidth = 5, color = col)
    plt.plot(arr['spline_2copy'].x, arr['spline_2copy'].y, ls = "-", linewidth = 5, color = col)
    plt.scatter(arr['point_cm'].x, arr['point_cm'].y, color = "black", s = 30, marker = "o")
    ###################################
   
    dataSS = []
    for i in range(len(arr['spline_1'].x)):
        dataSS.append([arr['spline_1'].x[i], arr['spline_1'].y[i]])
    dataSS = np.array(sorted(dataSS, key = lambda dataSS: dataSS[0]))
    tck = scint.splrep(dataSS[:, 0], dataSS[:, 1], k = 3, s = 1.0)
    splineSS = scint.BSpline(tck[0], tck[1], tck[2])
    x_back = np.arange(arr['point_S1'].x, arr['point_V2'].x, 0.01)
    y_back = splineSS(x_back)

    dataPS = []
    for i in range(len(arr['spline_2'].x)):
        dataPS.append([arr['spline_2'].x[i], arr['spline_2'].y[i]])
    dataPS = np.array(sorted(dataPS, key = lambda dataPS: dataPS[0]))
    tck = scint.splrep(dataPS[:, 0], dataPS[:, 1], k = 3, s = 1.0)
    splinePS = scint.BSpline(tck[0], tck[1], tck[2])
    x_trough = np.arange(arr['point_S2'].x, arr['point_V1'].x, 0.01)
    y_trough = splinePS(x_trough)

    dataPScopy = []
    for i in range(len(arr['spline_2copy'].x)):
        dataPScopy.append([arr['spline_2copy'].x[i], arr['spline_2copy'].y[i]])
    dataPScopy = np.array(sorted(dataPScopy, key = lambda dataPScopy: dataPScopy[0]))
    tck = scint.splrep(dataPScopy[:, 0], dataPScopy[:, 1], k = 3, s = 1.0)
    splinePScopy = scint.BSpline(tck[0], tck[1], tck[2])
    x_trough = np.arange(arr['point_S2'].x, arr['point_V1'].x, 0.01)
    y_trough = splinePScopy(x_trough)

    fit_data = fittingCircles(splinePScopy, splineSS, left_x = arr['point_S2'].x, right_x = arr['point_V1'].x)
    for i in np.arange(0, len(fit_data), 1):
        fax_main.add_artist(plt.Circle((fit_data[i, 0], fit_data[i, 1]), fit_data[i, 2], fill = False, color = "black", ls = "--"))
    k = lambda spline, x: spline(x, nu = 2) / (1 + spline(x, nu = 1) ** 2) ** (1.5)  # нахождение кривизны
    x_1 = np.arange(arr['point_S1'].x, arr['point_V2'].x, 0.01)
    x_2 = np.arange(arr['point_S2'].x, arr['point_V1'].x, 0.01)

    fax_dir = fig.add_subplot(gs[0, -1])
    fax_dir.set_title("Производная", size = 25)
    plt.tick_params(axis = 'both', which = 'major', labelsize = 20, 
                    direction = 'inout', length = 10, pad = 15) # настройка обозначений значений
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which = 'major', color = '#aaa', linewidth = 1) # настройка сетки
    plt.grid (which = 'minor', color = '#aaa', ls = ':')

    plt.plot(x_1, k(splinePS, x_1), ls = "-", color = "red", linewidth = 3)
    plt.plot(x_1, splinePS(x_1, nu = 2), ls = "--", color = "red", linewidth = 3)
    plt.plot(x_2, k(splineSS, x_2), ls = "-", color = "blue", linewidth = 3)
    plt.plot(x_2, splineSS(x_2, nu = 2), ls = "--", color = "blue", linewidth = 3)

    fax_r = fig.add_subplot(gs[1, -1])
    fax_r.set_title("Распределение окружностей", size = 25)
    plt.tick_params(axis = 'both', which = 'major', labelsize = 20, 
                    direction = 'inout', length = 10, pad = 15) # настройка обозначений значений
    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which = 'major', color = '#aaa', linewidth = 1) # настройка сетки
    plt.grid (which = 'minor', color = '#aaa', ls = ':')
    plt.plot(fit_data[:, 0], fit_data[:, 1], ls = "-", color = "black", linewidth = 3)
    plt.xlabel('x, мм', fontsize = 20, loc = 'center')
    plt.ylabel('R, мм', fontsize = 20, loc = 'center')
    plt.axis("equal")

    plt.show()

def profSoplRab_plot(sopl, rab):
    fig = plt.figure(figsize = (15, 8), constrained_layout = False)
    gs = fig.add_gridspec(1, 2)
    fax_main = fig.add_subplot()
    plt.tick_params(axis = 'both', which = 'major', labelsize = 20, 
    direction = 'inout', length = 10, pad = 15) # настройка обозначений значений

    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which = 'major', color = '#aaa', linewidth = 1) # настройка сетки
    plt.grid (which = 'minor', color = '#aaa', ls = ':')

    plt.xlabel('x, мм', fontsize = 20, loc = 'center')
    plt.ylabel('y, мм', fontsize = 20, loc = 'center')
    plt.axis("equal")
    fig.suptitle('Сечение ступени на среднем диаметре', size = 30, weight = 1000, ha = 'center', va = 'center_baseline', style = 'italic')

    # Входная кромка визуализация
    circle_inl_sopl = plt.Circle((sopl['point_O1'].x, sopl['point_O1'].y), sopl['r_inl'], fill = False, ls = "-", linewidth = 3, color = "red")  
    fax_main.add_artist(circle_inl_sopl)
    circle_inl_copy_sopl = plt.Circle((sopl['point_O1copy'].x, sopl['point_O1copy'].y), sopl['r_inl'], fill = False, ls = "-", linewidth = 3, color = "red")
    fax_main.add_artist(circle_inl_copy_sopl)
    plt.scatter(sopl['point_O1'].x, sopl['point_O1'].y, color = "red", s = 10, marker = "o")
    plt.scatter(sopl['point_O1copy'].x, sopl['point_O1copy'].y, color = "red", s = 10, marker = "o")
    ###################################   

    # Выходная кромка визуализация
    circle_out_sopl = plt.Circle((sopl['point_O2'].x, sopl['point_O2'].y), sopl['r_out'], fill = False, ls = "-", linewidth = 3, color = "red")
    fax_main.add_artist(circle_out_sopl)
    circle_out_copy_sopl = plt.Circle((sopl['point_O2copy'].x, sopl['point_O2copy'].y), sopl['r_out'], fill = False, ls = "-", linewidth = 3, color = "red")
    fax_main.add_artist(circle_out_copy_sopl)
    ###################################

    # Сплайн выпуклой спинки профиля
    plt.plot(sopl['spline_1'].x, sopl['spline_1'].y, ls = "-", linewidth = 3, color = "red")
    plt.plot(sopl['spline_2'].x, sopl['spline_2'].y, ls = "-", linewidth = 3, color = "red")
    plt.plot(sopl['spline_1copy'].x, sopl['spline_1copy'].y, ls = "-", linewidth = 3, color = "red")
    plt.plot(sopl['spline_2copy'].x, sopl['spline_2copy'].y, ls = "-", linewidth = 3, color = "red")
    # plt.scatter(sopl['point_cm'].x, sopl['point_cm'].y, color = "blue", s = 20, marker = "o")

    a = 30
    b = -10
    rab['spline_1'].x, rab['spline_1'].y = [x + sopl['point_O2copy'].x + a for x in rab['spline_1'].x], [y + sopl['point_O2copy'].y + b for y in rab['spline_1'].y]
    rab['spline_1copy'].x, rab['spline_1copy'].y = [x + sopl['point_O2copy'].x + a for x in rab['spline_1copy'].x], [y + sopl['point_O2copy'].y + b for y in rab['spline_1copy'].y]
    rab['spline_2'].x, rab['spline_2'].y = [x + sopl['point_O2copy'].x + a for x in rab['spline_2'].x], [y + sopl['point_O2copy'].y + b for y in rab['spline_2'].y]
    rab['spline_2copy'].x, rab['spline_2copy'].y = [x + sopl['point_O2copy'].x + a for x in rab['spline_2copy'].x], [y + sopl['point_O2copy'].y + b for y in rab['spline_2copy'].y]
    
    rab['point_O1'].x, rab['point_O1'].y = rab['point_O1'].x + sopl['point_O2copy'].x + a, rab['point_O1'].y + sopl['point_O2copy'].y + b
    rab['point_O1copy'].x, rab['point_O1copy'].y = rab['point_O1copy'].x + sopl['point_O2copy'].x + a, rab['point_O1copy'].y + sopl['point_O2copy'].y + b
    rab['point_O2'].x, rab['point_O2'].y = rab['point_O2'].x + sopl['point_O2copy'].x + a, rab['point_O2'].y + sopl['point_O2copy'].y + b
    rab['point_O2copy'].x, rab['point_O2copy'].y = rab['point_O2copy'].x + sopl['point_O2copy'].x + a, rab['point_O2copy'].y + sopl['point_O2copy'].y + b
    ###################################

    # Входная кромка визуализация
    circle_inl_rab = plt.Circle((rab['point_O1'].x, rab['point_O1'].y), rab['r_inl'], fill = False, ls = "-", linewidth = 3, color = "blue")  
    fax_main.add_artist(circle_inl_rab)
    circle_inl_copy_rab = plt.Circle((rab['point_O1copy'].x, rab['point_O1copy'].y), rab['r_inl'], fill = False, ls = "-", linewidth = 3, color = "blue")
    fax_main.add_artist(circle_inl_copy_rab)
    plt.scatter(rab['point_O1'].x, rab['point_O1'].y, color = "blue", s = 10, marker = "o")
    plt.scatter(rab['point_O1copy'].x, rab['point_O1copy'].y, color = "blue", s = 10, marker = "o")
    ###################################   

    # Выходная кромка визуализация
    circle_out_rab = plt.Circle((rab['point_O2'].x, rab['point_O2'].y), rab['r_out'], fill = False, ls = "-", linewidth = 3, color = "blue")
    fax_main.add_artist(circle_out_rab)
    circle_out_copy_rab = plt.Circle((rab['point_O2copy'].x, rab['point_O2copy'].y), rab['r_out'], fill = False, ls = "-", linewidth = 3, color = "blue")
    fax_main.add_artist(circle_out_copy_rab)
    ###################################

    # Сплайн выпуклой спинки профиля
    plt.plot(rab['spline_1'].x, rab['spline_1'].y, ls = "-", linewidth = 3, color = "blue")
    plt.plot(rab['spline_2'].x, rab['spline_2'].y, ls = "-", linewidth = 3, color = "blue")
    plt.plot(rab['spline_1copy'].x, rab['spline_1copy'].y, ls = "-", linewidth = 3, color = "blue")
    plt.plot(rab['spline_2copy'].x, rab['spline_2copy'].y, ls = "-", linewidth = 3, color = "blue")
    # plt.scatter(rab['point_cm'].x, rab['point_cm'].y, color = "red", s = 20, marker = "o")
    plt.show()

def profil_sect_plot(arr, method):
    fig = plt.figure(figsize = (15, 8), constrained_layout = False)
    gs = fig.add_gridspec(1, 2)
    fax_main = fig.add_subplot()
    plt.tick_params(axis = 'both', which = 'major', labelsize = 20, 
    direction = 'inout', length = 10, pad = 15) # настройка обозначений значений

    plt.grid(True)
    plt.minorticks_on()
    plt.grid(which = 'major', color = '#aaa', linewidth = 1) # настройка сетки
    plt.grid (which = 'minor', color = '#aaa', ls = ':')

    plt.xlabel('x, мм', fontsize = 20, loc = 'center')
    plt.ylabel('y, мм', fontsize = 20, loc = 'center')
    plt.axis("equal")
    
    if method == 'sopl':
        line_color = (1, 0, 0)
        fig.suptitle("Геометрия сопловой по сечениям", size = 30, weight = 1000, ha = 'center', va = 'center_baseline', style = 'italic')
    if method == 'rab':
        line_color = (0, 0, 1)
        fig.suptitle("Геометрия рабочей по сечениям", size = 30, weight = 1000, ha = 'center', va = 'center_baseline', style = 'italic')

    for i in range(len(arr)):
        # Входная кромка визуализация
        circle_inl = plt.Circle((arr[i]['point_O1'].x, arr[i]['point_O1'].y), arr[i]['r_inl'], fill = False, ls = "-", linewidth = 2, color = line_color)  
        fax_main.add_artist(circle_inl)
        circle_inl_copy = plt.Circle((arr[i]['point_O1copy'].x, arr[i]['point_O1copy'].y), arr[i]['r_inl'], fill = False, ls = "-", linewidth = 2, color = line_color)
        fax_main.add_artist(circle_inl_copy)
        plt.scatter(arr[i]['point_O1'].x, arr[i]['point_O1'].y, color = line_color, s = 5, marker = "o")
        plt.scatter(arr[i]['point_O1copy'].x, arr[i]['point_O1copy'].y, color = line_color, s = 5, marker = "o")
        ###################################  

        # Выходная кромка визуализация
        circle_out = plt.Circle((arr[i]['point_O2'].x, arr[i]['point_O2'].y), arr[i]['r_out'], fill = False, ls = "-", linewidth = 1, color = line_color)
        fax_main.add_artist(circle_out)
        circle_out_copy = plt.Circle((arr[i]['point_O2copy'].x, arr[i]['point_O2copy'].y), arr[i]['r_out'], fill = False, ls = "-", linewidth = 1, color = line_color)
        fax_main.add_artist(circle_out_copy)
        ###################################

        # Сплайн выпуклой спинки профиля
        plt.plot(arr[i]['spline_1'].x, arr[i]['spline_1'].y, ls = "-", linewidth = 2, color = line_color)
        plt.plot(arr[i]['spline_2'].x, arr[i]['spline_2'].y, ls = "-", linewidth = 2, color = line_color)
        plt.plot(arr[i]['spline_1copy'].x, arr[i]['spline_1copy'].y, ls = "-", linewidth = 2, color = line_color)
        plt.plot(arr[i]['spline_2copy'].x, arr[i]['spline_2copy'].y, ls = "-", linewidth = 2, color = line_color)
        if method == 'sopl':
            plt.scatter(arr[i]['point_cm'].x, arr[i]['point_cm'].y, color = "blue", s = 25, marker = "o")
        if method == 'rab':
            plt.scatter(arr[i]['point_cm'].x, arr[i]['point_cm'].y, color = "red", s = 25, marker = "o")
        ###################################
    plt.show()

def profil_plot_3D(arr, method):

    if method == 'sopl':
        X, Y, Z = [], [], []
        for i in range(len(arr)):
            X.append(arr[i]['sopl_profil'].x), 
            Y.append(arr[i]['sopl_profil'].y)
            Z.append([arr[i]['Dk_sopl'] for j in (range(len(arr[i]['sopl_profil'].x)))])        

        X_copy, Y_copy, Z_copy = [], [], []
        for i in range(len(arr)):
            X_copy.append(arr[i]['sopl_profil_copy'].x), 
            Y_copy.append(arr[i]['sopl_profil_copy'].y)
            Z_copy.append([arr[i]['Dk_sopl'] for j in (range(len(arr[i]['sopl_profil_copy'].x)))])        

        fig = go.Figure()
        fig.add_trace(go.Surface(x = X, y = Y, z = Z, colorscale = [[0, 'red'], [0.5, 'red']]))
        fig.add_trace(go.Surface(x = X_copy, y = Y_copy, z = Z_copy, colorscale = [[0, 'red'], [0.5, 'red']]))
        fig.update_layout(
            scene = dict(xaxis = dict(showgrid = False, showticklabels = False, showbackground = False,),
                         yaxis = dict(showgrid = False, showticklabels = False, showbackground = False,),
                         zaxis = dict(showgrid = False, showticklabels = False, showbackground = False,),), 
                         width = 900, height = 500)
        
    if method == 'rab':
        X, Y, Z = [], [], []
        for i in range(len(arr)):
            X.append(arr[i]['rab_profil'].x), 
            Y.append(arr[i]['rab_profil'].y)
            Z.append([arr[i]['Dk_rab'] for j in (range(len(arr[i]['rab_profil'].x)))])        

        X_copy, Y_copy, Z_copy = [], [], []
        for i in range(len(arr)):
            X_copy.append(arr[i]['rab_profil_copy'].x), 
            Y_copy.append(arr[i]['rab_profil_copy'].y)
            Z_copy.append([arr[i]['Dk_rab'] for j in (range(len(arr[i]['rab_profil_copy'].x)))])        

        fig = go.Figure()
        fig.add_trace(go.Surface(x = X, y = Y, z = Z, colorscale = 'reds'))
        fig.add_trace(go.Surface(x = X_copy, y = Y_copy, z = Z_copy, colorscale= 'reds'))
        fig.update_layout(
            scene = dict(xaxis = dict(showgrid = False, showticklabels = False, showbackground = False,),
                         yaxis = dict(showgrid = False, showticklabels = False, showbackground = False,),
                         zaxis = dict(showgrid = False, showticklabels = False, showbackground = False,),), 
                         width = 700, height = 500)

    return fig

def profil_parametrs_plot(arr, num):

    fig = plt.figure(figsize = (11, 5)) # параметры окна
    ax = plt.axes()
    plt.tick_params(axis = 'both', which = 'major', labelsize = 15, direction = 'inout', length = 3, pad = 3) # настройка обозначений значений
    plt.grid(True)
    plt.grid(which = 'major', color = 'black', linewidth = 0.4) # настройка сетки

    fig.suptitle(f'Распределение параметров по высоте ступени №{num+1}', size = 30, weight = 1000, ha = 'center', va = 'center_baseline', style = 'italic')

    radius_  = np.linspace(0, 1, len(arr[0]))
    B, = plt.plot(arr[0], radius_, color ='blue', marker = '^', ms = 8, linewidth = 3, linestyle = '-')  
    b, = plt.plot(arr[1], radius_, color ='red', marker = '>', ms = 8, linewidth = 3, linestyle = '-')  
    t, = plt.plot(arr[2], radius_, color ='green', marker = 'o', ms = 8, linewidth = 3, linestyle = '-')  
    radius_inl, = plt.plot(arr[3], radius_, color ='deeppink', marker = 'H', ms = 8, linewidth = 3, linestyle = '-')  
    radius_out, = plt.plot(arr[4], radius_, color ='teal', marker = 'X', ms = 8, linewidth = 3, linestyle = '-')  
    a_out, = plt.plot(arr[6], radius_, color ='navy', marker = 'D', ms = 8, linewidth = 3, linestyle = '-')  
    C_max, = plt.plot(arr[8], radius_, color ='purple', marker = 'p', ms = 8, linewidth = 3, linestyle = '-')      

    ax.legend((B, b, t, radius_inl, radius_out, a_out, C_max), ['Ширина решетки', 'Хорда решетки', 'Шаг решетки', 'Радиус вх. кромки', 'Радиус вых. кромки', 'Горло решетки', 'Толщина профиля'], fontsize = 12, frameon = True, framealpha = True, bbox_to_anchor=(1.05, 1.0), loc='upper left')
    plt.xlabel(r'мм ', fontsize = 20)
    plt.ylabel(r'-',fontsize = 20)
    plt.show()
