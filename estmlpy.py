# -*- coding: utf-8 -*-
"""EstMLpy.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1ZMAWkQTeG3KN_gBkdtJgYP0d-_cwRDIi
"""

import streamlit as st
import joblib  # Para cargar modelos guardados
import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder

# Diccionario de opciones para 'Marital status'
marital_status_options = {
    'Single': 1,
    'Married': 2,
    'Widower': 3,
    'Divorced': 4,
    'Facto union': 5,
    'Legally separated': 6
}

# Diccionario de opciones para 'Application mode'
application_mode_option = {
    1: '1st phase - general contingent',
    2: 'Ordinance No. 612/93',
    5: '1st phase - special contingent (Azores Island)',
    7: 'Holders of other higher courses',
    10: 'Ordinance No. 854-B/99',
    15: 'International student (bachelor)',
    16: '1st phase - special contingent (Madeira Island)',
    17: '2nd phase - general contingent',
    18: '3rd phase - general contingent',
    26: 'Ordinance No. 533-A/99, item b2) (Different Plan)',
    27: 'Ordinance No. 533-A/99, item b3 (Other Institution)',
    39: 'Over 23 years old',
    42: 'Transfer',
    43: 'Change of course',
    44: 'Technological specialization diploma holders',
    51: 'Change of institution/course',
    53: 'Short cycle diploma holders',
    57: 'Change of institution/course (International)'
}

# Invertir el diccionario para que las claves sean los nombres y los valores los números
application_mode_option_inverted = {v: k for k, v in application_mode_option.items()}
# Diccionario de opciones para 'Application order'
application_order_option = [0,1,2,3,4,5,6,7,8,9]

# Diccionario de opciones para 'Course'
course_option = {
    33: 'Biofuel Production Technologies',
    171: 'Animation and Multimedia Design',
    8014: 'Social Service (evening attendance)',
    9003: 'Agronomy',
    9070: 'Communication Design',
    9085: 'Veterinary Nursing',
    9119: 'Informatics Engineering',
    9130: 'Equinculture',
    9147: 'Management',
    9238: 'Social Service',
    9254: 'Tourism',
    9500: 'Nursing',
    9556: 'Oral Hygiene',
    9670: 'Advertising and Marketing Management',
    9773: 'Journalism and Communication',
    9853: 'Basic Education',
    9991: 'Management (evening attendance)'
}

# Diccionario de opciones para 'Daytime/evening attendance'
attendance_option = {
    1: 'Daytime',
    0: 'Evening'
}

# Diccionario para 'Previous qualification'
previous_qualification_option = {
    1: 'Secondary education',
    2: 'Higher education - bachelor\'s degree',
    3: 'Higher education - degree',
    4: 'Higher education - master\'s',
    5: 'Higher education - doctorate',
    6: 'Frequency of higher education',
    9: '12th year of schooling - not completed',
    10: '11th year of schooling - not completed',
    12: 'Other - 11th year of schooling',
    14: '10th year of schooling',
    15: '10th year of schooling - not completed',
    19: 'Basic education 3rd cycle (9th/10th/11th year) or equiv.',
    38: 'Basic education 2nd cycle (6th/7th/8th year) or equiv.',
    39: 'Technological specialization course',
    40: 'Higher education - degree (1st cycle)',
    42: 'Professional higher technical course',
    43: 'Higher education - master (2nd cycle)'
}

# Diccionario para 'Nationality'
nationality_option = {
    1: 'Portuguese',
    2: 'German',
    6: 'Spanish',
    11: 'Italian',
    13: 'Dutch',
    14: 'English',
    17: 'Lithuanian',
    21: 'Angolan',
    22: 'Cape Verdean',
    24: 'Guinean',
    25: 'Mozambican',
    26: 'Santomean',
    32: 'Turkish',
    41: 'Brazilian',
    62: 'Romanian',
    100: 'Moldova (Republic of)',
    101: 'Mexican',
    103: 'Ukrainian',
    105: 'Russian',
    108: 'Cuban',
    109: 'Colombian'
}

