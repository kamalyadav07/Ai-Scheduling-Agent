# ⚕️ Medicare AI Scheduling Agent

This project is an AI-powered conversational agent designed to book and manage appointments for the MediCare Allergy & Wellness Center. It uses a stateful graph built with LangGraph to guide the user through the scheduling process, from initial greeting to final confirmation.

The user interacts with the agent through a simple chat interface powered by Streamlit.

---

## ✨ Features

* **Conversational Interface:** Engages users in a natural conversation to gather information.
* **Patient Recognition:** Differentiates between new and returning patients to customize the booking flow.
* **Dynamic Availability:** Checks a schedule file (`doctor_schedules.xlsx`) to offer real-time appointment slots.
* **Automated Calendar Updates:** Marks a slot as "Booked" in the schedule file upon confirmation.
* **Admin Reporting:** Generates a report (`admin_report.xlsx`) for all confirmed appointments.
* **Email Confirmation:** Sends a confirmation email to the patient with an intake form attached.

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Streamlit:** For building the interactive web UI.
* **LangGraph:** To create the robust, stateful agent logic.
* **Pandas:** For reading from and writing to Excel and CSV files for patient data and schedules.
* **python-dotenv:** To manage environment variables and secrets.

---

## ⚙️ Setup and Installation

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

First, clone the repository to your local machine using git.


git clone [https://github.com/kamalyadav07/Ai-Scheduling-Agent.git](https://github.com/kamalyadav07/Ai-Scheduling-Agent.git)
cd Ai-Scheduling-Agent


# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

# Install Dependencies
# Install all the required Python libraries from the requirements.txt file
pip install -r requirements.txt


🔑 Configuration
The application uses a .env file to manage sensitive information like email credentials for sending confirmations.

Create the .env file: In the root directory of the project, create a new file named .env.

Add your credentials: Copy the following format into your .env file and replace the placeholder values with your actual credentials.

Code snippet

SENDER_EMAIL="your_email@gmail.com"
SENDER_PASSWORD="your_gmail_app_password"
RECEIVER_EMAIL="test_receiver_email@example.com"

Important Security Note: For the SENDER_PASSWORD, you must use a Gmail App Password, not your regular Google account password. You can generate one here: https://myaccount.google.com/apppasswords


▶️ Running the Application
Once the setup and configuration are complete, you can run the Streamlit application.

Make sure your virtual environment is activated.

Run the following command in your terminal:

Bash

streamlit run src/main.py
A new tab will automatically open in your web browser at http://localhost:8501, where you can interact with the scheduling agent.


Of course. Here is a comprehensive README.md file for your project. It includes a description, the technologies used, and detailed step-by-step instructions for setup and execution, so anyone can get your project running.

## How to Use This
In your project's main folder on your computer, create a new file named README.md.

Copy the entire content from the code block below and paste it into that new file.

Save the file and push it to your GitHub repository. It will automatically be displayed on your project's main page.

Markdown

# ⚕️ Medicare AI Scheduling Agent

This project is an AI-powered conversational agent designed to book and manage appointments for the MediCare Allergy & Wellness Center. It uses a stateful graph built with LangGraph to guide the user through the scheduling process, from initial greeting to final confirmation.

The user interacts with the agent through a simple chat interface powered by Streamlit.

---

## ✨ Features

* **Conversational Interface:** Engages users in a natural conversation to gather information.
* **Patient Recognition:** Differentiates between new and returning patients to customize the booking flow.
* **Dynamic Availability:** Checks a schedule file (`doctor_schedules.xlsx`) to offer real-time appointment slots.
* **Automated Calendar Updates:** Marks a slot as "Booked" in the schedule file upon confirmation.
* **Admin Reporting:** Generates a report (`admin_report.xlsx`) for all confirmed appointments.
* **Email Confirmation:** Sends a confirmation email to the patient with an intake form attached.

---

## 🛠️ Tech Stack

* **Python 3.10+**
* **Streamlit:** For building the interactive web UI.
* **LangGraph:** To create the robust, stateful agent logic.
* **Pandas:** For reading from and writing to Excel and CSV files for patient data and schedules.
* **python-dotenv:** To manage environment variables and secrets.

---

## ⚙️ Setup and Installation

Follow these steps to set up the project on your local machine.

### 1. Clone the Repository

First, clone the repository to your local machine using git.


git clone [https://github.com/kamalyadav07/Ai-Scheduling-Agent.git](https://github.com/kamalyadav07/Ai-Scheduling-Agent.git)
cd Ai-Scheduling-Agent
2. Create a Virtual Environment
It's highly recommended to use a virtual environment to keep project dependencies isolated.

Bash

# Create the virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate
3. Install Dependencies
Install all the required Python libraries from the requirements.txt file.

Bash

pip install -r requirements.txt
🔑 Configuration
The application uses a .env file to manage sensitive information like email credentials for sending confirmations.

Create the .env file: In the root directory of the project, create a new file named .env.

Add your credentials: Copy the following format into your .env file and replace the placeholder values with your actual credentials.

Code snippet

SENDER_EMAIL="your_email@gmail.com"
SENDER_PASSWORD="your_gmail_app_password"
RECEIVER_EMAIL="test_receiver_email@example.com"
Important Security Note: For the SENDER_PASSWORD, you must use a Gmail App Password, not your regular Google account password. You can generate one here: https://myaccount.google.com/apppasswords

▶️ Running the Application
Once the setup and configuration are complete, you can run the Streamlit application.

Make sure your virtual environment is activated.

Run the following command in your terminal:

Bash

streamlit run src/main.py
A new tab will automatically open in your web browser at http://localhost:8501, where you can interact with the scheduling agent.


📂 Project Structure
ai-scheduling-agent/
├── data/
│   ├── patients.csv              # Initial patient data
│   ├── doctor_schedules.xlsx     # Doctor's schedule (read and updated by the agent)
│   └── admin_report.xlsx         # Generated report of booked appointments
├── src/
│   ├── agent.py                  # Core LangGraph agent logic and nodes
│   └── main.py                   # Streamlit UI and application entry point
├── .env                          # Local file for storing secrets (not committed)
├── .gitignore                    # Specifies files for Git to ignore
├── requirements.txt              # List of Python dependencies
└── README.md                     # This file


```bash
