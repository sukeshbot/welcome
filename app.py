from flask import Flask, request, jsonify
import pandas as pd
import re

app = Flask(__name__)

def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None

def is_valid_phone(phone):
    regex = r'^\+?[0-9]{10,15}$'
    return re.match(regex, phone) is not None

@app.route('/upload_excel', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    try:
        df = pd.read_excel(file)
        required_columns = ['first name', 'last name', 'email', 'phone']
        
        if not all(col in df.columns for col in required_columns):
            return jsonify({"error": f"Missing one or more required columns: {', '.join(required_columns)}"}), 400

        validation_issues = []

        for index, row in df.iterrows():
            issues = []
            if not is_valid_email(row['email']):
                issues.append('Invalid email format')
            if not is_valid_phone(str(row['phone'])):
                issues.append('Invalid phone number format')

            if issues:
                validation_issues.append({
                    "row": index,
                    "issues": issues,
                    "data": row.to_dict()
                })

        if validation_issues:
            return jsonify({"validation_issues": validation_issues}), 400
        
        first_names = df['first name'].tolist()
        return jsonify({"message": "All formats are correct","first_names": first_names}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
