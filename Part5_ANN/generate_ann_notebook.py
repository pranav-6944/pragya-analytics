import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Part 5: ANN - Academic Performance Forecasting System
## Objective
Predict **Dropout Risk** (binary: At-Risk vs Safe) using a Feedforward Neural Network,
then compare with traditional ML models.

### Features Used
- Attendance Percentage
- Internal Marks (GPA x25)
- Course Load (total credits)
- Historical Performance (pass rate)
- Faculty Interaction (faculty count per student)

### Model Lineup
- Feedforward ANN (MLPClassifier - 3 hidden layers)
- Logistic Regression
- Random Forest
- Gradient Boosting (XGBoost equivalent)"""

code_1 = """import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.neural_network import MLPClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import (accuracy_score, classification_report,
                             confusion_matrix, roc_auc_score, roc_curve)
import warnings
warnings.filterwarnings('ignore')
print("Libraries loaded.")
"""

text_2 = "## 1. Feature Engineering"

code_2 = """file_path = r'c:\\Users\\prana_b2roblq\\Downloads\\university Analytics\\University_Management_Curation_Project.xlsx'
xl = pd.ExcelFile(file_path)

students    = xl.parse('students')
courses     = xl.parse('courses')
faculty     = xl.parse('faculty')
enrollments = xl.parse('enrollments')
attendance  = xl.parse('attendance')
grades      = xl.parse('grades')

# --- Internal Marks (GPA scaled 0-100) ---
grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'P': 4.0}
def std_grade(g):
    gs = str(g).strip().upper().replace('+','').replace('-','')
    if gs in grade_map: return grade_map[gs]
    try:
        v = float(gs); return min(v/25.0, 4.0) if v > 4.0 else v
    except: return np.nan

grades['gpa'] = grades['grade'].apply(std_grade)
grades['gpa'] = grades.groupby('course_id')['gpa'].transform(lambda x: x.fillna(x.median()))
grades['gpa'] = grades['gpa'].fillna(2.0)
grades['pass'] = (grades['gpa'] >= 1.0).astype(int)

student_gpa = grades.groupby('student_id')['gpa'].mean().reset_index().rename(columns={'gpa':'internal_marks'})
student_gpa['internal_marks'] *= 25   # scale to 100

# --- Historical Performance (pass rate per student) ---
hist_perf = grades.groupby('student_id')['pass'].mean().reset_index().rename(columns={'pass':'hist_pass_rate'})

# --- Attendance ---
attendance['present'] = attendance['status'].apply(lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
att = attendance.groupby('student_id').agg(total=('present','count'), attended=('present','sum')).reset_index()
att['attendance_pct'] = att['attended'] / att['total'] * 100

# --- Course Load (total enrolled credits) ---
courses['credits'] = pd.to_numeric(courses['credits'], errors='coerce').fillna(3)
enr = enrollments.merge(courses[['course_id','credits']], on='course_id', how='left')
course_load = enr.groupby('student_id')['credits'].sum().reset_index().rename(columns={'credits':'course_load'})

# --- Faculty Interaction (unique faculty count per student) ---
enr_fac = enrollments.merge(courses[['course_id','faculty_id']], on='course_id', how='left')
fac_interaction = enr_fac.groupby('student_id')['faculty_id'].nunique().reset_index().rename(columns={'faculty_id':'faculty_interaction'})

# --- Merge all ---
df = students[['student_id']].copy()
df = df.merge(student_gpa, on='student_id', how='left')
df = df.merge(hist_perf, on='student_id', how='left')
df = df.merge(att[['student_id','attendance_pct']], on='student_id', how='left')
df = df.merge(course_load, on='student_id', how='left')
df = df.merge(fac_interaction, on='student_id', how='left')

for col in ['internal_marks','hist_pass_rate','attendance_pct','course_load','faculty_interaction']:
    df[col] = df[col].fillna(df[col].median())

print("Feature matrix:", df.shape)
df.head()
"""

text_3 = "## 2. Target Variable - Dropout Risk"

code_3 = """# Dropout Risk: 1 if GPA < 1.5 (D/F level) OR attendance < 50%, else 0
gpa_raw = df['internal_marks'] / 25
df['dropout_risk'] = ((gpa_raw < 1.5) | (df['attendance_pct'] < 50)).astype(int)

print("Dropout Risk Distribution:")
print(df['dropout_risk'].value_counts())
print(f"Dropout Rate: {df['dropout_risk'].mean()*100:.1f}%")
"""

text_4 = "## 3. Normalize Data (MinMaxScaler)"

code_4 = """features = ['attendance_pct', 'internal_marks', 'course_load',
            'hist_pass_rate', 'faculty_interaction']

X = df[features]
y = df['dropout_risk']

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)
X_scaled_df = pd.DataFrame(X_scaled, columns=features)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y)

