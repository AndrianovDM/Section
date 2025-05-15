from math import *
from iapws import IAPWS97
from sectionPlot import *
from sectionTable import *
from streamlitFunction import *
from profiling import *
from profilingPlot import *
from profilingTable import *
from stageTable import *

# st.set_option('deprecation.showPyplotGlobalUse', False)
def spin_laws_stage(P_0_, t_0_, H_0_, L_u, alpha0, alpha1, alpha2, C1, C2, U1, U2, h_sopl, B_sopl, Dsr_sopl, h_rab, B_rab, Dsr_rab, sect, method):  

    radius_sopl_i = [(h_sopl / (sect - 1)) * i + (Dsr_sopl - h_sopl) / 2 for i in range(sect)]
    radius_rab_i = [(h_rab / (sect - 1)) * i + (Dsr_rab - h_rab) / 2 for i in range(sect)]
    
    radius_sopl_i_ = [radius_sopl_i[i] / (Dsr_sopl  / 2) for i in range(sect)]  
    radius_rab_i_ = [radius_rab_i[i] / (Dsr_rab / 2) for i in range(sect)]
    
    relative_sopl_i =[(1 / (sect - 1)) * i for i in range(sect)]
    relative_rab_i =[(1 / (sect - 1)) * i for i in range(sect)]

    B_sopl_i = [B_sopl for i in range(sect)]
    B_rab_i = [B_rab for i in range(sect)]

    h_sopl_i = [h_sopl for i in range(sect)]
    h_rab_i = [h_rab for i in range(sect)]
    
    D_sopl = [radius_sopl_i[i] * 2 for i in range(sect)]
    D_rab = [radius_rab_i[i] * 2 for i in range(sect)]

    fi_i = [0.98 - 0.008 * (B_sopl / h_sopl) + 0.001 * i for i in range(sect)]
    fi_i[0] = fi_i[0] - 0.0025
    fi_i[sect-1] = fi_i[sect - 1] - 0.0015

    psi_i = [0.96 - 0.014 * (B_rab / h_rab) + 0.001 * i for i in range(sect)]
    psi_i[0] = psi_i[0] - 0.0025
    psi_i[sect - 1] = psi_i[sect - 1] - 0.0015

    alpha_0_i = [alpha0 for i in range(sect)]

    if method == 'rtgconst':
        alpha_1_i = [degrees(atan(tan(radians(alpha1)) / radius_sopl_i_[i])) for i in range(sect)]  
        C_1a_i = [(C1 * sin(radians(alpha1))) * (1 + (tan(radians(alpha1)))**2) / (radius_sopl_i_[i]**2 + (tan(radians(alpha1)))**2) for i in range(sect)]
        C_1u_i = [C_1a_i[i] / (tan(radians(alpha_1_i[i]))) for i in range(sect)]

        C_1_i =  [C_1a_i[i] / (sin(radians(alpha_1_i[i]))) for i in range(sect)]
        C_1t_i = [C_1_i[i] / fi_i[i] for i in range(sect)]

        C_2a_i = [(C2 * sin(radians(alpha2))) for i in range(sect)]
        U_1_i =  [U1 * radius_sopl_i_[i] for i in range(sect)]
        U_2_i =  [U2 * radius_rab_i_[i]  for i in range(sect)]
        H_0_sa_i_ = [(C_1t_i[i]**2) / 2e3 for i in range(sect)]
        H_0_rk_i = [H_0_  - H_0_sa_i_[i] for i in range(sect)]        
        ro_term_i = [H_0_rk_i[i] / H_0_ for i in range(sect)]

        betta_1_i = []
        for i in range(sect):
            if C_1u_i[i] - U_1_i[i] >= 0:
                betta_1_i_ = degrees(atan((C_1a_i[i]) / (C_1u_i[i] - U_1_i[i])))
                betta_1_i.append(betta_1_i_)    
            else:
                betta_1_i_ = 180 - degrees(atan((C_1a_i[i]) / abs(C_1u_i[i] - U_1_i[i])))
                betta_1_i.append(betta_1_i_)

        W_1_i = [ C_1a_i[i] / (sin(radians(betta_1_i[i]))) for i in range(sect)]
        W_1u_i = [ C_1u_i[i] - U_1_i[i] for i in range(sect)]
        W_1a_i = [ W_1_i[i] * sin(radians(betta_1_i[i])) for i in range(sect) ]
        C_2u_i =[ (L_u * 1e3 / U_2_i[i]) - C_1u_i[i] for i in range(sect)]
        W_2u_i = [ C_2u_i[i] + U_2_i[i]  for i in range(sect)] 

        alpha_2_i = []
        for i in range(sect):
            if W_2u_i[i] >= U_2_i[i]:
                alpha_2_i_ = degrees(atan(C_2a_i[i] / abs((C_2u_i[i]))))
                alpha_2_i.append(alpha_2_i_)  
            else:
                alpha_2_i_ = 180 - degrees(atan(C_2a_i[i] / abs((C_2u_i[i]))))
                alpha_2_i.append(alpha_2_i_)  

        C_2_i = [C_2a_i[i] / (sin(radians(alpha_2_i[i]))) for i in range(sect)]
        C_2a_i = [C_2_i[i] * sin(radians(alpha_2_i[i])) for i in range(sect)]
        betta_2_i = [degrees(atan(C_2a_i[i] / (C_2u_i[i] + U_2_i[i]))) for i in range(sect)]
        W_2_i = [W_2u_i[i] / (cos(radians(betta_2_i[i]))) for i in range(sect)]
        W_2t_i = [W_2_i[i] / psi_i[i] for i in range(sect)]
        W_2a_i = [W_2_i[i] * sin(radians(betta_2_i[i])) for i in range(sect)]
        ro_k_i = [ 1 - ((C_1u_i[i] - (C_2u_i[i])) / (2 * U_1_i[i])) for i in range(sect)]

    if method == 'C1uconst':
        C_1a_i = [(C1 * sin(radians(alpha1))) for i in range(sect)]  
        C_1u_i = [(C1 * cos(radians(alpha1))) / (radius_sopl_i_[i]) for i in range(sect)]  
        alpha_1_i = [degrees(atan(C_1a_i[i] / C_1u_i[i])) for i in range(sect)]

        C_1_i =  [C_1a_i[i] / (sin(radians(alpha_1_i[i]))) for i in range(sect)]
        C_1t_i = [C_1_i[i] / fi_i[i] for i in range(sect)]
        
        C_2a_i = [(C2 * sin(radians(alpha2))) for i in range(sect)]
        U_1_i =  [U1 * radius_sopl_i_[i] for i in range(sect)]
        U_2_i =  [U2 * radius_rab_i_[i]  for i in range(sect)]
        H_0_sa_i_ = [(C_1t_i[i]**2) / 2e3 for i in range(sect)]
        H_0_rk_i = [H_0_  - H_0_sa_i_[i] for i in range(sect)]        
        ro_term_i = [H_0_rk_i[i] / H_0_ for i in range(sect)]

        betta_1_i = []
        for i in range(sect):
            if C_1u_i[i] - U_1_i[i] >= 0:
                betta_1_i_ = degrees(atan((C_1a_i[i]) / (C_1u_i[i] - U_1_i[i])))
                betta_1_i.append(betta_1_i_)    
            else:
                betta_1_i_ = 180 - degrees(atan((C_1a_i[i]) / abs(C_1u_i[i] - U_1_i[i])))
                betta_1_i.append(betta_1_i_)

        W_1_i = [ C_1a_i[i] / (sin(radians(betta_1_i[i]))) for i in range(sect)]
        W_1u_i = [ C_1u_i[i] - U_1_i[i] for i in range(sect)]
        W_1a_i = [ W_1_i[i] * sin(radians(betta_1_i[i])) for i in range(sect) ]
        C_2u_i =[ (L_u * 1e3 / U_2_i[i]) - C_1u_i[i] for i in range(sect)]
        W_2u_i = [ C_2u_i[i] + U_2_i[i]  for i in range(sect)] 

        alpha_2_i = []
        for i in range(sect):
            if W_2u_i[i] >= U_2_i[i]:
                alpha_2_i_ = degrees(atan(C_2a_i[i] / abs((C_2u_i[i]))))
                alpha_2_i.append(alpha_2_i_)  
            else:
                alpha_2_i_ = 180 - degrees(atan(C_2a_i[i] / abs((C_2u_i[i]))))
                alpha_2_i.append(alpha_2_i_)   

        C_2_i = [C_2a_i[i] / (sin(radians(alpha_2_i[i]))) for i in range(sect)]
        C_2a_i = [C_2_i[i] * sin(radians(alpha_2_i[i])) for i in range(sect)]
        betta_2_i = [degrees(atan(C_2a_i[i] / (C_2u_i[i] + U_2_i[i]))) for i in range(sect)]
        W_2_i = [W_2u_i[i] / (cos(radians(betta_2_i[i]))) for i in range(sect)]
        W_2t_i = [W_2_i[i] / psi_i[i] for i in range(sect)]
        W_2a_i = [W_2_i[i] * sin(radians(betta_2_i[i])) for i in range(sect)]
        ro_k_i = [ 1 - ((C_1u_i[i] - (C_2u_i[i])) / (2 * U_1_i[i])) for i in range(sect)]

    if method == 'alpha1const': 
        alpha_1_i = [alpha1 for i in range(sect)] 
        C_1a_i = [(C1 * sin(radians(alpha1))) / (radius_sopl_i_[i]**((fi_i[i]**2) * (cos(radians(alpha_1_i[i]))**2))) for i in range(sect)]  
        C_1u_i = [(C1 * cos(radians(alpha1))) / (radius_sopl_i_[i]**((fi_i[i]**2) * (cos(radians(alpha_1_i[i]))**2))) for i in range(sect)]

        C_1_i =  [C_1a_i[i] / (sin(radians(alpha_1_i[i]))) for i in range(sect)]
        C_1t_i = [C_1_i[i] / fi_i[i] for i in range(sect)]
        
        C_2a_i = [(C2 * sin(radians(alpha2))) for i in range(sect)]
        U_1_i =  [U1 * radius_sopl_i_[i] for i in range(sect)]
        U_2_i =  [U2 * radius_rab_i_[i]  for i in range(sect)]
        H_0_sa_i_ = [(C_1t_i[i]**2) / 2e3 for i in range(sect)]
        H_0_rk_i = [H_0_  - H_0_sa_i_[i] for i in range(sect)]        
        ro_term_i = [H_0_rk_i[i] / H_0_ for i in range(sect)]

        betta_1_i = []
        for i in range(sect):
            if C_1u_i[i] - U_1_i[i] >= 0:
                betta_1_i_ = degrees(atan((C_1a_i[i]) / (C_1u_i[i] - U_1_i[i])))
                betta_1_i.append(betta_1_i_)    
            else:
                betta_1_i_ = 180 - degrees(atan((C_1a_i[i]) / abs(C_1u_i[i] - U_1_i[i])))
                betta_1_i.append(betta_1_i_)

        W_1_i = [ C_1a_i[i] / (sin(radians(betta_1_i[i]))) for i in range(sect)]
        W_1u_i = [ C_1u_i[i] - U_1_i[i] for i in range(sect)]
        W_1a_i = [ W_1_i[i] * sin(radians(betta_1_i[i])) for i in range(sect) ]
        C_2u_i =[ (L_u * 1e3 / U_2_i[i]) - C_1u_i[i] for i in range(sect)]
        W_2u_i = [ C_2u_i[i] + U_2_i[i]  for i in range(sect)] 

        alpha_2_i = []
        for i in range(sect):
            if W_2u_i[i] >= U_2_i[i]:
                alpha_2_i_ = degrees(atan(C_2a_i[i] / abs((C_2u_i[i]))))
                alpha_2_i.append(alpha_2_i_)  
            else:
                alpha_2_i_ = 180 - degrees(atan(C_2a_i[i] / abs((C_2u_i[i]))))
                alpha_2_i.append(alpha_2_i_)   

        C_2_i = [C_2a_i[i] / (sin(radians(alpha_2_i[i]))) for i in range(sect)]
        C_2a_i = [C_2_i[i] * sin(radians(alpha_2_i[i])) for i in range(sect)]
        betta_2_i = [degrees(atan(C_2a_i[i] / (C_2u_i[i] + U_2_i[i]))) for i in range(sect)]
        W_2_i = [W_2u_i[i] / (cos(radians(betta_2_i[i]))) for i in range(sect)]
        W_2t_i = [W_2_i[i] / psi_i[i] for i in range(sect)]
        W_2a_i = [W_2_i[i] * sin(radians(betta_2_i[i])) for i in range(sect)]
        ro_k_i = [ 1 - ((C_1u_i[i] - (C_2u_i[i])) / (2 * U_1_i[i])) for i in range(sect)]

    point_0_i_ = IAPWS97(P = P_0_, T = t_0_ + 273.15)
    t_0_i_, P_0_i_, h_0_i_, S_0_i_, V_0_i_, x_0_i_ = [point_0_i_.T - 273.15 for i in range(sect)] , [point_0_i_.P for i in range(sect)], [point_0_i_.h for i in range(sect)], [point_0_i_.s for i in range(sect)], [point_0_i_.v for i in range(sect)], [point_0_i_.x for i in range(sect)]
    ###############################

    # Точка 1t
    ################################################################
    point_1t_i = [IAPWS97(h = h_0_i_[i] - (C_1_i[i]**2 / ((fi_i[i]**2) * 2e3)), s = S_0_i_[i]) for i in range(sect)]
    t_1t_i, P_1t_i, h_1t_i, S_1t_i, V_1t_i, x_1t_i = [point_1t_i[i].T - 273.15 for i in range(sect)], [point_1t_i[i].P for i in range(sect)], [point_1t_i[i].h for i in range(sect)], [point_1t_i[i].s for i in range(sect)], [point_1t_i[i].v for i in range(sect)], [point_1t_i[i].x for i in range(sect)]
    ################################################################

    # Точка 2t_
    ################################################################
    point_2t_i_ = [IAPWS97(h = h_1t_i[i] - H_0_rk_i[i], s = S_0_i_[i]) for i in range(sect)]
    t_2t_i_, P_2t_i_, h_2t_i_, S_2t_i_, V_2t_i_, x_2t_i_ = [point_2t_i_[i].T - 273.15 for i in range(sect)], [point_2t_i_[i].P for i in range(sect)], [point_2t_i_[i].h for i in range(sect)], [point_2t_i_[i].s for i in range(sect)], [point_2t_i_[i].v for i in range(sect)], [point_2t_i_[i].x for i in range(sect)]
    ################################################################

    # Точка 1
    ################################################################  
    point_1_i = [IAPWS97(h = h_0_i_[i] - (C_1_i[i]**2 / 2e3), P = P_1t_i[i]) for i in range(sect)]
    t_1_i, P_1_i, h_1_i, S_1_i, V_1_i, x_1_i = [point_1_i[i].T - 273.15 for i in range(sect)], [point_1_i[i].P for i in range(sect)], [point_1_i[i].h for i in range(sect)], [point_1_i[i].s for i in range(sect)], [point_1_i[i].v for i in range(sect)], [point_1_i[i].x for i in range(sect)]
    ################################################################   

    # Точка 2t
    ################################################################  
    point_2t_i = [IAPWS97(h = h_1_i[i]  - H_0_rk_i[i], s = S_1_i[i]) for i in range(sect)]
    t_2t_i, P_2t_i, h_2t_i, S_2t_i, V_2t_i, x_2t_i = [point_2t_i[i].T - 273.15 for i in range(sect)], [point_2t_i[i].P for i in range(sect)], [point_2t_i[i].h for i in range(sect)], [point_2t_i[i].s for i in range(sect)], [point_2t_i[i].v for i in range(sect)], [point_2t_i[i].x for i in range(sect)]
    ################################################################

    # Точка 2
    ################################################################
    point_2_i = [IAPWS97(P = P_2t_i[i], h = (h_2t_i[i] + ((sqrt(2e3 * H_0_rk_i[i] + W_1_i[i]**2)**2 /2e3) * (1 - psi_i[i]**2))))  for i in range(sect)]
    t_2_i, P_2_i, h_2_i, S_2_i, V_2_i, x_2_i = [point_2_i[i].T - 273.15 for i in range(sect)], [point_2_i[i].P for i in range(sect)], [point_2_i[i].h for i in range(sect)], [point_2_i[i].s for i in range(sect)], [point_2_i[i].v for i in range(sect)], [point_2_i[i].x for i in range(sect)]
    ################################################################

    # Точка 1w*
    ################################################################     
    point_1w_i = [IAPWS97(h = h_1_i[i] + (W_1_i[i]**2 / 2e3), s = S_1_i[i]) for i in range(sect)]
    t_1w_i, P_1w_i, h_1w_i, S_1w_i, V_1w_i, x_1w_i = [point_1w_i[i].T - 273.15 for i in range(sect)], [point_1w_i[i].P for i in range(sect)], [point_1w_i[i].h for i in range(sect)], [point_1w_i[i].s for i in range(sect)], [point_1w_i[i].v for i in range(sect)], [point_1w_i[i].x for i in range(sect)]
    ################################################################   

    # Точка 2w
    ################################################################
    point_2w_i = [IAPWS97(h = h_2_i[i] + (W_2_i[i]**2/ 2e3), s = S_2_i[i]) for i in range(sect)]
    t_2w_i, P_2w_i, h_2w_i, S_2w_i, V_2w_i, x_2w_i = [point_2w_i[i].T - 273.15 for i in range(sect)], [point_2w_i[i].P for i in range(sect)], [point_2w_i[i].h for i in range(sect)], [point_2w_i[i].s for i in range(sect)], [point_2w_i[i].v for i in range(sect)], [point_2w_i[i].x for i in range(sect)]
    ################################################################

    M_1t_i, M_2t_i, M_1c_i, M_2c_i,  M_1w_i, M_2w_i, lambda_C1, lambda_W2 = [], [], [], [], [], [], [], []

    for i in range(sect):
        if x_1t_i[i] or x_1_i[i] or x_2t_i[i] or x_2_i[i] < 1: 
            
            m1t = C_1t_i[i] / sqrt(1.33 * P_1t_i[i] * 1e6 * V_1t_i[i])
            m2t = W_2t_i[i] / sqrt(1.33 * P_2t_i[i] * 1e6 * V_2t_i[i])
            m1c = C_1_i[i] / sqrt(1.33 * P_1_i[i] * 1e6 * V_1_i[i])
            m2c = C_2_i[i] / sqrt(1.33 * P_2_i[i] * 1e6 * V_2_i[i])
            m1w = W_1_i[i] / sqrt(1.33 * P_1_i[i] * 1e6 * V_1_i[i])
            m2w = W_2_i[i] / sqrt(1.33 * P_2_i[i] * 1e6 * V_2_i[i])
            Lambda_C1 = ((1.33 + 1) / 2) * ((m1c**2) / (1 + (((1.33 - 1) / 2)* (m1c**2))))
            Lambda_W2 = ((1.33 + 1) / 2) * ((m2w**2) / (1 + (((1.33 - 1) / 2)* (m2w**2))))

            M_1t_i.append(m1t)
            M_2t_i.append(m2t)
            M_1c_i.append(m1c)
            M_2c_i.append(m2c)
            M_1w_i.append(m1w)
            M_2w_i.append(m2w)
            lambda_C1.append(Lambda_C1)   
            lambda_W2.append(Lambda_W2)

        else:
            m1t = C_1t_i[i] / sqrt(point_1t_i[i].cp0_cv * P_1t_i[i] * 1e6 * V_1t_i[i])
            m2t = W_2t_i[i] / sqrt(point_2t_i[i].cp0_cv * P_2t_i[i] * 1e6 * V_2t_i[i])
            m1c = C_1_i[i] / sqrt(point_1_i[i].cp0_cv * P_1_i[i] * 1e6 * V_1_i[i])
            m2c = C_2_i[i] / sqrt(point_2_i[i].cp0_cv * P_2_i[i] * 1e6 * V_2_i[i])
            m1w = W_1_i[i] / sqrt(point_1_i[i].cp0_cv * P_1_i[i] * 1e6 * V_1_i[i])
            m2w = W_2_i[i] / sqrt(point_2_i[i].cp0_cv * P_2_i[i] * 1e6 * V_2_i[i])
            Lambda_C1 = ((point_1_i[i].cp0_cv + 1) / 2) * ((m1c**2) / (1 + (((point_1_i[i].cp0_cv - 1) / 2)* (m1c**2))))
            Lambda_W2 = ((point_2_i[i].cp0_cv + 1) / 2) * ((m2w**2) / (1 + (((point_2_i[i].cp0_cv - 1) / 2)* (m2w**2))))

            M_1t_i.append(m1t)
            M_2t_i.append(m2t)
            M_1c_i.append(m1c)
            M_2c_i.append(m2c)
            M_1w_i.append(m1w)
            M_2w_i.append(m2w)

    param_0 = {'radius_sopl_i':radius_sopl_i, 'radius_sopl_i_':radius_sopl_i_, 'relative_sopl_i':relative_sopl_i,
                'radius_rab_i':radius_rab_i, 'radius_sopl_i_':radius_sopl_i_, 'relative_rab_i':relative_rab_i,
                't_0_i_':t_0_i_, 't_1t_i':t_1t_i, 't_1_i':t_1_i, 't_1w_i':t_1w_i, 't_2t_i_':t_2t_i_, 't_2t_i':t_2t_i, 't_2_i':t_2_i, 't_2w_i':t_2w_i,
                'P_0_i_':P_0_i_, 'P_1t_i':P_1t_i, 'P_1_i':P_1_i, 'P_1w_i':P_1w_i, 'P_2t_i_':P_2t_i_, 'P_2t_i':P_2t_i, 'P_2_i':P_2_i, 'P_2w_i':P_2w_i,
                'h_0_i_':h_0_i_, 'h_1t_i':h_1t_i, 'h_1_i':h_1_i, 'h_1w_i':h_1w_i, 'h_2t_i_':h_2t_i_, 'h_2t_i':h_2t_i, 'h_2_i':h_2_i, 'h_2w_i':h_2w_i,
                'V_0_i_':V_0_i_, 'V_1t_i':V_1t_i, 'V_1_i':V_1_i, 'V_1w_i':V_1w_i, 'V_2t_i_':h_2t_i_, 'V_2t_i':V_2t_i, 'V_2_i':V_2_i, 'V_2w_i':V_2w_i,
                'x_0_i_':x_0_i_, 'x_1t_i':x_1t_i, 'x_1_i':x_1_i, 'x_1w_i':x_1w_i, 'x_2t_i_':x_2t_i_, 'x_2t_i':x_2t_i, 'x_2_i':x_2_i, 'x_2w_i':x_2w_i,
                'H_0_sa_i_':H_0_sa_i_, 'H_0_rk_i':H_0_rk_i, 'ro_term_i':ro_term_i, 'ro_k_i':ro_k_i,
                'C_1_i':C_1_i, 'C_2_i':C_2_i, 'W_1_i':W_1_i, 'W_2_i':W_2_i, 'U_1_i':U_1_i, 'U_2_i':U_2_i, 
                'alpha_1_i':alpha_1_i, 'alpha_2_i':alpha_2_i, 'betta_1_i':betta_1_i, 'betta_2_i':betta_2_i,
                'fi_i':fi_i, 'psi_i':psi_i, 'M_1c_i':M_1c_i, 'M_1w_i':M_1w_i, 'M_2c_i':M_2c_i, 'M_2w_i':M_2w_i}
    
    param_1 = [radius_sopl_i, radius_sopl_i_, relative_sopl_i, radius_rab_i, radius_sopl_i_, relative_rab_i,
                t_0_i_, t_1t_i, t_1_i, t_1w_i, t_2t_i_, t_2t_i, t_2_i, t_2w_i,
                P_0_i_, P_1t_i, P_1_i, P_1w_i, P_2t_i_, P_2t_i, P_2_i, P_2w_i,
                h_0_i_, h_1t_i, h_1_i, h_1w_i, h_2t_i_, h_2t_i, h_2_i, h_2w_i,
                V_0_i_, V_1t_i, V_1_i, V_1w_i, V_2t_i_, V_2t_i, V_2_i, V_2w_i,
                x_0_i_, x_1t_i, x_1_i, x_1w_i, x_2t_i_, x_2t_i, x_2_i, x_2w_i,
                H_0_sa_i_, H_0_rk_i, ro_term_i, ro_k_i, C_1_i, C_2_i, W_1_i, W_2_i, U_1_i, U_2_i, alpha_1_i, alpha_2_i, betta_1_i, betta_2_i,
                fi_i, psi_i, M_1c_i, M_1w_i, M_2c_i, M_2w_i]

    param_2 = [C_1_i, W_1_i, U_1_i, alpha_1_i, betta_1_i, C_2_i, W_2_i, U_2_i, alpha_2_i, betta_2_i,
               M_1c_i, M_2c_i, M_1w_i, M_2w_i, fi_i, psi_i, relative_sopl_i]
    
    param_3 = [D_sopl, B_sopl_i, h_sopl_i, alpha_0_i, alpha_1_i, M_1c_i]
    
    param_4 = [D_rab, B_rab_i, h_rab_i, betta_1_i, betta_2_i, M_2w_i]
    
    return param_0, param_1, param_2, param_3, param_4

