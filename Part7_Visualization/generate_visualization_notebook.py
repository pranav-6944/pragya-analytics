import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Part 7: Visualization Dashboard
## Comprehensive Academic Analytics Charts
All required visualizations in one notebook:
1. Confusion Matrix (Classification)
2. Cluster Plots (K-Means + PCA)
3. GPA Distribution Graphs
4. Attendance vs Performance Charts"""

code_1 = """import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import seaborn as sns
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
import warnings
warnings.filterwarnings('ignore')

# Global style
plt.rcParams.update({'font.family': 'DejaVu Sans', 'figure.dpi': 120})
sns.set_theme(style='whitegrid', palette='muted')

print("Ready.")
"""

text_2 = "## Step 1: Load & Prepare Data"

code_2 = """FILE = r'c:\\Users\\prana_b2roblq\\Downloads\\university Analytics\\University_Management_Curation_Project.xlsx'
xl  = pd.ExcelFile(FILE)

students    = xl.parse('students')
courses     = xl.parse('courses')
enrollments = xl.parse('enrollments')
attendance  = xl.parse('attendance')
grades      = xl.parse('grades')

# Standardise grades
gmap = {'A':4.0,'B':3.0,'C':2.0,'D':1.0,'F':0.0,'P':4.0}
def sg(g):
    s = str(g).strip().upper().replace('+','').replace('-','')
    if s in gmap: return gmap[s]
    try:
        v=float(s); return min(v/25,4.0) if v>4 else v
    except: return np.nan

grades['gpa'] = grades['grade'].apply(sg)
grades['gpa'] = grades.groupby('course_id')['gpa'].transform(lambda x: x.fillna(x.median()))
grades['gpa'] = grades['gpa'].fillna(2.0)
grades['pass'] = (grades['gpa'] >= 1.0).astype(int)

# Attendance
attendance['present'] = attendance['status'].apply(
    lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
att = (attendance.groupby('student_id')
       .agg(total=('present','count'), attended=('present','sum')).reset_index())
att['att_pct'] = att['attended'] / att['total'] * 100

# GPA & pass rate per student
s_gpa  = grades.groupby('student_id')['gpa'].mean().reset_index().rename(columns={'gpa':'GPA'})
s_pass = grades.groupby('student_id')['pass'].mean().reset_index().rename(columns={'pass':'pass_rate'})

# Course load
courses['credits'] = pd.to_numeric(courses['credits'], errors='coerce').fillna(3)
enr    = enrollments.merge(courses[['course_id','credits']], on='course_id', how='left')
s_load = enr.groupby('student_id')['credits'].sum().reset_index().rename(columns={'credits':'course_load'})

# Merge
df = students[['student_id']].merge(s_gpa, on='student_id', how='left')
df = df.merge(att[['student_id','att_pct']], on='student_id', how='left')
df = df.merge(s_pass, on='student_id', how='left')
df = df.merge(s_load, on='student_id', how='left')
for c in ['GPA','att_pct','pass_rate','course_load']:
    df[c] = df[c].fillna(df[c].median())

df['internal_marks'] = df['GPA'] * 25

# Target for classification
def result(m):
    if m >= 75: return 'Distinction'
    elif m >= 40: return 'Pass'
    return 'Fail'
df['Result'] = df['internal_marks'].apply(result)

print("Data ready.", df.shape)
"""

text_3 = "## Chart 1: Confusion Matrix (Random Forest - 4 Classes)"

code_3 = """feats = ['att_pct','internal_marks','course_load','pass_rate']
X = df[feats]
le = LabelEncoder()
y  = le.fit_transform(df['Result'])

X_tr, X_te, y_tr, y_te = train_test_split(X, y, test_size=0.2,
                                            random_state=42, stratify=y)
rf = RandomForestClassifier(n_estimators=100, random_state=42)
rf.fit(X_tr, y_tr)
y_pred = rf.predict(X_te)

cm = confusion_matrix(y_te, y_pred)

fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# Heatmap
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[0],
            xticklabels=le.classes_, yticklabels=le.classes_,
            linewidths=0.5, linecolor='white', annot_kws={'size':14})
