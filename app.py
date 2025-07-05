from flask import Flask, render_template, request, send_file
import pandas as pd
import requests
from io import BytesIO
import re
import os

app = Flask(__name__)

# Google Sheet URL (download as .xlsx)
GOOGLE_SHEETS_URL = "https://docs.google.com/spreadsheets/d/1SGlbyY0QXOT0HxOel4KKnRyI6bTgp73B/export?format=xlsx"

# Caste/category column names
category_columns = [
    "OC BOYS", "OC GIRLS",
    "BC_A BOYS", "BC_A GIRLS",
    "BC_B BOYS", "BC_B GIRLS",
    "BC_C BOYS", "BC_C GIRLS",
    "BC_D BOYS", "BC_D GIRLS",
    "BC_E BOYS", "BC_E GIRLS",
    "SC BOYS", "SC GIRLS",
    "ST BOYS", "ST GIRLS",
    "EWS GEN OU", "EWS GIRLS OU"
]

# Branch mapping dictionary
branch_map = {
    'AGR': 'Agricultural Engineering', 'AI': 'Artificial Intelligence',
    'AID': 'AI & Data Science', 'AIM': 'AI & Machine Learning',
    'ANE': 'Automobile Engineering', 'AUT': 'Automation',
    'BIO': 'Biotechnology', 'BME': 'Biomedical Engineering',
    'BSE': 'Biological Systems Engg', 'CHE': 'Chemical Engineering',
    'CIC': 'Computer and Info. Science', 'CIV': 'Civil Engineering',
    'CME': 'Computer Engineering', 'CSA': 'CS and Applications',
    'CSB': 'CS and Business Systems', 'CSC': 'CS and Cyber Security',
    'CSD': 'CS and Design', 'CSE': 'Computer Science Engineering',
    'CSG': 'CS and Game Design', 'CSI': 'CS and IT',
    'CSM': 'CS and ML', 'CSN': 'CS and Networks',
    'CSO': 'CS and Optimization', 'CSW': 'CS and Web Tech',
    'DRG': 'Drug Technology', 'DTD': 'Design Tech',
    'ECE': 'Electronics & Comm Engg', 'ECI': 'Electronics & Computer Engg',
    'ECM': 'Electronics & Comm. Mgmt', 'EEE': 'Electrical & Electronics Engg',
    'EIE': 'Electronics & Instrumentation', 'ETM': 'Embedded Tech and Mgmt',
    'EVL': 'Environmental Engg', 'FDT': 'Fashion Design Tech',
    'GEO': 'Geoinformatics', 'INF': 'Information Technology',
    'MCT': 'Mechatronics', 'MEC': 'Mechanical Engineering',
    'MET': 'Metallurgy', 'MIN': 'Mining Engineering',
    'MMS': 'Materials Science', 'MMT': 'Manufacturing Mgmt',
    'MTE': 'Medical Technology', 'PHE': 'Pharmaceutical Engg',
    'PLG': 'Plastic Technology', 'TEX': 'Textile Engineering'
}

def fetch_data():
    """Fetch and clean data from Google Sheets."""
    try:
        response = requests.get(GOOGLE_SHEETS_URL)
        response.raise_for_status()
        file_data = BytesIO(response.content)
        df = pd.read_excel(file_data, engine='openpyxl')

        # Clean column names: remove \r, replace \n with space, compress multiple spaces, strip ends
        df.columns = df.columns.str.replace(r'\r', '', regex=False)\
                               .str.replace(r'\n', ' ', regex=False)\
                               .str.replace(r'\s+', ' ', regex=True)\
                               .str.strip()

        print("🧾 Cleaned Columns:")
        for col in df.columns:
            print(f"'{col}'")

        return df
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    df = fetch_data()
    if df is None:
        return "⚠️ Error loading data from Google Sheets"

    branches = sorted(df['Branch Code'].dropna().unique())

    if request.method == 'POST':
        try:
            category = request.form.get('category')
            rank_min = int(request.form.get('rank_min'))
            rank_max = int(request.form.get('rank_max'))
            selected_branches = request.form.getlist('branches')

            if not category or not selected_branches:
                raise ValueError("All fields are required.")

            if category not in df.columns:
                raise ValueError(f"'{category}' column not found in the data. Please check again.")

            # Filter DataFrame
            filtered_df = df[
                (df[category] >= rank_min) &
                (df[category] <= rank_max) &
                (df['Branch Code'].isin(selected_branches))
            ]

            # Add branch names
            filtered_df['Branch Name'] = filtered_df['Branch Code'].map(branch_map)

            # Final columns
            result_df = filtered_df[[
                "Inst Code", "Institute Name", category, "Branch Code", "Branch Name"
            ]].sort_values(by=category)

            result_html = result_df.to_html(
                index=False,
                classes='table table-striped table-hover table-bordered',
                justify='center'
            )

            return render_template(
                'index.html',
                categories=category_columns,
                branches=branches,
                result=result_html,
                branch_map=branch_map
            )

        except ValueError as ve:
            return render_template(
                'index.html',
                categories=category_columns,
                branches=branches,
                error=str(ve),
                result=None,
                branch_map=branch_map
            )

    return render_template(
        'index.html',
        categories=category_columns,
        branches=branches,
        result=None,
        branch_map=branch_map
    )

@app.route('/download', methods=['POST'])
def download():
    """Download filtered table as Excel."""
    filtered_data = request.form.get('data')
    if not filtered_data:
        return "⚠️ No data to download."

    df = pd.read_html(filtered_data)[0]

    output = BytesIO()
    df.to_excel(output, index=False)
    output.seek(0)

    return send_file(
        output,
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        as_attachment=True,
        download_name='filtered_results.xlsx'
    )

if __name__ == '__main__':
    app.run(debug=True)