# Diccionario para 'Mothers qualification'
mothers_qualification_option = {
    1: 'Secondary Education - 12th Year of Schooling or Eq.',
    2: 'Higher Education - Bachelor\'s Degree',
    3: 'Higher Education - Degree',
    4: 'Higher Education - Master\'s',
    5: 'Higher Education - Doctorate',
    6: 'Frequency of Higher Education',
    9: '12th Year of Schooling - Not Completed',
    10: '11th Year of Schooling - Not Completed',
    11: '7th Year (Old)',
    12: 'Other - 11th Year of Schooling',
    14: '10th Year of Schooling',
    18: 'General Commerce Course',
    19: 'Basic Education 3rd Cycle (9th/10th/11th Year) or Equivalent',
    22: 'Technical-professional course',
    26: '7th Year of Schooling',
    27: '2nd Cycle of the General High School Course',
    29: '9th Year of Schooling - Not Completed',
    30: '8th Year of Schooling',
    34: 'Unknown',
    35: 'Can\'t read or write',
    36: 'Can read without having a 4th Year of Schooling',
    37: 'Basic Education 1st Cycle (4th/5th Year) or Equivalent',
    38: 'Basic Education 2nd Cycle (6th/7th/8th Year) or Equivalent',
    39: 'Technological Specialization Course',
    40: 'Higher Education - Degree (1st Cycle)',
    41: 'Specialized Higher Studies Course',
    42: 'Professional Higher Technical Course',
    43: 'Higher Education - Master (2nd Cycle)',
    44: 'Higher Education - Doctorate (3rd Cycle)'
}

# Diccionario para 'Fathers qualification'
fathers_qualification_option = {
    1: 'Secondary Education - 12th Year of Schooling or Eq.',
    2: 'Higher Education - Bachelor\'s Degree',
    3: 'Higher Education - Degree',
    4: 'Higher Education - Master\'s',
    5: 'Higher Education - Doctorate',
    6: 'Frequency of Higher Education',
    9: '12th Year of Schooling - Not Completed',
    10: '11th Year of Schooling - Not Completed',
    11: '7th Year (Old)',
    12: 'Other - 11th Year of Schooling',
    13: '2nd Year Complementary High School Course',
    14: '10th Year of Schooling',
    18: 'General Commerce Course',
    19: 'Basic Education 3rd Cycle (9th/10th/11th Year) or Equivalent',
    20: 'Complementary High School Course',
    22: 'Technical-professional Course',
    25: 'Complementary High School Course - Not Concluded',
    26: '7th Year of Schooling',
    27: '2nd Cycle of the General High School Course',
    29: '9th Year of Schooling - Not Completed',
    30: '8th Year of Schooling',
    31: 'General Course of Administration and Commerce',
    33: 'Supplementary Accounting and Administration',
    34: 'Unknown',
    35: 'Can\'t Read or Write',
    36: 'Can Read Without Having a 4th Year of Schooling',
    37: 'Basic Education 1st Cycle (4th/5th Year) or Equivalent',
    38: 'Basic Education 2nd Cycle (6th/7th/8th Year) or Equivalent',
    39: 'Technological Specialization Course',
    40: 'Higher Education - Degree (1st Cycle)',
    41: 'Specialized Higher Studies Course',
    42: 'Professional Higher Technical Course',
    43: 'Higher Education - Master (2nd Cycle)',
    44: 'Higher Education - Doctorate (3rd Cycle)'
}

