import pandas as pd
import numpy as np
from sklearn.neural_network import MLPClassifier
from sklearn.cluster import KMeans
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.model_selection import train_test_split
import os, warnings
warnings.filterwarnings('ignore')

FILE = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Dataset\University_Management_Curation_Project.xlsx'
OUT  = r'c:\Users\prana_b2roblq\Downloads\university Analytics\PowerBI_Data'
os.makedirs(OUT, exist_ok=True)

xl = pd.ExcelFile(FILE)
students    = xl.parse('students')
courses     = xl.parse('courses')
faculty     = xl.parse('faculty')
departments = xl.parse('departments')
enrollments = xl.parse('enrollments')
attendance  = xl.parse('attendance')
grades      = xl.parse('grades')

# ── Grade standardisation ────────────────────────────────────────────────────
gmap = {'A':4.0,'B':3.0,'C':2.0,'D':1.0,'F':0.0,'P':4.0}
def sg(g):
    s=str(g).strip().upper().replace('+','').replace('-','')
    if s in gmap: return gmap[s]
    try: v=float(s); return min(v/25,4.0) if v>4 else v
    except: return np.nan

grades['gpa']  = grades['grade'].apply(sg)
grades['gpa']  = grades.groupby('course_id')['gpa'].transform(lambda x: x.fillna(x.median()))
grades['gpa']  = grades['gpa'].fillna(2.0)
grades['pass'] = (grades['gpa']>=1.0).astype(int)
grades['Result'] = grades['gpa'].apply(lambda g: 'Distinction' if g>=3.0 else ('Pass' if g>=1.0 else 'Fail'))

