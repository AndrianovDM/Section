from math import *
from function import *

def profiling(D_k, width , height, alpha_0, alpha_1, M_c1, value_1, value_2, value_3, value_4, value_5, value_6, method_2, number_blades = 0, method_3 = None):
    D_k, width , height = D_k*1e3, width*1e3, height*1e3
    alpha_instal = 42 + 40 * (alpha_1 / alpha_0) - 2 * (alpha_0 / alpha_1)
    
    if value_6 == 0 or value_6 == 1:
        chord = width / sin(radians(alpha_instal))
    else:
        chord = value_6
        width = chord * sin(radians(alpha_instal))

    if 25 < alpha_0 <= 40:
        alpha0_scapular = alpha_1 / ((1.167 * 10**(-3) * alpha_0**2) + (-7.12 * 10**(-2) * alpha_0) + (0.841) + (((-6.7 * 10**(-7) * alpha_0**2) + (-1.31 * 10**(-3) * alpha_0) + 8.12 * 10**(-2)) * alpha_1)) 
    elif 40 < alpha_0 <= 60:
        alpha0_scapular = alpha_1 / ((-2.194 * 10**(-4) * alpha_0**2) + (2.905 * 10**(-2) * alpha_0) + (-0.9509) + (((1.65 * 10**(-5) * alpha_0**2) + (-2.26 * 10**(-3) * alpha_0) + 9.17 * 10**(-2)) * alpha_1))
    else:
        alpha0_scapular = alpha_1 / ((-4.136 * 10**(-5) * alpha_0**2) + (6.755 * 10**(-3) * alpha_0) + (-0.2543) + (((2.9 * 10**(-6) * alpha_0**2) + (-6.085 * 10**(-4) * alpha_0) + 4.165 * 10**(-2)) * alpha_1))    

    alpha1_ef = alpha_1 - value_1 
    Gamma = 18.75 - 13.75 * M_c1

    if value_2 > 0.7:
        Cmax_ = 1 - value_2 * sin(radians(alpha0_scapular))  # range volue_1 = 0.7-1.2
    else:
        Cmax_ = value_2 # range volue_1 = 0.04-0.4

    if method_2 == "sopl":
        t_opt_ = (0.45 * (((180 * sin(radians(alpha_0))) / ((180 - alpha_0 - alpha_1) * sin(radians(alpha_1)))) ** (1 / 3)) * (1 - Cmax_))
    if method_2 == "rab":
        t_opt_ = (0.6 * (((180 * sin(radians(alpha_0))) / ((180 - alpha_0 - alpha_1) * sin(radians(alpha_1)))) ** (1 / 3)) * (1 - Cmax_))
    
    if number_blades == 0:
        number_blades = int_r((pi * D_k) / ((t_opt_) * chord))
    else:
        number_blades = number_blades

    pitch = (pi * D_k) / number_blades
    alpha1_scapular = alpha1_ef + 26.66 * Cmax_ - 0.276 * Gamma - 4.29 * (pitch / chord) + 4.13
    
    if value_3 == 0:
        X_ = (0.1092 + 1.008 * 10 ** (-3) * alpha0_scapular + 3.335 * 10 ** (-3) * alpha1_scapular - 0.1525 * (pitch / chord) + 0.2188 * Cmax_ + 4.697 * 10 ** (-3) * Gamma)
    else:
        X_ = value_3 # range volue_3 = 0.1-0.4
    
    r_inl_ = value_4 * (height / chord)  # range volue_3=0.008-0.08
    r_out_ = value_5 * (height / chord)  # range volue_3=0.005-0.025

    L_ = 1.32 - 2.182 * 10 ** (-3) * alpha0_scapular - 3.072 * 10 ** (-3) * alpha1_scapular + 0.367 * Cmax_
    fi_1 = 3.51 * degrees(atan(((Cmax_ / 2) - r_inl_) / ((X_) * (L_) - r_inl_)))
    fi_2 = 2.16 * degrees(atan(((Cmax_ / 2) - r_out_) / ((1 - (X_)) * (L_) - r_out_)))

    a1 = pitch * sin(radians(alpha_0))
    a2 = pitch * sin(radians(alpha1_ef))
    r_inl = r_inl_ * chord
    r_out = r_out_ * chord
    C_max = Cmax_ * chord
    X_max = X_ * chord
    L = L_ * chord

    # Рабочая область
    G = Vertex(0.0, 0.0)
    E = Vertex(0.0, pitch)
    H = Vertex(width, -chord * cos(radians(alpha_instal)))
    F = Vertex(H.x, H.y + pitch)
    #################################

    # Входная кромка
    GH = Line(G, H)
    O1 = Vertex(r_inl, 0.0)
    BC = r_inl / sin(radians(alpha_instal))
    O1.y = GH(O1.x) + BC
    
    K = Vertex(10 * -sin(radians(alpha0_scapular)), 10 * -cos(radians(alpha0_scapular))).move( getVectorFromPoints(G, O1))
    y1 = r_inl * cos(radians(fi_1 / 2.0))
    x1 = y1 / tan(radians(fi_1 / 2.0))
    O1temp = Vertex(x1 + r_inl * sin(radians(fi_1 / 2.0)), 0.0)
    S1 = Vertex(x1, y1).rotate(90.0 - alpha0_scapular)
    S2 = Vertex(x1, -y1).rotate(90.0 - alpha0_scapular)
    M = Vertex(0.0, 0.0).rotate(90.0 - alpha0_scapular)
    O1temp.rotate(90.0 - alpha0_scapular)
    vec = getVectorFromPoints(O1temp, O1)
    S1.move(vec)
    S2.move(vec)
    M.move(vec)
    O1temp.move(vec)
    ###################################

    # Выходная кромка
    O2 = Vertex(H.x - r_out, 0.0)
    BC = r_out / sin(radians(alpha_instal))
    O2.y = GH(O2.x) + BC
    L = Vertex(10 * sin(radians(alpha1_scapular)), 10 * -cos(radians(alpha1_scapular))).move(getVectorFromPoints(G, O2))  # Временная L
    y2 = r_out * cos(radians(fi_2 / 2.0))
    x2 = y2 / tan(radians(fi_2 / 2.0))
    O2temp = Vertex(x2 + r_out * sin(radians(fi_2 / 2.0)), 0.0)
    V1 = Vertex(x2, y2).rotate(90.0 + alpha1_scapular)
    V2 = Vertex(x2, -y2).rotate(90.0 + alpha1_scapular)
    N = Vertex(0.0, 0.0).rotate(90.0 + alpha1_scapular)
    O2temp.rotate(90.0 + alpha1_scapular)
    vec = getVectorFromPoints(O2temp, O2)
    V1.move(vec)
    V2.move(vec)
    N.move(vec)
    O2temp.move(vec)
    ###################################

    # Скилет профиля
    NV1 = Line(N, V1)
    MS1 = Line(M, S1)
    NV2 = Line(N, V2)
    MS2 = Line(M, S2)
    P = MS1 * NV2
    R = NV1 * MS2
    ###################################

    # Разбивка скилетных линий
    length1 = S1.length(P) / 5.0
    moveVec1 = getVectorFromPoints(S1, P).setLength(length1)
    length2 = V2.length(P) / 5.0
    moveVec2 = getVectorFromPoints(P, V2).setLength(length2)

    P1 = Vertex(S1.x, S1.y)
    P1.move(moveVec1)
    P2 = Vertex(P1.x, P1.y)
    P2.move(moveVec1)
    P3 = Vertex(P2.x, P2.y)
    P3.move(moveVec1)
    P4 = Vertex(P3.x, P3.y)
    P4.move(moveVec1)
    P5 = Vertex(P.x, P.y)
    P5.move(moveVec2)
    P6 = Vertex(P5.x, P5.y)
    P6.move(moveVec2)
    P7 = Vertex(P6.x, P6.y)
    P7.move(moveVec2)
    P8 = Vertex(P7.x, P7.y)
    P8.move(moveVec2)
    ###################################

    # Вычисление координат кривой Безье
    spline_1 = Point(bezier_curve(np.linspace(0, 1, 100), S1.x, P.x, V2.x), bezier_curve(np.linspace(0, 1, 100), S1.y, P.y, V2.y))
    spline_2 = Point(bezier_curve(np.linspace(0, 1, 100), S2.x, R.x, V1.x), bezier_curve(np.linspace(0, 1, 100), S2.y, R.y, V1.y))
    ###################################

    # Построение соседнего профиля
    spline_1copy = Point(spline_1.x, [spline_1.y[i] + pitch for i in range(len(spline_1.y))])
    spline_2copy = Point(spline_2.x, [spline_2.y[i] + pitch for i in range(len(spline_2.y))])
    O1copy = Point(O1.x, O1.y + pitch)
    O2copy = Point(O2.x, O2.y + pitch)
    ###################################

    if method_2 == "sopl":
        dx = 0.0 - O1.x
        dy = 0.0 - O1.y

        if method_3 == "r_1":
            dx = 0.0 - O1.x
            dy = 0.0 - O1.y

        if method_3 == "r_2":
            dx = 0.0 - O2.x
            dy = 0.0 - O2.y

        if method_3 == "C_m":
            cm = Point(((sum(spline_1.x) + sum(spline_2.x) + O1.x + O2.x) / (2 * (len(spline_1.x)))), ((sum(spline_1.y) + sum(spline_2.y) + O1.y + O2.y) / (2 * (len(spline_1.x)))))
            dx = 0.0 - cm.x
            dy = 0.0 - cm.y

        G.x, G.y, E.x, E.y, H.x, H.y, F.x, F.y = G.x + dx, G.y + dy, E.x + dx, E.y + dy, H.x + dx, H.y + dy, F.x + dx, F.y + dy
        O1.x, O1.y, O1copy.x, O1copy.y, S1.x, S1.y, S2.x, S2.y, M.x, M.y, K.x, K.y, R.x, R.y = O1.x + dx, O1.y + dy, O1copy.x + dx, O1copy.y + dy, S1.x + dx, S1.y + dy, S2.x + dx, S2.y + dy, M.x + dx, M.y + dy, K.x + dx, K.y + dy, R.x + dx, R.y + dy
        O2.x, O2.y, O2copy.x, O2copy.y, V1.x, V1.y, V2.x, V2.y, N.x, N.y, L.x, L.y, P.x, P.y = O2.x + dx, O2.y + dy, O2copy.x + dx, O2copy.y + dy, V1.x + dx, V1.y + dy, V2.x + dx, V2.y + dy, N.x + dx, N.y + dy, L.x + dx, L.y + dy, P.x + dx, P.y + dy
        P1.x, P1.y, P2.x, P2.y, P3.x, P3.y, P4.x, P4.y = P1.x + dx, P1.y + dy, P2.x + dx, P2.y + dy, P3.x + dx, P3.y + dy, P4.x + dx, P4.y + dy
        P5.x, P5.y, P6.x, P6.y, P7.x, P7.y, P8.x, P8.y = P5.x + dx, P5.y + dy, P6.x + dx, P6.y + dy, P7.x + dx, P7.y + dy, P8.x + dx, P8.y + dy
        spline_1.x, spline_1.y = [x + dx for x in spline_1.x], [y + dy for y in spline_1.y]
        spline_2.x, spline_2.y = [x + dx for x in spline_2.x], [y + dy for y in spline_2.y]
        spline_1copy.x, spline_1copy.y = [x + dx for x in spline_1copy.x], [y + dy for y in spline_1copy.y]
        spline_2copy.x, spline_2copy.y = [x + dx for x in spline_2copy.x], [y + dy for y in spline_2copy.y]
        cm = Point(((sum(spline_1.x) + sum(spline_2.x) + O1.x + O2.x) / (2 * (len(spline_1.x)))), ((sum(spline_1.y) + sum(spline_2.y) + O1.y + O2.y) / (2 * (len(spline_1.x)))))

        if method_3 == "C_m":
            cm = Point(((sum(spline_1.x) + sum(spline_2.x) + O1.x + O2.x) / (2 * (len(spline_1.x)))), ((sum(spline_1.y) + sum(spline_2.y) + O1.y + O2.y) / (2 * (len(spline_1.x)))))
            cm = Point(0, 0)

        angle_inl_1 = np.arctan2(spline_1.y[0] - O1.y, spline_1.x[0] - O1.x)
        angle_inl_2 = np.arctan2(spline_2.y[0] - O1.y, spline_2.x[0] - O1.x)
        theta_inl = angle_inl_2 - angle_inl_1
        if theta_inl < 0:
            theta_inl += 2 * np.pi
        angles_inl = np.linspace(angle_inl_1, angle_inl_1 + theta_inl, 20)
        segment_inl_x = O1.x + r_inl * np.cos(angles_inl)
        segment_inl_y = O1.y + r_inl * np.sin(angles_inl)

        angle_out_1 = np.arctan2(spline_1.y[len(spline_1.y)-1] - O2.y, spline_1.x[len(spline_1.x)-1] - O2.x)
        angle_out_2 = np.arctan2(spline_2.y[len(spline_2.y)-1] - O2.y, spline_2.x[len(spline_2.x)-1] - O2.x)
        theta_out = angle_out_2 - angle_out_1
        if theta_out > 0:
            theta_out += 2 * np.pi
        angles_out = np.linspace(angle_out_1, angle_out_1 + theta_out, 20)
        segment_out_x = O2.x + r_out * np.cos(angles_out)
        segment_out_y = O2.y + r_out * np.sin(angles_out)

        angle_inl_copy_1 = np.arctan2(spline_1copy.y[0] - O1copy.y, spline_1copy.x[0] - O1copy.x)
        angle_inl_copy_2 = np.arctan2(spline_2copy.y[0] - O1copy.y, spline_2copy.x[0] - O1copy.x)
        theta_copy_inl = angle_inl_copy_2 - angle_inl_copy_1
        if theta_copy_inl < 0:
            theta_copy_inl += 2 * np.pi
        angles_copy_inl = np.linspace(angle_inl_copy_1, angle_inl_copy_1 + theta_copy_inl, 20)
        segment_copy_inl_x = O1copy.x + r_inl * np.cos(angles_copy_inl)
        segment_copy_inl_y = O1copy.y + r_inl * np.sin(angles_copy_inl)

        angle_out_copy_1 = np.arctan2(spline_1copy.y[len(spline_1copy.y)-1] - O2copy.y, spline_1copy.x[len(spline_1copy.x)-1] - O2copy.x)
        angle_out_copy_2 = np.arctan2(spline_2copy.y[len(spline_2copy.y)-1] - O2copy.y, spline_2copy.x[len(spline_2copy.x)-1] - O2copy.x)
        theta_copy_out = angle_out_copy_2 - angle_out_copy_1
        if theta_copy_out > 0:
            theta_copy_out += 2 * np.pi
        angles_copy_out = np.linspace(angle_out_copy_1, angle_out_copy_1 + theta_copy_out, 20)
        segment_copy_out_x = O2copy.x + r_out * np.cos(angles_copy_out)
        segment_copy_out_y = O2copy.y + r_out * np.sin(angles_copy_out)

        profil_x = []
        for i in range(len(spline_1.x)):
            profil_x.append(spline_1.x[i])
        profil_x.pop()
        for i in range(len(segment_out_x)):
            profil_x.append(segment_out_x[i])
        spline_2.x.reverse()
        for i in range(len(spline_2.x)):
            profil_x.append(spline_2.x[i])
        segment_inl_x = np.flip(segment_inl_x)  
        for i in range(len(segment_inl_x)):
            profil_x.append(segment_inl_x[i])

        profil_y = []
        for i in range(len(spline_1.y)):
            profil_y.append(spline_1.y[i])
        profil_y.pop()
        for i in range(len(segment_out_y)):
            profil_y.append(segment_out_y[i])
        spline_2.y.reverse()
        for i in range(len(spline_2.y)):
            profil_y.append(spline_2.y[i])  
        segment_inl_y = np.flip(segment_inl_y)  
        for i in range(len(segment_inl_y)):
            profil_y.append(segment_inl_y[i])        
        sopl_profil = Point(profil_x, profil_y)

        profil_copy_x = []
        for i in range(len(spline_1copy.x)):
            profil_copy_x.append(spline_1copy.x[i])
        profil_copy_x.pop()
        for i in range(len(segment_copy_out_x)):
            profil_copy_x.append(segment_copy_out_x[i])
        spline_2copy.x.reverse()
        for i in range(len(spline_2copy.x)):
            profil_copy_x.append(spline_2copy.x[i])
        segment_copy_inl_x = np.flip(segment_copy_inl_x)  
        for i in range(len(segment_copy_inl_x)):
            profil_copy_x.append(segment_copy_inl_x[i])

        profil_copy_y = []
        for i in range(len(spline_1copy.y)):
            profil_copy_y.append(spline_1copy.y[i])
        profil_copy_y.pop()
        for i in range(len(segment_copy_out_y)):
            profil_copy_y.append(segment_copy_out_y[i])
        spline_2copy.y.reverse()
        for i in range(len(spline_2copy.y)):
            profil_copy_y.append(spline_2copy.y[i])  
        segment_copy_inl_y = np.flip(segment_copy_inl_y)  
        for i in range(len(segment_copy_inl_y)):
            profil_copy_y.append(segment_copy_inl_y[i])        
        sopl_profil_copy = Point(profil_copy_x, profil_copy_y)

        param_0 = {"B_sopl": width,
                "b_sopl": chord,
                "t_sopl": pitch,
                "r_inl_sopl": r_inl,
                "r_out_sopl": r_out,
                "a_inl_sopl": a1,
                "a_out_sopl": a2,
                "Xmax_sopl": X_max,
                "Cmax_sopl": C_max,
                "Dk_sopl": D_k,
                "height_sopl": height,
                "alpha_instal": alpha_instal,
                "alpha0sc_sopl": alpha0_scapular,
                "alpha1sc_sopl": alpha1_scapular,
                "fi1_sopl": fi_1,
                "fi2_sopl": fi_2,
                "gamma_sopl": Gamma,
                "number_sopl": number_blades}

        param_1 = {'point_G':G, 'point_E':E, 'point_H':H, 'point_F':F,
                   'point_O1':O1, 'point_O1copy':O1copy, 'r_inl':r_inl, 'point_S1':S1, 'point_S2':S2, 'point_M':M, 'point_K':K, 'point_R':R,
                   'point_O2':O2, 'point_O2copy':O2copy, 'r_out':r_out,'point_V1':V1, 'point_V2':V2, 'point_N':N, 'point_L':L, 'point_P':P,
                   'point_P1':P1, 'point_P2':P2, 'point_P3':P3, 'point_P4':P4, 'point_P5':P5, 'point_P6':P6, 'point_P7':P7, 'point_P8':P8, 'point_cm':cm,
                   'spline_1':spline_1, 'spline_2':spline_2, 'spline_1copy':spline_1copy, 'spline_2copy':spline_2copy}

        param_2 = {'Dk_sopl':D_k, 'sopl_profil':sopl_profil, 'sopl_profil_copy':sopl_profil_copy, 'spline_1':spline_1, 'spline_2':spline_2, 'spline_1copy':spline_1copy, 'spline_2copy':spline_2copy, 
                   'point_O1':O1, 'point_O1copy':O1copy, 'r_inl':r_inl, 'point_O2':O2, 'point_O2copy':O2copy, 'r_out':r_out, 'point_cm':cm}
            
    if method_2 == "rab":
        cm = Point(((sum(spline_1.x) + sum(spline_2.x) + O1.x + O2.x) / (2 * (len(spline_1.x)))), ((sum(spline_1.y) + sum(spline_2.y) + O1.y + O2.y) / (2 * (len(spline_1.x)))))
        dx = 0.0 - cm.x
        dy = 0.0 - cm.y

        if method_3 == "r_1":
            dx = 0.0 - O1.x
            dy = 0.0 - O1.y

        if method_3 == "r_2":
            dx = 0.0 - O2.x
            dy = 0.0 - O2.y

        if method_3 == "C_m":
            cm = Point(((sum(spline_1.x) + sum(spline_2.x) + O1.x + O2.x) / (2 * (len(spline_1.x)))), ((sum(spline_1.y) + sum(spline_2.y) + O1.y + O2.y) / (2 * (len(spline_1.x)))))
            dx = 0.0 - cm.x
            dy = 0.0 - cm.y

        G.x, G.y, E.x, E.y, H.x, H.y, F.x, F.y = G.x + dx, -(G.y + dy), E.x + dx, -(E.y + dy), H.x + dx, -(H.y + dy), F.x + dx, -(F.y + dy)
        O1.x, O1.y, O1copy.x, O1copy.y, S1.x, S1.y, S2.x, S2.y, M.x, M.y, K.x, K.y, R.x, R.y = O1.x + dx, -(O1.y + dy), O1copy.x + dx, -(O1copy.y + dy), S1.x + dx, -(S1.y + dy), S2.x + dx, -(S2.y + dy), M.x + dx, -(M.y + dy), K.x + dx, -(K.y + dy), R.x + dx, -(R.y + dy)
        O2.x, O2.y, O2copy.x, O2copy.y, V1.x, V1.y, V2.x, V2.y, N.x, N.y, L.x, L.y, P.x, P.y = O2.x + dx, -(O2.y + dy), O2copy.x + dx, -(O2copy.y + dy), V1.x + dx, -(V1.y + dy), V2.x + dx, -(V2.y + dy), N.x + dx, -(N.y + dy), L.x + dx, -(L.y + dy), P.x + dx, -(P.y + dy)
        P1.x, P1.y, P2.x, P2.y, P3.x, P3.y, P4.x, P4.y = P1.x + dx, -(P1.y + dy), P2.x + dx, -(P2.y + dy), P3.x + dx, -(P3.y + dy), P4.x + dx, -(P4.y + dy)
        P5.x, P5.y, P6.x, P6.y, P7.x, P7.y, P8.x, P8.y = P5.x + dx, -(P5.y + dy), P6.x + dx, -(P6.y + dy), P7.x + dx, -(P7.y + dy), P8.x + dx, -(P8.y + dy)
        spline_1.x, spline_1.y = [x + dx for x in spline_1.x], [-(y + dy) for y in spline_1.y]
        spline_2.x, spline_2.y = [x + dx for x in spline_2.x], [-(y + dy) for y in spline_2.y]
        spline_1copy.x, spline_1copy.y = [x + dx for x in spline_1copy.x], [-(y + dy)for y in spline_1copy.y]
        spline_2copy.x, spline_2copy.y = [x + dx for x in spline_2copy.x], [-(y + dy) for y in spline_2copy.y]
        cm = Point(0, 0)

        if method_3 == "C_m":
            cm = Point(((sum(spline_1.x) + sum(spline_2.x) + O1.x + O2.x) / (2 * (len(spline_1.x)))), ((sum(spline_1.y) + sum(spline_2.y) + O1.y + O2.y) / (2 * (len(spline_1.x)))))
            cm = Point(0, 0)

        angle_inl_1 = np.arctan2(spline_1.y[0] - O1.y, spline_1.x[0] - O1.x)
        angle_inl_2 = np.arctan2(spline_2.y[0] - O1.y, spline_2.x[0] - O1.x)
        theta_inl = angle_inl_2 - angle_inl_1
        if theta_inl > 0:
            theta_inl -= 2 * np.pi
        angles_inl = np.linspace(angle_inl_1, angle_inl_1 + theta_inl, 20)
        segment_inl_x = O1.x + r_inl * np.cos(angles_inl)
        segment_inl_y = O1.y + r_inl * np.sin(angles_inl)

        angle_out_1 = np.arctan2(spline_1.y[len(spline_1.y)-1] - O2.y, spline_1.x[len(spline_1.x)-1] - O2.x)
        angle_out_2 = np.arctan2(spline_2.y[len(spline_2.y)-1] - O2.y, spline_2.x[len(spline_2.x)-1] - O2.x)
        theta_out = angle_out_2 - angle_out_1
        if theta_out < 0:
            theta_out -= 2 * np.pi
        angles_out = np.linspace(angle_out_1, angle_out_1 + theta_out, 20)
        segment_out_x = O2.x + r_out * np.cos(angles_out)
        segment_out_y = O2.y + r_out * np.sin(angles_out)

        angle_inl_copy_1 = np.arctan2(spline_1copy.y[0] - O1copy.y, spline_1copy.x[0] - O1copy.x)
        angle_inl_copy_2 = np.arctan2(spline_2copy.y[0] - O1copy.y, spline_2copy.x[0] - O1copy.x)
        theta_copy_inl = angle_inl_copy_2 - angle_inl_copy_1
        if theta_copy_inl > 0:
            theta_copy_inl -= 2 * np.pi
        angles_copy_inl = np.linspace(angle_inl_copy_1, angle_inl_copy_1 + theta_copy_inl, 20)
        segment_copy_inl_x = O1copy.x + r_inl * np.cos(angles_copy_inl)
        segment_copy_inl_y = O1copy.y + r_inl * np.sin(angles_copy_inl)

        angle_out_copy_1 = np.arctan2(spline_1copy.y[len(spline_1copy.y)-1] - O2copy.y, spline_1copy.x[len(spline_1copy.x)-1] - O2copy.x)
        angle_out_copy_2 = np.arctan2(spline_2copy.y[len(spline_2copy.y)-1] - O2copy.y, spline_2copy.x[len(spline_2copy.x)-1] - O2copy.x)
        theta_copy_out = angle_out_copy_2 - angle_out_copy_1
        if theta_copy_out < 0:
            theta_copy_out -= 2 * np.pi
        angles_copy_out = np.linspace(angle_out_copy_1, angle_out_copy_1 + theta_copy_out, 20)
        segment_copy_out_x = O2copy.x + r_out * np.cos(angles_copy_out)
        segment_copy_out_y = O2copy.y + r_out * np.sin(angles_copy_out)

        profil_x = []
        for i in range(len(spline_1.x)):
            profil_x.append(spline_1.x[i])
        profil_x.pop()
        for i in range(len(segment_out_x)):
            profil_x.append(segment_out_x[i])
        spline_2.x.reverse()
        for i in range(len(spline_2.x)):
            profil_x.append(spline_2.x[i])
        segment_inl_x = np.flip(segment_inl_x)  
        for i in range(len(segment_inl_x)):
            profil_x.append(segment_inl_x[i])

        profil_y = []
        for i in range(len(spline_1.y)):
            profil_y.append(spline_1.y[i])
        profil_y.pop()
        for i in range(len(segment_out_y)):
            profil_y.append(segment_out_y[i])
        spline_2.y.reverse()
        for i in range(len(spline_2.y)):
            profil_y.append(spline_2.y[i])  
        segment_inl_y = np.flip(segment_inl_y)  
        for i in range(len(segment_inl_y)):
            profil_y.append(segment_inl_y[i])        
        rab_profil = Point(profil_x, profil_y)

        profil_copy_x = []
        for i in range(len(spline_1copy.x)):
            profil_copy_x.append(spline_1copy.x[i])
        profil_copy_x.pop()
        for i in range(len(segment_copy_out_x)):
            profil_copy_x.append(segment_copy_out_x[i])
        spline_2copy.x.reverse()
        for i in range(len(spline_2copy.x)):
            profil_copy_x.append(spline_2copy.x[i])
        segment_copy_inl_x = np.flip(segment_copy_inl_x)  
        for i in range(len(segment_copy_inl_x)):
            profil_copy_x.append(segment_copy_inl_x[i])

        profil_copy_y = []
        for i in range(len(spline_1copy.y)):
            profil_copy_y.append(spline_1copy.y[i])
        profil_copy_y.pop()
        for i in range(len(segment_copy_out_y)):
            profil_copy_y.append(segment_copy_out_y[i])
        spline_2copy.y.reverse()
        for i in range(len(spline_2copy.y)):
            profil_copy_y.append(spline_2copy.y[i])  
        segment_copy_inl_y = np.flip(segment_copy_inl_y)  
        for i in range(len(segment_copy_inl_y)):
            profil_copy_y.append(segment_copy_inl_y[i])        
        rab_profil_copy = Point(profil_copy_x, profil_copy_y)

        param_0 = {"B_rab": width,
                "b_rab": chord,
                "t_rab": pitch,
                "r_inl_rab": r_inl,
                "r_out_rab": r_out,
                "a_inl_rab": a1,
                "a_out_rab": a2,
                "Xmax_rab": X_max,
                "Cmax_rab": C_max,
                "Dk_rab": D_k,
                "height_rab": height,
                "betta_instal": alpha_instal,
                "betta0sc_rab": alpha0_scapular,
                "betta1sc_rab": alpha1_scapular,
                "fi1_rab": fi_1,
                "fi2_rab": fi_2,
                "gamma_rab": Gamma,
                "number_rab": number_blades}

        param_1 = {'point_G':G, 'point_E':E, 'point_H':H, 'point_F':F,
                   'point_O1':O1, 'point_O1copy':O1copy, 'r_inl':r_inl, 'point_S1':S1, 'point_S2':S2, 'point_M':M, 'point_K':K, 'point_R':R,
                   'point_O2':O2, 'point_O2copy':O2copy, 'r_out':r_out, 'point_V1':V1, 'point_V2':V2, 'point_N':N, 'point_L':L, 'point_P':P,
                   'point_P1':P1, 'point_P2':P2, 'point_P3':P3, 'point_P4':P4, 'point_P5':P5, 'point_P6':P6, 'point_P7':P7, 'point_P8':P8, 'point_cm':cm,
                   'spline_1':spline_1, 'spline_2':spline_2, 'spline_1copy':spline_1copy, 'spline_2copy':spline_2copy}

        param_2 = {'Dk_rab':D_k, 'rab_profil':rab_profil, 'rab_profil_copy':rab_profil_copy, 'spline_1':spline_1, 'spline_2':spline_2, 'spline_1copy':spline_1copy, 'spline_2copy':spline_2copy, 
                   'point_O1':O1, 'point_O1copy':O1copy, 'r_inl':r_inl, 'point_O2':O2, 'point_O2copy':O2copy, 'r_out':r_out, 'point_cm':cm}

    return param_0, param_1, param_2, number_blades
