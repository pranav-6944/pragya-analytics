import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Part 6: Advanced Analytics - Unified Academic Intelligence System
## Objective
Combine insights from **Association Rule Mining**, **Classification**, and **Clustering**
to produce a comprehensive academic risk and performance dashboard.

### Three Core Analyses
1. **At-Risk Student Identification** — Cross-validated using ANN dropout risk + KMeans cluster labels
2. **High-Performing Departments** — Leveraging ARM department rules + pass rate metrics
3. **Course Difficulty Bottlenecks** — ARM failure rules + GPA distribution per course"""

code_1 = """import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.preprocessing import MinMaxScaler, StandardScaler
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules
import warnings
warnings.filterwarnings('ignore')

print("Libraries loaded.")
"""

text_2 = "## 1. Load & Rebuild All Features (Unified Dataset)"

code_2 = """file_path = r'c:\\Users\\prana_b2roblq\\Downloads\\university Analytics\\University_Management_Curation_Project.xlsx'
xl = pd.ExcelFile(file_path)

students    = xl.parse('students')
courses     = xl.parse('courses')
faculty     = xl.parse('faculty')
departments = xl.parse('departments')
enrollments = xl.parse('enrollments')
attendance  = xl.parse('attendance')
grades      = xl.parse('grades')

# -- Standardise grades --
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

# -- Student GPA & Historical pass rate --
student_gpa  = grades.groupby('student_id')['gpa'].mean().reset_index().rename(columns={'gpa':'GPA'})
hist_pass    = grades.groupby('student_id')['pass'].mean().reset_index().rename(columns={'pass':'hist_pass_rate'})