# Diccionario para 'Mothers occupation'
mothers_occupation_option = {
    0: 'Student',
    1: 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers',
    2: 'Specialists in Intellectual and Scientific Activities',
    3: 'Intermediate Level Technicians and Professions',
    4: 'Administrative staff',
    5: 'Personal Services, Security and Safety Workers and Sellers',
    6: 'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry',
    7: 'Skilled Workers in Industry, Construction and Craftsmen',
    8: 'Installation and Machine Operators and Assembly Workers',
    9: 'Unskilled Workers',
    10: 'Armed Forces Professions',
    90: 'Other Situation',
    99: '(blank)',
    122: 'Health professionals',
    123: 'Teachers',
    125: 'Specialists in information and communication technologies (ICT)',
    131: 'Intermediate level science and engineering technicians and professions',
    132: 'Technicians and professionals, of intermediate level of health',
    134: 'Intermediate level technicians from legal, social, sports, cultural and similar services',
    141: 'Office workers, secretaries in general and data processing operators',
    143: 'Data, accounting, statistical, financial services and registry-related operators',
    144: 'Other administrative support staff',
    151: 'Personal service workers',
    152: 'Sellers',
    153: 'Personal care workers and the like',
    171: 'Skilled construction workers and the like, except electricians',
    173: 'Skilled workers in printing, precision instrument manufacturing, jewelers, artisans and the like',
    175: 'Workers in food processing, woodworking, clothing and other industries and crafts',
    191: 'Cleaning workers',
    192: 'Unskilled workers in agriculture, animal production, fisheries and forestry',
    193: 'Unskilled workers in extractive industry, construction, manufacturing and transport',
    194: 'Meal preparation assistants'
}

# Diccionario para 'Fathers occupation'
fathers_occupation_option = {
    0: 'Student',
    1: 'Representatives of the Legislative Power and Executive Bodies, Directors, Directors and Executive Managers',
    2: 'Specialists in Intellectual and Scientific Activities',
    3: 'Intermediate Level Technicians and Professions',
    4: 'Administrative staff',
    5: 'Personal Services, Security and Safety Workers and Sellers',
    6: 'Farmers and Skilled Workers in Agriculture, Fisheries and Forestry',
    7: 'Skilled Workers in Industry, Construction and Craftsmen',
    8: 'Installation and Machine Operators and Assembly Workers',
    9: 'Unskilled Workers',
    10: 'Armed Forces Professions',
    90: 'Other Situation',
    99: '(blank)',
    101: 'Armed Forces Officers',
    102: 'Armed Forces Sergeants',
    103: 'Other Armed Forces personnel',
    112: 'Directors of administrative and commercial services',
    114: 'Hotel, catering, trade and other services directors',
    121: 'Specialists in the physical sciences, mathematics, engineering and related techniques',
    122: 'Health professionals',
    123: 'Teachers',
    124: 'Specialists in finance, accounting, administrative organization, public and commercial relations',
    131: 'Intermediate level science and engineering technicians and professions',
    132: 'Technicians and professionals, of intermediate level of health',
    134: 'Intermediate level technicians from legal, social, sports, cultural and similar services',
    135: 'Information and communication technology technicians',
    141: 'Office workers, secretaries in general and data processing operators',
    143: 'Data, accounting, statistical, financial services and registry-related operators',
    144: 'Other administrative support staff',
    151: 'Personal service workers',
    152: 'Sellers',
    153: 'Personal care workers and the like',
    154: 'Protection and security services personnel',
    161: 'Market-oriented farmers and skilled agricultural and animal production workers',
    163: 'Farmers, livestock keepers, fishermen, hunters and gatherers, subsistence',
    171: 'Skilled construction workers and the like, except electricians',
    172: 'Skilled workers in metallurgy, metalworking and similar',
    174: 'Skilled workers in electricity and electronics',
    175: 'Workers in food processing, woodworking, clothing and other industries and crafts',
    181: 'Fixed plant and machine operators',
    182: 'Assembly workers',
    183: 'Vehicle drivers and mobile equipment operators',
    192: 'Unskilled workers in agriculture, animal production, fisheries and forestry',
    193: 'Unskilled workers in extractive industry, construction, manufacturing and transport',
    194: 'Meal preparation assistants',
    195: 'Street vendors (except food) and street service providers'
}

# Diccionario para 'Displaced'
displaced_option = {
    1: 'Yes',
    0: 'No'
}

# Diccionario para 'Educational special needs'
educational_special_needs_option = {
    1: 'Yes',
    0: 'No'
}

