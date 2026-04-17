import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# University Analytics: Data Integration and Preprocessing
This notebook focuses strictly on merging datasets, deriving key features, handling missing values and outliers, and generating a final clean dataset in Excel form."""

code_1 = """import pandas as pd
import numpy as np
import warnings
warnings.filterwarnings('ignore')
"""

text_2 = "## 1. Data Loading and Merging"

code_2 = """file_path = 'University_Management_Curation_Project.xlsx'
xl = pd.ExcelFile(file_path)

# Load sheets
students = xl.parse('students')
courses = xl.parse('courses')
enrollments = xl.parse('enrollments')
attendance = xl.parse('attendance')
grades = xl.parse('grades')
faculty = xl.parse('faculty')

print("Data loaded successfully.")
"""

text_3 = "## 2. Standardize Inconsistent Grading Formats"

code_3 = """# Assuming A, B, C, D, F, with F being fail. Maybe some numerical grades or P/F?
grade_mapping = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'P': 4.0}

def standardize_grade(g):
    if pd.isna(g):
        return np.nan
    g_str = str(g).strip().upper()
    g_str = g_str.replace('+', '').replace('-', '')
    if g_str in grade_mapping:
        return grade_mapping[g_str]
    try:
        val = float(g_str)
        if val > 4.0:
            return min(val / 25.0, 4.0)
        return val
    except:
        return np.nan

grades['gpa_score'] = grades['grade'].apply(standardize_grade)

# Create 'pass' binary indicator
grades['pass'] = (grades['gpa_score'] >= 1.0).astype(int)
print("Grading formats standardized.")
"""

text_4 = "## 3. Handle Missing Values and Outliers"

code_4 = """# Impute missing values in grades using course medians
grades['gpa_score'] = grades.groupby('course_id')['gpa_score'].transform(lambda x: x.fillna(x.median()))
grades['gpa_score'] = grades['gpa_score'].fillna(grades['gpa_score'].median())

# Fill missing credits in courses with median if any exist
courses['credits'] = pd.to_numeric(courses['credits'], errors='coerce')
courses['credits'] = courses['credits'].fillna(courses['credits'].median())

print("Missing values handled.")
"""

text_5 = "## 4. Feature Engineering"

code_5 = """# Attendance Percentage
attendance['is_present'] = attendance['status'].apply(lambda x: 1 if str(x).lower().strip() in ['present', 'late', 'p'] else 0)
att_summary = attendance.groupby(['student_id', 'course_id']).agg(
    total_classes=('attendance_date', 'count'),
    attended_classes=('is_present', 'sum')
).reset_index()
att_summary['attendance_pct'] = (att_summary['attended_classes'] / att_summary['total_classes']) * 100

# Course Load per semester
course_load = enrollments.merge(courses[['course_id', 'credits']], on='course_id', how='left')
student_load = course_load.groupby(['student_id', 'semester']).agg(
    total_credits=('credits', 'sum')
).reset_index()

# Overall student GPA
student_gpa = grades.groupby('student_id')['gpa_score'].mean().reset_index().rename(columns={'gpa_score': 'overall_gpa'})

# Course Pass Rate
course_pass_rate = grades.groupby('course_id').agg(
    total_students=('student_id', 'nunique'),
    passed_students=('pass', 'sum')
).reset_index()
course_pass_rate['pass_rate'] = (course_pass_rate['passed_students'] / course_pass_rate['total_students']) * 100

print("Derived features: GPA, Attendance Percentage, Course load, Pass rate created.")
"""

text_6 = "## 5. Merge Datasets and Handle Features Outliers"

code_6 = """# Merge derived metrics onto the students base table
final_df = students.copy()
final_df = final_df.merge(student_gpa, on='student_id', how='left')

# Average attendance per student overall
avg_attendance = att_summary.groupby('student_id')['attendance_pct'].mean().reset_index().rename(columns={'attendance_pct': 'avg_attendance_pct'})
final_df = final_df.merge(avg_attendance, on='student_id', how='left')

# Average course load per student (across all semesters)
avg_load = student_load.groupby('student_id')['total_credits'].mean().reset_index().rename(columns={'total_credits': 'avg_course_load'})
final_df = final_df.merge(avg_load, on='student_id', how='left')

# Filling final missing values for students without grades/enrollments
final_df['overall_gpa'] = final_df['overall_gpa'].fillna(final_df['overall_gpa'].median())
final_df['avg_attendance_pct'] = final_df['avg_attendance_pct'].fillna(final_df['avg_attendance_pct'].median())
final_df['avg_course_load'] = final_df['avg_course_load'].fillna(final_df['avg_course_load'].median())

# Handle Outliers using IQR rule for attendance and course load
def cap_outliers(df, col):
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df[col] = np.clip(df[col], lower_bound, upper_bound)

cap_outliers(final_df, 'avg_attendance_pct')
cap_outliers(final_df, 'avg_course_load')

# Merging with faculty (Adding FacultyID to Course Pass Rates to demonstrate cross-table merging)
# courses table has faculty_id
course_with_faculty = courses[['course_id', 'faculty_id']].merge(course_pass_rate, on='course_id', how='left')
course_with_faculty['pass_rate'] = course_with_faculty['pass_rate'].fillna(0)

print("Final datasets prepared.")
final_df.head()
"""

text_7 = "## 6. Export to Excel"

code_7 = """# Save the processed data into an Excel file with multiple sheets
output_path = 'Processed_University_Data.xlsx'

with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
    final_df.to_excel(writer, sheet_name='Student_Derived_Metrics', index=False)
    course_with_faculty.to_excel(writer, sheet_name='Course_Faculty_PassRates', index=False)
    
print(f"Data successfully exported to {output_path}")
"""

cells = [
    nbf.v4.new_markdown_cell(text_1),
    nbf.v4.new_code_cell(code_1),
    nbf.v4.new_markdown_cell(text_2),
    nbf.v4.new_code_cell(code_2),
    nbf.v4.new_markdown_cell(text_3),
    nbf.v4.new_code_cell(code_3),
    nbf.v4.new_markdown_cell(text_4),
    nbf.v4.new_code_cell(code_4),
    nbf.v4.new_markdown_cell(text_5),
    nbf.v4.new_code_cell(code_5),
    nbf.v4.new_markdown_cell(text_6),
    nbf.v4.new_code_cell(code_6),
    nbf.v4.new_markdown_cell(text_7),
    nbf.v4.new_code_cell(code_7)
]

nb['cells'] = cells

# Save the notebook
with open('University_Predictive_Analysis.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook 'University_Predictive_Analysis.ipynb' generated successfully.")
