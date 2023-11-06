import pickle
import streamlit as st
import smtplib
from streamlit_option_menu import option_menu
from pdfkit import from_string


# Function to generate a PDF report from the given user data and diagnosis.
def generate_report(user_data, diagnosis):
    html_content = """
    <h1>Multiple Disease Prediction Report</h1>
    <p>
    User data:
    <ul>
        <li>Name: {}</li>
        <li>Age: {}</li>
        <li>Sex: {}</li>
    </ul>
    </p>
    <p>
    Diagnosis: {}
    </p>
    """.format(user_data["name"], user_data["age"], user_data["sex"], diagnosis)

    pdf = from_string(html_content, output_path="report.pdf")

    return pdf


# Function to send an email with the given PDF report to the given user email address.
def send_report_email(user_email, pdf_report):
    msg = MIMEMultipart()
    msg["From"] = "your_gmail_address"
    msg["To"] = user_email
    msg["Subject"] = "Multiple Disease Prediction Report"

    # Add the PDF report as an attachment
    attachment = MIMEText(pdf_report, "application/pdf")
    attachment.add_header("Content-Disposition", "attachment", filename="report.pdf")
    msg.attach(attachment)

    # Send the email
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login("your_gmail_address", "your_gmail_password")
    server.sendmail("your_gmail_address", user_email, msg.as_string())
    server.quit()


# Loading the saved models
diabetes_model = pickle.load(open(
    'C:\\Users\\Harsh shah\\ML Projects\\Course Recomendation System\\Multiple Disease Prediction System\\saved models\\diabetes_model.sav',
    'rb'), encoding='latin1')
parkinson_model = pickle.load(open(
    'C:\\Users\\Harsh shah\\ML Projects\\Course Recomendation System\\Multiple Disease Prediction System\\saved models\\parkinsons_model.sav',
    'rb'), encoding='latin1')
heart_model = pickle.load(open(
    'C:\\Users\\Harsh shah\\ML Projects\\Course Recomendation System\\Multiple Disease Prediction System\\saved models\\heart_disease_model.sav',
    'rb'), encoding='latin1')

# Sidebar for navigation
with st.sidebar:
    selected = option_menu('Multiple Disease Prediction System',

                           ['Diabetes Prediction',
                            'Heart Disease Prediction',
                            'Parkinsons Prediction'],
                           icons=['activity', 'heart', 'person'],
                           default_index=0)

    # Add a button to the sidebar to generate the report.
    if st.sidebar.button("Generate Report"):
        # Get the user's data.
        user_data = {}
        user_data["name"] = st.sidebar.text_input("Name")
        user_data["age"] = st.sidebar.text_input("Age")
        user_data["sex"] = st.sidebar.text_input("Sex")

        # Get the user's diagnosis.
        diagnosis = st.sidebar.text_input("Diagnosis")

        # Generate the PDF report.
        pdf_report = generate_report(user_data, diagnosis)

        # Send the report email.
        send_report_email(user_email, pdf_report)

# Diabetes Prediction Page
if (selected == 'Diabetes Prediction'):
    # Page title
    st.title('Diabetes Prediction using ML')

    # Getting the input data from the user
    col1, col2, col3 = st.columns(3)

    with col1:
        Pregnancies = st.text_input('Number of Pregnancies')

    with col2:
        Glucose = st.text_input('Glucose Level')
