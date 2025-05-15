from iapws import IAPWS97
from sympy import *
# import win32com.client
# import pythoncom
import subprocess as sb
from scipy.optimize import fsolve
from scipy import optimize as scop
from math import *
import scipy as sp
import pandas as pd
import numpy as np
import io
import streamlit as st

mu_0_t = [0.931, 0.931, 0.931, 0.931, 0.931, 0.931]
t_0_t = [6, 26, 167, 268, 370, 480]
ro_0_t = [0 for i in range(len(mu_0_t))]

mu_005_t = [0.937, 0.937, 0.937, 0.937, 0.937]
t_005_t = [6.557, 22.951, 177.049, 360.656, 476.667]
ro_005_t = [0.05 for i in range(len(mu_005_t))]

mu_01_t = [0.943, 0.943, 0.943, 0.943, 0.943]
t_01_t = [6.557, 154.098, 275.41, 383.607, 476.667]
ro_01_t = [0.1 for i in range(len(mu_01_t))]

mu_02_t = [0.955, 0.955, 0.955, 0.955]
t_02_t = [16.393, 157.377, 314.754, 480]
ro_02_t = [0.2 for i in range(len(mu_02_t))]

mu_05_t = [0.965, 0.965, 0.965, 0.965, 0.965, 0.965]
t_05_t = [6.557, 16.393, 127.869, 259.016, 373.77, 476.667]
ro_05_t = [0.5 for i in range(len(mu_05_t))]

mu_1_t = [0.972, 0.972, 0.972, 0.972]
t_1_t = [3.279, 203.279, 340.984, 476.667]
ro_1_t = [1 for i in range(len(mu_1_t))]

mu_0_y = [0.931, 0.931, 0.931, 0.931, 0.931, 0.931, 0.931, 0.931, 0.931]
y_0_y = [0.001, 0.012, 0.022, 0.055, 0.073, 0.126, 0.138, 0.152, 0.159]
ro_0_y = [0 for i in range(len(mu_0_y))]

mu_005_y = [0.937, 0.939, 0.94, 0.94, 0.941, 0.942, 0.943, 0.943, 0.944, 0.945, 0.945, 0.945]
y_005_y = [0.001, 0.012, 0.022, 0.038, 0.048, 0.064, 0.076, 0.093, 0.107, 0.128, 0.148, 0.159]
ro_005_y = [0.05 for i in range(len(mu_005_y))]

mu_01_y = [0.943, 0.944, 0.946, 0.949, 0.953, 0.955, 0.957, 0.958, 0.96, 0.96, 0.96]
y_01_y = [0.001, 0.008, 0.019, 0.036, 0.056, 0.074, 0.096, 0.113, 0.131, 0.144, 0.159]
ro_01_y = [0.1 for i in range(len(mu_01_y))]

mu_02_y = [0.955, 0.958, 0.961, 0.965, 0.968, 0.972, 0.975, 0.978, 0.98, 0.981, 0.981, 0.982, 0.982, 0.982]
y_02_y = [0.001, 0.011, 0.023, 0.033, 0.046, 0.064, 0.078, 0.093, 0.108, 0.126, 0.143, 0.155, 0.158, 0.159]
ro_02_y = [0.2 for i in range(len(mu_02_y))]

mu_05_y = [0.965, 0.965, 0.97, 0.976, 0.984, 0.991, 0.996, 1.001, 1.006, 1.01, 1.011, 1.012, 1.012]
y_05_y = [0.001, 0.004, 0.011, 0.022, 0.036, 0.049, 0.063, 0.077, 0.095, 0.117, 0.136, 0.149, 0.16]
ro_05_y = [0.5 for i in range(len(mu_05_y))]

mu_1_y = [0.972, 0.972, 0.977, 0.981, 0.986, 0.994, 1.002, 1.008, 1.013, 1.018, 1.022, 1.025, 1.028, 1.029, 1.03, 1.03]
y_1_y = [0.001, 0.003, 0.009, 0.017, 0.024, 0.036, 0.05, 0.063, 0.076, 0.09, 0.106, 0.119, 0.135, 0.147, 0.157, 0.159]
ro_1_y = [1 for i in range(len(mu_1_y))]

