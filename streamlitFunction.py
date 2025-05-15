import pandas as pd
import numpy as np
import streamlit as st
from PIL import Image

def Save_to_file_stage(stage, name , extension ):
    with pd.ExcelWriter((name + extension)) as writer:
        stage.to_excel(writer, sheet_name ='sheet2', index = False, header = False,)
        
def count(counter, column, name, format, ke):
    if counter not in st.session_state:
        st.session_state[counter] = 0.00
    val = column.number_input((name), format = format, value = st.session_state[counter], key = ke)
    if val:
        st.session_state[counter] = st.session_state[ke]
    return st.session_state[counter]

def countSRVVV(i, method_2):
    if method_2 == 'sopl':

        value1_sopl_index_ = f'value1_sopl_{i + 1}'
        value2_sopl_index_ = f'value2_sopl_{i + 1}'
        value3_sopl_index_ = f'value3_sopl_{i + 1}'
        value4_sopl_index_ = f'value4_sopl_{i + 1}'
        value5_sopl_index_ = f'value5_sopl_{i + 1}'
        value6_sopl_index_ = f'value6_sopl_{i + 1}'

        value1_sopl_index_, value2_sopl_index_, value3_sopl_index_ = st.columns(3)
        value4_sopl_index_, value5_sopl_index_, value6_sopl_index_ = st.columns(3)
        value1_sopl_ = count(counter = f'value1_sopl{i}', column = value1_sopl_index_, name = f"Эффективный угол СР. № {i+1}, град", format = "%f", ke = f'value1_sopl_{i + 1}')  
        value2_sopl_ = count(counter = f'value2_sopl{i}', column = value2_sopl_index_, name = f"Коэфф. толщины профиля СР. № {i+1}, -", format = "%f", ke = f'value2_sopl_{i + 1}')
        value3_sopl_ = count(counter = f'value3_sopl{i}', column = value3_sopl_index_, name = f"Коэфф. расположения Сmax СР. № {i+1}, -", format = "%f", ke = f'value3_sopl_{i + 1}')
        value4_sopl_ = count(counter = f'value4_sopl{i}', column = value4_sopl_index_, name = f"Коэфф. вх.кромки СР. № {i+1}, -", format = "%f", ke = f'value4_sopl_{i + 1}')
        value5_sopl_ = count(counter = f'value5_sopl{i}', column = value5_sopl_index_, name = f"Коэфф. вых.кромки СР. № {i+1}, -", format = "%f", ke = f'value5_sopl_{i + 1}')
        value6_sopl_ = count(counter = f'value6_sopl{i}', column = value6_sopl_index_, name = f"Хорда СР. № {i+1}, мм", format = "%g", ke = f'value6_sopl_{i + 1}')
        return value1_sopl_, value2_sopl_, value3_sopl_, value4_sopl_, value5_sopl_, value6_sopl_
    
    if method_2 == 'rab':

        value1_rab_index_ = f'value1_rab_{i + 1}'
        value2_rab_index_ = f'value2_rab_{i + 1}'
        value3_rab_index_ = f'value3_rab_{i + 1}'
        value4_rab_index_ = f'value4_rab_{i + 1}'
        value5_rab_index_ = f'value5_rab_{i + 1}'
        value6_rab_index_ = f'value6_rab_{i + 1}'

        value1_rab_index_, value2_rab_index_, value3_rab_index_ = st.columns(3)
        value4_rab_index_, value5_rab_index_, value6_rab_index_ = st.columns(3)
        value1_rab_ = count(counter = f'value1_rab{i}', column = value1_rab_index_, name = f"Эффективный угол РК. № {i+1}, град", format = "%f", ke = f'value1_rab_{i + 1}')  
        value2_rab_ = count(counter = f'value2_rab{i}', column = value2_rab_index_, name = f"Коэфф. толщины профиля РК. № {i+1}, -", format = "%f", ke = f'value2_rab_{i + 1}')
        value3_rab_ = count(counter = f'value3_rab{i}', column = value3_rab_index_, name = f"Коэфф. расположения Сmax РК. № {i+1}, -", format = "%f", ke = f'value3_rab_{i + 1}')
        value4_rab_ = count(counter = f'value4_rab{i}', column = value4_rab_index_, name = f"Коэфф. вх.кромки РК. № {i+1}, -", format = "%f", ke = f'value4_rab_{i + 1}')
        value5_rab_ = count(counter = f'value5_rab{i}', column = value5_rab_index_, name = f"Коэфф. вых.кромки РК. № {i+1}, -", format = "%f", ke = f'value5_rab_{i + 1}')     
        value6_rab_ = count(counter = f'value6_rab{i}', column = value6_rab_index_, name = f"Хорда РК. № {i+1}, мм", format = "%g", ke = f'value6_rab_{i + 1}')     
        return value1_rab_, value2_rab_, value3_rab_, value4_rab_, value5_rab_, value6_rab_

