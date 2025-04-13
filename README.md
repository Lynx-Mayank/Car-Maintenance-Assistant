# Micho: Advanced Car Maintenance Assistant

Micho is a smart car maintenance assistant built with Python, [Gradio](https://gradio.app/), and Google’s Gemini API. It helps users diagnose car issues, get professional repair recommendations, and view personalized maintenance advice—all through a friendly web interface.

---

## 🔧 Features

- **Car Issue Diagnosis** using Google Gemini Pro LLM
- **Common Car Models and Issues** with manual override
- **Maintenance History Log** with timestamped records
- **Preventive Maintenance Tips**
- **Multi-tab Interface** using Gradio
- **Simple & Responsive Layout** – just run and use in browser

---

## 💻 Demo UI

| Tab               | Functionality                                                                                   |
|-------------------|-------------------------------------------------------------------------------------------------|
| Diagnose Issue    | Select or enter car model, issue, mileage, service info, and get intelligent repair suggestions |
| History           | View last 5 diagnoses stored locally in a JSON file                                             |
| Maintenance Tips  | Handy general tips for regular car care and dashboard light meanings                            |

---

## 🛠 Requirements

- Python 3.10+
- Gradio `>=4.9`
- `google-generativeai`
- Gemini API Key to be added in the genai.configure() function.

---
## Install Dependancies
pip install gradio==4.9.0 google-generativeai
