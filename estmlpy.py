import streamlit as st
import pandas as pd
from joblib import load

# Título de la aplicación
st.title("Predicción de Resultados de Estudiantes")

# Descripción breve de la aplicación
st.write("""
Esta aplicación predice si un estudiante será un **Dropout**, **Enrolled**, o **Graduate** basándose en sus características.
Por favor, ingresa los datos y presiona el botón para obtener la predicción.
""")

# Formulario de entrada para el usuario
st.header("Ingresa las características del estudiante")
# Cargar el pipeline desde el archivo
pipeline_path = "svm_pipeline_complete.joblib"
pipeline = load(pipeline_path)

# 'Marital status'
marital_status_options = {
    'Single': 1,
    'Married': 2,
    'Widower': 3,
    'Divorced': 4,
    'Facto union': 5,
    'Legally separated': 6
}
marital_status = st.selectbox("Estado civil", options=list(marital_status_options.keys()))
marital_status_value = marital_status_options[marital_status]

# 'Application mode'
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
application_mode = st.selectbox(
    "Modo de aplicación",
    options=list(application_mode_option.values())
)
application_mode_value = list(application_mode_option.keys())[
    list(application_mode_option.values()).index(application_mode)
]

# 'Gender'
gender_option = {'Male': 1, 'Female': 0}
gender = st.selectbox("Género", options=list(gender_option.keys()))
gender_value = gender_option[gender]

# 'Scholarship holder'
scholarship_option = {'Yes': 1, 'No': 0}
scholarship = st.selectbox("¿Es becario?", options=list(scholarship_option.keys()))
scholarship_value = scholarship_option[scholarship]

# 'Age'
age = st.selectbox("Edad", options=sorted([20, 19, 45, 50, 18, 22, 21, 34, 37, 43, 55, 39, 29, 24, 27, 23, 26, 33, 35,
                                            25, 44, 36, 47, 28, 38, 30, 31, 32, 40, 42, 48, 49, 46, 41, 70, 60, 53, 51,
                                            52, 54, 61, 58, 59, 17, 57, 62]))
age_value = age

# 'International'
international_option = {'Yes': 1, 'No': 0}
international = st.selectbox("¿Es estudiante internacional?", options=list(international_option.keys()))
international_value = international_option[international]

# 'Curricular units 1st sem (credited)'
curricular_units_1_credited = st.selectbox(
    "Unidades curriculares 1o semestre (credited)",
    options=sorted([0, 2, 3, 6, 7, 13, 4, 1, 5, 19, 11, 8, 10, 9, 15, 12, 14, 18, 17, 16, 20])
)
curricular_units_1_credited_value = curricular_units_1_credited

# 'Curricular units 1st sem (enrolled)'
curricular_units_1_enrrolled = st.selectbox(
    "Unidades curriculares 1o semestre (matriculado)",
    options=sorted([0, 6, 5, 7, 8, 1, 12, 10, 18, 9, 21, 3, 17, 16, 11, 14, 13, 2, 4, 15, 19, 23, 26])
)
curricular_units_1_enrrolled_value = curricular_units_1_enrrolled

# 'Curricular units 1st sem (evaluations)'
curricular_units_1_evaluations = st.selectbox(
    "Unidades curriculares 1o semestre (evaluaciones)",
    options=sorted([0, 6, 8, 9, 10, 5, 7, 14, 12, 15, 13, 11, 1, 17, 18, 19, 21, 4, 16, 3, 24, 2, 22, 45, 20, 26, 29, 36, 32, 23, 27, 31, 28, 25, 33])
)
curricular_units_1_evaluations_value = curricular_units_1_evaluations

# 'Curricular units 1st sem (approved)'
curricular_units_1_approved = st.selectbox(
    "Unidades curriculares 1o semestre (aprobadas)",
    options=sorted([0, 6, 5, 7, 4, 1, 3, 2, 8, 18, 10, 9, 21, 11, 13, 12, 16, 14, 17, 19, 15, 20, 26])
)
curricular_units_1_approved_value = curricular_units_1_approved

# 'Curricular units 1st sem (grade)'
average_1_grade = st.number_input(
    "Ingresa el promedio de calificaciones en el 1er semestre (entre 0 y 20)",
    min_value=0.0,  # Valor mínimo
    max_value=20.0,  # Valor máximo
    value=0.0,  # Valor inicial
    step=0.01,  # Incremento de 0.01 para dos decimales
    format="%.2f"  # Formato para mostrar dos decimales
)
average_1_grade_value = average_1_grade

#'Curricular units 1st sem (without evaluations)'
curricular_units_1_we = st.selectbox(
    "Unidades curriculares 1o semestre (sin evaluaciones)",
    options=sorted([0, 1, 2, 4, 3, 6, 12, 10, 7, 5, 8])
)
curricular_units_1_value=curricular_units_1_we
#'Curricular units 2nd sem (credited)'
curricular_units_2_credited = st.selectbox(
    "Unidades curriculares 2do semestre (acreditadas)",
    options=sorted([0, 1, 2, 5, 7, 4, 10, 3, 13, 9, 6, 11, 12, 8, 14, 15, 16, 18, 19])
)
curricular_units_2_credited_value = curricular_units_2_credited
#'Curricular units 2nd sem (enrolled)'
curricular_units_2_enrrolled = st.selectbox(
    "Unidades curriculares 2o semestre (matriculado)",
    options=sorted([
                0, 6, 5, 8, 7, 11, 12, 9, 13, 19, 3, 10, 4, 17, 2, 1, 14, 15, 16, 23, 18, 21])
)
curricular_units_2_enrrolled_value = curricular_units_2_enrrolled
#'Curricular units 2nd sem (evaluations)'
curricular_units_2_evaluations = st.selectbox(
    "Unidades curriculares 2o semestre (evaluaciones)",
    options=sorted([
                    0, 6, 10, 17, 8, 5, 7, 14, 9, 12, 11, 13, 19, 3, 15, 16, 4, 18, 2, 21, 1, 26, 27, 22, 20, 24, 28, 23, 25, 33])
                )