panel_global = st.sidebar.radio('Этапы расчета:', ["I. - Этап расчета по сечениям",
                                                   "II. - Этап профилирование"])

if panel_global == "I. - Этап расчета по сечениям":
    st.markdown("<h1 style='text-align: center; color: #1C2833;'><ins>Расчет ступени ПТУ по сечениям</ins></h1>", unsafe_allow_html=True)
    st.header(f'Ввод исходных данных ступени')

    with st.form(key = 'my_form_1'):
        _vP_0_, _vt_0_, _vH_0_, = st.columns(3)
        _vL_u, _valpha0, _valpha1 = st.columns(3)
        _valpha2, _vC1, _vC2, = st.columns(3)
        _vU1, _vU2, _vh_sopl = st.columns(3)
        _vDsr_sopl, _vh_rab, _vDsr_rab, = st.columns(3)
        _vB_sopl, _vB_rab = st.columns(2)

        P_0_ = count(counter = 'vP_0_', column = _vP_0_, name = "P_0_, МПа", format = "%f", ke = 'count1')
        t_0_ = count(counter = 'vt_0_', column = _vt_0_, name = "t_0_, ℃", format = "%f", ke = 'count2')
        H_0_ = count(counter = 'vH_0_', column = _vH_0_, name = "H_0_, кДж/кг", format = "%f", ke = 'count3')
        L_u = count(counter = 'vL_u', column = _vL_u, name = "L_u, кДж/кг", format = "%f", ke = 'count4')
        alpha0 = count(counter = 'valpha0', column = _valpha0, name = "alpha0, град", format = "%f", ke = 'count5')
        alpha1 = count(counter = 'valpha1', column = _valpha1, name = "alpha1, град", format = "%f", ke = 'count6')
        alpha2 = count(counter = 'valpha2', column = _valpha2, name = "alpha2, град", format = "%f", ke = 'count7')
        C1 = count(counter = 'vC1', column = _vC1, name = "C1, м/с", format = "%f", ke = 'count8')
        C2 = count(counter = 'vC2', column = _vC2, name = "C2, м/с", format = "%f", ke = 'count9')
        U1 = count(counter = 'vU1', column = _vU1, name = "U1, м/с", format = "%f", ke = 'count10')
        U2 = count(counter = 'vU2', column = _vU2, name = "U2, м/с", format = "%f", ke = 'count11')
        h_sopl = count(counter = 'vh_sopl', column = _vh_sopl, name = "h_sopl, м", format = "%f", ke = 'count12')
        Dsr_sopl = count(counter = 'vDsr_sopl', column = _vDsr_sopl, name = "Dsr_sopl, м", format = "%f", ke = 'count13')
        h_rab = count(counter = 'vh_rab', column = _vh_rab, name = "h_rab, м", format = "%f", ke = 'count14')
        Dsr_rab = count(counter = 'vDsr_rab', column = _vDsr_rab, name = "Dsr_rab, м", format = "%f", ke = 'count15')
        B_sopl = count(counter = 'vB_sopl', column = _vB_sopl, name = "B_sopl, м", format = "%f", ke = 'count16')
        B_rab = count(counter = 'vB_rab', column = _vB_rab, name = "B_rab, м", format = "%f", ke = 'count17')

        select_2 = st.radio('Выбор закона закрутки:', ['Закон постоянства угла выхода: 𝛼1(𝑟) = 𝑐𝑜𝑛𝑠𝑡', 'Обратный закон закрутки: 𝑟 ∙ 𝑡𝑔(𝛼1) = 𝑐𝑜𝑛𝑠𝑡', 'Закон постоянства циркуляции: 𝐶1𝑢 ∙ 𝑟𝜑2 = 𝑐𝑜𝑛𝑠𝑡'])  
        if select_2 == 'Обратный закон закрутки: 𝑟 ∙ 𝑡𝑔(𝛼1) = 𝑐𝑜𝑛𝑠𝑡':
            param_5 = countNum(0)
            st.session_state.value_num_ = param_5
            st.session_state.method_section = 'rtgconst' 

        if select_2 == 'Закон постоянства циркуляции: 𝐶1𝑢 ∙ 𝑟𝜑2 = 𝑐𝑜𝑛𝑠𝑡':
            param_5 = countNum(0)
            st.session_state.value_num_ = param_5
            st.session_state.method_section = 'C1uconst'                   

        if select_2 == 'Закон постоянства угла выхода: 𝛼1(𝑟) = 𝑐𝑜𝑛𝑠𝑡':
            param_5 = countNum(0)
            st.session_state.value_num_ = param_5
            st.session_state.method_section = 'alpha1const'     

        if st.form_submit_button('Расчет'): 

            section = spin_laws_stage(P_0_ = st.session_state.vP_0_, t_0_ = st.session_state.vt_0_, H_0_ = st.session_state.vH_0_, 
                                    L_u = st.session_state.vL_u, alpha0 = st.session_state.valpha0, alpha1 = st.session_state.valpha1, 
                                    alpha2 = st.session_state.valpha2, C1 = st.session_state.vC1, C2 = st.session_state.vC2, 
                                    U1 = st.session_state.vU1, U2 = st.session_state.vU2, h_sopl = st.session_state.vh_sopl, B_sopl = st.session_state.vB_sopl,
                                    Dsr_sopl = st.session_state.vDsr_sopl, h_rab = st.session_state.vh_rab, B_rab = st.session_state.vB_rab, Dsr_rab = st.session_state.vDsr_rab, 
                                    sect = int(st.session_state.value_num_), method = st.session_state.method_section) 
            
            st.session_state.section = section
                                        
            st.session_state.data_sopl = []
            st.session_state.data_sopl.insert(0, st.session_state.section[3])

            st.session_state.data_rab = []
            st.session_state.data_rab.insert(0, st.session_state.section[4])

            st.header(f'Результаты расчета параметров по сечениям ступени №{1}')
            st.table(sectionTable(st.session_state.section[1]))
            Save_to_file_stage(sectionTable(st.session_state.section[1]), f'Таблица №7 параметры по сечениям ступени №{1}', '.xlsx')
                                        
            st.pyplot(velocity_triangle_i(C_1_i = st.session_state.section[2][0], W_1_i = st.session_state.section[2][1], U_1_i = st.session_state.section[2][2], alpha_1_i = st.session_state.section[2][3], betta_1_i = st.session_state.section[2][4],
            C_2_i = st.session_state.section[2][5], W_2_i = st.session_state.section[2][6], U_2_i = st.session_state.section[2][7], alpha_2_i = st.session_state.section[2][8], betta_2_i = st.session_state.section[2][9], num = 0))
                                        
            st.pyplot(parametrs(alpha_1_i = st.session_state.section[2][3], betta_1_i = st.session_state.section[2][4], 
                                alpha_2_i = st.session_state.section[2][8], betta_2_i = st.session_state.section[2][9], 
                                C_1_i = st.session_state.section[2][0], C_2_i = st.session_state.section[2][5], 
                                W_1_i = st.session_state.section[2][1], W_2_i = st.session_state.section[2][6], 
                                M_1c_i = st.session_state.section[2][10], M_2c_i = st.session_state.section[2][11], 
                                M_1w_i = st.session_state.section[2][12], M_2w_i = st.session_state.section[2][13], 
                                fi_i = st.session_state.section[2][14], psi_i = st.session_state.section[2][15], 
                                num = 0, sect = st.session_state.section[2][16], method = 'angle'))

            st.pyplot(parametrs(alpha_1_i = st.session_state.section[2][3], betta_1_i = st.session_state.section[2][4], 
                                alpha_2_i = st.session_state.section[2][8], betta_2_i = st.session_state.section[2][9], 
                                C_1_i = st.session_state.section[2][0], C_2_i = st.session_state.section[2][5], 
                                W_1_i = st.session_state.section[2][1], W_2_i = st.session_state.section[2][6], 
                                M_1c_i = st.session_state.section[2][10], M_2c_i = st.session_state.section[2][11], 
                                M_1w_i = st.session_state.section[2][12], M_2w_i = st.session_state.section[2][13], 
                                fi_i = st.session_state.section[2][14], psi_i = st.session_state.section[2][15], 
                                num = 0, sect = st.session_state.section[2][16], method = 'velocity'))

            st.pyplot(parametrs(alpha_1_i = st.session_state.section[2][3], betta_1_i = st.session_state.section[2][4], 
                                alpha_2_i = st.session_state.section[2][8], betta_2_i = st.session_state.section[2][9], 
                                C_1_i = st.session_state.section[2][0], C_2_i = st.session_state.section[2][5], 
                                W_1_i = st.session_state.section[2][1], W_2_i = st.session_state.section[2][6], 
                                M_1c_i = st.session_state.section[2][10], M_2c_i = st.session_state.section[2][11], 
                                M_1w_i = st.session_state.section[2][12], M_2w_i = st.session_state.section[2][13], 
                                fi_i = st.session_state.section[2][14], psi_i = st.session_state.section[2][15], 
                                num = 0, sect = st.session_state.section[2][16], method = 'Mach'))

            st.pyplot(parametrs(alpha_1_i = st.session_state.section[2][3], betta_1_i = st.session_state.section[2][4], 
                                alpha_2_i = st.session_state.section[2][8], betta_2_i = st.session_state.section[2][9], 
                                C_1_i = st.session_state.section[2][0], C_2_i = st.session_state.section[2][5], 
                                W_1_i = st.session_state.section[2][1], W_2_i = st.session_state.section[2][6], 
                                M_1c_i = st.session_state.section[2][10], M_2c_i = st.session_state.section[2][11], 
                                M_1w_i = st.session_state.section[2][12], M_2w_i = st.session_state.section[2][13], 
                                fi_i = st.session_state.section[2][14], psi_i = st.session_state.section[2][15], 
                                num = 0, sect = st.session_state.section[2][16], method = 'losses'))
                                    
