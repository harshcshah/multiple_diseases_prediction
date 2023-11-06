import streamlit as st
import pickle
import smtplib
from streamlit_option_menu import option_menu

# Load the saved models
diabetes_model = pickle.load(open('diabetes_model.sav', 'rb'))
parkinson_model = pickle.load(open('parkinson_model.sav', 'rb'))
heart_model = pickle.load(open('heart_disease_model.sav', 'rb'))

# Define the function to generate a PDF report
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

    pdf = pdfkit.from_string(html_content, output_path="report.pdf")

    return pdf

# Define the function to send an email with the PDF report attached
def send_report_email(user_email, pdf_report):

    msg = smtplib.SMTP("smtp.gmail.com", 587)
    msg.starttls()
    msg.login("your_email@example.com", "your_password")

    msg["From"] = "your_email@example.com"
    msg["To"] = user_email
    msg["Subject"] = "Multiple Disease Prediction Report"

    with open("report.pdf", "rb") as f:
        msg.add_attachment(f.read(), filename="report.pdf")

    msg.sendmail("your_email@example.com", user_email, msg.as_string())

# Define the main function
def main():

    # Create a sidebar with navigation options
    selected = option_menu('Multiple Disease Prediction System',
                          
                          ['Diabetes Prediction',
                           'Heart Disease Prediction',
                           'Parkinsons Prediction'],
                          icons=['activity','heart','person'],
                          default_index=0)

    # Get the user's data
    user_data = {}
    user_data["name"] = st.sidebar.text_input("Name")
    user_data["age"] = st.sidebar.text_input("Age")
    user_data["sex"] = st.sidebar.text_input("Sex")

    # Predict the user's diagnosis
    if selected == 'Diabetes Prediction':
        diagnosis = diabetes_model.predict_proba([user_data])[0, 1]
    elif selected == 'Heart Disease Prediction':
        diagnosis = heart_model.predict_proba([user_data])[0, 1]
    elif selected == 'Parkinsons Prediction':
        diagnosis = parkinson_model.predict_proba([user_data])[0, 1]

    # Display the user's diagnosis
    st.title('Your diagnosis is: {}'.format(diagnosis))

    # Add a button to generate the report
    if st.sidebar.button("Generate Report"):
        # Generate the PDF report
        pdf_report = generate_report(user_data, diagnosis)

        # Send the report email
        send_report_email(user_email, pdf_report)

# Run the main function
if __name__ == '__main__':
    main()
