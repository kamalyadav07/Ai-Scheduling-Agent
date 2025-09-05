# src/agent.py

import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from typing import TypedDict, List
from langgraph.graph import StateGraph, END
import pandas as pd
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Agent State Definition ---
class AgentState(TypedDict):
    patient_name: str
    patient_id: int
    patient_dob: str
    patient_status: str
    appointment_duration: int
    available_slots: List[str]
    selected_slot: str
    insurance_carrier: str
    member_id: str
    group_number: str
    confirmation_status: str

# --- Node Functions ---

def greet_patient(state: AgentState):
    print("🤖 Hello! I'm the AI scheduling agent for the MediCare Allergy & Wellness Center.")
    print("🤖 I can help you book an appointment. First, could I get your full name and date of birth (MM/DD/YYYY)?")

    # Simulate user input for demo
    name_input = "Peter Jones"
    dob_input = "02/15/2001"
    print(f"👤 Name: {name_input}")
    print(f"👤 DOB: {dob_input}")

    state['patient_name'] = name_input
    state['patient_dob'] = dob_input
    return state


def lookup_patient(state: AgentState):
    print("🤖 Checking our records for you...")
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '..', 'data', 'patients.csv')
    patients_df = pd.read_csv(file_path)

    try:
        input_dob_obj = datetime.strptime(state['patient_dob'], '%m/%d/%Y')
        dob_to_check = input_dob_obj.strftime('%Y-%m-%d')
    except ValueError:
        print("🤖 Error: Invalid date format provided.")
        state['patient_status'] = "lookup_failed"
        return state

    match = patients_df[
        (patients_df['FirstName'] + ' ' + patients_df['LastName'] == state['patient_name']) &
        (patients_df['DOB'] == dob_to_check)
    ]

    if not match.empty:
        patient_data = match.iloc[0]
        state['patient_id'] = int(patient_data['PatientID'])
        if patient_data['IsReturning']:
            print("🤖 Welcome back! I see you are a returning patient.")
            state['patient_status'] = "returning"
            state['appointment_duration'] = 30
        else:
            print("🤖 It looks like you're a new patient. Welcome! We'll need a bit more information to get you set up.")
            state['patient_status'] = "new"
            state['appointment_duration'] = 60
    else:
        print("🤖 It looks like you're a new patient. Welcome! We'll need a bit more information to get you set up.")
        state['patient_status'] = "new"
        state['appointment_duration'] = 60
        state['patient_id'] = -1

    return state


def show_availability(state: AgentState):
    duration = state['appointment_duration']
    print(f"🤖 You need a {duration}-minute appointment. Let me check the doctor's calendar...")

    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, '..', 'data', 'doctor_schedules.xlsx')
    schedule_df = pd.read_excel(file_path)

    available_slots_df = schedule_df[
        (schedule_df['Status'] == 'Available') &
        (schedule_df['Duration (min)'] == duration)
    ].copy()

    if available_slots_df.empty:
        print(f"🤖 I'm sorry, but there are no available {duration}-minute slots.")
        state['available_slots'] = []
        state['selected_slot'] = None
        return state

    # Parse and clean safely
    available_slots_df['Date'] = pd.to_datetime(
        available_slots_df['Date'], errors='coerce'
    ).dt.date
    available_slots_df['StartTime'] = pd.to_datetime(
        available_slots_df['StartTime'], errors='coerce'
    ).dt.time

    # Drop invalid rows (NaT)
    available_slots_df = available_slots_df.dropna(subset=["Date", "StartTime"])

    slots = []
    for _, row in available_slots_df.iterrows():
        if pd.notna(row["Date"]) and pd.notna(row["StartTime"]):
            date_str = row["Date"].strftime("%Y-%m-%d")
            time_str = row["StartTime"].strftime("%H:%M")
            slots.append(f"{date_str} at {time_str}")

    if not slots:
        print("🤖 No valid slots found after cleaning.")
        state['available_slots'] = []
        state['selected_slot'] = None
        return state

    print("🤖 Here are the available slots I found:")
    for i, slot in enumerate(slots, 1):
        print(f"  {i}. {slot}")

    selected_slot_str = slots[0]  # Simulate patient picking the first slot
    print(f"👤 I'd like the slot on {selected_slot_str}, please.")

    state['available_slots'] = slots
    state['selected_slot'] = selected_slot_str
    return state


def collect_insurance(state: AgentState):
    print("🤖 As a new patient, I need to collect your insurance information.")
    print("🤖 Could you please provide your insurance carrier, member ID, and group number?")

    carrier = "Cigna"
    member_id = "CIN98765"
    group_num = "GRP999"
    print(f"👤 Carrier: {carrier}, Member ID: {member_id}, Group #: {group_num}")

    state['insurance_carrier'] = carrier
    state['member_id'] = member_id
    state['group_number'] = group_num
    return state


