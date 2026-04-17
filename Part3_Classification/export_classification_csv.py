"""
Part 3 - Classification: Export all results to CSV
Saves:
  - feature_matrix.csv          : Full feature dataset with target
  - class_distribution.csv      : Pass/Fail/Distinction counts
  - model_metrics_summary.csv   : Accuracy, Precision, Recall, F1 per model
  - classification_report_<model>.csv : Per-class metrics for each model
  - confusion_matrix_<model>.csv      : Raw confusion matrix for each model
  - feature_importances_rf.csv  : Random Forest feature importances
  - test_predictions.csv        : Test set with true label + all model predictions
"""

import pandas as pd
import numpy as np
import os, warnings
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (classification_report, confusion_matrix,
                             accuracy_score, precision_score, recall_score, f1_score)

warnings.filterwarnings('ignore')

BASE = os.path.dirname(os.path.abspath(__file__))
FILE = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Dataset\University_Management_Curation_Project.xlsx'
OUT  = os.path.join(BASE, 'csv_outputs')
os.makedirs(OUT, exist_ok=True)

# ── 1. Load ────────────────────────────────────────────────────────────────────
print("Loading data...")
xl          = pd.ExcelFile(FILE)
students    = xl.parse('students')
courses     = xl.parse('courses')
faculty     = xl.parse('faculty')
enrollments = xl.parse('enrollments')
attendance  = xl.parse('attendance')
grades      = xl.parse('grades')

# ── 2. Feature Engineering ────────────────────────────────────────────────────
grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'P': 4.0}

def std_grade(g):
    s = str(g).strip().upper().replace('+','').replace('-','')
    if s in grade_map: return grade_map[s]
    try:
        v = float(s); return min(v/25.0, 4.0) if v > 4.0 else v
    except: return np.nan

grades['gpa_score'] = grades['grade'].apply(std_grade)
grades['gpa_score'] = grades.groupby('course_id')['gpa_score'].transform(lambda x: x.fillna(x.median()))
grades['gpa_score'] = grades['gpa_score'].fillna(2.0)

