import gradio as gr
import google.generativeai as genai
import time
import json
import os

# Gemini API Key setup (replace with your actual key)
genai.configure(api_key="")

# Load Gemini model
model = genai.GenerativeModel("models/gemini-1.5-pro-latest")

# History file for saved diagnoses
HISTORY_FILE = "car_diagnosis_history.json"

# Common car models for dropdown
COMMON_CAR_MODELS = [
    "Select a model or type your own",
    "Toyota Corolla",
    "Honda Civic",
    "Suzuki Alto",
    "Suzuki WagonR",
    "Suzuki Swift",
    "Suzuki Brezza",
    "Hyundai Creta",
    "Kia Seltos",
    "VW Polo",
    "Renault Duster",
    "Renault Kwid",
    "Renault Kiger",
    "Toyota Innova",
    "Ford F-150",
    "Toyota Camry",
    "Honda Accord",
    "Toyota RAV4",
    "Nissan Altima",
    "Chevrolet Silverado",
    "Honda CR-V",
    "Ford Escape"
]

# Common issues for dropdown
COMMON_ISSUES = [
    "Select an issue or type your own",
    "Engine overheating",
    "Check engine light on",
    "Unusual noise when braking",
    "Car doesn't start",
    "Poor fuel economy",
    "Transmission slipping",
    "A/C not cooling",
    "Battery dies quickly",
    "Steering wheel vibration",
    "Oil leaking"
]

# Common driving conditions
DRIVING_CONDITIONS = [
    "Select conditions or type your own",
    "City traffic",
    "Highway/Freeway",
    "Off-road/Rough terrain",
    "Mixed driving",
    "Extreme hot weather",
    "Extreme cold weather",
    "Stop-and-go traffic",
    "Mostly short trips"
]

# Main logic for car maintenance assistant
def car_maintenance_assistant(car_model, issue, mileage, last_service, driving_conditions):
    # Input validation
    if not car_model or car_model == "Select a model or type your own":
        return "Please enter a car model."
    if not issue or issue == "Select an issue or type your own":
        return "Please describe the issue you're experiencing."
    
    prompt = f""" 
    You are an expert car maintenance assistant.
    
    Given the following car details:
    - Car Model: {car_model}
    - Reported Issue: {issue}
    - Current Mileage: {mileage}
    - Last Service Done: {last_service}
    - Driving Conditions: {driving_conditions}
    
    Analyze the issue and suggest:
    1. Possible Causes
    2. Fix Recommendations
    3. Whether it needs urgent attention
    4. Preventive Maintenance Tips
    
    Respond in a clear, structured, and user-friendly format.
    """
    
    try:
        response = model.generate_content(prompt)
        diagnosis = response.text
        
        # Save to history
        save_to_history(car_model, issue, mileage, last_service, driving_conditions, diagnosis)
        
        return diagnosis
    except Exception as e:
        return f"Error generating diagnosis: {str(e)}\n\nPlease try again later."

# Function to save diagnoses to history
def save_to_history(car_model, issue, mileage, last_service, driving_conditions, diagnosis):
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    
    new_entry = {
        "timestamp": timestamp,
        "car_model": car_model,
        "issue": issue,
        "mileage": mileage,
        "last_service": last_service,
        "driving_conditions": driving_conditions,
        "diagnosis": diagnosis
    }
    
    # Load existing history or create new
    if os.path.exists(HISTORY_FILE):
        try:
            with open(HISTORY_FILE, "r") as f:
                history = json.load(f)
        except:
            history = []
    else:
        history = []
    
    # Add new entry and save
    history.append(new_entry)
    try:
        with open(HISTORY_FILE, "w") as f:
            json.dump(history, f, indent=2)
    except:
        pass  # Silently fail if can't write to file

