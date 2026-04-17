from docx import Document
from docx.shared import Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
import os

def create_viva_doc():
    doc = Document()
    
    # Title
    title = doc.add_heading('PRAGYA: University Academic Analytics', 0)
    title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    subtitle = doc.add_paragraph('Potential Viva Questions & Explanations')
    subtitle.alignment = WD_ALIGN_PARAGRAPH.CENTER
    
    doc.add_paragraph() # Add some space

    questions = [
        {
            "q": "1. What is the main objective of your project (PRAGYA)?",
            "a": "The objective is to move beyond simply viewing past student data (Exploratory Data Analysis) and build a real-time Predictive Analytics System. The system automatically identifies at-risk students and predicts academic outcomes so that the university can intervene early."
        },
        {
            "q": "2. There are no saved model files (like .pkl/.h5) in your backend folder. Where is your AI model?",
            "a": "The machine learning models are trained 'on-the-fly' inside system memory (RAM). When the FastAPI server boots up, it reads the raw dataset, extracts features, trains the Random Forest and Neural Network models, and stores them in memory. This ensures the models are always trained on the absolute latest data dynamically without needing manual re-exporting."
        },
        {
            "q": "3. Why didn't you use your previously pre-processed CSV file from Part 1? Why are you coding the data cleaning logic again in main.py?",
            "a": "This was a deliberate software engineering choice to ensure 'Data Lineage'. By having the web application process the raw Excel file itself on startup, it acts as a standalone ETL (Extract, Transform, Load) microservice. This guarantees that the features passed into the live API completely match the exact mathematical scaling and encoding the model expects, avoiding 'transformation skew'."
        },
        {
            "q": "4. Why is the GPA scale limited to 1.0 to 4.0 in this project, instead of a 10-point CGPA system?",
            "a": "The original raw dataset provided letter grades (A, B, C, D, F). To normalize this data mathematically for the AI, the backend maps these letters to the universal standard 4.0 US University GPA scale (where A=4.0, F=0.0). Slider inputs from 0-100 are simply divided by 25 to estimate the equivalent 4.0 GPA."
        },
        {
            "q": "5. Which Machine Learning algorithms did you use in the web application and why?",
            "a": "1. Random Forest Classifier: Chosen for its high accuracy in multi-class prediction (Pass, Fail, Distinction) when dealing with non-linear student behavior patterns.\n2. MLP Neural Network (Deep Learning): Used specifically for calculating the exact probability (0-100%) of a student's 'Dropout Risk'.\n3. K-Means Clustering: An unsupervised model that runs in the background to separate the entire student population into 4 behavioral segments (High Achievers, Average, Struggling, At-Risk)."
        },
        {
            "q": "6. How does the 'Predict Student' page actually function behind the scenes?",
            "a": "When a user adjusts the sliders on the React frontend, it sends a JSON payload via an HTTP POST request to the FastAPI backend. The backend routes those 5 metrics (Attendance, Marks, Course Load, Pass Rate, Faculty Interaction) through the mathematical weights of the pre-trained Random Forest and Neural Network in memory. It then instantly returns the classification and risk percentage back to the screen."
        },
        {
            "q": "7. What were the most important features / data points in determining if a student would fail or drop out?",
            "a": "Based on the Feature Importance charts from the Random Forest model, the two strongest predictors of failure were 'Internal Marks (GPA)' and 'Attendance Percentage'. If a student's attendance dropped under 50% and their GPA dropped under 1.5 simultaneously, the Neural Network correctly flagged them with a very high dropout risk."
        },
        {
            "q": "8. Why did you use FastAPI and React instead of just submitting a Jupyter Notebook?",
            "a": "A Jupyter Notebook is great for experimenting (EDA), but it is not useful for a real-world user. Moving to FastAPI and React transforms this project from a Data Science research script into a fully operationalized 'Software as a Service' (SaaS) product that academic counselors can actively use via a web browser."
        }
    ]

    for item in questions:
        # Question paragraph
        p_q = doc.add_paragraph()
        runner = p_q.add_run(item["q"])
        runner.bold = True
        runner.font.size = Pt(12)
        runner.font.color.rgb = RGBColor(0, 51, 102) # Dark blue for questions
        
        # Answer paragraph
        p_a = doc.add_paragraph()
        run_a = p_a.add_run(item["a"])
        run_a.font.size = Pt(11)
        
        doc.add_paragraph() # Spacing

    output_path = r"c:\Users\prana_b2roblq\Downloads\university Analytics\PRAGYA_Viva_Preparation.docx"
    doc.save(output_path)
    print(f"Document successfully created at: {output_path}")

if __name__ == "__main__":
    create_viva_doc()
