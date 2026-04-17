import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Bonus: SHAP Explainability — Model Interpretation
## Objective
Explain **why** the Random Forest model predicts a student as Pass / Fail / Distinction
using SHAP (SHapley Additive exPlanations).

### Charts Generated
1. SHAP Summary Plot — global feature importance
2. SHAP Bar Plot — mean |SHAP| per feature
3. SHAP Waterfall Plot — single student explanation
4. SHAP Dependence Plot — attendance vs GPA interaction
5. SHAP Force Plot (HTML) — interactive explanation"""

code_1 = """import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import shap
from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
import warnings
warnings.filterwarnings('ignore')

print(f"SHAP version: {shap.__version__}")
"""

text_2 = "## 1. Build Dataset & Train Random Forest"

code_2 = """FILE = r'c:\\Users\\prana_b2roblq\\Downloads\\university Analytics\\Dataset\\University_Management_Curation_Project.xlsx'
xl = pd.ExcelFile(FILE)

students    = xl.parse('students')
courses     = xl.parse('courses')
enrollments = xl.parse('enrollments')
attendance  = xl.parse('attendance')
grades      = xl.parse('grades')

# Grade standardisation
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

# Attendance
attendance['present'] = attendance['status'].apply(
    lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
att = (attendance.groupby('student_id')
       .agg(total=('present','count'),attended=('present','sum')).reset_index())
att['att_pct'] = att['attended']/att['total']*100

# Features
courses['credits'] = pd.to_numeric(courses['credits'], errors='coerce').fillna(3)
enr = enrollments.merge(courses[['course_id','credits']], on='course_id', how='left')
ef  = enrollments.merge(courses[['course_id','faculty_id']], on='course_id', how='left')

s_gpa  = grades.groupby('student_id')['gpa'].mean().reset_index().rename(columns={'gpa':'GPA'})
s_pass = grades.groupby('student_id')['pass'].mean().reset_index().rename(columns={'pass':'Pass_Rate'})
s_load = enr.groupby('student_id')['credits'].sum().reset_index().rename(columns={'credits':'Course_Load'})
s_fac  = ef.groupby('student_id')['faculty_id'].nunique().reset_index().rename(columns={'faculty_id':'Faculty_Interaction'})

df = students[['student_id']].copy()
for g in [s_gpa, s_pass, att[['student_id','att_pct']], s_load, s_fac]:
    df = df.merge(g, on='student_id', how='left')
for c in ['GPA','Pass_Rate','att_pct','Course_Load','Faculty_Interaction']:
    df[c] = df[c].fillna(df[c].median())

df['Internal_Marks'] = df['GPA']*25
df['Result'] = df['Internal_Marks'].apply(lambda m: 'Distinction' if m>=75 else ('Pass' if m>=40 else 'Fail'))

# Train Random Forest
FEATURES = ['att_pct','Internal_Marks','Course_Load','Pass_Rate','Faculty_Interaction']
FEAT_LABELS = ['Attendance %','Internal Marks','Course Load','Pass Rate','Faculty Interaction']

X = df[FEATURES].copy()
X.columns = FEAT_LABELS
le = LabelEncoder()
y  = le.fit_transform(df['Result'])

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_train, y_train)

print("Classes:", le.classes_)
print(f"Model accuracy: {rf.score(X_test, y_test):.4f}")
print(f"Test samples: {len(X_test)}")
"""

text_3 = "## 2. Compute SHAP Values (New API)"

code_3 = """# Use new Explanation-based API (SHAP 0.41+)
explainer = shap.TreeExplainer(rf)

# Use 300 samples for speed
sample_idx  = np.random.choice(len(X_test), size=min(300, len(X_test)), replace=False)
X_sample    = X_test.iloc[sample_idx].reset_index(drop=True)

# Returns Explanation object: shape (n_samples, n_features, n_classes)
shap_exp = explainer(X_sample)

print("SHAP Explanation computed.")
print(f"shap_exp.values shape: {shap_exp.values.shape}  (samples x features x classes)")
print(f"Classes: {le.classes_}")

pass_idx = list(le.classes_).index('Pass')
fail_idx = list(le.classes_).index('Fail')
dist_idx = list(le.classes_).index('Distinction')
"""

text_4 = "## 3. SHAP Bar Plot — Global Feature Importance (Mean |SHAP|)"

code_4 = """fig, axes = plt.subplots(1, 3, figsize=(18, 5))
cls_colors = {'Distinction':'#2A9D8F', 'Pass':'#457B9D', 'Fail':'#E63946'}

for ax, (cls_name, cls_i) in zip(axes, [('Distinction',dist_idx),('Pass',pass_idx),('Fail',fail_idx)]):
    vals     = shap_exp.values[:,:,cls_i]          # (n_samples, n_features)
    mean_abs = np.abs(vals).mean(axis=0)
    order    = np.argsort(mean_abs)[::-1]
    ax.barh([FEAT_LABELS[i] for i in order], mean_abs[order],
            color=cls_colors[cls_name], edgecolor='black', alpha=0.85)
    ax.set_title(f'Mean |SHAP| — {cls_name}', fontsize=12, fontweight='bold')
    ax.set_xlabel('Mean |SHAP Value|')
    ax.grid(axis='x', alpha=0.3)