# Diccionario para 'Debtor'
debtor_option = {
    1: 'Yes',
    0: 'No'
}

# Diccionario para 'Tuition fees up to date'
tuition_fees_option = {
    1: 'Yes',
    0: 'No'
}

# Diccionario para 'Gender'
gender_option = {
    1: 'Male',
    0: 'Female'
}

# Diccionario para 'Scholarship holder'
scholarship_option = {
    1: 'Yes',
    0: 'No'
}

# Lista de valores de 'Age'
age_option = [20, 19, 45, 50, 18, 22, 21, 34, 37, 43, 55, 39, 29, 24, 27, 23, 26, 33, 35, 25, 44, 36, 47,
              28, 38, 30, 31, 32, 40, 42, 48, 49, 46, 41, 70, 60, 53, 51, 52, 54, 61, 58, 59, 17, 57, 62]


# Diccionario de valores para 'International'
international_option = {
    1: 'Yes',
    0: 'No'
}

# Lista de valores para 'Curricular units 1st sem (credited)'
curricular_units_option = [0, 2, 3, 6, 7, 13, 4, 1, 5, 19, 11, 8, 10, 9, 15, 12, 14, 18, 17, 16, 20]

# Lista de valores para 'Curricular units 1st sem (enrolled)'
curricular_units_enrolled_option = [0, 6, 5, 7, 8, 1, 12, 10, 18, 9, 21, 3, 17, 16, 11, 14, 13, 2, 4, 15, 19, 23, 26]

# Lista de valores para 'Curricular units 1st sem (evaluations)'
curricular_units_evaluations_option = [0, 6, 8, 9, 10, 5, 7, 14, 12, 15, 13, 11, 1, 17, 18, 19, 21, 4, 16, 3, 24, 2, 22, 45,
                                       20, 26, 29, 36, 32, 23, 27, 31, 28, 25, 33]

# Lista de valores para 'Curricular units 1st sem (approved)'
curricular_units_approved_option = [0, 6, 5, 7, 4, 1, 3, 2, 8, 18, 10,
                                     9, 21, 11, 13, 12, 16, 14,
                                     17, 19, 15, 20, 26]

# Campo para ingresar el promedio de calificaciones 'Curricular units 1st sem (grade)'
average_grade = st.number_input(
    "Ingresa el promedio de calificaciones en el 1er semestre (entre 0 y 20)",
    min_value=0.0,  # Valor mínimo
    max_value=20.0,  # Valor máximo
    value=0.0,  # Valor inicial
    step=0.01,  # Incremento de 0.01 para dos decimales
    format="%.2f"  # Formato para mostrar dos decimales
)

# Lista de valores para 'Curricular units 1st sem (without evaluations)' ordenada de forma ascendente
curricular_units_without_evaluations_option = [0, 1, 2, 3, 4, 5, 6, 7, 8, 10, 12]

# Lista de valores para 'Curricular units 2nd sem (credited)' ordenada de forma ascendente
curricular_units_credited_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 18, 19]

# Lista de valores para 'Curricular units 2nd sem (enrolled)'
curricular_units_enrolled_option = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 21, 23]

# Lista de valores para 'Curricular units 2nd sem (evaluations)'
curricular_units_evaluations_option = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19,
                                       20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 33]

# Lista de valores para 'Curricular units 2nd sem (approved)'
curricular_units_approved_option = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9,
                                     10, 11, 12, 13, 14, 16,
                                     17, 18, 19, 20]


# Campo para ingresar el promedio de calificaciones 'Curricular units 2nd sem (grade)'
average_grade_2nd_sem = st.number_input(
    "Ingresa el promedio de calificaciones en el 2º semestre (entre 0 y 20)",
    min_value=0.0,  # Valor mínimo
    max_value=20.0,  # Valor máximo
    value=0.0,  # Valor inicial
    step=0.01,  # Incremento de 0.01 para dos decimales
    format="%.2f"  # Formato para mostrar dos decimales
)