def countSRVVVV(i, j, method_2):
    if method_2 == 'sopl':

        value1_sopl_index_ = f'value1_sopl_{i + 1}_{j + 1}'
        value2_sopl_index_ = f'value2_sopl_{i + 1}_{j + 1}'
        value3_sopl_index_ = f'value3_sopl_{i + 1}_{j + 1}'
        value4_sopl_index_ = f'value4_sopl_{i + 1}_{j + 1}'
        value5_sopl_index_ = f'value5_sopl_{i + 1}_{j + 1}'
        value6_sopl_index_ = f'value6_sopl_{i + 1}_{j + 1}'
        value1_sopl_index_, value2_sopl_index_, value3_sopl_index_ = st.columns(3)
        value4_sopl_index_, value5_sopl_index_, value6_sopl_index_= st.columns(3)
        value1_sopl_ = count(counter = f'value1_sopl{i}_{j}', column = value1_sopl_index_, name = f"Эффективный угол СР. № {i+1}, град", format = "%f", ke = f'value1_sopl_{i + 1}_{j + 1}')  
        value2_sopl_ = count(counter = f'value2_sopl{i}_{j}', column = value2_sopl_index_, name = f"Коэфф. толщины профиля СР. № {i+1}, -", format = "%f", ke = f'value2_sopl_{i + 1}_{j + 1}')
        value3_sopl_ = count(counter = f'value3_sopl{i}_{j}', column = value3_sopl_index_, name = f"Коэфф. расположения Сmax СР. № {i+1}, -", format = "%f", ke = f'value3_sopl_{i + 1}_{j + 1}')
        value4_sopl_ = count(counter = f'value4_sopl{i}_{j}', column = value4_sopl_index_, name = f"Коэфф. вх.кромки СР. № {i+1}, -", format = "%f", ke = f'value4_sopl_{i + 1}_{j + 1}')
        value5_sopl_ = count(counter = f'value5_sopl{i}_{j}', column = value5_sopl_index_, name = f"Коэфф. вых.кромки СР. № {i+1}, -", format = "%f", ke = f'value5_sopl_{i + 1}_{j + 1}')
        value6_sopl_ = count(counter = f'value6_sopl{i}_{j}', column = value6_sopl_index_, name = f"Хорда СР. № {i+1}, -", format = "%f", ke = f'value6_sopl_{i + 1}_{j + 1}')
        return value1_sopl_, value2_sopl_, value3_sopl_, value4_sopl_, value5_sopl_, value6_sopl_
    
    if method_2 == 'rab':

        value1_rab_index_ = f'value1_rab_{i + 1}_{j + 1}'
        value2_rab_index_ = f'value2_rab_{i + 1}_{j + 1}'
        value3_rab_index_ = f'value3_rab_{i + 1}_{j + 1}'
        value4_rab_index_ = f'value4_rab_{i + 1}_{j + 1}'
        value5_rab_index_ = f'value5_rab_{i + 1}_{j + 1}'
        value6_rab_index_ = f'value6_rab_{i + 1}_{j + 1}'

        value1_rab_index_, value2_rab_index_, value3_rab_index_ = st.columns(3)
        value4_rab_index_, value5_rab_index_, value6_rab_index_= st.columns(3)
        value1_rab_ = count(counter = f'value1_rab{i}_{j}', column = value1_rab_index_, name = f"Эффективный угол РК. № {i+1}, град", format = "%f", ke = f'value1_rab_{i + 1}_{j + 1}')  
        value2_rab_ = count(counter = f'value2_rab{i}_{j}', column = value2_rab_index_, name = f"Коэфф. толщины профиля РК. № {i+1}, -", format = "%f", ke = f'value2_rab_{i + 1}_{j + 1}')
        value3_rab_ = count(counter = f'value3_rab{i}_{j}', column = value3_rab_index_, name = f"Коэфф. расположения Сmax РК. № {i+1}, -", format = "%f", ke = f'value3_rab_{i + 1}_{j + 1}')
        value4_rab_ = count(counter = f'value4_rab{i}_{j}', column = value4_rab_index_, name = f"Коэфф. вх.кромки РК. № {i+1}, -", format = "%f", ke = f'value4_rab_{i + 1}_{j + 1}')
        value5_rab_ = count(counter = f'value5_rab{i}_{j}', column = value5_rab_index_, name = f"Коэфф. вых.кромки РК. № {i+1}, -", format = "%f", ke = f'value5_rab_{i + 1}_{j + 1}')     
        value6_rab_ = count(counter = f'value6_rab{i}_{j}', column = value6_rab_index_, name = f"Хорда РК. № {i+1}, -", format = "%f", ke = f'value6_rab_{i + 1}_{j + 1}')     
        return value1_rab_, value2_rab_, value3_rab_, value4_rab_, value5_rab_, value6_rab_

