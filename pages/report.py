import io
from datetime import datetime
import json
import streamlit as st
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from backend.crud import list_workout_logs, list_meal_logs


if "user" not in st.session_state or not st.session_state.user:
    st.warning("Please log in to access this page.")
    st.stop()

st.title("Download Wellness Report")
st.caption("Generate a snapshot of your recent activity.")

u = st.session_state.user

def generate_pdf(user: dict) -> bytes:
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter
    y = height - 50
    c.setFont("Helvetica-Bold", 16)
    c.drawString(50, y, "Wellness Report")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(50, y, f"Name: {user.get('name','-')}  Email: {user.get('email','-')}")
    y -= 15
    c.drawString(50, y, f"Generated: {datetime.utcnow().isoformat()} UTC")
    y -= 30
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Recent Meals")
    y -= 15
    c.setFont("Helvetica", 10)
    for m in list_meal_logs(user["id"], limit=10):
        line = f"- {m['date']} | {m.get('description') or ''} | kcal: {m.get('calories_est') or '-'}"
        c.drawString(50, y, line[:100])
        y -= 12
        if y < 80:
            c.showPage(); y = height - 50
    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(50, y, "Recent Workouts")
    y -= 15
    c.setFont("Helvetica", 10)
    for w in list_workout_logs(user["id"], limit=10):
        line = f"- {w['date']} | {w['routine']} | kcal: {w.get('calories_burned') or '-'}"
        c.drawString(50, y, line[:100])
        y -= 12
        if y < 80:
            c.showPage(); y = height - 50
    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer.read()


if st.button("Generate PDF"):
    data = generate_pdf(u)
    st.download_button(
        label="Download Report PDF",
        data=data,
        file_name=f"wellness_report_{datetime.utcnow().date().isoformat()}.pdf",
        mime="application/pdf",
    )