# ── Attendance ───────────────────────────────────────────────────────────────
attendance['present'] = attendance['status'].apply(
    lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
att = (attendance.groupby('student_id')
       .agg(Total_Classes=('present','count'), Classes_Attended=('present','sum')).reset_index())
att['Attendance_Pct'] = (att['Classes_Attended'] / att['Total_Classes'] * 100).round(2)
att['Attendance_Level'] = att['Attendance_Pct'].apply(
    lambda x: 'High (>75%)' if x>=75 else ('Medium (50-75%)' if x>=50 else 'Low (<50%)'))

# ── Student metrics ──────────────────────────────────────────────────────────
courses['credits'] = pd.to_numeric(courses['credits'], errors='coerce').fillna(3)
enr = enrollments.merge(courses[['course_id','credits','department_id']], on='course_id', how='left')
ef  = enrollments.merge(courses[['course_id','faculty_id']], on='course_id', how='left')

s_gpa      = grades.groupby('student_id')['gpa'].mean().reset_index().rename(columns={'gpa':'Overall_GPA'})
s_pass     = grades.groupby('student_id')['pass'].mean().reset_index().rename(columns={'pass':'Pass_Rate'})
s_load     = enr.groupby('student_id')['credits'].sum().reset_index().rename(columns={'credits':'Course_Load'})
s_fac      = ef.groupby('student_id')['faculty_id'].nunique().reset_index().rename(columns={'faculty_id':'Faculty_Interaction'})
s_courses  = enrollments.groupby('student_id')['course_id'].nunique().reset_index().rename(columns={'course_id':'Courses_Enrolled'})

df = students[['student_id']].copy()
for g in [s_gpa, s_pass, att[['student_id','Attendance_Pct','Attendance_Level']], s_load, s_fac, s_courses]:
    df = df.merge(g, on='student_id', how='left')
for c in ['Overall_GPA','Pass_Rate','Attendance_Pct','Course_Load','Faculty_Interaction']:
    df[c] = df[c].fillna(df[c].median())
df['Internal_Marks'] = (df['Overall_GPA'] * 25).round(2)

# ── Classification result ────────────────────────────────────────────────────
df['Academic_Result'] = df['Internal_Marks'].apply(
    lambda m: 'Distinction' if m>=75 else ('Pass' if m>=40 else 'Fail'))

# ── Clustering ───────────────────────────────────────────────────────────────
km_feats = ['Overall_GPA','Attendance_Pct','Course_Load','Pass_Rate']
X_km = StandardScaler().fit_transform(df[km_feats])
km = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster_ID'] = km.fit_predict(X_km)
cl_gpa = df.groupby('Cluster_ID')['Overall_GPA'].mean().sort_values(ascending=False)
seg_map = {cl_gpa.index[0]:'High Achievers', cl_gpa.index[1]:'Average Performers',
           cl_gpa.index[2]:'Struggling Students', cl_gpa.index[3]:'At-Risk Students'}
df['Student_Segment'] = df['Cluster_ID'].map(seg_map)

# ── Dropout Risk ─────────────────────────────────────────────────────────────
ann_feats = ['Attendance_Pct','Internal_Marks','Course_Load','Pass_Rate','Faculty_Interaction']
df['Dropout_Risk_Label'] = ((df['Overall_GPA']<1.5)|(df['Attendance_Pct']<50)).astype(int)
X_ann = MinMaxScaler().fit_transform(df[ann_feats])
y_ann = df['Dropout_Risk_Label']
Xtr,Xte,ytr,yte = train_test_split(X_ann, y_ann, test_size=0.2, random_state=42, stratify=y_ann)
ann = MLPClassifier(hidden_layer_sizes=(128,64,32), activation='relu', solver='adam', max_iter=200, random_state=42)
ann.fit(Xtr, ytr)
df['Dropout_Risk_Score'] = ann.predict_proba(X_ann)[:,1].round(4)
df['Dropout_Risk'] = df['Dropout_Risk_Score'].apply(lambda x: 'High Risk' if x>0.6 else ('Medium Risk' if x>0.3 else 'Low Risk'))

# ── GPA tier ────────────────────────────────────────────────────────────────
df['GPA_Tier'] = pd.cut(df['Overall_GPA'], bins=[0,1.0,2.0,3.0,4.0],
                         labels=['Failing (0-1)','Pass (1-2)','Good (2-3)','Excellent (3-4)'])

# ──────────────────────────────────────────────────────────────────────────────
# TABLE 1: Student Analytics (main table)
# ──────────────────────────────────────────────────────────────────────────────
student_table = df[['student_id','Overall_GPA','Internal_Marks','Attendance_Pct',
                     'Attendance_Level','Course_Load','Faculty_Interaction',
                     'Courses_Enrolled','Pass_Rate','Academic_Result',
                     'Student_Segment','Dropout_Risk','Dropout_Risk_Score','GPA_Tier']].copy()
student_table.to_csv(os.path.join(OUT, '1_Student_Analytics.csv'), index=False)
print(f"Saved: 1_Student_Analytics.csv  ({len(student_table)} rows)")

# ──────────────────────────────────────────────────────────────────────────────
# TABLE 2: Department Performance
# ──────────────────────────────────────────────────────────────────────────────
grade_dept = grades.merge(courses[['course_id','department_id']], on='course_id', how='left')
dept_stats = grade_dept.groupby('department_id').agg(
    Avg_GPA          = ('gpa','mean'),
    Pass_Rate_Pct    = ('pass','mean'),
    Total_Students   = ('student_id','nunique'),
    Total_Grades     = ('student_id','count')
).reset_index()
dept_stats['Pass_Rate_Pct']  = (dept_stats['Pass_Rate_Pct']*100).round(2)
dept_stats['Avg_GPA']        = dept_stats['Avg_GPA'].round(3)
dept_stats['Dept_Rank']      = dept_stats['Avg_GPA'].rank(ascending=False).astype(int)
dept_stats['Performance']    = dept_stats['Avg_GPA'].apply(
    lambda x: 'High' if x>=2.1 else ('Medium' if x>=1.9 else 'Low'))
dept_stats.to_csv(os.path.join(OUT, '2_Department_Performance.csv'), index=False)
print(f"Saved: 2_Department_Performance.csv  ({len(dept_stats)} rows)")

# ──────────────────────────────────────────────────────────────────────────────
# TABLE 3: Course Difficulty Analysis
# ──────────────────────────────────────────────────────────────────────────────
course_stats = grades.merge(courses[['course_id','credits','department_id','faculty_id']], on='course_id', how='left')
course_agg = course_stats.groupby('course_id').agg(
    Avg_GPA         = ('gpa','mean'),
    Pass_Rate_Pct   = ('pass','mean'),
    Enrollment      = ('student_id','nunique'),
    Avg_Credits     = ('credits','mean')
).reset_index()
course_agg['Pass_Rate_Pct']     = (course_agg['Pass_Rate_Pct']*100).round(2)
course_agg['Avg_GPA']           = course_agg['Avg_GPA'].round(3)
course_agg['Difficulty_Score']  = ((1-course_agg['Pass_Rate_Pct']/100)*course_agg['Avg_Credits']).round(3)
course_agg['Difficulty_Level']  = course_agg['Difficulty_Score'].apply(
    lambda x: 'Very Hard' if x>1.2 else ('Hard' if x>0.8 else ('Medium' if x>0.4 else 'Easy')))
course_agg.to_csv(os.path.join(OUT, '3_Course_Difficulty.csv'), index=False)
print(f"Saved: 3_Course_Difficulty.csv  ({len(course_agg)} rows)")

# ──────────────────────────────────────────────────────────────────────────────
# TABLE 4: Attendance Analysis
# ──────────────────────────────────────────────────────────────────────────────
att_analysis = att[['student_id','Attendance_Pct','Attendance_Level']].merge(
    df[['student_id','Overall_GPA','Academic_Result','Dropout_Risk']], on='student_id', how='left')
att_analysis['Att_Bucket'] = pd.cut(att_analysis['Attendance_Pct'],
                                     bins=[0,25,50,75,100],
                                     labels=['0-25%','25-50%','50-75%','75-100%'])
att_analysis.to_csv(os.path.join(OUT, '4_Attendance_Analysis.csv'), index=False)
print(f"Saved: 4_Attendance_Analysis.csv  ({len(att_analysis)} rows)")

# ──────────────────────────────────────────────────────────────────────────────
# TABLE 5: Grade Distribution (for trend charts)
# ──────────────────────────────────────────────────────────────────────────────
grade_dist = grades[['student_id','course_id','semester','grade','gpa','pass','Result']].copy()
grade_dist = grade_dist.merge(courses[['course_id','department_id','credits']], on='course_id', how='left')
grade_dist.to_csv(os.path.join(OUT, '5_Grade_Distribution.csv'), index=False)
print(f"Saved: 5_Grade_Distribution.csv  ({len(grade_dist)} rows)")

# ──────────────────────────────────────────────────────────────────────────────
# TABLE 6: Cluster Summary (for segment card visuals)
# ──────────────────────────────────────────────────────────────────────────────
cluster_summary = df.groupby('Student_Segment').agg(
    Count           = ('student_id','count'),
    Avg_GPA         = ('Overall_GPA','mean'),
    Avg_Attendance  = ('Attendance_Pct','mean'),
    Avg_Course_Load = ('Course_Load','mean'),
    Avg_Risk_Score  = ('Dropout_Risk_Score','mean')
).reset_index().round(3)
cluster_summary.to_csv(os.path.join(OUT, '6_Cluster_Summary.csv'), index=False)
print(f"Saved: 6_Cluster_Summary.csv")

print("\nAll Power BI CSVs exported to:", OUT)
print("\nSuggested Power BI Visuals:")
print("  1_Student_Analytics    -> Pie (Academic_Result), Bar (GPA_Tier), Scatter (Attendance vs GPA)")
print("  2_Department_Perf      -> Bar chart (Avg GPA by Dept), Table with Dept_Rank")
print("  3_Course_Difficulty    -> Bar (Difficulty Score), Filter by Difficulty_Level")
print("  4_Attendance_Analysis  -> Clustered Bar (Att_Bucket vs Avg GPA)")
print("  5_Grade_Distribution   -> Line chart (GPA by Semester), Slicer by Department")
print("  6_Cluster_Summary      -> Card visuals per Segment, Radar chart")
