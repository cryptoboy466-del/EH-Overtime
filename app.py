import streamlit as st
import pandas as pd

# Application Configuration
st.set_page_config(page_title="EH Employee Overtime Sedra/Roshn", layout="centered", page_icon="🕒")

# ---------- Custom CSS ----------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #eaf2f8 0%, #f4f6f7 100%);
}

.header-box {
    background: linear-gradient(90deg, #1a5276, #2874a6);
    padding: 25px 20px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 4px 14px rgba(0,0,0,0.15);
    margin-bottom: 25px;
}
.header-box h1 {
    color: #ffffff;
    font-size: 1.8rem;
    margin: 0;
    font-weight: 700;
}
.header-box p {
    color: #d6eaf8;
    margin-top: 6px;
    font-size: 0.95rem;
}

div[data-testid="stForm"] {
    background: #ffffff;
    padding: 20px 25px;
    border-radius: 14px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.08);
}

.stTextInput input {
    border-radius: 10px !important;
    border: 1.5px solid #aed6f1 !important;
    padding: 10px !important;
}

.stFormSubmitButton button {
    background: linear-gradient(90deg, #1a5276, #2874a6) !important;
    color: white !important;
    border-radius: 10px !important;
    border: none !important;
    font-weight: 600 !important;
    padding: 8px 25px !important;
    width: 100%;
    transition: 0.2s ease-in-out;
}
.stFormSubmitButton button:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 12px rgba(26,82,118,0.35);
}

.card {
    background: #ffffff;
    border-radius: 16px;
    padding: 22px 28px;
    margin-top: 22px;
    box-shadow: 0 4px 16px rgba(0,0,0,0.10);
    border-top: 5px solid #1a5276;
    animation: fadeIn 0.4s ease-in-out;
}
@keyframes fadeIn {
    from {opacity: 0; transform: translateY(8px);}
    to {opacity: 1; transform: translateY(0);}
}
.card h3 {
    color: #1a5276;
    margin-bottom: 18px;
    font-weight: 700;
    display: flex;
    align-items: center;
    gap: 8px;
}
.row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 4px;
    border-bottom: 1px solid #eef1f2;
}
.row:last-child { border-bottom: none; }
.label {
    font-weight: 600;
    color: #566573;
    font-size: 0.92rem;
}
.value {
    color: #17202a;
    font-weight: 600;
    font-size: 0.95rem;
}
.value.ot {
    color: #117a65;
    background: #eafaf1;
    padding: 3px 12px;
    border-radius: 20px;
}
.value.absent {
    color: #c0392b;
    background: #fdedec;
    padding: 3px 12px;
    border-radius: 20px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="header-box">
    <h1>🕒 EH Employee Overtime — Sedra / Roshn</h1>
    <p>Enter your File Number to check your overtime & absence summary</p>
</div>
""", unsafe_allow_html=True)

# The exact case-sensitive sheet name from your Excel file
EXCEL_FILE = "data.xlsx"
SHEET_NAME = "EH Staff"

# ---------- Column positions (0-indexed), matched to your actual sheet ----------
COL_FILE_NO  = 1   # B  - FILE #
COL_NAME     = 2   # C  - EMPLOYEE NAME
COL_POSITION = 3   # D  - POSITION
COL_COMPANY  = 4   # E  - COMPANY
COL_OVERTIME = 69  # BR - TOTAL OVERTIME
COL_ABSENT   = 70  # BS - TOTAL ABSENT
COL_REMARKS  = 71  # BT - REMARKS

try:
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME, header=None)

    with st.form(key="search_form"):
        emp_id_input = st.text_input("File Number", placeholder="e.g., 220")
        submit_button = st.form_submit_button(label="🔍 Submit")

    if submit_button:
        search_val = emp_id_input.strip()
        if search_val == "":
            st.warning("Please enter a valid File Number.")
        else:
            matched_rows = df[df[COL_FILE_NO].astype(str).str.strip() == search_val]

            if not matched_rows.empty:
                row = matched_rows.iloc[0]

                def safe(val, default="-"):
                    return default if pd.isna(val) or str(val).strip().lower() == "nan" else str(val).strip()

                file_no  = safe(row[COL_FILE_NO])
                name     = safe(row[COL_NAME])
                position = safe(row[COL_POSITION])
                company  = safe(row[COL_COMPANY])
                overtime = safe(row[COL_OVERTIME], "0")
                absent   = safe(row[COL_ABSENT], "0")
                remarks  = safe(row[COL_REMARKS], "")

                remarks_html = (
                    f'<div class="row"><span class="label">📝 Remarks</span>'
                    f'<span class="value">{remarks}</span></div>'
                    if remarks else ""
                )

                st.markdown(f"""
                <div class="card">
                    <h3>✅ Record Found</h3>
                    <div class="row"><span class="label">🆔 File #</span><span class="value">{file_no}</span></div>
                    <div class="row"><span class="label">👤 Name</span><span class="value">{name}</span></div>
                    <div class="row"><span class="label">🛠️ Position</span><span class="value">{position}</span></div>
                    <div class="row"><span class="label">🏢 Company</span><span class="value">{company}</span></div>
                    <div class="row"><span class="label">⏱️ Total Overtime</span><span class="value ot">{overtime}</span></div>
                    <div class="row"><span class="label">🚫 Total Absent</span><span class="value absent">{absent}</span></div>
                    {remarks_html}
                </div>
                """, unsafe_allow_html=True)
            else:
                st.error(f"File Number '{search_val}' not found in '{SHEET_NAME}' sheet. Please verify.")

except FileNotFoundError:
    st.error(f"Error: Excel file '{EXCEL_FILE}' not found in the directory.")
except ValueError as ve:
    st.error(f"Sheet Error: {ve}")
except Exception as e:
    st.error(f"An error occurred: {e}")