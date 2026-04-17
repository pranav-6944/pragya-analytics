import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Association Rule Mining: Discovering Academic Patterns
## Phase 2: Transaction Dataset Generation & Mining

**Objective:** Discover patterns between Courses, Departments, and Student Performance.
**Techniques:** Apriori and FP-Growth algorithms via `mlxtend`."""

code_1 = """import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
import warnings
warnings.filterwarnings('ignore')
"""

text_2 = "## 1. Prepare Transaction Dataset"

code_2 = """# Load raw data to fetch explicit Student -> Course -> Department relationships
file_path = r'c:\\Users\\prana_b2roblq\\Downloads\\university Analytics\\University_Management_Curation_Project.xlsx'
xl = pd.ExcelFile(file_path)

courses = xl.parse('courses')
enrollments = xl.parse('enrollments')
attendance = xl.parse('attendance')
grades = xl.parse('grades')

# Standardize Grades (Failure vs Pass)
grade_mapping = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'P': 4.0}
def std_grade(g):
    g_str = str(g).strip().upper().replace('+', '').replace('-', '')
    if g_str in grade_mapping: return grade_mapping[g_str]
    try:
        v = float(g_str)
        return min(v/25.0, 4.0) if v > 4.0 else v
    except: return np.nan

grades['gpa'] = grades['grade'].apply(std_grade)
grades['gpa'] = grades.groupby('course_id')['gpa'].transform(lambda x: x.fillna(x.median()))
grades['gpa'] = grades['gpa'].fillna(2.0)
grades['Result'] = np.where(grades['gpa'] >= 1.0, 'Pass', 'Fail')

# Determine Attendance Level per Student-Course
attendance['is_present'] = attendance['status'].apply(lambda x: 1 if str(x).lower().strip() in ['present', 'late', 'p'] else 0)
att_summary = attendance.groupby(['student_id', 'course_id']).agg(
    total=('attendance_date', 'count'),
    present=('is_present', 'sum')
).reset_index()
att_summary['att_pct'] = att_summary['present'] / att_summary['total']
att_summary['AttendanceLevel'] = np.where(att_summary['att_pct'] >= 0.75, 'HighAttendance', 'LowAttendance')

# Base linkage table
df = enrollments[['student_id', 'course_id']].drop_duplicates()
df = df.merge(courses[['course_id', 'department_id']], on='course_id', how='left')
df = df.merge(grades[['student_id', 'course_id', 'Result']], on=['student_id', 'course_id'], how='left')
df = df.merge(att_summary[['student_id', 'course_id', 'AttendanceLevel']], on=['student_id', 'course_id'], how='left')

df['Result'] = df['Result'].fillna('Pass') # Assume pass if missing
df['AttendanceLevel'] = df['AttendanceLevel'].fillna('HighAttendance') # Assume normal if missing

print("Dataset relationships mapped.")
"""

text_3 = "## 2. Compile Transactions per Student"

code_3 = """# Create transactions grouping by student
# For a student, we will compile all courses (C_xxx), departments (Dept_xxx).
# For results and attendance, we represent an overall picture or per-course picture.
# The simplest approach is putting the specific course IDs and a single unified Result/Attendance, 
# or specific Result per course (e.g., C101_Fail).
# To find 'course combinations lead to failures', let's use an overall 'Result_Fail' if they failed ANY course.
# We also include 'Dept_xxx' for any accessed departments.

transactions = []
grouped = df.groupby('student_id')

for student, group in grouped:
    transaction = []
    # Add Courses
    transaction.extend(['Course_' + str(c) for c in group['course_id'].unique()])
    
    # Add Departments
    transaction.extend(['Dept_' + str(d) for d in group['department_id'].unique() if pd.notnull(d)])
    
    # Add Academic Pattern (Result)
    if 'Fail' in group['Result'].values:
        transaction.append('Result_Fail')
    else:
        transaction.append('Result_Pass')
        
    # Add Attendance Level
    if 'LowAttendance' in group['AttendanceLevel'].values:
        transaction.append('Attendance_Low')
    else:
        transaction.append('Attendance_High')
        
    transactions.append(transaction)

print(f"Generated {len(transactions)} transactions.")
print("Sample Transaction:", transactions[0])

# One-hot encoding the transactions list
te = TransactionEncoder()
te_ary = te.fit(transactions).transform(transactions)
basket = pd.DataFrame(te_ary, columns=te.columns_)
"""

text_4 = "## 3. Frequent Itemsets (Apriori vs FP-Growth)"

code_4 = """# Apriori
frequent_itemsets_apriori = apriori(basket, min_support=0.001, use_colnames=True)
frequent_itemsets_apriori['length'] = frequent_itemsets_apriori['itemsets'].apply(lambda x: len(x))

# FP-Growth (Faster for large datasets)
frequent_itemsets_fp = fpgrowth(basket, min_support=0.001, use_colnames=True)
frequent_itemsets_fp['length'] = frequent_itemsets_fp['itemsets'].apply(lambda x: len(x))

print(f"Discovered {len(frequent_itemsets_fp)} frequent itemsets using FP-Growth.")
"""

text_5 = "## 4. Association Rules Generation"

code_5 = """# Generate rules with confidence >= 0.01
rules = association_rules(frequent_itemsets_fp, metric="confidence", min_threshold=0.01)
rules = rules.sort_values(by='lift', ascending=False)
print(f"Generated {len(rules)} association rules.")
"""

text_6 = "## 5. Answering Specific Academic Questions"

code_6 = """import warnings
warnings.filterwarnings('ignore')

print("--- Q1: Which courses are frequently taken together? ---")
course_rules = rules[
    rules['antecedents'].apply(lambda x: all(str(i).startswith('Course_') for i in x)) & 
    rules['consequents'].apply(lambda x: all(str(i).startswith('Course_') for i in x))
]
print(course_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5))

print("\\n--- Q2: Which course combinations lead to failures? ---")
fail_rules = rules[
    rules['consequents'].apply(lambda x: 'Result_Fail' in x) &
    rules['antecedents'].apply(lambda x: any(str(i).startswith('Course_') for i in x))
]
print(fail_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5))

print("\\n--- Q3: Which departments have strong performance patterns? ---")
dept_perf_rules = rules[
    rules['antecedents'].apply(lambda x: any(str(i).startswith('Dept_') for i in x)) &
    rules['consequents'].apply(lambda x: 'Result_Pass' in x or 'Result_Fail' in x)
]
print(dept_perf_rules[['antecedents', 'consequents', 'support', 'confidence', 'lift']].head(5))
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
    nbf.v4.new_code_cell(code_6)
]

nb['cells'] = cells

with open('University_Association_Mining.ipynb', 'w') as f:
    nbf.write(nb, f)

print("Notebook 'University_Association_Mining.ipynb' generated successfully.")