# Lista de valores para 'Curricular units 2nd sem (without evaluations)'
curricular_units_without_evaluations_values = [0, 1, 2, 3, 4, 5, 6, 7, 8, 12]

# Campo para ingresar la tasa de desempleo 'Unemployment rate'
unemployment_rate = st.number_input(
    "Ingresa la tasa de desempleo (entre 5% y 20%)",
    min_value=5.0,  # Valor mínimo
    max_value=20.0,  # Valor máximo
    value=5.0,  # Valor inicial
    step=0.1,  # Incremento de 0.1 para permitir decimales
    format="%.1f"  # Formato para mostrar un decimal
)

# Campo para ingresar la tasa de inflación 'Inflation rate'
inflation_rate = st.number_input(
    "Ingresa la tasa de inflación (entre -1% y 10%)",
    min_value=-1.0,  # Valor mínimo
    max_value=10.0,  # Valor máximo
    value=0.0,  # Valor inicial
    step=0.1,  # Incremento de 0.1 para permitir decimales
    format="%.1f"  # Formato para mostrar un decimal
)

# Campo para ingresar el PIB 'GDP'
gdp_rate = st.number_input(
    "Ingresa la tasa de PIB (entre -5% y 10%)",
    min_value=-5.0,  # Valor mínimo
    max_value=10.0,  # Valor máximo
    value=0.0,  # Valor inicial
    step=0.1,  # Incremento de 0.1 para permitir decimales
    format="%.1f"  # Formato para mostrar un decimal
)

# Función para cargar los modelos
def load_model(model_path):
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        st.error(f"Error al cargar el modelo desde {model_path}: {str(e)}")
        return None

# Ruta a los modelos
svm_model = load_model('/content/MLProject/svm_model.joblib')
xgb_model = load_model('/content/MLProject/xgb_model.joblib')
rf_model = load_model('/content/MLProject/rf_model.joblib')

# Asegurarse de que los modelos se hayan cargado correctamente
models = {
    'SVM': svm_model,
    'XGBoost': xgb_model,
    'Random Forest': rf_model
}

# Diccionario de características por modelo
model_features = {
    'SVM': [
        'Curricular units 2nd sem (approved)', 'Curricular units 1st sem (approved)', 
        'Curricular units 2nd sem (grade)', 'Tuition fees up to date_1', 'Curricular units 1st sem (grade)', 
        'Debtor_1', 'Age', 'Curricular units 1st sem (evaluations)', 'Scholarship holder_1', 
        'Curricular units 2nd sem (evaluations)', 'Curricular units 2nd sem (credited)', 
        'Curricular units 1st sem (credited)', 'Curricular units 1st sem (enrolled)', 
        'Curricular units 2nd sem (without evaluations)', 'Curricular units 2nd sem (enrolled)', 
        'Application mode', 'Nationality', 'Course', 'Curricular units 1st sem (without evaluations)', 
        'Displaced_1'
    ],
    'XGBoost': [
        'Curricular units 2nd sem (approved)', 'Tuition fees up to date_1', 
        'Educational special needs_1', 'Marital status', 'Curricular units 1st sem (approved)', 
        'Curricular units 1st sem (evaluations)', 'Curricular units 2nd sem (enrolled)', 
        'Curricular units 2nd sem (evaluations)', 'Age'
    ],
    'Random Forest': [
        'Curricular units 2nd sem (approved)', 'Curricular units 2nd sem (grade)', 
        'Curricular units 1st sem (approved)', 'Curricular units 1st sem (grade)', 
        'Curricular units 2nd sem (evaluations)', 'Curricular units 1st sem (evaluations)', 
        'Age', 'Tuition fees up to date_1', 'Mothers occupation', 'Course', 
        'Application mode', 'Unemployment rate', 'Inflation rate', 'GDP', 
        'Fathers occupation', 'Mothers qualification', 'Fathers qualification', 
        'Curricular units 2nd sem (enrolled)', 'Application order', 'Curricular units 1st sem (enrolled)', 
        'Debtor_1', 'Gender_1'
    ]
}