attendance['present'] = attendance['status'].apply(
    lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
att = (attendance.groupby('student_id')
       .agg(total=('present','count'), attended=('present','sum')).reset_index())
att['attendance_pct'] = att['attended'] / att['total'] * 100

internal = (grades.groupby('student_id')['gpa_score'].mean().reset_index()
            .rename(columns={'gpa_score':'internal_marks'}))
internal['internal_marks'] = internal['internal_marks'] * 25

courses['credits'] = pd.to_numeric(courses['credits'], errors='coerce').fillna(3)
enr_courses = enrollments.merge(courses[['course_id','credits']], on='course_id', how='left')
difficulty  = (enr_courses.groupby('student_id')['credits'].mean().reset_index()
               .rename(columns={'credits':'course_difficulty'}))
study_load  = (enr_courses.groupby('student_id')['credits'].sum().reset_index()
               .rename(columns={'credits':'study_load'}))

fac_exp     = (faculty.groupby('department_id').size().reset_index()
               .rename(columns={0:'faculty_experience'}))
enr_fac = (enrollments
           .merge(courses[['course_id','faculty_id']], on='course_id', how='left')
           .merge(faculty[['faculty_id','department_id']], on='faculty_id', how='left')
           .merge(fac_exp, on='department_id', how='left'))
fac_per_stu = enr_fac.groupby('student_id')['faculty_experience'].mean().reset_index()

df = students[['student_id']].copy()
for tbl, key in [(att[['student_id','attendance_pct']], 'student_id'),
                 (internal, 'student_id'),
                 (difficulty, 'student_id'),
                 (study_load, 'student_id'),
                 (fac_per_stu, 'student_id')]:
    df = df.merge(tbl, on=key, how='left')

for col in ['attendance_pct','internal_marks','course_difficulty','study_load','faculty_experience']:
    df[col] = df[col].fillna(df[col].median())

df['Result'] = df['internal_marks'].apply(
    lambda m: 'Distinction' if m >= 75 else ('Pass' if m >= 40 else 'Fail'))

print(f"Feature matrix: {df.shape}")

# ── 3. Save feature matrix & class distribution ───────────────────────────────
df.to_csv(os.path.join(OUT, 'feature_matrix.csv'), index=False)
cls_dist = df['Result'].value_counts().reset_index()
cls_dist.columns = ['Result', 'Count']
cls_dist.to_csv(os.path.join(OUT, 'class_distribution.csv'), index=False)

# ── 4. Train/Test Split ───────────────────────────────────────────────────────
features = ['attendance_pct','internal_marks','course_difficulty','study_load','faculty_experience']
X = df[features]
le = LabelEncoder()
y  = le.fit_transform(df['Result'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
scaler = StandardScaler()
X_train_sc = scaler.fit_transform(X_train)
X_test_sc  = scaler.transform(X_test)

print(f"Train: {len(X_train)} | Test: {len(X_test)} | Classes: {list(le.classes_)}")

# ── 5. Train Models & Export Metrics ─────────────────────────────────────────
models = {
    'Logistic_Regression': LogisticRegression(max_iter=1000, random_state=42),
    'Decision_Tree'      : DecisionTreeClassifier(max_depth=5, random_state=42),
    'Random_Forest'      : RandomForestClassifier(n_estimators=100, random_state=42),
    'SVM'                : SVC(kernel='rbf', probability=True, random_state=42),
}

summary_rows = []
pred_df = X_test.copy().reset_index(drop=True)
pred_df['True_Label'] = le.inverse_transform(y_test)

for name, model in models.items():
    scale = name in ['Logistic_Regression', 'SVM']
    Xtr, Xte = (X_train_sc, X_test_sc) if scale else (X_train, X_test)
    print(f"  Training {name}...")
    model.fit(Xtr, y_train)
    y_pred = model.predict(Xte)

    acc  = accuracy_score(y_test, y_pred)
    prec = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    rec  = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1   = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    summary_rows.append({'Model': name, 'Accuracy': round(acc,4),
                         'Precision': round(prec,4), 'Recall': round(rec,4), 'F1_Score': round(f1,4)})

    # Classification report per class
    rpt = classification_report(y_test, y_pred, target_names=le.classes_, output_dict=True)
    rpt_df = pd.DataFrame(rpt).T.reset_index().rename(columns={'index':'class'})
    rpt_df.to_csv(os.path.join(OUT, f'classification_report_{name}.csv'), index=False)

    # Confusion matrix
    cm = confusion_matrix(y_test, y_pred)
    cm_df = pd.DataFrame(cm, index=le.classes_, columns=le.classes_)
    cm_df.index.name = 'Actual \\ Predicted'
    cm_df.to_csv(os.path.join(OUT, f'confusion_matrix_{name}.csv'))

    # Add predictions column
    pred_df[f'Pred_{name}'] = le.inverse_transform(y_pred)

# ── 6. Summary & Predictions CSV ─────────────────────────────────────────────
pd.DataFrame(summary_rows).to_csv(os.path.join(OUT, 'model_metrics_summary.csv'), index=False)
pred_df.to_csv(os.path.join(OUT, 'test_predictions.csv'), index=False)

# ── 7. Feature Importances (RF) ───────────────────────────────────────────────
rf = models['Random_Forest']
fi = (pd.Series(rf.feature_importances_, index=features)
        .sort_values(ascending=False)
        .reset_index())
fi.columns = ['Feature', 'Importance']
fi.to_csv(os.path.join(OUT, 'feature_importances_rf.csv'), index=False)

# ── Summary ───────────────────────────────────────────────────────────────────
print("\nDone! All CSVs saved to:", OUT)
files = [
    ('feature_matrix.csv',                    len(df)),
    ('class_distribution.csv',                len(cls_dist)),
    ('model_metrics_summary.csv',             len(summary_rows)),
    ('classification_report_<model>.csv',     '4 files'),
    ('confusion_matrix_<model>.csv',          '4 files'),
    ('feature_importances_rf.csv',            len(fi)),
    ('test_predictions.csv',                  len(pred_df)),
]
for fname, rows in files:
    print(f"  {fname:<45} {rows} rows")