def send_confirmation_email(state: AgentState):
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    if not all([sender_email, sender_password, receiver_email]):
        print("🛑 Email credentials not found in .env file. Skipping email.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = "Your Upcoming Appointment at MediCare Allergy & Wellness Center"

    body = f"Dear {state['patient_name']},\n\nThis email confirms your appointment for {state['selected_slot']}.\n\nPlease complete the attached intake form before your visit.\n\nThank you,\nMediCare Allergy & Wellness Center"
    msg.attach(MIMEText(body, 'plain'))

    script_dir = os.path.dirname(__file__)
    attachment_path = os.path.join(script_dir, '..', 'New Patient Intake Form.pdf')

    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(attachment.read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', f"attachment; filename= New Patient Intake Form.pdf")
        msg.attach(part)
    except FileNotFoundError:
        print(f"🛑 Attachment not found at {attachment_path}. Skipping attachment.")

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, receiver_email, text)
        server.quit()
        print("✉️ Confirmation email with intake form sent successfully!")
    except Exception as e:
        print(f"🛑 Failed to send email: {e}")


def confirm_booking(state: AgentState):
    print("🤖 Great! Let's confirm the details of your appointment:")
    print(f"  - Patient: {state['patient_name']}")
    print(f"  - Appointment: {state['selected_slot']}")
    if state.get('insurance_carrier'):
        print(f"  - Insurance: {state['insurance_carrier']} (ID: {state['member_id']})")

    script_dir = os.path.dirname(__file__)
    schedule_path = os.path.join(script_dir, '..', 'data', 'doctor_schedules.xlsx')
    schedule_df = pd.read_excel(schedule_path)

    # Fix parsing (robust to datetime or plain time)
    slot_date_str, slot_time_str = state['selected_slot'].split(' at ')
    slot_date = datetime.strptime(slot_date_str, '%Y-%m-%d').date()
    slot_time = datetime.strptime(slot_time_str, '%H:%M').time()

    schedule_df.loc[
        (pd.to_datetime(schedule_df['Date'], errors='coerce').dt.date == slot_date) &
        (pd.to_datetime(schedule_df['StartTime'], errors='coerce').dt.time == slot_time),
        ['Status', 'BookedByPatientID']
    ] = ['Booked', state['patient_id']]

    schedule_df.to_excel(schedule_path, index=False)
    print("🗓️ Calendar updated.")

    report_path = os.path.join(script_dir, '..', 'data', 'admin_report.xlsx')
    report_data = {
        'PatientID': [state.get('patient_id')],
        'PatientName': [state.get('patient_name')],
        'AppointmentTime': [state.get('selected_slot')],
        'Status': ['Confirmed']
    }
    new_report_df = pd.DataFrame(report_data)

    try:
        existing_report_df = pd.read_excel(report_path)
        updated_report_df = pd.concat([existing_report_df, new_report_df], ignore_index=True)
    except FileNotFoundError:
        updated_report_df = new_report_df

    updated_report_df.to_excel(report_path, index=False)
    print("📊 Admin report generated.")

    print("\n✅ Your appointment is confirmed!")
    state['confirmation_status'] = 'confirmed'

    send_confirmation_email(state)
    return state

# --- Conditional Edges ---
def decide_next_step_after_lookup(state: AgentState):
    if state['patient_status'] in ["returning", "new"]:
        return "show_availability"
    else:
        return END

def decide_next_step_after_availability(state: AgentState):
    if not state.get('selected_slot'):
        return END
    if state['patient_status'] == 'new':
        return "collect_insurance"
    else:
        return "confirm_booking"

# --- Graph Definition ---
workflow = StateGraph(AgentState)
workflow.add_node("greet_patient", greet_patient)
workflow.add_node("lookup_patient", lookup_patient)
workflow.add_node("show_availability", show_availability)
workflow.add_node("collect_insurance", collect_insurance)
workflow.add_node("confirm_booking", confirm_booking)
workflow.set_entry_point("greet_patient")
workflow.add_edge("greet_patient", "lookup_patient")
workflow.add_edge("collect_insurance", "confirm_booking")
workflow.add_edge("confirm_booking", END)
workflow.add_conditional_edges(
    "lookup_patient",
    decide_next_step_after_lookup,
    {"show_availability": "show_availability", END: END}
)
workflow.add_conditional_edges(
    "show_availability",
    decide_next_step_after_availability,
    {"collect_insurance": "collect_insurance", "confirm_booking": "confirm_booking", END: END}
)
app = workflow.compile()

if __name__ == "__main__":
    inputs = {}
    for event in app.stream(inputs):
        for key, value in event.items():
            print(f"--- Event: {key} ---")
            print(value)
            print("\n")