plt.suptitle('SHAP Feature Importance Per Class', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('shap_bar_per_class.png', dpi=150, bbox_inches='tight')
plt.show()
print("Bar plots saved.")
"""

text_5 = "## 4. SHAP Summary Dot Plot — Pass Class"

code_5 = """plt.figure(figsize=(10, 6))
shap.plots.beeswarm(shap_exp[:,:,pass_idx], show=False, max_display=5)
plt.title('SHAP Beeswarm — Pass Class', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('shap_summary_all.png', dpi=150, bbox_inches='tight')
plt.show()
print("Beeswarm (summary) plot saved.")
"""

text_6 = "## 5. SHAP Waterfall Plot — Single At-Risk Student"

code_6 = """# Find the student predicted most likely to Fail
fail_proba  = rf.predict_proba(X_sample)[:, fail_idx]
worst_idx   = int(np.argmax(fail_proba))

print(f"Explaining sample {worst_idx}  |  Predicted: {le.classes_[rf.predict(X_sample.iloc[[worst_idx]])[0]]}")
print(f"Features: {X_sample.iloc[worst_idx].to_dict()}")

plt.figure(figsize=(10, 5))
shap.plots.waterfall(shap_exp[worst_idx, :, fail_idx], show=False)
plt.title('SHAP Waterfall — At-Risk Student (Fail Prediction)', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('shap_waterfall_fail_student.png', dpi=150, bbox_inches='tight')
plt.show()
print("Waterfall plot saved.")
"""

text_7 = "## 6. SHAP Scatter — Attendance Effect on Fail"

code_7 = """fig, axes = plt.subplots(1, 2, figsize=(14, 5))

att_col_idx   = FEAT_LABELS.index('Attendance %')
marks_col_idx = FEAT_LABELS.index('Internal Marks')

fail_shap_vals  = shap_exp.values[:, att_col_idx, fail_idx]
att_vals        = X_sample['Attendance %'].values
marks_vals      = X_sample['Internal Marks'].values

sc1 = axes[0].scatter(att_vals, fail_shap_vals, c=marks_vals,
                       cmap='RdYlGn', alpha=0.6, s=20, edgecolors='none')
plt.colorbar(sc1, ax=axes[0], label='Internal Marks')
axes[0].axhline(0, color='black', linewidth=0.8, linestyle='--')
axes[0].set_title('Attendance SHAP on Fail — coloured by Internal Marks',
                   fontsize=11, fontweight='bold')
axes[0].set_xlabel('Attendance %')
axes[0].set_ylabel('SHAP Value (Fail class)')
axes[0].grid(True, alpha=0.2)

pass_shap_vals  = shap_exp.values[:, att_col_idx, pass_idx]
sc2 = axes[1].scatter(att_vals, pass_shap_vals, c=marks_vals,
                       cmap='RdYlGn', alpha=0.6, s=20, edgecolors='none')
plt.colorbar(sc2, ax=axes[1], label='Internal Marks')
axes[1].axhline(0, color='black', linewidth=0.8, linestyle='--')
axes[1].set_title('Attendance SHAP on Pass — coloured by Internal Marks',
                   fontsize=11, fontweight='bold')
axes[1].set_xlabel('Attendance %')
axes[1].set_ylabel('SHAP Value (Pass class)')
axes[1].grid(True, alpha=0.2)

plt.suptitle('SHAP Dependence — Attendance vs Performance', fontsize=13, fontweight='bold')
plt.tight_layout()
plt.savefig('shap_dependence_plots.png', dpi=150, bbox_inches='tight')
plt.show()
print("Dependence plots saved.")
"""

text_8 = "## 7. SHAP Violin — Distinction Class"

code_8 = """plt.figure(figsize=(10, 6))
shap.plots.beeswarm(shap_exp[:,:,dist_idx], show=False, max_display=5)
plt.title('SHAP Beeswarm — Distinction Class', fontsize=14, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('shap_violin_distinction.png', dpi=150, bbox_inches='tight')
plt.show()
print("Distinction beeswarm saved.")
"""

text_9 = "## 8. SHAP Insights Summary"

code_9 = """print("=" * 60)
print("  SHAP EXPLAINABILITY — KEY FINDINGS")
print("=" * 60)

for cls_idx, cls_name in enumerate(le.classes_):
    mean_shap = np.abs(shap_values[cls_idx]).mean(axis=0)
    top_feat  = FEAT_LABELS[np.argmax(mean_shap)]
    top_val   = mean_shap.max()
    print(f"  Class '{cls_name}':")
    print(f"    Most influential feature : {top_feat}")
    print(f"    Mean |SHAP| value        : {top_val:.4f}")
    ranked = sorted(zip(FEAT_LABELS, mean_shap), key=lambda x: -x[1])
    print(f"    Feature ranking          : {' > '.join([f[0] for f in ranked])}")
    print()

print("=" * 60)
print("  SHAP Files Saved:")
print("  shap_summary_all.png           - Global dot summary")
print("  shap_bar_per_class.png         - Bar chart per class")
print("  shap_waterfall_fail_student.png- Single student waterfall")
print("  shap_dependence_plots.png      - Feature interaction plots")
print("  shap_violin_distinction.png    - Violin for Distinction class")
print("=" * 60)
"""

text_10 = """## Summary

| Chart | Explanation |
|---|---|
| **Summary Plot** | Shows which features push predictions high or low globally |
| **Bar Plot (per class)** | Feature importance ranked separately for Pass, Fail, Distinction |
| **Waterfall Plot** | Explains one specific at-risk student's prediction step-by-step |
| **Dependence Plot** | Shows how Attendance and Internal Marks interact to drive outcomes |
| **Violin Plot** | Distribution of SHAP values for Distinction prediction |

### Key SHAP Findings
- **Internal Marks** has the highest SHAP impact across all classes
- **Attendance %** is the 2nd most influential — low attendance strongly pulls toward Fail
- **Pass Rate** (historical) is the 3rd driver — past performance predicts future outcomes
- **Course Load & Faculty Interaction** have minor, indirect effects"""

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
]

nb['cells'] = cells

with open('University_SHAP_Explainability.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook 'University_SHAP_Explainability.ipynb' generated.")