def mu(rho, t, x):
    def Mu_inter(function, parametr, x):
        parametr, residuals, rank, sv, rcond = np.polyfit(parametr, function, 8, full=True)
        function = np.poly1d(parametr)
        return function(x)
    
    if x == 1:
        r = [0, 0.05, 0.1, 0.2, 0.5, 1]
        mu_0 = Mu_inter(mu_0_t, t_0_t, t) 
        mu_005 = Mu_inter(mu_005_t, t_005_t, t) 
        mu_01 = Mu_inter(mu_01_t, t_01_t, t)
        mu_02 = Mu_inter(mu_02_t, t_02_t, t)
        mu_05 = Mu_inter(mu_05_t, t_05_t, t)
        mu_1 = Mu_inter(mu_1_t, t_1_t, t)

        mu_data = [mu_0, mu_005, mu_01, mu_02, mu_05, mu_1]
        mu = Mu_inter(mu_data, r, rho)
    else:
        r = [0, 0.05, 0.1, 0.2, 0.5, 1]
        mu_0 = Mu_inter(mu_0_y, y_0_y, (1 - x)) 
        mu_005 = Mu_inter(mu_005_y, y_005_y, (1 - x)) 
        mu_01 = Mu_inter(mu_01_y, y_01_y, (1 - x))
        mu_02 = Mu_inter(mu_02_y, y_02_y, (1 - x))
        mu_05 = Mu_inter(mu_05_y, y_05_y, (1 - x))
        mu_1 = Mu_inter(mu_1_y, y_1_y, (1 - x))

        mu_data = [mu_0, mu_005, mu_01, mu_02, mu_05, mu_1]
        mu = Mu_inter(mu_data, r, rho)

    return mu

def spline(x_1, x_2, y_1, y_2, n, i):

    x = np.array([x_1, x_2])
    y = np.array([y_1, y_2])

    if i > 0:
        coef = np.polyfit(np.array([x_1, x_2]), np.array([y_1, y_2]), i)
        polynom = np.poly1d(coef)
        x_new = np.linspace(1, n, n) 
        y_new =  polynom(x_new)

    if i == 0:
        x_new = np.linspace(1, n, n) 
        x_left = x_new[:int(2/3 * len(x_new))]
        x_right = x_new[int(2/3 * len(x_new)):]
        
        y_new = [y_1 for i in range(len(x_left))]
        y_new_2 = np.linspace(y_1, y_2, len(x_right))
        y_new.extend(y_new_2)
    return list(y_new)

def Re(temperature, pressure, velocity_outlet, chord):
    re = (velocity_outlet * chord) / (IAPWS97(T = temperature + 273.15, P = pressure).nu)
    return re

class Vector(object):
    #инициализация входных данных вектора
    def __init__(self,_x,_y):
        self.x = _x
        self.y = _y

    #Длина отрезка вектора
    def length(self):
        return (sqrt(self.x ** 2 + self.y ** 2))
    
    #скалярное произведение векторов
    def dot(self, vec):
        return (self.x * vec.x + self.y * vec.y)

    #угол между векторами
    def getAngleBetween(self, vec):
        return acos(self.dot(vec) / (self.length() * vec.length()))

    # развернуть вектор
    def reverse(self):
        self.x = self.x*-1
        self.y = self.y *-1
        return self

    # увеличеть вектор
    def increase(self, value):
        self.x *= value
        self.y *= value
        return self
    
    # привести вектор к единичной длине
    def normalize(self):
        self.increase(1/self.length())
        return self
    
    # установить длину вектора
    def setLength(self, value):
        self.normalize()
        self.x *= value
        self.y *= value
        return self

    # нормаль к вектору
    def normal2vector(self):
        return Vector(-self.y,self.x).normalize()   

class Vertex(object):
    x = float(0)
    y = float(0)

    #инициализация входных данных вектора
    def __init__(self,_x,_y):
        self.x = _x
        self.y = _y

    #Длина вектора до точки
    def length(self, point):
        return sqrt((point.x - self.x)**2 + (point.y - self.y)**2)
    
    #переместить вектор в точку
    def move(self, vector):
        self.x+=vector.x
        self.y+=vector.y
        return self

    # повернуть вектор
    def rotate(self, angleDeg, direction = True):
        if (direction):
            k = 1.0
        else:
            k = -1.0
        rad = radians(angleDeg)
        x = self.x*cos(rad) + (-k)*self.y*sin(rad)
        y = (k)*self.x*sin(rad) + self.y*cos(rad)
        self.x = x
        self.y = y
        return self

