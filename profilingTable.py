import pandas as pd

def profiling_table(array, method = True):
    if method == 'profile sopl':
        data_1 = {'Ширина профиля СА':'B_sopl', 
                    'Хорда профиля СА': 'b_sopl', 
                    'Шаг решетки СА':'t_sopl',
                    'Радиус входной кромки СА':'r_inl_sopl', 
                    'Радиус выходной кромки СА': 'r_out_sopl',
                    'Горло решетки на входе СА':'a_inl_sopl',
                    'Горло решетки на выходе СА':'a_out_sopl', 
                    'Координата центра СА':'Xmax_sopl', 
                    'Толщина профиля СА':'Cmax_sopl',
                    'Корневой диаметр СА':'Dk_sopl', 
                    'Высота лопатки СА':'height_sopl', 
                    'Угол установки СА':'alpha_instal',
                    'Лопаточный угол на входе СА':'alpha0sc_sopl',
                    'Лопаточный угол на выходе СА':'alpha1sc_sopl',
                    'Угол заострения на вх. СА':'fi1_sopl', 
                    'Угол заострения на вых. СА':'fi2_sopl',
                    'Угол отгиба СА':'gamma_sopl',
                    'Количество лопаток СА':'number_sopl'}
    
    if method == 'profile rab':
        data_1 = {'Ширина профиля РК':'B_rab', 
                  'Хорда профиля РК': 'b_rab', 
                  'Шаг решетки РК':'t_rab',
                  'Радиус входной кромки РК':'r_inl_rab', 
                  'Радиус выходной кромки РК': 'r_out_rab',
                  'Горло решетки на входе РК':'a_inl_rab',
                  'Горло решетки на выходе РК':'a_out_rab', 
                  'Координата центра РК':'Xmax_rab',
                  'Толщина профиля РК':'Cmax_rab',
                  'Корневой диаметр РК':'Dk_rab', 
                  'Высота лопатки РК':'height_rab', 
                  'Угол установки РК':'betta_instal',
                  'Лопаточный угол на входе РК':'betta0sc_rab',
                  'Лопаточный угол на выходе РК':'betta1sc_rab',
                  'Угол заострения на вх. РК':'fi1_rab', 
                  'Угол заострения на вых. РК':'fi2_rab',
                  'Угол отгиба РК':'gamma_rab',
                  'Количество лопаток РК':'number_rab'}

    df_1 = pd.DataFrame(list(data_1.items()),columns=['Параметры','Обозначение']) 
    df_2_ = pd.DataFrame(['мм', 'мм', 'мм', 'мм', 'мм', 'мм', 'мм', 'мм', 'мм', 'мм', 'мм', 'град', 'град', 'град', 'град', 'град', 'град', 'шт'], columns = ['Разм'])
    df_2 = pd.DataFrame((array))
    df12_merged = df_1.join(df_2_, rsuffix='_right')
    df_merged = df12_merged.join(df_2, rsuffix='_right')
    pd.set_option("display.precision", 3)
    return df_merged