print(f"Train: {X_train.shape[0]} | Test: {X_test.shape[0]}")
print("Feature ranges after normalization (min, max):")
print(pd.DataFrame(X_scaled, columns=features).describe().loc[['min','max']])
"""

text_5 = "## 4. Build & Train Feedforward ANN"

code_5 = """# ANN: 3 hidden layers [128 -> 64 -> 32], ReLU activation, Adam optimizer
ann = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation='relu',
    solver='adam',
    learning_rate_init=0.001,
    max_iter=200,
    random_state=42,
    verbose=False
)

ann.fit(X_train, y_train)
ann_pred = ann.predict(X_test)
ann_prob = ann.predict_proba(X_test)[:, 1]

ann_acc = accuracy_score(y_test, ann_pred)
ann_auc = roc_auc_score(y_test, ann_prob)

print("ANN - Feedforward Neural Network")
print(f"Architecture: Input(5) -> 128 -> 64 -> 32 -> Output(2)")
print(f"Accuracy : {ann_acc:.4f}")
print(f"AUC-ROC  : {ann_auc:.4f}")
print()
print(classification_report(y_test, ann_pred, target_names=['Safe','At-Risk']))
"""

text_6 = "## 5. Training Loss Curve"

code_6 = """plt.figure(figsize=(9, 5))
plt.plot(ann.loss_curve_, color='#E63946', linewidth=2)
plt.title('ANN Training Loss Curve', fontsize=14, fontweight='bold')
plt.xlabel('Iterations (Epochs)', fontsize=12)
plt.ylabel('Loss', fontsize=12)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('ann_loss_curve.png', dpi=150, bbox_inches='tight')
plt.show()
print("Loss curve saved.")
"""

text_7 = "## 6. Compare with Traditional ML Models"

code_7 = """models = {
    'ANN (MLP)'           : ann,
    'Logistic Regression' : LogisticRegression(max_iter=500, random_state=42),
    'Random Forest'       : RandomForestClassifier(n_estimators=100, random_state=42),
    'Gradient Boosting'   : GradientBoostingClassifier(n_estimators=100, random_state=42)
}

# Train remaining models
for name, model in models.items():
    if name != 'ANN (MLP)':
        model.fit(X_train, y_train)

results = []
for name, model in models.items():
    y_pred = model.predict(X_test)
    y_prob = model.predict_proba(X_test)[:, 1]
    results.append({
        'Model'    : name,
        'Accuracy' : round(accuracy_score(y_test, y_pred), 4),
        'AUC-ROC'  : round(roc_auc_score(y_test, y_prob), 4),
        'F1-Score' : round(__import__('sklearn.metrics', fromlist=['f1_score']).f1_score(
                            y_test, y_pred, average='weighted', zero_division=0), 4)
    })

results_df = pd.DataFrame(results)
print(results_df.to_string(index=False))
"""

text_8 = "## 7. ROC Curve Comparison"

code_8 = """plt.figure(figsize=(9, 7))
colors = ['#E63946', '#457B9D', '#2A9D8F', '#E9C46A']

