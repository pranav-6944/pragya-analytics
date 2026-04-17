"""
Part 2 – Association Rule Mining: Export results to CSV
Saves:
  - frequent_itemsets_apriori.csv
  - frequent_itemsets_fpgrowth.csv
  - association_rules_all.csv
  - rules_courses_together.csv
  - rules_fail_predictors.csv
  - rules_dept_performance.csv
"""

import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, fpgrowth, association_rules
import warnings, os

warnings.filterwarnings('ignore')

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE = os.path.dirname(os.path.abspath(__file__))
FILE = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Dataset\University_Management_Curation_Project.xlsx'
OUT  = os.path.join(BASE, 'csv_outputs')
os.makedirs(OUT, exist_ok=True)

# ── 1. Load Data ───────────────────────────────────────────────────────────────
print("Loading data...")
xl          = pd.ExcelFile(FILE)
courses     = xl.parse('courses')
enrollments = xl.parse('enrollments')
attendance  = xl.parse('attendance')
grades      = xl.parse('grades')

# ── 2. Preprocess ──────────────────────────────────────────────────────────────
grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'P': 4.0}

def std_grade(g):
    s = str(g).strip().upper().replace('+','').replace('-','')
    if s in grade_map: return grade_map[s]
    try:
        v = float(s)
        return min(v/25.0, 4.0) if v > 4.0 else v
    except: return np.nan

grades['gpa']    = grades['grade'].apply(std_grade)
grades['gpa']    = grades.groupby('course_id')['gpa'].transform(lambda x: x.fillna(x.median()))
grades['gpa']    = grades['gpa'].fillna(2.0)
grades['Result'] = np.where(grades['gpa'] >= 1.0, 'Pass', 'Fail')

attendance['is_present'] = attendance['status'].apply(
    lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
att = attendance.groupby(['student_id','course_id']).agg(
    total=('attendance_date','count'), present=('is_present','sum')).reset_index()
att['att_pct']        = att['present'] / att['total']
att['AttendanceLevel'] = np.where(att['att_pct'] >= 0.75, 'HighAttendance', 'LowAttendance')

df = enrollments[['student_id','course_id']].drop_duplicates()
df = df.merge(courses[['course_id','department_id']], on='course_id', how='left')
df = df.merge(grades[['student_id','course_id','Result']], on=['student_id','course_id'], how='left')
df = df.merge(att[['student_id','course_id','AttendanceLevel']], on=['student_id','course_id'], how='left')
df['Result']         = df['Result'].fillna('Pass')
df['AttendanceLevel'] = df['AttendanceLevel'].fillna('HighAttendance')

# ── 3. Build Transactions ──────────────────────────────────────────────────────
print("Building transactions...")
transactions = []
for _, grp in df.groupby('student_id'):
    t = (['Course_' + str(c) for c in grp['course_id'].unique()] +
         ['Dept_'   + str(d) for d in grp['department_id'].unique() if pd.notnull(d)])
    t.append('Result_Fail' if 'Fail' in grp['Result'].values else 'Result_Pass')
    t.append('Attendance_Low' if 'LowAttendance' in grp['AttendanceLevel'].values else 'Attendance_High')
    transactions.append(t)

print(f"  {len(transactions)} transactions generated.")

te      = TransactionEncoder()
te_ary  = te.fit(transactions).transform(transactions)
basket  = pd.DataFrame(te_ary, columns=te.columns_)

# ── 4. Frequent Itemsets ───────────────────────────────────────────────────────
print("Mining frequent itemsets (Apriori)...")
fi_apriori = apriori(basket, min_support=0.001, use_colnames=True)
fi_apriori['length']   = fi_apriori['itemsets'].apply(len)
fi_apriori['itemsets'] = fi_apriori['itemsets'].apply(lambda x: ', '.join(sorted(x)))

print("Mining frequent itemsets (FP-Growth)...")
fi_fp = fpgrowth(basket, min_support=0.001, use_colnames=True)
fi_fp['length']   = fi_fp['itemsets'].apply(len)
fi_fp['itemsets'] = fi_fp['itemsets'].apply(lambda x: ', '.join(sorted(x)))

fi_apriori.to_csv(os.path.join(OUT, 'frequent_itemsets_apriori.csv'), index=False)
fi_fp.to_csv(     os.path.join(OUT, 'frequent_itemsets_fpgrowth.csv'), index=False)
print(f"  Apriori: {len(fi_apriori)} itemsets | FP-Growth: {len(fi_fp)} itemsets")

# ── 5. Association Rules ───────────────────────────────────────────────────────
print("Generating association rules...")
# Re-mine with frozensets for rule generation
fi_fp_raw = fpgrowth(basket, min_support=0.001, use_colnames=True)
rules = association_rules(fi_fp_raw, metric="confidence", min_threshold=0.01)
rules = rules.sort_values('lift', ascending=False)

# Stringify frozensets for CSV export
def fs(col): return col.apply(lambda x: ', '.join(sorted(x)))

rules_out = rules.copy()
rules_out['antecedents'] = fs(rules_out['antecedents'])
rules_out['consequents'] = fs(rules_out['consequents'])
rules_out.to_csv(os.path.join(OUT, 'association_rules_all.csv'), index=False)
print(f"  {len(rules)} rules generated.")

# ── 6. Filtered Question-Based Rules ──────────────────────────────────────────
# Q1: Courses taken together
course_rules = rules[
    rules['antecedents'].apply(lambda x: all(str(i).startswith('Course_') for i in x)) &
    rules['consequents'].apply(lambda x: all(str(i).startswith('Course_') for i in x))
].copy()
course_rules['antecedents'] = fs(course_rules['antecedents'])
course_rules['consequents'] = fs(course_rules['consequents'])
course_rules[['antecedents','consequents','support','confidence','lift']].to_csv(
    os.path.join(OUT, 'rules_courses_together.csv'), index=False)

# Q2: Course combos → Failure
fail_rules = rules[
    rules['consequents'].apply(lambda x: 'Result_Fail' in x) &
    rules['antecedents'].apply(lambda x: any(str(i).startswith('Course_') for i in x))
].copy()
fail_rules['antecedents'] = fs(fail_rules['antecedents'])
fail_rules['consequents'] = fs(fail_rules['consequents'])
fail_rules[['antecedents','consequents','support','confidence','lift']].to_csv(
    os.path.join(OUT, 'rules_fail_predictors.csv'), index=False)

# Q3: Dept → Performance
dept_rules = rules[
    rules['antecedents'].apply(lambda x: any(str(i).startswith('Dept_') for i in x)) &
    rules['consequents'].apply(lambda x: 'Result_Pass' in x or 'Result_Fail' in x)
].copy()
dept_rules['antecedents'] = fs(dept_rules['antecedents'])
dept_rules['consequents'] = fs(dept_rules['consequents'])
dept_rules[['antecedents','consequents','support','confidence','lift']].to_csv(
    os.path.join(OUT, 'rules_dept_performance.csv'), index=False)

print("\nDone! All CSVs saved to:", OUT)
print(f"  frequent_itemsets_apriori.csv  – {len(fi_apriori)} rows")
print(f"  frequent_itemsets_fpgrowth.csv – {len(fi_fp)} rows")
print(f"  association_rules_all.csv      – {len(rules)} rows")
print(f"  rules_courses_together.csv     – {len(course_rules)} rows")
print(f"  rules_fail_predictors.csv      – {len(fail_rules)} rows")
print(f"  rules_dept_performance.csv     – {len(dept_rules)} rows")