# Título de la aplicación
st.title("Modelos de Clasificación de estudiantes para Enrolled, Graduate o Dropout")
st.write("Esta aplicación utiliza 3 modelos de Machine Learning: SVM, XGBoost y Random Forest")

# Selector de modelo
model_options = ['SVM', 'XGBoost', 'Random Forest']
selected_model = st.selectbox('Selecciona el modelo a utilizar:', model_options)

# Mostrar el modelo seleccionado
st.write(f"Has seleccionado el modelo: {selected_model}")

# Solicitar entrada de características al usuario
st.write("Ingresa los valores de las características:")
input_data = []

for feature in model_features[selected_model]:
    if feature == 'Marital status':
        selected_option = st.selectbox(f"{feature}:", list(marital_status_options.keys()))
        value = marital_status_options[selected_option]
    elif feature == 'Application mode':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(application_mode_option_inverted.keys()))
        value = application_mode_option_inverted[selected_option]  # Guardar el valor numérico correspondiente
    elif feature == 'Course':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(course_option.values()))  # Mostrar descripciones
        value = [k for k, v in course_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Daytime/evening attendance':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(attendance_option.values()))  # Mostrar descripciones
        value = [k for k, v in attendance_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Previous qualification':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(previous_qualification_option.values()))  # Mostrar descripciones
        value = [k for k, v in previous_qualification_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Nationality':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(nationality_option.values()))  # Mostrar descripciones
        value = [k for k, v in nationality_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Mothers qualification':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(mothers_qualification_option.values()))  # Mostrar descripciones
        value = [k for k, v in mothers_qualification_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Fathers qualification':  # Característica categórica con opciones descriptivas
         selected_option = st.selectbox(f"{feature}:", list(fathers_qualification_option.values()))  # Mostrar descripciones
         value = [k for k, v in fathers_qualification_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Mothers occupation':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(mothers_occupation_option.values()))  # Mostrar descripciones
        value = [k for k, v in mothers_occupation_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Fathers occupation':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(fathers_occupation_option.values()))  # Mostrar descripciones
        value = [k for k, v in fathers_occupation_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Displaced':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(displaced_option.values()))  # Mostrar descripciones
        value = [k for k, v in displaced_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Educational special needs':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(educational_special_needs_option.values()))  # Mostrar descripciones
        value = [k for k, v in educational_special_needs_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Debtor':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(debtor_option.values()))  # Mostrar descripciones
        value = [k for k, v in debtor_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Tuition fees up to date':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(tuition_fees_option.values()))  # Mostrar descripciones
        value = [k for k, v in tuition_fees_option.items() if v == selected_option][0]  #
    elif feature == 'Gender':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(gender_option.values()))  # Mostrar descripciones
        value = [k for k, v in gender_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Scholarship holder_1':  # Característica categórica con opciones descriptivas
        selected_option = st.selectbox(f"{feature}:", list(scholarship_option.values()))  # Mostrar descripciones
        value = [k for k, v in scholarship_option.items() if v == selected_option][0]  # Guardar el valor numérico correspondiente
    elif feature == 'Age':  # Característica numérica (Edad)
        sorted_age_option = sorted(age_option)  # Ordena la lista de edades de forma ascendente
        selected_age = st.selectbox(f"Selecciona la {feature}:", sorted_age_option)  # Desplegable con valores numéricos ordenados
        value = selected_age  # El valor seleccionado se guarda directamente como número
    elif feature == 'International':  # Característica 'International'
        international_option = {
        1: 'Yes',
        0: 'No'
        }
        selected_international = st.selectbox(f"Selecciona si el estudiante es internacional:", list(international_option.values()))
        value = [key for key, val in international_option.items() if val == selected_international][0]  # Obtiene el valor numérico correspondiente
    elif feature == 'Curricular units 1st sem (credited)':  # Característica 'Curricular units 1st sem (credited)'
        curricular_units_option = [0, 2, 3, 6, 7, 13, 4, 1, 5, 19, 11, 8, 10, 9, 15, 12, 14, 18, 17, 16, 20]
        curricular_units_option.sort()  # Ordenar la lista de forma ascendente
        selected_curricular_units = st.selectbox(f"Selecciona el número de unidades curriculares acreditadas en el 1er semestre:", curricular_units_option)
        value = selected_curricular_units  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 1st sem (enrolled)':  # Característica 'Curricular units 1st sem (enrolled)'
        curricular_units_enrolled_option = [0, 6, 5, 7, 8, 1, 12, 10, 18, 9, 21, 3, 17, 16, 11, 14, 13, 2, 4, 15, 19, 23, 26]
        curricular_units_enrolled_option.sort()  # Ordenar la lista de forma ascendente
        selected_curricular_units_enrolled = st.selectbox(
        f"Selecciona el número de unidades curriculares inscritas en el 1er semestre:", curricular_units_enrolled_option
        )
        value = selected_curricular_units_enrolled  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 1st sem (evaluations)':  # Característica 'Curricular units 1st sem (evaluations)'
        curricular_units_evaluations_option = [0, 6, 8, 9, 10, 5, 7, 14, 12, 15, 13, 11, 1, 17, 18, 19, 21, 4, 16, 3, 24, 2, 22, 45,
                                           20, 26, 29, 36, 32, 23, 27, 31, 28, 25, 33]
        curricular_units_evaluations_option.sort()  # Ordenar la lista de forma ascendente
        selected_curricular_units_evaluations = st.selectbox(
        f"Selecciona el número de unidades curriculares evaluadas en el 1er semestre:", curricular_units_evaluations_option
        )
        value = selected_curricular_units_evaluations  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 1st sem (approved)':  # Característica 'Curricular units 1st sem (approved)'
        curricular_units_approved_option = [0, 6, 5, 7, 4, 1, 3, 2, 8, 18, 10, 
                                        9, 21, 11, 13, 12, 16, 14, 
                                        17, 19, 15, 20, 26]
        curricular_units_approved_option.sort()  # Ordenar la lista de forma ascendente
        selected_curricular_units_approved = st.selectbox(
        f"Selecciona el número de unidades curriculares aprobadas en el 1er semestre:", curricular_units_approved_option
        )
        value = selected_curricular_units_approved  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 1st sem (grade)':  # Característica 'Curricular units 1st sem (grade)'
        # Campo para ingresar el promedio de calificaciones en el 1er semestre
        average_grade = st.number_input(
          "Ingresa el promedio de calificaciones en el 1er semestre (entre 0 y 20)",
          min_value=0.0,  # Valor mínimo
          max_value=20.0,  # Valor máximo
          value=0.0,  # Valor inicial
          step=0.01,  # Incremento de 0.01 para dos decimales
          format="%.2f"  # Formato para mostrar dos decimales
        )
        value = average_grade  # El valor seleccionado es el promedio ingresado
    elif feature == 'Curricular units 1st sem (without evaluations)':  # Característica 'Curricular units 1st sem (without evaluations)'
        selected_curricular_units_without_evaluations = st.selectbox(
          "Selecciona el número de unidades curriculares en el 1er semestre (sin evaluaciones):", 
          curricular_units_without_evaluations_option
        )
        value = selected_curricular_units_without_evaluations  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 2nd sem (credited)':  # Característica 'Curricular units 2nd sem (credited)'
        selected_curricular_units_credited = st.selectbox(
          "Selecciona el número de unidades curriculares acreditadas en el 2do semestre:", 
          curricular_units_credited_values
        )
        value = selected_curricular_units_credited  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 2nd sem (enrolled)':  # Característica 'Curricular units 2nd sem (enrolled)'
        selected_curricular_units_enrolled = st.selectbox(
          "Selecciona el número de unidades curriculares matriculadas en el 2do semestre:", 
          curricular_units_enrolled_option
        )
        value = selected_curricular_units_enrolled  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 2nd sem (evaluations)':  # Característica 'Curricular units 2nd sem (evaluations)'
        selected_curricular_units_evaluations = st.selectbox(
          "Selecciona el número de unidades curriculares evaluadas en el 2do semestre:", 
          curricular_units_evaluations_option
        )
        value = selected_curricular_units_evaluations  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 2nd sem (approved)':  # Característica 'Curricular units 2nd sem (approved)'
        selected_curricular_units_approved = st.selectbox(
          "Selecciona el número de unidades curriculares aprobadas en el 2do semestre:", 
          curricular_units_approved_option
        )
        value = selected_curricular_units_approved  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Curricular units 2nd sem (grade)':  # Caso para promedio de 2º semestre
        average_grade_2nd_sem = st.number_input(
          "Ingresa el promedio de calificaciones en el 2º semestre (entre 0 y 20)",
          min_value=0.0, 
          max_value=20.0, 
          value=0.0, 
          step=0.01, 
          format="%.2f"
        )
    elif feature == 'Curricular units 2nd sem (without evaluations)':  # Característica 'Curricular units 2nd sem (without evaluations)'
        selected_curricular_units_without_evaluations = st.selectbox(
          "Selecciona el número de unidades curriculares sin evaluaciones en el 2º semestre:", 
          curricular_units_without_evaluations_values
        )
        value = selected_curricular_units_without_evaluations  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Unemployment rate':  # Caso para tasa de desempleo
        unemployment_rate = st.number_input(
          "Ingresa la tasa de desempleo (entre 5% y 20%)",
          min_value=5.0,  # Valor mínimo
          max_value=20.0,  # Valor máximo
          value=5.0,  # Valor inicial
          step=0.1,  # Incremento de 0.1 para permitir decimales
          format="%.1f"  # Formato para mostrar un decimal
        )
        value = unemployment_rate  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'Inflation rate':  # Caso para tasa de inflación
        inflation_rate = st.number_input(
          "Ingresa la tasa de inflación (entre -1% y 10%)",
          min_value=-1.0,  # Valor mínimo
          max_value=10.0,  # Valor máximo
          value=0.0,  # Valor inicial
          step=0.1,  # Incremento de 0.1 para permitir decimales
          format="%.1f"  # Formato para mostrar un decimal
        )
        value = inflation_rate  # El valor seleccionado es el valor numérico correspondiente
    elif feature == 'GDP':  # Caso para tasa de PIB
        gdp_rate = st.number_input(
          "Ingresa la tasa de PIB (entre -5% y 10%)",
          min_value=-5.0,  # Valor mínimo
          max_value=10.0,  # Valor máximo
          value=0.0,  # Valor inicial
          step=0.1,  # Incremento de 0.1 para permitir decimales
          format="%.1f"  # Formato para mostrar un decimal
        )

# Botón para realizar la predicción
if st.button("Realizar Predicción"):
    
    # Crear un diccionario para asegurarte de que tienes todas las características con valores predeterminados
    input_data_dict = {feature: input_data.get(feature, 0) for feature in model_features[selected_model]}
    
    # Convertir el diccionario a un array en el orden de expected_features
    input_data_array = np.array([input_data_dict[feature] for feature in model_features[selected_model]]).reshape(1, -1)

    # Obtener el modelo seleccionado
    model = models[selected_model]

    # Realizar la predicción
    prediction = predict_with_model(model, input_data_array, selected_model)

    if prediction is not None:
        st.write(f"La predicción con el modelo {selected_model} es: {prediction[0]}")
        
        # Mostrar el resultado final según el modelo seleccionado
        if selected_model == 'Random Forest':
            st.write("Usted ha obtenido: F1 Score ponderado: 0.7630 con el modelo Random Forest")
        elif selected_model == 'XGBoost':
            st.write("Usted ha obtenido: F1 Score ponderado: 0.7654 con el modelo XGBoost")
        elif selected_model == 'SVM':
            st.write("Usted ha obtenido: F1-score ponderado: 0.7700, con SVM, el mejor modelo de clasificación")
        
    else:
        st.write("Hubo un error al realizar la predicción.")