for (name, model), color in zip(models.items(), colors):
    y_prob = model.predict_proba(X_test)[:, 1]
    fpr, tpr, _ = roc_curve(y_test, y_prob)
    auc = roc_auc_score(y_test, y_prob)
    plt.plot(fpr, tpr, color=color, linewidth=2, label=f'{name} (AUC={auc:.3f})')

plt.plot([0,1],[0,1],'k--', alpha=0.4, label='Random')
plt.xlabel('False Positive Rate', fontsize=12)
plt.ylabel('True Positive Rate', fontsize=12)
plt.title('ROC Curve - All Models', fontsize=14, fontweight='bold')
plt.legend(loc='lower right', fontsize=10)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('roc_curves.png', dpi=150, bbox_inches='tight')
plt.show()
print("ROC curves saved.")
"""

text_9 = "## 8. ANN Confusion Matrix"

code_9 = """cm = confusion_matrix(y_test, ann_pred)
plt.figure(figsize=(6, 5))
sns.heatmap(cm, annot=True, fmt='d', cmap='Reds',
            xticklabels=['Safe','At-Risk'], yticklabels=['Safe','At-Risk'])
plt.title('ANN Confusion Matrix', fontsize=13, fontweight='bold')
plt.xlabel('Predicted'); plt.ylabel('Actual')
plt.tight_layout()
plt.savefig('ann_confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()
"""

text_10 = "## 9. Model Accuracy Comparison Chart"

code_10 = """palette = ['#E63946','#457B9D','#2A9D8F','#E9C46A']

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Accuracy
bars1 = axes[0].bar(results_df['Model'], results_df['Accuracy'], color=palette, edgecolor='black')
axes[0].set_ylim(0, 1.1)
axes[0].set_title('Model Accuracy', fontsize=13, fontweight='bold')
axes[0].set_ylabel('Accuracy')
axes[0].tick_params(axis='x', rotation=20)
for bar, v in zip(bars1, results_df['Accuracy']):
    axes[0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01, f'{v:.4f}', ha='center', fontsize=9)

# AUC-ROC
bars2 = axes[1].bar(results_df['Model'], results_df['AUC-ROC'], color=palette, edgecolor='black')
axes[1].set_ylim(0, 1.1)
axes[1].set_title('Model AUC-ROC', fontsize=13, fontweight='bold')
axes[1].set_ylabel('AUC-ROC')
axes[1].tick_params(axis='x', rotation=20)
for bar, v in zip(bars2, results_df['AUC-ROC']):
    axes[1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01, f'{v:.4f}', ha='center', fontsize=9)

plt.suptitle('ANN vs Traditional Models', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('model_comparison.png', dpi=150, bbox_inches='tight')
plt.show()
"""

text_11 = """## 10. Summary Report

| Model | Role | Strength |
|---|---|---|
| **ANN (MLP 128-64-32)** | Primary forecaster | Learns complex non-linear patterns |
| Logistic Regression | Baseline | Fast, interpretable |
| Random Forest | Robust baseline | Handles noise well |
| Gradient Boosting | Strong competitor | Best accuracy typically |

### Key Findings
- ANN architecture: **Input(5) -> 128 -> 64 -> 32 -> Output(2)**
- MinMaxScaler normalization ensures all features in [0,1] range
- Dropout risk defined as: **GPA < 1.5 OR Attendance < 50%**
- ANN competes strongly with ensemble methods on this dataset
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
    nbf.v4.new_code_cell(code_7),
    nbf.v4.new_markdown_cell(text_8),
    nbf.v4.new_code_cell(code_8),
    nbf.v4.new_markdown_cell(text_9),
    nbf.v4.new_code_cell(code_9),
    nbf.v4.new_markdown_cell(text_10),
    nbf.v4.new_code_cell(code_10),
    nbf.v4.new_markdown_cell(text_11),
]

nb['cells'] = cells

with open('University_ANN.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook 'University_ANN.ipynb' generated.")