# класс по созданию линии    
class Line(object):
    k = float(0)
    b = float(0)

    # инициализация коэф прямой
    def __init__(self,vertex1,vertex2):
        self.k = (vertex2.y-vertex1.y)/(vertex2.x-vertex1.x)
        self.b = (vertex1.y-self.k*vertex1.x)

    # уравнние прямой
    def __call__(self,x):
        return self.k*x+self.b
    
    # получить координаты прямой
    def getY(self,x):
        return self.k*x+self.b
    def getX(self,y):
        return (y-self.b)/self.k
    
    def __mul__(self, line):
        x = (line.b-self.b)/(self.k-line.k)
        y = self.k*x+self.b
        return Vertex(x,y)
    
    def __eq__(self, line):
        return line;

    # получить угол между прямыми
    def getAngel(self, line):
        deg1 = degrees(atan(self.k))
        deg2 = degrees(atan(line.k))
        return abs(deg1 - deg2)

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y   

# создать вектор по координатам
def getVectorFromPoints(firstPoint, secondPoint):
    return Vector(secondPoint.x-firstPoint.x,secondPoint.y-firstPoint.y)

# получить прямую через уравнение прямой
def getLine(k,b):
    AB = Line(Vertex(0,0),Vertex(1,1))
    AB.k = k
    AB.b = b
    return AB

def fittingCircles(main_spline, fitting_spline, left_x = 0, right_x = 200, step_x = 1.5):
    result = []
    for x in np.arange(left_x,right_x,step_x):
        x1 = x
        y1 = float(main_spline(x1))
        point1 = Vertex(x1,y1)
        n1 = getLine((-1.0/float(main_spline(x1,nu=1))),y1-(-1.0/float(main_spline(x1,nu=1)))*x1)
        def f(x):
            x2 = x
            y2 = float(fitting_spline(x2))
            point2 = Vertex(x2,y2)
            n2 = getLine((-1.0/float(fitting_spline(x2,nu=1))),y2-(-1.0/float(fitting_spline(x2,nu=1)))*x2)
            o = n1*n2
            return (o.length(point1) - o.length(point2))**2
        sol = scop.fmin(f,x1-20)
        x2 = sol[0]
        if f(x2) < 1e-3:
            y2 = float(fitting_spline(x2))
            point2 = Vertex(x2,y2)
            n2 = getLine((-1.0/float(fitting_spline(x2,nu=1))),y2-(-1.0/float(fitting_spline(x2,nu=1)))*x2)
            o = n1*n2
            result.append((o.x,o.y,o.length(point2)))
    return np.array(result)

def TangentLinePoints(Point, k, dx = 1e-3, onlyLeft = False, onlyRight = False):
    PointLeft = Vertex(-dx, k * (-dx)) 
    PointRight = Vertex(+dx, k * (+dx))
    vec = Vector(Point.x, Point.y)
    PointLeft.move(vec)
    PointRight.move(vec)
    points = []
    if (onlyLeft):
        points.append(PointLeft)
    if (onlyRight):
        points.append(PointRight)
    if (not onlyLeft and not onlyRight):
        points.append(PointLeft)
        points.append(PointRight)
    return points

def bezier_curve(t, P0, P1, P2):
    u = 1 - t
    return u**2 * P0 + 2 * u * t * P1 + t**2 * P2

def int_r(num):
    num = int(num + (0.5 if num > 0 else -0.5))
    return num

def solid_profiling(array, h, i, method):
    return
#     a = 1000
#     pythoncom.CoInitialize()
#     sb.Popen(r'D:/SOLIDWORKS/SOLIDWORKS/SLDWORKS.exe')
#     sw = win32com.client.Dispatch("SldWorks.Application")
#     sw.newpart
#     VT_BYREF = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, -1)
#     Nothing = win32com.client.VARIANT(9, None)
#     sw.ActivateDoc3(f'Part{i + 1}', True, 0, VT_BYREF)
#     swDoc = sw.ActiveDoc

