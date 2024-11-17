from flask import Flask, render_template, request, jsonify
import os
import pandas as pd

app = Flask(__name__, template_folder='docs', static_folder='static')


csv_directory = "LeetCode-Questions-CompanyWise-master"

file_names = [f for f in os.listdir(csv_directory) if f.endswith('.csv')]
company_data = {}

for f in file_names:
    company_name = f.split('_')[0]
    timeframe = f.split('_')[1].replace('.csv', '')
    if company_name not in company_data:
        company_data[company_name] = []
    company_data[company_name].append(timeframe)

@app.route('/')
def index():
    """Render the homepage with a dropdown."""
    return render_template('index.html', companies=list(company_data.keys()))

@app.route('/get_timeframes', methods=['POST'])
def get_timeframes():
    """Return available timeframes for the selected company."""
    company_name = request.json.get('company')
    if company_name not in company_data:
        return jsonify({"error": "Company not found"}), 404
    return jsonify({"timeframes": company_data[company_name]})

@app.route('/get_company_data', methods=['POST'])
def get_company_data():
    """Return the data for the selected company and timeframe."""
    company_name = request.form.get('company')
    timeframe = request.form.get('timeframe')
    if not company_name or not timeframe:
        return "Invalid input.", 400
    
    file_name = f"{company_name}_{timeframe}.csv"
    file_path = os.path.join(csv_directory, file_name)
    
    if not os.path.exists(file_path):
        return f"No data found for {company_name} ({timeframe}).", 404

    df = pd.read_csv(file_path)

    df.columns = ['ID', 'Title', 'Acceptance', 'Difficulty', 'Frequency', 'Leetcode Question Link']

    df['Link'] = df['Leetcode Question Link'].apply(lambda url: 
        f'<a href="{url}" target="_blank"><img src="https://leetcode.com/favicon.ico" alt="Leetcode Icon" style="width: 20px; height: 20px;"></a>'
    )

    table_html = df.to_html(classes='table table-striped table-bordered table-dark', index=False, escape=False)

    return f'<div class="table-responsive">{table_html}</div>'

if __name__ == '__main__':
    app.run(debug=True)