# -- Attendance --
attendance['present'] = attendance['status'].apply(
    lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
att = (attendance.groupby('student_id')
       .agg(total=('present','count'), attended=('present','sum')).reset_index())
att['att_pct'] = att['attended'] / att['total'] * 100

# -- Course load --
courses['credits'] = pd.to_numeric(courses['credits'], errors='coerce').fillna(3)
enr = enrollments.merge(courses[['course_id','credits','department_id']], on='course_id', how='left')
course_load = enr.groupby('student_id')['credits'].sum().reset_index().rename(columns={'credits':'course_load'})

# -- Faculty interaction --
enr_fac = enrollments.merge(courses[['course_id','faculty_id']], on='course_id', how='left')
fac_int = enr_fac.groupby('student_id')['faculty_id'].nunique().reset_index().rename(columns={'faculty_id':'fac_interaction'})

# -- Merge unified student table --
df = students[['student_id']].copy()
for grp in [student_gpa, hist_pass, att[['student_id','att_pct']], course_load, fac_int]:
    df = df.merge(grp, on='student_id', how='left')

for col in ['GPA','hist_pass_rate','att_pct','course_load','fac_interaction']:
    df[col] = df[col].fillna(df[col].median())

df['internal_marks'] = df['GPA'] * 25

print("Unified student dataset:", df.shape)
"""

text_3 = "## 2. LAYER 1 - At-Risk Student Identification"

code_3 = """# ── ANN Dropout Risk Score ──────────────────────────────────────────────────
features = ['att_pct','internal_marks','course_load','hist_pass_rate','fac_interaction']
df['dropout_risk'] = ((df['GPA'] < 1.5) | (df['att_pct'] < 50)).astype(int)

scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(df[features])

X_tr, X_te, y_tr, y_te = train_test_split(X_scaled, df['dropout_risk'],
                                            test_size=0.2, random_state=42, stratify=df['dropout_risk'])

ann = MLPClassifier(hidden_layer_sizes=(128, 64, 32), activation='relu',
                    solver='adam', max_iter=200, random_state=42)
ann.fit(X_tr, y_tr)
df['ANN_Risk_Score'] = ann.predict_proba(X_scaled)[:, 1]

# ── KMeans Cluster Risk Labels ───────────────────────────────────────────────
km_features = ['GPA','att_pct','course_load','hist_pass_rate']
X_km = StandardScaler().fit_transform(df[km_features])
km = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = km.fit_predict(X_km)

cluster_gpa = df.groupby('Cluster')['GPA'].mean()
risk_cluster = cluster_gpa.idxmin()  # lowest GPA = highest risk cluster

df['Cluster_Risk'] = (df['Cluster'] == risk_cluster).astype(int)

# ── Combined At-Risk Flag (ANN score > 0.5 OR risk cluster) ─────────────────
df['At_Risk'] = ((df['ANN_Risk_Score'] > 0.5) | (df['Cluster_Risk'] == 1)).astype(int)

at_risk_count = df['At_Risk'].sum()
print(f"Total Students    : {len(df)}")
print(f"At-Risk Students  : {at_risk_count} ({at_risk_count/len(df)*100:.1f}%)")
print(f"Safe Students     : {len(df) - at_risk_count}")
"""

text_4 = "## 3. At-Risk Dashboard Visualization"

code_4 = """fig, axes = plt.subplots(1, 3, figsize=(18, 6))

# GPA distribution: At-Risk vs Safe
axes[0].hist(df[df['At_Risk']==0]['GPA'], bins=30, alpha=0.7, color='#2A9D8F', label='Safe')
axes[0].hist(df[df['At_Risk']==1]['GPA'], bins=30, alpha=0.7, color='#E63946', label='At-Risk')
axes[0].set_title('GPA Distribution by Risk', fontsize=13, fontweight='bold')
axes[0].set_xlabel('GPA'); axes[0].set_ylabel('Count')
axes[0].legend()

# Attendance vs GPA scatter coloured by risk
sc = axes[1].scatter(df['att_pct'], df['GPA'], c=df['At_Risk'],
                     cmap='RdYlGn_r', alpha=0.4, s=10)
axes[1].set_title('Attendance vs GPA (Risk)', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Attendance %'); axes[1].set_ylabel('GPA')
plt.colorbar(sc, ax=axes[1], label='At-Risk')

# Risk breakdown pie
risk_counts = df['At_Risk'].value_counts()
axes[2].pie(risk_counts.values, labels=['Safe','At-Risk'],
            autopct='%1.1f%%', colors=['#2A9D8F','#E63946'], startangle=90,
            textprops={'fontsize':12})
axes[2].set_title('Student Risk Breakdown', fontsize=13, fontweight='bold')

plt.suptitle('LAYER 1: At-Risk Student Analysis', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('advanced_at_risk.png', dpi=150, bbox_inches='tight')
plt.show()
print("At-risk dashboard saved.")
"""

text_5 = "## 4. LAYER 2 - High-Performing Departments"

code_5 = """# Join grades -> courses -> departments
grade_dept = grades.merge(courses[['course_id','department_id']], on='course_id', how='left')

dept_stats = grade_dept.groupby('department_id').agg(
    avg_gpa    = ('gpa', 'mean'),
    pass_rate  = ('pass', 'mean'),
    total_records = ('student_id', 'count')
).reset_index()

dept_stats['pass_rate_pct'] = dept_stats['pass_rate'] * 100
dept_stats = dept_stats.sort_values('avg_gpa', ascending=False)

top5_dept    = dept_stats.head(5)
bottom5_dept = dept_stats.tail(5)

print("Top 5 High-Performing Departments:")
print(top5_dept[['department_id','avg_gpa','pass_rate_pct']].to_string(index=False))
print("\\nBottom 5 Departments (needs support):")
print(bottom5_dept[['department_id','avg_gpa','pass_rate_pct']].to_string(index=False))
"""

text_6 = "## 5. Department Performance Visualization"

code_6 = """fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Top 10 departments by GPA
top10 = dept_stats.head(10)
colors = ['#2A9D8F' if i < 5 else '#E9C46A' for i in range(len(top10))]
bars = axes[0].barh(top10['department_id'], top10['avg_gpa'], color=colors, edgecolor='black')
axes[0].set_title('Top 10 Departments by Avg GPA', fontsize=13, fontweight='bold')
axes[0].set_xlabel('Average GPA')
axes[0].axvline(x=dept_stats['avg_gpa'].mean(), color='red', linestyle='--', label=f'Mean GPA')
axes[0].legend()
for bar, v in zip(bars, top10['avg_gpa']):
    axes[0].text(bar.get_width()+0.01, bar.get_y()+bar.get_height()/2,
                 f'{v:.2f}', va='center', fontsize=9)

# Pass Rate by department (all)
dept_sorted_pass = dept_stats.sort_values('pass_rate_pct', ascending=False)
axes[1].bar(range(len(dept_sorted_pass)), dept_sorted_pass['pass_rate_pct'],
            color=['#2A9D8F' if v >= 75 else '#E63946' for v in dept_sorted_pass['pass_rate_pct']],
            edgecolor='none', alpha=0.8)
axes[1].axhline(y=75, color='orange', linestyle='--', label='75% threshold')
axes[1].set_title('Department Pass Rates', fontsize=13, fontweight='bold')
axes[1].set_xlabel('Department Index')
axes[1].set_ylabel('Pass Rate %')
axes[1].legend()

plt.suptitle('LAYER 2: Department Performance Analysis', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('advanced_dept_performance.png', dpi=150, bbox_inches='tight')
plt.show()
"""

text_7 = "## 6. LAYER 3 - Course Difficulty Bottlenecks"

code_7 = """# Course-level stats: avg GPA, pass rate, enrollment count
course_stats = grades.merge(courses[['course_id','credits','department_id']], on='course_id', how='left')
course_agg = course_stats.groupby('course_id').agg(
    avg_gpa    = ('gpa', 'mean'),
    pass_rate  = ('pass', 'mean'),
    enrollment = ('student_id', 'nunique'),
    avg_credits= ('credits', 'mean')
).reset_index()

course_agg['pass_rate_pct'] = course_agg['pass_rate'] * 100
course_agg['difficulty_score'] = (1 - course_agg['pass_rate']) * course_agg['avg_credits']

# Bottleneck courses: low pass rate + high credits
bottlenecks = course_agg.sort_values('difficulty_score', ascending=False).head(10)
easiest     = course_agg.sort_values('difficulty_score').head(10)

print("Top 10 Course Difficulty Bottlenecks:")
print(bottlenecks[['course_id','avg_gpa','pass_rate_pct','avg_credits','difficulty_score']].to_string(index=False))
"""

text_8 = "## 7. Course Bottleneck Visualization"

code_8 = """fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Difficulty score heatmap (top 15 hard courses)
hard = course_agg.sort_values('difficulty_score', ascending=False).head(15)
axes[0].barh(hard['course_id'], hard['difficulty_score'],
             color=['#E63946' if v > hard['difficulty_score'].median() else '#E9C46A' for v in hard['difficulty_score']],
             edgecolor='black')
axes[0].set_title('Top 15 Hardest Courses (Difficulty = Fail Rate x Credits)',
                  fontsize=12, fontweight='bold')
axes[0].set_xlabel('Difficulty Score')

# GPA vs Pass Rate scatter (all courses)
sc2 = axes[1].scatter(course_agg['avg_gpa'], course_agg['pass_rate_pct'],
                      c=course_agg['difficulty_score'], cmap='YlOrRd',
                      s=course_agg['enrollment']/3, alpha=0.7, edgecolors='gray', linewidths=0.3)
plt.colorbar(sc2, ax=axes[1], label='Difficulty Score')
axes[1].set_title('Course GPA vs Pass Rate (Size = Enrollment)', fontsize=12, fontweight='bold')
axes[1].set_xlabel('Average GPA')
axes[1].set_ylabel('Pass Rate %')
axes[1].axhline(y=60, color='red', linestyle='--', alpha=0.5, label='60% threshold')
axes[1].legend()

plt.suptitle('LAYER 3: Course Difficulty Bottleneck Analysis', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('advanced_course_bottlenecks.png', dpi=150, bbox_inches='tight')
plt.show()
"""

text_9 = "## 8. Combined Intelligence Dashboard"

code_9 = """fig = plt.figure(figsize=(20, 12))
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.4, wspace=0.35)

# Panel 1: Risk pie
ax1 = fig.add_subplot(gs[0, 0])
rc = df['At_Risk'].value_counts()
ax1.pie(rc.values, labels=['Safe','At-Risk'], autopct='%1.1f%%',
        colors=['#2A9D8F','#E63946'], startangle=90)
ax1.set_title('Student Risk Distribution', fontweight='bold')

# Panel 2: Top 5 Depts GPA bar
ax2 = fig.add_subplot(gs[0, 1])
ax2.bar(top5_dept['department_id'], top5_dept['avg_gpa'], color='#457B9D', edgecolor='black')
ax2.set_title('Top 5 Departments (GPA)', fontweight='bold')
ax2.set_ylabel('Avg GPA'); ax2.set_ylim(0, 4.2)
for i, (d, v) in enumerate(zip(top5_dept['department_id'], top5_dept['avg_gpa'])):
    ax2.text(i, v+0.05, f'{v:.2f}', ha='center', fontsize=9)

# Panel 3: Top 5 Bottleneck courses
ax3 = fig.add_subplot(gs[0, 2])
top5_hard = bottlenecks.head(5)
ax3.barh(top5_hard['course_id'], top5_hard['pass_rate_pct'], color='#E63946', edgecolor='black')
ax3.set_title('Hardest Courses (Pass Rate %)', fontweight='bold')
ax3.set_xlabel('Pass Rate %')
ax3.axvline(x=60, color='orange', linestyle='--')

# Panel 4: GPA histogram all students
ax4 = fig.add_subplot(gs[1, 0])
ax4.hist(df['GPA'], bins=30, color='#2A9D8F', edgecolor='black', alpha=0.8)
ax4.axvline(x=df['GPA'].mean(), color='red', linestyle='--', label=f"Mean={df['GPA'].mean():.2f}")
ax4.set_title('Overall GPA Distribution', fontweight='bold')
ax4.set_xlabel('GPA'); ax4.legend()

# Panel 5: At-risk by attendance bucket
ax5 = fig.add_subplot(gs[1, 1])
df['att_bucket'] = pd.cut(df['att_pct'], bins=[0,40,60,75,100], labels=['<40%','40-60%','60-75%','>75%'])
risk_by_att = df.groupby('att_bucket', observed=True)['At_Risk'].mean() * 100
ax5.bar(risk_by_att.index.astype(str), risk_by_att.values,
        color=['#E63946','#E9C46A','#457B9D','#2A9D8F'], edgecolor='black')
ax5.set_title('At-Risk Rate by Attendance Bucket', fontweight='bold')
ax5.set_ylabel('At-Risk %'); ax5.set_xlabel('Attendance Range')

# Panel 6: Dept pass rate bar (top 10)
ax6 = fig.add_subplot(gs[1, 2])
top10d = dept_stats.head(10)
ax6.bar(top10d['department_id'], top10d['pass_rate_pct'],
        color=['#2A9D8F' if v >= 75 else '#E9C46A' for v in top10d['pass_rate_pct']], edgecolor='black')
ax6.set_title('Top 10 Dept Pass Rates', fontweight='bold')
ax6.set_ylabel('Pass Rate %')
ax6.axhline(y=75, color='red', linestyle='--', alpha=0.7)

plt.suptitle('PART 6: Advanced Analytics - Unified Academic Intelligence Dashboard',
             fontsize=16, fontweight='bold', y=1.01)
plt.savefig('advanced_unified_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("Unified dashboard saved.")
"""

text_10 = "## 9. Key Insights Summary"

code_10 = """print("=" * 65)
print("   ADVANCED ANALYTICS - KEY FINDINGS SUMMARY")
print("=" * 65)

at_risk_total  = df['At_Risk'].sum()
at_risk_pct    = df['At_Risk'].mean() * 100
avg_gpa_risk   = df[df['At_Risk']==1]['GPA'].mean()
avg_att_risk   = df[df['At_Risk']==1]['att_pct'].mean()
best_dept      = top5_dept.iloc[0]
worst_dept     = bottom5_dept.iloc[-1]
hardest        = bottlenecks.iloc[0]
top3_hard      = ', '.join(bottlenecks.head(3)['course_id'].tolist())

print(f"[LAYER 1 - At-Risk Students]")
print(f"  Total At-Risk  : {at_risk_total} ({at_risk_pct:.1f}% of students)")
print(f"  Criteria       : ANN score > 0.5 OR lowest GPA cluster")
print(f"  Avg GPA (risk) : {avg_gpa_risk:.3f}")
print(f"  Avg Att (risk) : {avg_att_risk:.1f}%")
print()
print(f"[LAYER 2 - High-Performing Departments]")
print(f"  Best Dept  : {best_dept['department_id']} (GPA={best_dept['avg_gpa']:.3f}, Pass={best_dept['pass_rate_pct']:.1f}%)")
print(f"  Worst Dept : {worst_dept['department_id']} (GPA={worst_dept['avg_gpa']:.3f}, Pass={worst_dept['pass_rate_pct']:.1f}%)")
print()
print(f"[LAYER 3 - Course Difficulty Bottlenecks]")
print(f"  Hardest Course    : {hardest['course_id']} (Pass={hardest['pass_rate_pct']:.1f}%, Credits={hardest['avg_credits']:.1f})")
print(f"  Top 3 Bottlenecks : {top3_hard}")
print("=" * 65)
"""

text_11 = """## 10. Final Report

### Methodology
| Layer | Source Parts | Method |
|---|---|---|
| At-Risk Detection | Part 4 (Clustering) + Part 5 (ANN) | KMeans + MLP combined flag |
| Dept Performance | Part 2 (ARM dept rules) + Part 3 (Classification) | GPA + Pass rate aggregation |
| Course Bottlenecks | Part 2 (ARM failure rules) + Part 4 (Clustering) | Difficulty Score = Fail Rate x Credits |

### Actionable Recommendations
- **Intervene** with At-Risk students (low GPA + low attendance) before mid-semester
- **Reward** high-performing departments and replicate their practices
- **Redesign** bottleneck courses with high difficulty scores (tutorial support, grading review)
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

with open('University_Advanced_Analytics.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook 'University_Advanced_Analytics.ipynb' generated.")