#     plane = []
#     for j in range(len(h)):
#         boolstatus = swDoc.Extension.SelectByID2("Сверху", "PLANE", 0, 0, 0, True, 0, Nothing, 0)
#         myRefPlane = swDoc.FeatureManager.InsertRefPlane(8, h[j] /(2 * a), 0, 0, 0, 0)
#         plane.append(myRefPlane)

#     for j in range(len(h)):
       
#         plane[j].Select2(False, -1)
#         swDoc.SketchManager.InsertSketch(True)
#         swDoc.ClearSelection2(True)
#         sketch = swDoc.SketchManager.ActiveSketch  

#         if method == 'profile rab':
#             points = []
#             for k in range(len(array[j]["rab_profil"].x)):
#                 points.append(array[j]["rab_profil"].x[k] / a)
#                 points.append(array[j]["rab_profil"].y[k] / a)
#                 points.append([0 for i in range(len(array[j]["rab_profil"].y))][k] / a)
            
#         if method == 'profile sopl':
#             points = []
#             for k in range(len(array[j]["sopl_profil"].x)):
#                 points.append(array[j]["sopl_profil"].x[k] / a)
#                 points.append(array[j]["sopl_profil"].y[k] / a)
#                 points.append([0 for i in range(len(array[j]["sopl_profil"].y))][k] / a)
            
#         point_inl = swDoc.SketchManager.CreatePoint(np.round((array[j]["point_O1"].x / a),8), np.round((array[j]["point_O1"].y / a),8), 0)
#         point_out = swDoc.SketchManager.CreatePoint(np.round((array[j]["point_O2"].x / a),8), np.round((array[j]["point_O2"].y / a),8), 0)
        
#         status = win32com.client.VARIANT(16396, None)  
#         pointArray = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, points)
#         skSegment = swDoc.SketchManager.CreateSpline3(pointArray, Nothing, Nothing, True, status)
        
#         swDoc.SketchManager.InsertSketch(False)
#     if method == 'profile sopl':
#         swDoc.SaveAs3(f'B:\\Postgraduate studies\\ДИСЕРТАЦИЯ АСПИАРНТУРА\\NEW DISERT\\Programm PTUV1\\Сопловая лопатка №{i + 1}.SLDPRT', 0, 1)
#     if method == 'profile rab':
#         swDoc.SaveAs3(f'B:\\Postgraduate studies\\ДИСЕРТАЦИЯ АСПИАРНТУРА\\NEW DISERT\\Programm PTUV1\\Рабочая лопатка №{i + 1}.SLDPRT', 0, 1)
#     # pythoncom.CoUninitialize()
#     # sw.ExitApp()

# def writeExcel(array1, array2, method):
#     if method == 'sopl':
#         df_list_sopl = []
#         for i in range(len(array1)):
#             df_list_sopl.append(pd.DataFrame(array1[i], columns = ['X', 'Y']))
#         buffer = io.BytesIO()

#         with pd.ExcelWriter(buffer, engine ='xlsxwriter') as writer:
#             for i in range(len(df_list_sopl)):
#                 df_list_sopl[i].to_excel(writer, sheet_name = f'Sheet{i}')
#             writer.close()

#             st.download_button(
#             label = "Сохранить координаты сопловой решетки",
#             data = buffer,
#             file_name ="координаты профилей сопловой решетки.xlsx",
#             mime = "application/vnd.ms-excel")

#     if method == 'rab':
#         df_list_rab = []
#         for i in range(len(array1)):
#             df_list_rab.append(pd.DataFrame(array2[i], columns = ['X', 'Y']))
#         buffer = io.BytesIO()

#         with pd.ExcelWriter(buffer, engine ='xlsxwriter') as writer:
#             for i in range(len(df_list_rab)):
#                 df_list_rab[i].to_excel(writer, sheet_name = f'Sheet{i}')
#             writer.close()

#             st.download_button(
#             label = "Сохранить координаты рабочей решетки",
#             data = buffer,
#             file_name ="координаты профилей рабочей решетки.xlsx",
#             mime = "application/vnd.ms-excel")