if panel_global == "II. - Этап профилирование":
    if st.session_state.section == None:
        st.markdown("<h1 style='text-align: center; color: #1C2833;'><ins>Профилирование</ins></h1>", unsafe_allow_html=True)
        st.header('Необходимо выполнить: "III. - Этап расчета по сечениям"')
    else:
        panel_4 = st.sidebar.radio('Этапы расчета ступени:', [f'Ступень №{i+1}' for i in range(len(st.session_state.data_sopl))])
        num_2 = [f'Ступень №{i+1}' for i in range(len(st.session_state.data_sopl))]
        for i in range(len(st.session_state.data_sopl)):
            if panel_4 == num_2[i]:
                panel_5 = st.sidebar.radio('Тип решетки:', [f'Сопловая №{i+1}', f'Рабочая №{i+1}', f'Результаты расчета ступени №{i+1}'])
                num_3 = [f'Сопловая №{i+1}', f'Рабочая №{i+1}', f'Результаты расчета ступени №{i+1}']
                if panel_5 == num_3[0]:
                    st.markdown(f"<h1 style='text-align: center; color: #1C2833;'><ins>Сопловая решетка №{i+1}</ins></h1>", unsafe_allow_html = True)
                    st.session_state.sopl_val1 = [] 
                    st.session_state.sopl_val2 = [] 
                    st.session_state.sopl_val3 = [] 
                    st.session_state.sopl_val4 = [] 
                    st.session_state.sopl_val5 = []  
                    st.session_state.sopl_val6 = []   
                    st.session_state.sopl_spline = [] 
                    st.session_state.sopl_param = []
                    st.session_state.sopl_section_list = None 
                    st.session_state.rab_section_list = None
                    for j in range(len(st.session_state.data_sopl[i][0])):
                        with st.form(key = f'my_form_sopl_{j+1}'):
                            st.markdown(f"<h2 style='text-align: center; color: #1C2833;'>Сечение №{j+1}</h2>", unsafe_allow_html = True)
                            param_6 = countSRVVVV(j, i, 'sopl')
                            st.session_state.value1_sopl_sect_ = param_6[0]
                            st.session_state.value2_sopl_sect_ = param_6[1]
                            st.session_state.value3_sopl_sect_ = param_6[2]
                            st.session_state.value4_sopl_sect_ = param_6[3]
                            st.session_state.value5_sopl_sect_ = param_6[4]
                            st.session_state.value6_sopl_sect_ = param_6[5]

                            st.session_state.sopl_val1.append(st.session_state.value1_sopl_sect_)
                            st.session_state.sopl_val2.append(st.session_state.value2_sopl_sect_)  
                            st.session_state.sopl_val3.append(st.session_state.value3_sopl_sect_) 
                            st.session_state.sopl_val4.append(st.session_state.value4_sopl_sect_) 
                            st.session_state.sopl_val5.append(st.session_state.value5_sopl_sect_) 
                            st.session_state.sopl_val6.append(st.session_state.value6_sopl_sect_) 

                            if st.form_submit_button(f'Расчет сечения {1+j}'):
                                if j == 0:
                                    st.session_state.sopl_number_blades = 0.0
                                    sopl_prof_sect_ij = profiling(D_k = st.session_state.data_sopl[i][0][j], width = st.session_state.data_sopl[i][1][j],
                                    height = st.session_state.data_sopl[i][2][j], alpha_0 = st.session_state.data_sopl[i][3][j], alpha_1 = st.session_state.data_sopl[i][4][j], M_c1 = st.session_state.data_sopl[i][5][j], 
                                    value_1 = st.session_state.value1_sopl_sect_, value_2 = st.session_state.value2_sopl_sect_, value_3 = st.session_state.value3_sopl_sect_, value_4 = st.session_state.value4_sopl_sect_, value_5 = st.session_state.value5_sopl_sect_, value_6 = st.session_state.value6_sopl_sect_, method_2 = 'sopl')
                                    st.session_state.sopl_prof_sect_ij = sopl_prof_sect_ij
                                    st.session_state.sopl_number_blades = st.session_state.sopl_prof_sect_ij[3]
                                else:
                                    sopl_prof_sect_ij = profiling(D_k = st.session_state.data_sopl[i][0][j], width = st.session_state.data_sopl[i][1][j],
                                    height = st.session_state.data_sopl[i][2][j], alpha_0 = st.session_state.data_sopl[i][3][j], alpha_1 = st.session_state.data_sopl[i][4][j], M_c1 = st.session_state.data_sopl[i][5][j], 
                                    value_1 = st.session_state.value1_sopl_sect_, value_2 = st.session_state.value2_sopl_sect_, value_3 = st.session_state.value3_sopl_sect_, value_4 = st.session_state.value4_sopl_sect_, value_5 = st.session_state.value5_sopl_sect_, value_6 = st.session_state.value6_sopl_sect_, method_2 = 'sopl', number_blades = st.session_state.sopl_number_blades)
                                    st.session_state.sopl_prof_sect_ij = sopl_prof_sect_ij

                                st.markdown(f"<h2 style='text-align: center; color: #1C2833;'>Геометрические параметры профиля сопловой №{j+1}</h2>", unsafe_allow_html = True)
                                st.pyplot(profiling_plot(st.session_state.sopl_prof_sect_ij[1], method = 'sopl'))
                                st.table(stage_table(st.session_state.sopl_prof_sect_ij[0], method = "profile sopl"))
                    select_3_sopl = st.radio(f'Выбор позиционирования профиля сопловой №{i + 1} :', ['по входной кромки', 'по выходной кромки', 'по центру масс'], horizontal = True)
                            
                    if select_3_sopl == 'по входной кромки':
                        st.session_state.position_sopl = 'r_1'
                            
                    if select_3_sopl == 'по выходной кромки':
                        st.session_state.position_sopl = 'r_2'
   
                    if select_3_sopl == 'по центру масс':
                        st.session_state.position_sopl = 'C_m'
            
                    if st.button(f'Показать сопловую лопатку №{i+1}'):
                        for j in range(len(st.session_state.data_sopl[i][0])): 
                            sopl_prof_sect_ij = profiling(D_k = st.session_state.data_sopl[i][0][j], width = st.session_state.data_sopl[i][1][j],
                            height = st.session_state.data_sopl[i][2][j], alpha_0 = st.session_state.data_sopl[i][3][j], alpha_1 = st.session_state.data_sopl[i][4][j], M_c1 = st.session_state.data_sopl[i][5][j], 
                            value_1 = st.session_state.sopl_val1[j], value_2 = st.session_state.sopl_val2[j], value_3 = st.session_state.sopl_val3[j], value_4 = st.session_state.sopl_val4[j], value_5 = st.session_state.sopl_val5[j], value_6 = st.session_state.sopl_val6[j], method_2 = 'sopl', method_3 = st.session_state.position_sopl, number_blades = st.session_state.sopl_number_blades)
                            st.session_state.sopl_param.append(sopl_prof_sect_ij[0])
                            st.session_state.sopl_spline.append(sopl_prof_sect_ij[2])
                        st.plotly_chart(profil_plot_3D(st.session_state.sopl_spline, method = 'sopl'))
                        st.pyplot(profil_sect_plot(st.session_state.sopl_spline, method = 'sopl'))

                        st.session_state.sopl_section_dict = {}
                        for n in st.session_state.sopl_param[0].keys():
                            st.session_state.sopl_section_dict[n] = list(d[n] for d in st.session_state.sopl_param)               
                        st.session_state.sopl_section_list = list(st.session_state.sopl_section_dict.values()) 

                if panel_5 == num_3[1]:
                    st.markdown(f"<h1 style='text-align: center; color: #1C2833;'><ins>Рабочая решетка №{i+1}</ins></h1>", unsafe_allow_html = True)
                    st.session_state.rab_val1 = [] 
                    st.session_state.rab_val2 = [] 
                    st.session_state.rab_val3 = [] 
                    st.session_state.rab_val4 = [] 
                    st.session_state.rab_val5 = []
                    st.session_state.rab_val6 = []    
                    st.session_state.rab_spline = [] 
                    st.session_state.rab_param = []
                
                    for j in range(len(st.session_state.data_rab[i][0])):
                        with st.form(key = f'my_form_rab_{j+1}'):
                            st.markdown(f"<h2 style='text-align: center; color: #1C2833;'>Сечение №{j+1}</h2>", unsafe_allow_html = True)
                            param_7 = countSRVVVV(j, i, 'rab')
                            st.session_state.value1_rab_sect_ = param_7[0]
                            st.session_state.value2_rab_sect_ = param_7[1]
                            st.session_state.value3_rab_sect_ = param_7[2]
                            st.session_state.value4_rab_sect_ = param_7[3]
                            st.session_state.value5_rab_sect_ = param_7[4]
                            st.session_state.value6_rab_sect_ = param_7[5]

                            st.session_state.rab_val1.append(st.session_state.value1_rab_sect_)
                            st.session_state.rab_val2.append(st.session_state.value2_rab_sect_)  
                            st.session_state.rab_val3.append(st.session_state.value3_rab_sect_) 
                            st.session_state.rab_val4.append(st.session_state.value4_rab_sect_) 
                            st.session_state.rab_val5.append(st.session_state.value5_rab_sect_)
                            st.session_state.rab_val6.append(st.session_state.value6_rab_sect_)

                            if st.form_submit_button(f'Расчет сечения {1+j}'):
                                if j == 0:
                                    st.session_state.rab_number_blades = 0.0
                                    rab_prof_sect_ij = profiling(D_k = st.session_state.data_rab[i][0][j], width = st.session_state.data_rab[i][1][j],
                                    height = st.session_state.data_rab[i][2][j], alpha_0 = st.session_state.data_rab[i][3][j], alpha_1 = st.session_state.data_rab[i][4][j], M_c1 = st.session_state.data_rab[i][5][j], 
                                    value_1 = st.session_state.value1_rab_sect_, value_2 = st.session_state.value2_rab_sect_, value_3 = st.session_state.value3_rab_sect_, value_4 = st.session_state.value4_rab_sect_, value_5 = st.session_state.value5_rab_sect_, value_6 = st.session_state.value6_rab_sect_, method_2 = 'rab')
                                    st.session_state.rab_prof_sect_ij = rab_prof_sect_ij
                                    st.session_state.rab_number_blades = st.session_state.rab_prof_sect_ij[3]

                                else:
                                    rab_prof_sect_ij = profiling(D_k = st.session_state.data_rab[i][0][j], width = st.session_state.data_rab[i][1][j],
                                    height = st.session_state.data_rab[i][2][j], alpha_0 = st.session_state.data_rab[i][3][j], alpha_1 = st.session_state.data_rab[i][4][j], M_c1 = st.session_state.data_rab[i][5][j], 
                                    value_1 = st.session_state.value1_rab_sect_, value_2 = st.session_state.value2_rab_sect_, value_3 = st.session_state.value3_rab_sect_, value_4 = st.session_state.value4_rab_sect_, value_5 = st.session_state.value5_rab_sect_, value_6 = st.session_state.value6_rab_sect_, method_2 = 'rab', number_blades = st.session_state.rab_number_blades)
                                    st.session_state.rab_prof_sect_ij = rab_prof_sect_ij

                                st.markdown(f"<h2 style='text-align: center; color: #1C2833;'>Геометрические параметры профиля рабочей №{j+1}</h2>", unsafe_allow_html = True)
                                st.pyplot(profiling_plot(st.session_state.rab_prof_sect_ij[1], method = 'rab'))
                                st.table(stage_table(st.session_state.rab_prof_sect_ij[0], method = "profile rab"))

                    select_3_rab = st.radio(f'Выбор позиционирования профиля рабочей №{i + 1} :', ['по центру масс', 'по входной кромки', 'по выходной кромки'], horizontal = True)
                            
                    if select_3_rab == 'по входной кромки':
                        st.session_state.position_rab = 'r_1'
                            
                    if select_3_rab == 'по выходной кромки':
                        st.session_state.position_rab = 'r_2'
   
                    if select_3_rab == 'по центру масс':
                        st.session_state.position_rab = 'C_m'

                    if st.button(f'Показать рабочую лопатку №{i+1}'):
                        for j in range(len(st.session_state.data_rab[i][0])): 
                            rab_prof_sect_ij = profiling(D_k = st.session_state.data_rab[i][0][j], width = st.session_state.data_rab[i][1][j],
                            height = st.session_state.data_rab[i][2][j], alpha_0 = st.session_state.data_rab[i][3][j], alpha_1 = st.session_state.data_rab[i][4][j], M_c1 = st.session_state.data_rab[i][5][j], 
                            value_1 = st.session_state.rab_val1[j], value_2 = st.session_state.rab_val2[j], value_3 = st.session_state.rab_val3[j], value_4 = st.session_state.rab_val4[j], value_5 = st.session_state.rab_val5[j], value_6 = st.session_state.rab_val6[j], method_2 = 'rab', method_3 = st.session_state.position_rab, number_blades = st.session_state.rab_number_blades)
                            st.session_state.rab_param.append(rab_prof_sect_ij[0])
                            st.session_state.rab_spline.append(rab_prof_sect_ij[2]) 
                        st.plotly_chart(profil_plot_3D(st.session_state.rab_spline, method = 'rab'))
                        st.pyplot(profil_sect_plot(st.session_state.rab_spline, method = 'rab'))
            
                        st.session_state.rab_section_dict = {}
                        for n in st.session_state.rab_param[0].keys():
                            st.session_state.rab_section_dict[n] = list(d[n] for d in st.session_state.rab_param)               
                        st.session_state.rab_section_list = list(st.session_state.rab_section_dict.values()) 

                if panel_5 == num_3[2]:
                    st.markdown(f"<h1 style='text-align: center; color: #1C2833;'><ins>Сопловая решетка №{i+1} по сечениям</ins></h1>", unsafe_allow_html = True)
                    if st.session_state.sopl_section_list == None:
                        st.header('Необходимо выполнить профилирование сопловой решетки')
                    else:
                        st.table(profiling_table(st.session_state.sopl_section_list, method = "profile sopl"))
                        Save_to_file_stage(profiling_table(st.session_state.sopl_section_list, method = "profile sopl"), f'Таблица №8 Геометрия профиля сопловой №{i+1}', '.xlsx')
                                    
                        st.pyplot(profil_parametrs_plot(st.session_state.sopl_section_list, i))   
                        col1, col2, col3 = st.columns(3)
                        if col2.button(f'Сохранить сопловую лопатку №{i+1} в SolidWorks'):
                            solid_profiling(st.session_state.sopl_spline, st.session_state.sopl_section_list[9], i, method = 'profile sopl')

                    st.markdown(f"<h1 style='text-align: center; color: #1C2833;'><ins>Рабочая решетка №{i+1} по сечениям</ins></h1>", unsafe_allow_html = True)
                    if st.session_state.rab_section_list == None:
                        st.header('Необходимо выполнить профилирование рабочей решетки')
                    else:               
                        st.table(profiling_table(st.session_state.rab_section_list, method = "profile rab"))
                        Save_to_file_stage(profiling_table(st.session_state.rab_section_list, method = "profile rab"), f'Таблица №8 Геометрия профиля рабочей №{i+1}', '.xlsx')
                                    
                        st.pyplot(profil_parametrs_plot(st.session_state.rab_section_list, i))   
                        col1, col2, col3 = st.columns(3)
                        if col2.button(f'Сохранить рабочую лопатку №{i+1} в SolidWorks'):
                            solid_profiling(st.session_state.rab_spline, st.session_state.rab_section_list[9], i, method = 'profile rab')
                        