# Function to load history entries
def load_history():
    if not os.path.exists(HISTORY_FILE):
        return "No diagnosis history found."
    
    try:
        with open(HISTORY_FILE, "r") as f:
            history = json.load(f)
        
        if not history:
            return "No diagnosis history found."
        
        history_text = "# Diagnosis History\n\n"
        for entry in history[-5:]:  # Show last 5 entries
            history_text += f"**{entry['timestamp']}** - {entry['car_model']}: {entry['issue']}\n\n"
            history_text += f"*Mileage:* {entry['mileage']}, *Last Service:* {entry['last_service']}, *Conditions:* {entry['driving_conditions']}\n\n"
            history_text += f"**Diagnosis:**\n{entry['diagnosis']}\n\n"
            history_text += "---\n\n"
        
        return history_text
    except:
        return "Error loading diagnosis history."

# Clear form after diagnosis
def clear_form():
    return "Select a model or type your own", "Select an issue or type your own", "", "", "Select conditions or type your own", ""

# Create the Gradio interface with enhanced features
with gr.Blocks() as demo:
    gr.Markdown("<h1 style='text-align: center;'>Micho Advanced Car Maintenance Assistant</h1>")
    
    with gr.Tabs():
        with gr.TabItem("Diagnose Issue"):
            # All input fields in a single row
            with gr.Row():
                car_model = gr.Dropdown(
                    label="Car Model", 
                    choices=COMMON_CAR_MODELS,
                    value="Select a model or type your own",
                    allow_custom_value=True,
                    scale=1
                )
                issue = gr.Dropdown(
                    label="Issue", 
                    choices=COMMON_ISSUES,
                    value="Select an issue or type your own",
                    allow_custom_value=True,
                    scale=2
                )
                
            with gr.Row():
                mileage = gr.Textbox(label="Mileage", placeholder="e.g., 45000 km", scale=1)
                last_service = gr.Textbox(label="Last Service", placeholder="e.g., 6 months ago", scale=1)
                driving_conditions = gr.Dropdown(
                    label="Driving Conditions",
                    choices=DRIVING_CONDITIONS,
                    value="Select conditions or type your own",
                    allow_custom_value=True,
                    scale=1
                )
            
            # Buttons row
            with gr.Row():
                submit_btn = gr.Button("🔍 Diagnose Issue", variant="primary")
                clear_btn = gr.Button("🗑️ Clear Form")
            
            # Output box
            with gr.Row():
                output = gr.Markdown(label="Maintenance Suggestions", value="")
            
            # Connect the buttons to functions
            submit_btn.click(
                fn=car_maintenance_assistant,
                inputs=[car_model, issue, mileage, last_service, driving_conditions],
                outputs=[output]
            )
            
            clear_btn.click(
                fn=clear_form,
                inputs=[],
                outputs=[car_model, issue, mileage, last_service, driving_conditions, output]
            )
        
        # History tab
        with gr.TabItem("History"):
            with gr.Row():
                refresh_btn = gr.Button("🔄 Refresh History")
                history_output = gr.Markdown(value="Click 'Refresh History' to view your past diagnoses")
            
            refresh_btn.click(
                fn=load_history,
                inputs=[],
                outputs=[history_output]
            )
            
        # Maintenance Tips tab
        with gr.TabItem("Maintenance Tips"):
            gr.Markdown("""
            # General Car Maintenance Tips
            
            ## Regular Maintenance Schedule
            - **Oil Change**: Every 3,000-5,000 miles for conventional oil; 7,500-10,000 miles for synthetic oil
            - **Tire Rotation**: Every 5,000-7,500 miles
            - **Air Filter**: Every 15,000-30,000 miles
            - **Brake Pads**: Every 30,000-70,000 miles
            - **Transmission Fluid**: Every 30,000-60,000 miles
            - **Coolant**: Every 30,000 miles or 2 years
            
            ## Dashboard Warning Lights
            - **Check Engine Light**: Could indicate various issues from minor to serious
            - **Oil Pressure Warning**: Stop immediately and check oil levels
            - **Temperature Warning**: Car is overheating; pull over and let it cool down
            - **Battery Alert**: Electrical system issues
            - **Brake Warning**: Check brake fluid or brake system issues
            
            ## Tips for Longer Car Life
            1. Follow the manufacturer's maintenance schedule
            2. Check tire pressure monthly
            3. Address strange noises or handling issues promptly
            4. Keep your car clean to prevent rust and corrosion
            5. Drive gently and avoid aggressive acceleration or braking
            """)

# Launch the app
demo.launch()