# def solid(array, i, method):
#     a = 1000
#     pythoncom.CoInitialize()
#     sw = win32com.client.Dispatch("SLDWORKS.Application")
#     sw.newpart
#     VT_BYREF = win32com.client.VARIANT(pythoncom.VT_BYREF | pythoncom.VT_I4, -1)
#     Nothing = win32com.client.VARIANT(9, None)
#     sw.ActivateDoc3(f'Part{i + 1}', True, 0, VT_BYREF)
#     swDoc = sw.ActiveDoc

#     boolstatus = swDoc.Extension.SelectByID2("Сверху", "PLANE", 0, 0, 0, True, 0, Nothing, 0)
#     myRefPlane = swDoc.FeatureManager.InsertRefPlane(8, 0, 0, 0, 0, 0)
#     myRefPlane.Select2(False, -1)
#     swDoc.SketchManager.InsertSketch(True)
#     swDoc.ClearSelection2(True)
#     sketch = swDoc.SketchManager.ActiveSketch  

#     points1, points2 = [], []
#     for k in range(len(array["spline_1"].x)):
#         points1.append(array["spline_1"].x[k] / a)
#         points1.append(array["spline_1"].y[k] / a)
#         points1.append([0 for i in range(len(array["spline_1"].y))][k] / a)
         
#         points2.append(array["spline_2"].x[k] / a)
#         points2.append(array["spline_2"].y[k] / a)
#         points2.append([0 for i in range(len(array["spline_2"].y))][k] / a)

#     if method == 'profile sopl':
#         revers_inl, revers_out = 1, -1

#     if method == 'profile rab':
#         revers_inl, revers_out = -1, 1 

#     arc_inl = swDoc.SketchManager.CreateArc(np.round((array["point_O1"].x / a),8), np.round((array["point_O1"].y / a),8), 0, 
#                                 np.round((array["spline_1"].x[0] / a),8), np.round((array["spline_1"].y[0] / a),8), 0, 
#                                     np.round((array["spline_2"].x[0] / a),8), np.round((array["spline_2"].y[0] / a),8), 0, revers_inl)
        
#     arc_out = swDoc.SketchManager.CreateArc(np.round((array["point_O2"].x / a),8), np.round((array["point_O2"].y / a),8), 0, 
#                                     np.round((array["spline_1"].x[len(array["spline_1"].x) - 1] / a),8), np.round((array["spline_1"].y[len(array["spline_1"].y) - 1] / a),8), 0, 
#                                     np.round((array["spline_2"].x[len(array["spline_2"].x) - 1] / a),8), np.round((array["spline_2"].y[len(array["spline_2"].y) - 1] / a),8), 0, revers_out)

#     point_inl = swDoc.SketchManager.CreatePoint(np.round((array["point_O1"].x / a),8), np.round((array["point_O1"].y / a),8), 0)
#     point_out = swDoc.SketchManager.CreatePoint(np.round((array["point_O2"].x / a),8), np.round((array["point_O2"].y / a),8), 0)
        
#     status1 = win32com.client.VARIANT(16396, None)  
#     pointArray1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, points1)
#     skSegment1 = swDoc.SketchManager.CreateSpline3(pointArray1, Nothing, Nothing, True, status1)
        
#     status2 = win32com.client.VARIANT(16396, None)
#     pointArray2=win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8,points2)
#     skSegment2 = swDoc.SketchManager.CreateSpline3(pointArray2, Nothing, Nothing, True, status2)

#     swDoc.SketchManager.InsertSketch(False)
#     if method == 'profile sopl':
#         swDoc.SaveAs3(f'B:\\Postgraduate studies\\ДИСЕРТАЦИЯ АСПИАРНТУРА\\NEW DISERT\\Programm PTUV1\\Сопловой профиль №{i + 1}.SLDPRT', 0, 2)
#     if method == 'profile rab':
#         swDoc.SaveAs3(f'B:\\Postgraduate studies\\ДИСЕРТАЦИЯ АСПИАРНТУРА\\NEW DISERT\\Programm PTUV1\\Рабочий профиль №{i + 1}.SLDPRT', 0, 2)

#     sw.ExitApp()
#     pythoncom.CoUninitialize()