def countLosses(i, method_1, method_2):

    if method_2 == 'sopl':

        if method_1 ==  'ANM':
            coef_sopl_index_ = f'coef_sopl_{i + 1}'
            B_sopl_index_ = f'B_sopl_{i + 1}'
            coef_sopl_index_, B_sopl_index_ = st.columns(2)
            coef_sopl_ = count(counter = f'coef_sopl{i}', column = coef_sopl_index_, name = f"Зазор между ротором. № {i+1}, м", format = "%f", ke = f'coef_sopl_{i + 1}')  
            B_sopl_ = count(counter = f'B_sopl{i}', column = B_sopl_index_, name = f"Зазор между бандажом. № {i+1}, м", format = "%f", ke = f'B_sopl_{i + 1}')
            return coef_sopl_, B_sopl_
        
        if method_1 ==  'CAC':
            ks_sopl_index_ = f'ks_sopl_{i + 1}'
            ks_sopl_index_, _, = st.columns(2)
            ks_sopl_ = count(counter = f'ks_sopl{i}', column = ks_sopl_index_, name = f"Коэфф. шероховатости СР. № {i+1}, -", format = "%f", ke = f'ks_sopl_{i + 1}')  
            return ks_sopl_, _ 

        if method_1 ==  'DN':
            sorU_sopl_index_ = f'sorU_sopl_{i + 1}'
            sorU_sopl_index_, _, = st.columns(2)
            sorU_sopl_ = count(counter = f'sorU_sopl{i}', column = sorU_sopl_index_, name = f"Наличие бандажа № {i+1}, -", format = "%f", ke = f'sorU_sopl_{i + 1}')  
            return sorU_sopl_, _,

    if method_2 ==  'rab':

        if method_1 ==  'ANM':
            coef_rab_index_ = f'coef_rab_{i + 1}'
            B_rab_index_ = f'B_rab_{i + 1}'
            coef_rab_index_, B_rab_index_ = st.columns(2)
            coef_rab_ = count(counter = f'coef_rab{i}', column = coef_rab_index_, name = f"Зазор между ротором. № {i+1}, м", format = "%f", ke = f'coef_rab_{i + 1}')  
            B_rab_ = count(counter = f'B_rab{i}', column = B_rab_index_, name = f"Зазор между бандажом. № {i+1}, м", format = "%f", ke = f'B_rab_{i + 1}')
            return coef_rab_, B_rab_
        
        if method_1 ==  'CAC':
            ks_rab_index_ = f'ks_rab_{i + 1}'
            ks_rab_index_, _, = st.columns(2)
            ks_rab_ = count(counter = f'ks_rab{i}', column = ks_rab_index_, name = f"Коэфф. шероховатости РК. № {i+1}, -", format = "%f", ke = f'ks_rab_{i + 1}')  
            return ks_rab_, _
        
        if method_1 ==  'DN':
            sorU_rab_index_ = f'sorU_rab_{i + 1}'
            sorU_rab_index_, _, = st.columns(2)
            sorU_rab_ = count(counter = f'sorU_rab{i}', column = sorU_rab_index_, name = f"Наличие бандажа № {i+1}, -", format = "%f", ke = f'sorU_rab_{i + 1}')  
            return sorU_rab_, _,

def countNum(i):
    value_num_index_ = f'value1_sopl_{i + 1}'
    value_num_index_, _ = st.columns(2)
    value_num_ = count(counter = f'value_num{i}', column = value_num_index_, name = f"Кол-во сечений ступени. № {i+1}, -", format = "%g", ke = f'value_num_{i + 1}')  
    return value_num_
