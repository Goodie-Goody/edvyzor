# IMPORT SECTION

import streamlit as st
import pandas as pd
import joblib
import os
import requests
import json
from supabase import create_client, Client
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
import openpyxl

# SUPABASE AUTHENTICATION

# Supabase client setup
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_KEY')

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Supabase URL and Key must be set in environment variables")
else:
    headers = {
        "apikey": SUPABASE_KEY,
        "Authorization": f"Bearer {SUPABASE_KEY}",
        "Content-Type": "application/json"
    }

# SITE INTRODUCTION SECTION

# Streamlit app
st.title('Final Exams Prediction')
st.write("""This tool serves as an early warning system to help students, teachers, parents, and school administrators reduce failure rates in exams. By analyzing historical data and predicting students' performance, it allows educators to identify at-risk students early and intervene with personalized support. It promotes collaborative efforts among all stakeholders to improve outcomes and ensure timely interventions to mitigate potential failures. However, it must be noted that this tool is merely a proof of concept and not based on real data.""")

st.download_button(
    label="Download Data Dictionary", data=open("uploads/data_dictionary.txt").read(), file_name="data_dictionary.txt"
    )

st.download_button(
    label="Download Sample Data",
        data=open("uploads/example_table.xlsx", "rb").read(),
        file_name="updated_data.xlsx"
    )

    
# MODEL PREDICTIONS WORKFLOW AND OUTPUT

# Load the saved pipeline
pipeline = joblib.load('saved_models/pipeline_lr')

# Upload and process Excel file
uploaded_file = st.file_uploader("Choose an Excel file", type="xlsx")
if uploaded_file is not None:
    try:
        df = pd.read_excel(uploaded_file)

        # Process data
        categorical_features = [col for col in df.select_dtypes(include=['object']).columns if col not in ['student_id']]
        numerical_features = df.select_dtypes(exclude=['object']).columns.tolist()

        preprocessor = ColumnTransformer(
            transformers=[
                ('onehot', OneHotEncoder(handle_unknown='ignore'), categorical_features),
                ('scaler', StandardScaler(), numerical_features)
            ]
        )

        pipeline_lr = Pipeline(steps=[
            ('preprocessor', preprocessor),
            ('classifier', LogisticRegression(C=0.1, solver='lbfgs'))
        ])

        # Make predictions
        predictions = pipeline.predict(df)
        probabilities = pipeline.predict_proba(df)

        # Add predictions and confidence to the DataFrame
        df['predictions'] = predictions
        df['confidence'] = [f'{max(prob)*100:.2f}%' for prob in probabilities]  # Confidence in percentage

        # Define the expected columns
        expected_columns = [
            'student_id', 'school', 'sex', 'age', 'address', 'famsize', 'pstatus', 'medu', 'fedu', 'mjob', 'fjob', 'reason', 'guardian', 
            'traveltime', 'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 
            'famrel', 'freetime', 'goout', 'health', 'mat_absences', 'mat_ss2_3rd', 'mat_ss3_1st', 'mat_ss3_2nd', 'eng_absences', 'eng_ss2_3rd', 
            'eng_ss3_1st', 'eng_ss3_2nd', 'csubj1_ss2_3rd', 'csubj1_ss3_1st', 'csubj1_ss3_2nd', 'csubj2_ss2_3rd', 'csubj2_ss3_1st', 'csubj2_ss3_2nd', 
            'csubj3_ss2_3rd', 'csubj3_ss3_1st', 'csubj3_ss3_2nd', 'mat_average', 'eng_average', 'csubj1_average', 'csubj2_average', 'csubj3_average', 
            'overall_average', 'grade', 'waec_grade', 'csubj1_absences', 'csubj2_absences', 'csubj3_absences', 'predictions', 'confidence'
        ]

        # Validate columns for actual results
        missing_results_columns = [col for col in expected_columns if col not in df.columns]
        if missing_results_columns:
            st.error(f"The processed data is missing columns: {', '.join(missing_results_columns)}")
        else:
            st.write(df)
        
            # Assign to upload_df for readability purposes
            upload_df = df.drop(columns=['student_id'])

            # Define the function to upload the data via the Supabase URL
            def post_to_supabase(data):
                url = f"{SUPABASE_URL}/rest/v1/model_predictions"
                response = requests.post(url, headers=headers, data=json.dumps(data))
                return response
            
            # Upload data to Supabase
            if st.button('Upload to Supabase'):
                data = upload_df.to_dict('records')
                try:
                    response = post_to_supabase(data)
                    if response.status_code == 201:
                        st.success("Data successfully uploaded to Supabase")
                        if response.content:
                            st.write(response.json())
                    else:
                        st.error(f"Failed to upload to Supabase: {response.status_code}")
                        if response.content:
                            st.write(response.json())
                except Exception as e:
                    st.error(f"Failed to upload to Supabase: {str(e)}")
                    
                # A button to download the output on the client end
                st.download_button(
                    label="Download predictions as CSV",
                    data=df.to_csv(index=False).encode('utf-8'),
                    file_name='predictions.csv',
                    mime='text/csv'
                )
    except ValueError as e:
        st.error(f"Error reading the Excel file: {str(e)}")      


