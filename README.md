

```markdown
# 🎓 College Branch Rank Filter Web App

This is a Flask-based web application that allows users to filter engineering college branches based on entrance exam rank ranges and reservation categories (OC, BC, SC, ST, EWS, etc.) using data from a Google Sheet.

## 📌 Features

- Fetches data dynamically from a Google Sheet (`.xlsx` format)
- Filters colleges based on:
  - Category (OC, BC, SC, ST, EWS, etc.)
  - Rank range (min and max)
  - Selected branches (CSE, ECE, etc.)
- Displays filtered results in a sortable HTML table
- Allows downloading the filtered data as an Excel file

## 🛠️ Technologies Used

- Python 3
- Flask
- Pandas
- HTML (with Bootstrap classes for tables)
- Google Sheets (as data source)

## 📂 Project Structure

```
project/
│
├── app.py               # Main Flask app
├── templates/
│   └── index.html       # HTML template for homepage
├── static/              # (Optional) CSS/JS if needed
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/college-rank-filter.git
cd college-rank-filter
```

### 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

**`requirements.txt` might look like:**

```
Flask
pandas
requests
openpyxl
```

### 4. Run the App

```bash
python app.py
```

Visit `http://127.0.0.1:5000/` in your browser.

---

## 📥 Google Sheets Data Format

Ensure your Google Sheet:
- Is publicly accessible or shared with "Anyone with the link can view"
- Has a structure like:

| Inst Code | Institute Name | Branch Code | OC BOYS | OC GIRLS | BC_A BOYS | ... |
|-----------|----------------|-------------|---------|----------|-----------|-----|

Update the `GOOGLE_SHEETS_URL` in `app.py` accordingly.

---

## ⚠️ Notes

- Make sure column names in your Google Sheet match the names listed in `category_columns`.
- The app maps branch codes like `CSE`, `ECE`, etc., to full names using `branch_map`.

---

## 📄 License

This project is open-source and free to use under the MIT License.

---

## 🙋‍♂️ Contribution

Feel free to open issues or pull requests. Suggestions and improvements are welcome!
```

---

Let me know if you want the `index.html` template created too.
