import streamlit as st
import pandas as pd
import random
from datetime import datetime
from fpdf import FPDF

# Title
st.set_page_config(page_title="ShiftEase", layout="wide")
st.title("📋 ShiftEase – Daily Staff Planner (07:30 – 20:00)")

st.markdown("Assign roles like 1:1s, general obs, breaks, and smoke breaks fairly across your team.")

# Number of staff
num_staff = st.number_input("👥 Number of Staff on Shift", min_value=1, max_value=20, value=5)

# Staff names input
staff_names = []
for i in range(num_staff):
    name = st.text_input(f"Staff {i+1} Name", key=f"name_{i}")
    staff_names.append(name)

st.divider()

# Roles
roles = ["1:1", "General Obs", "Break Cover", "Smoke Break", "Float"]
num_roles = len(roles)

if st.button("🧠 Generate Shift Plan"):
    if any(name.strip() == "" for name in staff_names):
        st.warning("Please fill in all staff names.")
    else:
        assigned_roles = random.sample(roles * (num_staff // num_roles + 1), num_staff)
        shift_plan = pd.DataFrame({
            "Staff Name": staff_names,
            "Assigned Role": assigned_roles[:num_staff]
        })

        st.success("✅ Shift plan generated!")
        st.dataframe(shift_plan, use_container_width=True)

        # Download as CSV
        csv = shift_plan.to_csv(index=False).encode('utf-8')
        st.download_button("⬇️ Download CSV", data=csv, file_name='shift_plan.csv', mime='text/csv')

        # Download as PDF
        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt="ShiftEase – Daily Staff Plan", ln=True, align='C')
        pdf.cell(200, 10, txt=f"Generated on {datetime.now().strftime('%Y-%m-%d %H:%M')}", ln=True, align='C')
        pdf.ln(10)
        for index, row in shift_plan.iterrows():
            pdf.cell(200, 10, txt=f"{row['Staff Name']} – {row['Assigned Role']}", ln=True)
        pdf_path = "/tmp/shift_plan.pdf"
        pdf.output(pdf_path)

        with open(pdf_path, "rb") as f:
            st.download_button("⬇️ Download PDF", data=f, file_name="shift_plan.pdf", mime="application/pdf")
