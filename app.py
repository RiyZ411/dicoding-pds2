# Library
import streamlit as st
import pandas as pd
from sklearn.preprocessing import StandardScaler
import joblib
import base64
import numpy as np

# Fungsi untuk mendapatkan string base64 dari file gambar
def get_base64_of_bin_file(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Fungsi untuk mengatur gambar lokal sebagai latar belakang halaman
def set_png_as_page_bg(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    page_bg_img = '''
    <style>
    body {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    opacity: 0.92;
    }
    </style>
    ''' % bin_str

    st.markdown(page_bg_img, unsafe_allow_html=True)

# Menggunakan fungsi di atas
set_png_as_page_bg('./Images/DO.jpg')

# Sidebar contact
with st.sidebar:
    st.title("Profil")
    st.markdown("**Nama:** Riyan Zaenal Arifin")
    st.markdown("**Email:** riyanzaenal411@gmail.com")

# Custom CSS to increase form width and center the title
st.markdown(
    """
    <style>
    .block-container {
        max-width: 1400px; /* Maintain the wider form */
        padding: 20px;
    }
    .css-1aumxhk {
        width: 100%; /* Ensure columns take full available width */
    }
    .stNumberInput > div > div > input {
        width: 100%; /* Ensure number inputs are wider */
    }
    .stSelectbox > div > div > select {
        width: 100%; /* Ensure select boxes are wider */
    }
    h1 {
        text-align: center; /* Center the title */
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("Student Dropout Prediction")

# Mapping display labels to dataset codes
categorical_features = {
    "Marital_status": {
        "options": ["Single", "Married", "Widowed", "Divorced", "Facto union", "Legally separated"],
        "mapping": {1: "Single", 2: "Married", 3: "Widowed", 4: "Divorced", 5: "Facto union", 6: "Legally separated"}
    },
    "Application_mode": {
        "options": [
            "1st phase - general contingent", "Ordinance No. 612/93", "1st phase - special contingent (Azores)",
            "Holders of other higher courses", "Ordinance No. 854-B/99", "International student (bachelor)",
            "1st phase - special contingent (Madeira)", "2nd phase - general contingent", "3rd phase - general contingent",
            "Over 23 years old", "Transfer", "Change of course", "Short cycle diploma holders",
            "Change of institution/course", "Technological specialization diploma holders",
            "Change of institution/course (International)", "Ordinance No. 533-A/99, item b2) (Different Plan)",
            "Ordinance No. 533-A/99, item b3 (Other Institution)"
        ],
        "mapping": {
            1: "1st phase - general contingent", 2: "Ordinance No. 612/93", 5: "1st phase - special contingent (Azores)",
            7: "Holders of other higher courses", 10: "Ordinance No. 854-B/99", 15: "International student (bachelor)",
            16: "1st phase - special contingent (Madeira)", 17: "2nd phase - general contingent", 18: "3rd phase - general contingent",
            39: "Over 23 years old", 42: "Transfer", 43: "Change of course", 44: "Short cycle diploma holders",
            51: "Change of institution/course", 53: "Technological specialization diploma holders",
            57: "Change of institution/course (International)", 26: "Ordinance No. 533-A/99, item b2) (Different Plan)",
            27: "Ordinance No. 533-A/99, item b3 (Other Institution)"
        }
    },
    "Course": {
        "options": [
            "Biofuel Production Technologies", "Animation and Multimedia Design", "Social Service (evening attendance)",
            "Agronomy", "Communication Design", "Veterinary Nursing", "Informatics Engineering", "Equinculture",
            "Management", "Social Service", "Tourism", "Nursing", "Oral Hygiene", "Advertising and Marketing",
            "Journalism and Communication", "Basic Education", "Management (evening attendance)"
        ],
        "mapping": {
            33: "Biofuel Production Technologies", 171: "Animation and Multimedia Design", 8014: "Social Service (evening attendance)",
            9003: "Agronomy", 9070: "Communication Design", 9085: "Veterinary Nursing", 9119: "Informatics Engineering",
            9130: "Equinculture", 9147: "Management", 9238: "Social Service", 9254: "Tourism", 9500: "Nursing",
            9556: "Oral Hygiene", 9670: "Advertising and Marketing", 9773: "Journalism and Communication",
            9853: "Basic Education", 9991: "Management (evening attendance)"
        }
    },
    "Daytime_evening_attendance": {
        "options": ["Daytime", "Evening"],
        "mapping": {1: "Daytime", 0: "Evening"}
    },
    "Previous_qualification": {
        "options": [
            "Secondary education", "Higher education - bachelor's degree", "Higher education - degree",
            "Higher education - master's", "Higher education - doctorate", "Frequency of higher education",
            "12th year of schooling - not completed", "11th year of schooling - not completed", "Other - 11th year of schooling",
            "10th year of schooling", "10th/11th year of schooling - not completed", "Basic education 3rd cycle",
            "Basic education 2nd cycle", "Technological specialization course", "Higher education - degree (1st cycle)",
            "Professional higher technical course", "Higher education - master's (2nd cycle)"
        ],
        "mapping": {
            1: "Secondary education", 2: "Higher education - bachelor's degree", 3: "Higher education - degree",
            4: "Higher education - master's", 5: "Higher education - doctorate", 6: "Frequency of higher education",
            9: "12th year of schooling - not completed", 10: "11th year of schooling - not completed",
            11: "Other - 11th year of schooling", 12: "10th year of schooling", 14: "10th/11th year of schooling - not completed",
            15: "Basic education 3rd cycle", 19: "Basic education 2nd cycle", 38: "Technological specialization course",
            39: "Higher education - degree (1st cycle)", 40: "Professional higher technical course",
            42: "Higher education - master's (2nd cycle)"
        }
    },
    "Nacionality": {
        "options": [
            "Portuguese", "German", "Spanish", "Italian", "Dutch", "English", "Lithuanian", "Angolan",
            "Cape Verdean", "Guinean", "Mozambican", "Santomean", "Turkish", "Brazilian", "Romanian",
            "Moldova", "Mexican", "Ukrainian", "Russian", "Cuban", "Colombian"
        ],
        "mapping": {
            1: "Portuguese", 2: "German", 6: "Spanish", 11: "Italian", 13: "Dutch", 14: "English", 17: "Lithuanian",
            21: "Angolan", 22: "Cape Verdean", 24: "Guinean", 25: "Mozambican", 26: "Santomean", 32: "Turkish",
            41: "Brazilian", 62: "Romanian", 100: "Moldova", 101: "Mexican", 103: "Ukrainian", 105: "Russian",
            108: "Cuban", 109: "Colombian"
        }
    },
    "Mothers_qualification": {
        "options": [
            "Basic education 1st cycle", "Basic education 2nd cycle", "Basic education 3rd cycle",
            "Secondary education", "Technological specialization course", "Higher education - degree",
            "Professional higher technical course", "Higher education - bachelor's degree",
            "Higher education - master's", "Higher education - doctorate", "Unknown", "Other"
        ],
        "mapping": {
            1: "Basic education 1st cycle", 2: "Basic education 2nd cycle", 3: "Basic education 3rd cycle",
            4: "Secondary education", 5: "Technological specialization course", 6: "Higher education - degree",
            9: "Professional higher technical course", 10: "Higher education - bachelor's degree",
            11: "Higher education - master's", 12: "Higher education - doctorate", 29: "Unknown", 19: "Other"
        }
    },
    "Fathers_qualification": {
        "options": [
            "Basic education 1st cycle", "Basic education 2nd cycle", "Basic education 3rd cycle",
            "Secondary education", "Technological specialization course", "Higher education - degree",
            "Professional higher technical course", "Higher education - bachelor's degree",
            "Higher education - master's", "Higher education - doctorate", "Unknown", "Other"
        ],
        "mapping": {
            1: "Basic education 1st cycle", 2: "Basic education 2nd cycle", 3: "Basic education 3rd cycle",
            4: "Secondary education", 5: "Technological specialization course", 6: "Higher education - degree",
            9: "Professional higher technical course", 10: "Higher education - bachelor's degree",
            11: "Higher education - master's", 12: "Higher education - doctorate", 29: "Unknown", 19: "Other"
        }
    },
    "Mothers_occupation": {
        "options": [
            "Student", "Representatives of the Legislative Power", "Specialists in Intellectual and Scientific Activities",
            "Intermediate Level Technicians", "Administrative Staff", "Personal Service Workers",
            "Farmers and Skilled Agricultural Workers", "Skilled Workers in Industry", "Plant and Machine Operators",
            "Unskilled Workers", "Armed Forces Professions", "Unknown", "Other"
        ],
        "mapping": {
            0: "Student", 1: "Representatives of the Legislative Power", 2: "Specialists in Intellectual and Scientific Activities",
            3: "Intermediate Level Technicians", 4: "Administrative Staff", 5: "Personal Service Workers",
            6: "Farmers and Skilled Agricultural Workers", 7: "Skilled Workers in Industry", 8: "Plant and Machine Operators",
            9: "Unskilled Workers", 10: "Armed Forces Professions", 99: "Unknown", 90: "Other"
        }
    },
    "Fathers_occupation": {
        "options": [
            "Student", "Representatives of the Legislative Power", "Specialists in Intellectual and Scientific Activities",
            "Intermediate Level Technicians", "Administrative Staff", "Personal Service Workers",
            "Farmers and Skilled Agricultural Workers", "Skilled Workers in Industry", "Plant and Machine Operators",
            "Unskilled Workers", "Armed Forces Professions", "Unknown", "Other"
        ],
        "mapping": {
            0: "Student", 1: "Representatives of the Legislative Power", 2: "Specialists in Intellectual and Scientific Activities",
            3: "Intermediate Level Technicians", 4: "Administrative Staff", 5: "Personal Service Workers",
            6: "Farmers and Skilled Agricultural Workers", 7: "Skilled Workers in Industry", 8: "Plant and Machine Operators",
            9: "Unskilled Workers", 10: "Armed Forces Professions", 99: "Unknown", 90: "Other"
        }
    },
    "Displaced": {
        "options": ["Yes", "No"],
        "mapping": {1: "Yes", 0: "No"}
    },
    "Educational_special_needs": {
        "options": ["Yes", "No"],
        "mapping": {1: "Yes", 0: "No"}
    },
    "Debtor": {
        "options": ["Yes", "No"],
        "mapping": {1: "Yes", 0: "No"}
    },
    "Tuition_fees_up_to_date": {
        "options": ["Yes", "No"],
        "mapping": {1: "Yes", 0: "No"}
    },
    "Gender": {
        "options": ["Male", "Female"],
        "mapping": {1: "Male", 0: "Female"}
    },
    "Scholarship_holder": {
        "options": ["Yes", "No"],
        "mapping": {1: "Yes", 0: "No"}
    },
    "International": {
        "options": ["Yes", "No"],
        "mapping": {1: "Yes", 0: "No"}
    }
}

# Reverse mapping for prediction
reverse_mapping = {key: {v: k for k, v in value["mapping"].items()} for key, value in categorical_features.items()}

# Define numeric features and their min/max values (18 features as per UCI dataset)
numeric_features = {
    "Application_order": (0.0, 9.0),
    "Previous_qualification_grade": (95.0, 190.0),
    "Admission_grade": (95.0, 190.0),
    "Age_at_enrollment": (17.0, 70.0),
    "Curricular_units_1st_sem_credited": (0.0, 20.0),
    "Curricular_units_1st_sem_enrolled": (0.0, 26.0),
    "Curricular_units_1st_sem_evaluations": (0.0, 45.0),
    "Curricular_units_1st_sem_approved": (0.0, 26.0),
    "Curricular_units_1st_sem_grade": (0.0, 18.875),
    "Curricular_units_1st_sem_without_evaluations": (0.0, 12.0),
    "Curricular_units_2nd_sem_credited": (0.0, 19.0),
    "Curricular_units_2nd_sem_enrolled": (0.0, 23.0),
    "Curricular_units_2nd_sem_evaluations": (0.0, 33.0),
    "Curricular_units_2nd_sem_approved": (0.0, 20.0),
    "Curricular_units_2nd_sem_grade": (0.0, 18.571429),
    "Curricular_units_2nd_sem_without_evaluations": (0.0, 12.0),
    "Unemployment_rate": (7.6, 16.2),
    "Inflation_rate": (-0.8, 3.7),
    "GDP" : (-4.06 , 3.51)
}

# Create a dictionary to store input values
input_data = {}

# Create four columns for layout
col1, col2, col3, col4 = st.columns(4)

# Split features across columns
all_features = list(categorical_features.keys()) + list(numeric_features.keys())
features_per_column = len(all_features) // 4 + (1 if len(all_features) % 4 else 0)

# Assign features to each column
col1_features = all_features[:features_per_column]
col2_features = all_features[features_per_column:2*features_per_column]
col3_features = all_features[2*features_per_column:3*features_per_column]
col4_features = all_features[3*features_per_column:]

# Helper function to create input widgets
def create_input(feature, column):
    if feature in categorical_features:
        input_data[feature] = column.selectbox(
            label=feature.replace("_", " ").title(),
            options=categorical_features[feature]["options"],
            key=feature
        )
    else:
        min_val, max_val = numeric_features[feature]
        input_data[feature] = column.number_input(
            label=feature.replace("_", " ").title(),
            min_value=min_val,
            max_value=max_val,
            value=min_val,
            step=0.01 if max_val <= 190.0 else 1.0,
            format="%.2f" if max_val <= 190.0 else "%.0f",
            key=feature,
            help=f"Masukkan nilai antara {min_val} dan {max_val}"
        )

# Populate columns with input widgets
for feature in col1_features:
    with col1:
        create_input(feature, st)

for feature in col2_features:
    with col2:
        create_input(feature, st)

for feature in col3_features:
    with col3:
        create_input(feature, st)

for feature in col4_features:
    with col4:
        create_input(feature, st)

# Load the machine learning model and scaler
try:
    model = joblib.load("./Model/model.pkl")
    scaler = joblib.load("./Model/scaler.pkl")
except FileNotFoundError as e:
    st.error(f"File not found: {str(e)}. Please ensure 'model.joblib' and 'scaler.joblib' are in the correct directory.")
    st.stop()
except Exception as e:
    st.error(f"Error loading model or scaler: {str(e)}")
    st.stop()

# Submit button and prediction
if st.button("Prediction"):
    st.write("### Data yang Dimasukkan:")
    for column, value in input_data.items():
        st.write(f"**{column.replace('_', ' ').title()}:** {value}")

    # Prepare data for prediction
    # Convert categorical inputs to their respective codes
    prediction_data = {}
    for feature, value in input_data.items():
        if feature in categorical_features:
            prediction_data[feature] = reverse_mapping[feature][value]
        else:
            prediction_data[feature] = value

    # The column order during training
    ex = ['Marital_status',
    'Application_mode',
    'Application_order',
    'Course',
    'Daytime_evening_attendance',
    'Previous_qualification',
    'Previous_qualification_grade',
    'Nacionality',
    'Mothers_qualification',
    'Fathers_qualification',
    'Mothers_occupation',
    'Fathers_occupation',
    'Admission_grade',
    'Displaced',
    'Educational_special_needs',
    'Debtor',
    'Tuition_fees_up_to_date',
    'Gender',
    'Scholarship_holder',
    'Age_at_enrollment',
    'International',
    'Curricular_units_1st_sem_credited',
    'Curricular_units_1st_sem_enrolled',
    'Curricular_units_1st_sem_evaluations',
    'Curricular_units_1st_sem_approved',
    'Curricular_units_1st_sem_grade',
    'Curricular_units_1st_sem_without_evaluations',
    'Curricular_units_2nd_sem_credited',
    'Curricular_units_2nd_sem_enrolled',
    'Curricular_units_2nd_sem_evaluations',
    'Curricular_units_2nd_sem_approved',
    'Curricular_units_2nd_sem_grade',
    'Curricular_units_2nd_sem_without_evaluations',
    'Unemployment_rate',
    'Inflation_rate',
    'GDP']

    # Validasi kelengkapan fitur
    missing = [feat for feat in ex if feat not in prediction_data]
    if missing:
        st.error(f"Fitur berikut belum disediakan: {missing}")
        st.stop()

    # Membuat DataFrame untuk prediksi
    df_pred = pd.DataFrame([prediction_data])[ex]

    # Normalisasi dengan scaler
    try:
        df_scaled = scaler.transform(df_pred)
    except Exception as e:
        st.error(f"Kesalahan saat normalisasi: {e}")
        st.stop()

    # Prediksi
    try:
        prediction = model.predict(df_scaled)[0]
        label_mapping = {
                        0: 'Dropout',
                        1: 'Graduate',
                        2: 'Enrolled'
                    }
        predicted_label = label_mapping.get(prediction, 'Unknown')
        st.success(f"Hasil Prediksi: {predicted_label}")
        probabilities = model.predict_proba(df_scaled)[0]
        confidence = probabilities[prediction] * 100
        st.success(f"Probabilitas Hasil Prediksi: {predicted_label} (Confidence: {confidence:.2f}%)")
    except Exception as e:
        st.error(f"Gagal melakukan prediksi: {e}")