curricular_units_2_evaluations_value = curricular_units_2_evaluations
#'Curricular units 2nd sem (approved)'
curricular_units_2_approved = st.selectbox(
    "Unidades curriculares 2o semestre (aprobadas)",
    options=sorted([0, 6, 5, 8, 2, 7, 4, 1, 3, 10, 13, 11, 19, 9, 12, 17, 14, 20, 16, 18])
                  )
curricular_units_2_approved_value = curricular_units_2_approved
#'Curricular units 2nd sem (grade)'
average_2_grade = st.number_input(
    "Ingresa el promedio de calificaciones en el 2do semestre (entre 0 y 20)",
    min_value=0.0,  # Valor mínimo
    max_value=20.0,  # Valor máximo
    value=0.0,  # Valor inicial
    step=0.01,  # Incremento de 0.01 para dos decimales
    format="%.2f"  # Formato para mostrar dos decimales
    )
average_2_grade_value = average_2_grade
#'Curricular units 2nd sem (without evaluations)'
curricular_units_2_we = st.selectbox(
    "Unidades curriculares 2o semestre (sin evaluaciones)",
    options=sorted([0, 5, 2, 1, 3, 6, 4, 12, 7, 8])
             )
curricular_units_2_value=curricular_units_2_we
# 'Unemployment rate'
unemployment_rate = st.number_input(
    "Tasa de desempleo (5%-20%)",
    min_value=5.0, max_value=20.0, value=5.0, step=0.1, format="%.1f"
)
unemployment_rate_value = unemployment_rate

# 'Inflation rate'
inflation_rate = st.number_input(
    "Tasa de inflación (-1% a 10%)",
    min_value=-1.0, max_value=10.0, value=0.0, step=0.1, format="%.1f"
)
inflation_rate_value = inflation_rate

# Recopilar todos los valores seleccionados
features_dict = {
    'Marital status': marital_status_value,
    'Application mode': application_mode_value,
    'Gender': gender_value,
    'Scholarship holder': scholarship_value,
    'Age': age_value,
    'International': international_value,
    'Curricular units 1st sem (credited)': curricular_units_1_credited_value,
    'Curricular units 1st sem (enrolled)': curricular_units_1_enrrolled_value,
    'Curricular units 1st sem (evaluations)': curricular_units_1_evaluations_value,
    'Curricular units 1st sem (approved)': curricular_units_1_approved_value,
    'Curricular units 1st sem (grade)': average_1_grade_value,
    'Curricular units 1st sem (without evaluations)':curricular_units_1_value,
    'Curricular units 2nd sem (credited)': curricular_units_2_credited_value,
    'Curricular units 2nd sem (enrolled)': curricular_units_2_enrrolled_value,
    'Curricular units 2nd sem (evaluations)': curricular_units_2_evaluations_value,
    'Curricular units 2nd sem (approved)': curricular_units_2_approved_value,
    'Curricular units 2nd sem (grade)': average_2_grade_value,
    'Curricular units 2nd sem (without evaluations)':curricular_units_2_value,
    'Unemployment rate': unemployment_rate_value,
    'Inflation rate': inflation_rate_value,
}

# Convertir el diccionario a un DataFrame para pasarlo al modelo
input_data = pd.DataFrame([features_dict])

# Asegurarse de que las columnas del DataFrame coincidan con las esperadas por el modelo
model_columns = [
    "Marital status", "Application mode", "Gender", "Scholarship holder", 
    "Age", "International", "Curricular units 1st sem (credited)", 
    "Curricular units 1st sem (enrolled)", "Curricular units 1st sem (evaluations)", 
    "Curricular units 1st sem (approved)", "Curricular units 1st sem (grade)", 
    "Curricular units 1st sem (without evaluations)", "Curricular units 2nd sem (credited)", 
    "Curricular units 2nd sem (enrolled)", "Curricular units 2nd sem (evaluations)", 
    "Curricular units 2nd sem (approved)", "Curricular units 2nd sem (grade)", 
    "Curricular units 2nd sem (without evaluations)", "Unemployment rate", "Inflation rate"
]

# Asegurarse de que el DataFrame tenga las columnas correctas (reordenar las columnas si es necesario)
input_data = input_data[model_columns]

# Mapeo de etiquetas actualizado (ajustado según la predicción real)
label_mapping = {'Dropout': 0, 'Enrolled': 1, 'Graduate': 2}

# Botón para hacer la predicción
if st.button("Predecir"):
    try:
        # Realizar la predicción
        prediction = pipeline.predict(input_data)  # Usamos el DataFrame directamente
        
        # Mapear las etiquetas de texto a valores numéricos
        predicted_label = label_mapping.get(prediction[0], prediction[0])

        st.write(f"**Valor predicho por el modelo:** {prediction[0]}")
        st.write(f"**Valor predicho (numérico):** {predicted_label}")

    except Exception as e:
        st.error(f"Error al realizar la predicción: {e}")
        st.write("Detalles del error:", str(e))