# ACTUAL RESULTS UPLOAD SECTION
# Upload actual results
uploaded_results = st.file_uploader("Upload Actual Results", type="csv")
if uploaded_results is not None:
    try:
        results_df = pd.read_csv(uploaded_results)

        # Define the expected columns
        expected_columns_two = [
            'school', 'sex', 'age', 'address', 'famsize', 'pstatus', 'medu', 'fedu', 'mjob', 'fjob', 'reason', 'guardian', 'traveltime', 
            'studytime', 'failures', 'schoolsup', 'famsup', 'paid', 'activities', 'nursery', 'higher', 'internet', 'romantic', 'famrel', 'freetime', 
            'goout', 'health', 'mat_absences', 'mat_ss2_3rd', 'mat_ss3_1st', 'mat_ss3_2nd', 'eng_absences', 'eng_ss2_3rd', 'eng_ss3_1st', 'eng_ss3_2nd', 
            'csubj1_ss2_3rd', 'csubj1_ss3_1st', 'csubj1_ss3_2nd', 'csubj2_ss2_3rd', 'csubj2_ss3_1st', 'csubj2_ss3_2nd', 'csubj3_ss2_3rd', 'csubj3_ss3_1st', 
            'csubj3_ss3_2nd', 'mat_average', 'eng_average', 'csubj1_average', 'csubj2_average', 'csubj3_average', 'overall_average', 'grade', 
            'waec_grade', 'csubj1_absences', 'csubj2_absences', 'csubj3_absences', 'predictions', 'confidence', 'actual_results'
        ]

        # Validate columns for actual results
        missing_results_columns_two = [col for col in expected_columns_two if col not in results_df.columns]

        if missing_results_columns_two:
            st.error(f"The uploaded file is missing columns: {', '.join(missing_results_columns_two)}")
        else:
            st.write(results_df)

            # Function to define upload of actual results data
            def post_to_supabase_results(data):
                url = f"{SUPABASE_URL}/rest/v1/actual_results"
                response = requests.post(url, headers=headers, data=json.dumps(data))
                if response.status_code == 201:
                    if response.content:
                        return response.json()
                    else:
                        return {"message": "Upload successful but no content returned"}
                else:
                    if response.content:
                        return {'error': response.json()}
                    else:
                        return {'error': {'message': 'Empty response'}}

            # Upload actual results to Supabase
            if st.button('Upload Actual Results to Supabase'):
                results_data = results_df.to_dict('records')
                try:
                    response = post_to_supabase_results(results_data)
                    if 'error' in response:
                        st.error(f"Failed to upload actual results to Supabase: {response['error']['message']}")
                    else:
                        st.success("Uploaded actual results successfully.")
                        st.write(response)
                except Exception as e:
                    st.error(f"Failed to upload actual results to Supabase: {str(e)}")
    except ValueError as e:
        st.error(f"Error reading the CSV file: {str(e)}")