axes[0].set_title('Confusion Matrix - Random Forest', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Predicted Label', fontsize=12)
axes[0].set_ylabel('True Label', fontsize=12)

# Normalised version
cm_norm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
sns.heatmap(cm_norm, annot=True, fmt='.2f', cmap='RdYlGn', ax=axes[1],
            xticklabels=le.classes_, yticklabels=le.classes_,
            linewidths=0.5, linecolor='white', annot_kws={'size':13}, vmin=0, vmax=1)
axes[1].set_title('Normalised Confusion Matrix', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Predicted Label', fontsize=12)
axes[1].set_ylabel('True Label', fontsize=12)

plt.tight_layout()
plt.savefig('viz_confusion_matrix.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 1 saved.")
"""

text_4 = "## Chart 2: K-Means Cluster Plots (PCA 2D + Feature Scatter)"

code_4 = """km_feats = ['GPA','att_pct','course_load','pass_rate']
X_km  = StandardScaler().fit_transform(df[km_feats])
km    = KMeans(n_clusters=4, random_state=42, n_init=10)
df['Cluster'] = km.fit_predict(X_km)

# Assign risk labels by GPA rank
cl_gpa = df.groupby('Cluster')['GPA'].mean().sort_values(ascending=False)
label_map = {cl_gpa.index[0]: 'High Achievers',
             cl_gpa.index[1]: 'Average Performers',
             cl_gpa.index[2]: 'Struggling Students',
             cl_gpa.index[3]: 'At-Risk Students'}
df['Segment'] = df['Cluster'].map(label_map)

pca = PCA(n_components=2, random_state=42)
pcs = pca.fit_transform(X_km)
df['PC1'] = pcs[:,0]; df['PC2'] = pcs[:,1]

PALETTE = {'High Achievers':'#2A9D8F','Average Performers':'#457B9D',
           'Struggling Students':'#E9C46A','At-Risk Students':'#E63946'}

fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# PCA scatter
for seg, color in PALETTE.items():
    mask = df['Segment'] == seg
    axes[0].scatter(df.loc[mask,'PC1'], df.loc[mask,'PC2'],
                    c=color, label=seg, alpha=0.55, s=18, edgecolors='none')
axes[0].set_title('K-Means Clusters (PCA 2D Projection)', fontsize=14, fontweight='bold')
axes[0].set_xlabel(f"PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% var)", fontsize=11)
axes[0].set_ylabel(f"PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% var)", fontsize=11)
axes[0].legend(fontsize=10, title='Segment')
axes[0].grid(True, alpha=0.2)

# GPA vs Attendance scatter coloured by segment
for seg, color in PALETTE.items():
    mask = df['Segment'] == seg
    axes[1].scatter(df.loc[mask,'att_pct'], df.loc[mask,'GPA'],
                    c=color, label=seg, alpha=0.4, s=15, edgecolors='none')
axes[1].set_title('Attendance vs GPA by Segment', fontsize=14, fontweight='bold')
axes[1].set_xlabel('Attendance %', fontsize=12)
axes[1].set_ylabel('GPA', fontsize=12)
axes[1].legend(fontsize=10, title='Segment')
axes[1].axhline(y=1.5, color='red', linestyle='--', alpha=0.6, label='Risk GPA=1.5')
axes[1].grid(True, alpha=0.2)

plt.tight_layout()
plt.savefig('viz_cluster_plots.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 2 saved.")
"""

text_5 = "## Chart 3: GPA Distribution Graphs (4-Panel)"

code_5 = """fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 3a: Overall GPA histogram
axes[0,0].hist(df['GPA'], bins=40, color='#457B9D', edgecolor='white', alpha=0.85)
axes[0,0].axvline(df['GPA'].mean(), color='red', linestyle='--', linewidth=2,
                   label=f"Mean = {df['GPA'].mean():.2f}")
axes[0,0].axvline(df['GPA'].median(), color='orange', linestyle='--', linewidth=2,
                   label=f"Median = {df['GPA'].median():.2f}")
axes[0,0].set_title('Overall GPA Distribution', fontsize=13, fontweight='bold')
axes[0,0].set_xlabel('GPA'); axes[0,0].set_ylabel('Count')
axes[0,0].legend()

# 3b: GPA by Result category (violin)
result_order = ['Distinction','Pass','Fail']
result_colors = ['#2A9D8F','#457B9D','#E63946']
for i, (res, col) in enumerate(zip(result_order, result_colors)):
    sub = df[df['Result']==res]['GPA']
    axes[0,1].violinplot([sub.values], positions=[i], showmedians=True,
                          widths=0.6)
axes[0,1].set_xticks([0,1,2])
axes[0,1].set_xticklabels(result_order)
axes[0,1].set_title('GPA by Result Category (Violin)', fontsize=13, fontweight='bold')
axes[0,1].set_ylabel('GPA')

# 3c: GPA by Segment (box)
sns.boxplot(data=df, x='Segment', y='GPA', ax=axes[1,0],
            palette=PALETTE, order=list(PALETTE.keys()), linewidth=1.2)
axes[1,0].set_title('GPA by Student Segment (Box)', fontsize=13, fontweight='bold')
axes[1,0].set_xlabel(''); axes[1,0].set_ylabel('GPA')
axes[1,0].tick_params(axis='x', rotation=15)

# 3d: Cumulative GPA distribution (CDF)
sorted_gpa = np.sort(df['GPA'].values)
cdf = np.arange(1, len(sorted_gpa)+1) / len(sorted_gpa)
axes[1,1].plot(sorted_gpa, cdf, color='#E63946', linewidth=2)
axes[1,1].axvline(x=1.5, color='orange', linestyle='--', label='Risk threshold (1.5)')
axes[1,1].axvline(x=2.0, color='green', linestyle='--', label='Pass threshold (2.0)')
axes[1,1].set_title('Cumulative GPA Distribution (CDF)', fontsize=13, fontweight='bold')
axes[1,1].set_xlabel('GPA'); axes[1,1].set_ylabel('Cumulative Proportion')
axes[1,1].legend(fontsize=10)
axes[1,1].grid(True, alpha=0.3)

plt.suptitle('GPA Distribution Analysis', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('viz_gpa_distributions.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 3 saved.")
"""

text_6 = "## Chart 4: Attendance vs Performance (4-Panel)"

code_6 = """fig, axes = plt.subplots(2, 2, figsize=(14, 10))

# 4a: Attendance distribution histogram
axes[0,0].hist(df['att_pct'], bins=40, color='#2A9D8F', edgecolor='white', alpha=0.85)
axes[0,0].axvline(df['att_pct'].mean(), color='red', linestyle='--', linewidth=2,
                   label=f"Mean = {df['att_pct'].mean():.1f}%")
axes[0,0].axvline(50, color='orange', linestyle='--', linewidth=2, label='50% threshold')
axes[0,0].set_title('Attendance % Distribution', fontsize=13, fontweight='bold')
axes[0,0].set_xlabel('Attendance %'); axes[0,0].set_ylabel('Count')
axes[0,0].legend()

# 4b: Scatter Attendance vs GPA with trend line
axes[0,1].scatter(df['att_pct'], df['GPA'], alpha=0.2, s=10,
                   color='#457B9D', edgecolors='none')
z = np.polyfit(df['att_pct'], df['GPA'], 1)
p = np.poly1d(z)
x_line = np.linspace(df['att_pct'].min(), df['att_pct'].max(), 200)
axes[0,1].plot(x_line, p(x_line), color='#E63946', linewidth=2.5, label='Trend')
axes[0,1].set_title('Attendance vs GPA (Scatter + Trend)', fontsize=13, fontweight='bold')
axes[0,1].set_xlabel('Attendance %'); axes[0,1].set_ylabel('GPA')
axes[0,1].legend()
axes[0,1].grid(True, alpha=0.2)

# 4c: Avg GPA by attendance bucket
df['att_bucket'] = pd.cut(df['att_pct'],
                           bins=[0,25,50,75,100],
                           labels=['0-25%','25-50%','50-75%','75-100%'])
bucket_gpa = df.groupby('att_bucket', observed=True)['GPA'].mean()
bars = axes[1,0].bar(bucket_gpa.index.astype(str), bucket_gpa.values,
                      color=['#E63946','#E9C46A','#457B9D','#2A9D8F'],
                      edgecolor='black', alpha=0.9)
axes[1,0].set_title('Avg GPA by Attendance Bucket', fontsize=13, fontweight='bold')
axes[1,0].set_xlabel('Attendance Range'); axes[1,0].set_ylabel('Average GPA')
for bar, v in zip(bars, bucket_gpa.values):
    axes[1,0].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01,
                    f'{v:.2f}', ha='center', fontsize=11, fontweight='bold')
axes[1,0].set_ylim(0, 3.0)
axes[1,0].grid(axis='y', alpha=0.3)

# 4d: Pass Rate by attendance bucket
bucket_pass = df.groupby('att_bucket', observed=True)['pass_rate'].mean() * 100
bars2 = axes[1,1].bar(bucket_pass.index.astype(str), bucket_pass.values,
                       color=['#E63946','#E9C46A','#457B9D','#2A9D8F'],
                       edgecolor='black', alpha=0.9)
axes[1,1].set_title('Pass Rate % by Attendance Bucket', fontsize=13, fontweight='bold')
axes[1,1].set_xlabel('Attendance Range'); axes[1,1].set_ylabel('Pass Rate %')
for bar, v in zip(bars2, bucket_pass.values):
    axes[1,1].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.5,
                    f'{v:.1f}%', ha='center', fontsize=10, fontweight='bold')
axes[1,1].set_ylim(0, 110)
axes[1,1].axhline(y=75, color='red', linestyle='--', alpha=0.7, label='75% target')
axes[1,1].legend()
axes[1,1].grid(axis='y', alpha=0.3)

plt.suptitle('Attendance vs Academic Performance Analysis', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('viz_attendance_vs_performance.png', dpi=150, bbox_inches='tight')
plt.show()
print("Chart 4 saved.")
"""

text_7 = "## Chart 5: Master Dashboard (All-in-One)"

code_7 = """fig = plt.figure(figsize=(20, 14))
gs  = gridspec.GridSpec(3, 3, figure=fig, hspace=0.45, wspace=0.35)

# Panel 1 - GPA Histogram
ax1 = fig.add_subplot(gs[0, 0])
ax1.hist(df['GPA'], bins=35, color='#457B9D', edgecolor='white', alpha=0.85)
ax1.axvline(df['GPA'].mean(), color='red', linestyle='--', linewidth=1.5)
ax1.set_title('GPA Distribution', fontweight='bold')
ax1.set_xlabel('GPA')

# Panel 2 - Attendance Histogram
ax2 = fig.add_subplot(gs[0, 1])
ax2.hist(df['att_pct'], bins=35, color='#2A9D8F', edgecolor='white', alpha=0.85)
ax2.axvline(50, color='red', linestyle='--', linewidth=1.5, label='50%')
ax2.set_title('Attendance Distribution', fontweight='bold')
ax2.set_xlabel('Attendance %'); ax2.legend()

# Panel 3 - Segment Pie
ax3 = fig.add_subplot(gs[0, 2])
sc = df['Segment'].value_counts()
ax3.pie(sc.values, labels=sc.index, autopct='%1.1f%%',
        colors=list(PALETTE.values()), startangle=90, textprops={'fontsize':9})
ax3.set_title('Student Segments', fontweight='bold')

# Panel 4 - Confusion Matrix
ax4 = fig.add_subplot(gs[1, 0])
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=ax4,
            xticklabels=le.classes_, yticklabels=le.classes_, annot_kws={'size':11})
ax4.set_title('Confusion Matrix (RF)', fontweight='bold')
ax4.set_xlabel('Predicted'); ax4.set_ylabel('Actual')

# Panel 5 - Cluster PCA
ax5 = fig.add_subplot(gs[1, 1])
for seg, color in PALETTE.items():
    mask = df['Segment']==seg
    ax5.scatter(df.loc[mask,'PC1'], df.loc[mask,'PC2'],
                c=color, alpha=0.4, s=10, label=seg, edgecolors='none')
ax5.set_title('Clusters (PCA 2D)', fontweight='bold')
ax5.set_xlabel('PC1'); ax5.set_ylabel('PC2')
ax5.legend(fontsize=7)

# Panel 6 - Attendance vs GPA scatter
ax6 = fig.add_subplot(gs[1, 2])
ax6.scatter(df['att_pct'], df['GPA'], alpha=0.15, s=8, color='#E9C46A', edgecolors='none')
ax6.plot(x_line, p(x_line), color='#E63946', linewidth=2)
ax6.set_title('Attendance vs GPA', fontweight='bold')
ax6.set_xlabel('Attendance %'); ax6.set_ylabel('GPA')

# Panel 7 - Avg GPA by bucket
ax7 = fig.add_subplot(gs[2, 0])
ax7.bar(bucket_gpa.index.astype(str), bucket_gpa.values,
        color=['#E63946','#E9C46A','#457B9D','#2A9D8F'], edgecolor='black')
ax7.set_title('Avg GPA by Attendance Bucket', fontweight='bold')
ax7.set_xlabel('Attendance Range'); ax7.set_ylabel('GPA')
ax7.set_ylim(0, 3.0)

# Panel 8 - Pass rate by bucket
ax8 = fig.add_subplot(gs[2, 1])
ax8.bar(bucket_pass.index.astype(str), bucket_pass.values,
        color=['#E63946','#E9C46A','#457B9D','#2A9D8F'], edgecolor='black')
ax8.set_title('Pass Rate by Attendance Bucket', fontweight='bold')
ax8.set_xlabel('Attendance Range'); ax8.set_ylabel('Pass Rate %')
ax8.set_ylim(0, 110)

# Panel 9 - GPA by Result box
ax9 = fig.add_subplot(gs[2, 2])
sns.boxplot(data=df, x='Result', y='GPA', ax=ax9,
            palette={'Distinction':'#2A9D8F','Pass':'#457B9D','Fail':'#E63946'},
            order=['Distinction','Pass','Fail'], linewidth=1)
ax9.set_title('GPA by Result Category', fontweight='bold')
ax9.set_xlabel('Result'); ax9.set_ylabel('GPA')

plt.suptitle('Part 7: Comprehensive Visualization Dashboard', fontsize=17, fontweight='bold', y=1.01)
plt.savefig('viz_master_dashboard.png', dpi=150, bbox_inches='tight')
plt.show()
print("Master dashboard saved.")
"""

text_8 = """## Summary of All Charts

| Chart | File | Content |
|---|---|---|
| 1 | `viz_confusion_matrix.png` | Raw + Normalised confusion matrices (RF) |
| 2 | `viz_cluster_plots.png` | PCA cluster scatter + Attendance vs GPA by segment |
| 3 | `viz_gpa_distributions.png` | Histogram, Violin, Box, CDF of GPA |
| 4 | `viz_attendance_vs_performance.png` | Attendance distribution, vs GPA scatter, bucket analysis |
| 5 | `viz_master_dashboard.png` | 9-panel combined dashboard (all charts at once) |"""

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
]

nb['cells'] = cells

with open('University_Visualization.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook 'University_Visualization.ipynb' generated.")
