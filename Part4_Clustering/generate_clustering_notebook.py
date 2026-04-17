import nbformat as nbf

nb = nbf.v4.new_notebook()

text_1 = """# Part 4: Clustering - Student Segmentation & Risk Analysis
## Objective
Segment students into meaningful groups using:
- GPA (Grade Point Average)
- Attendance Percentage
- Credits Completed
- Study Load (proxy for study patterns)

### Techniques
- K-Means Clustering (with Elbow Method)
- Hierarchical (Agglomerative) Clustering (with Dendrogram)"""

code_1 = """import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage
import warnings
warnings.filterwarnings('ignore')
print("Libraries loaded.")
"""

text_2 = "## 1. Feature Engineering - Build Student-Level Dataset"

code_2 = """file_path = r'c:\\Users\\prana_b2roblq\\Downloads\\university Analytics\\University_Management_Curation_Project.xlsx'
xl = pd.ExcelFile(file_path)

students    = xl.parse('students')
courses     = xl.parse('courses')
enrollments = xl.parse('enrollments')
attendance  = xl.parse('attendance')
grades      = xl.parse('grades')

# --- GPA ---
grade_map = {'A': 4.0, 'B': 3.0, 'C': 2.0, 'D': 1.0, 'F': 0.0, 'P': 4.0}
def std_grade(g):
    gs = str(g).strip().upper().replace('+','').replace('-','')
    if gs in grade_map: return grade_map[gs]
    try:
        v = float(gs); return min(v/25.0,4.0) if v>4.0 else v
    except: return np.nan

grades['gpa_score'] = grades['grade'].apply(std_grade)
grades['gpa_score'] = grades.groupby('course_id')['gpa_score'].transform(lambda x: x.fillna(x.median()))
grades['gpa_score'] = grades['gpa_score'].fillna(2.0)
student_gpa = grades.groupby('student_id')['gpa_score'].mean().reset_index().rename(columns={'gpa_score':'GPA'})

# --- Attendance Percentage ---
attendance['present'] = attendance['status'].apply(lambda x: 1 if str(x).lower().strip() in ['present','late','p'] else 0)
att = attendance.groupby('student_id').agg(total=('present','count'), attended=('present','sum')).reset_index()
att['Attendance_Pct'] = att['attended'] / att['total'] * 100

# --- Credits Completed (passed courses only) ---
grades['pass'] = (grades['gpa_score'] >= 1.0).astype(int)
passed = grades[grades['pass']==1].merge(courses[['course_id','credits']], on='course_id', how='left')
passed['credits'] = pd.to_numeric(passed['credits'], errors='coerce').fillna(3)
credits_done = passed.groupby('student_id')['credits'].sum().reset_index().rename(columns={'credits':'Credits_Completed'})

# --- Study Load (total enrolled credits) ---
enr = enrollments.merge(courses[['course_id','credits']], on='course_id', how='left')
enr['credits'] = pd.to_numeric(enr['credits'], errors='coerce').fillna(3)
study_load = enr.groupby('student_id')['credits'].sum().reset_index().rename(columns={'credits':'Study_Load'})

# --- Merge ---
df = students[['student_id']].merge(student_gpa, on='student_id', how='left')
df = df.merge(att[['student_id','Attendance_Pct']], on='student_id', how='left')
df = df.merge(credits_done, on='student_id', how='left')
df = df.merge(study_load, on='student_id', how='left')

for col in ['GPA','Attendance_Pct','Credits_Completed','Study_Load']:
    df[col] = df[col].fillna(df[col].median())

print("Feature matrix shape:", df.shape)
df.describe()
"""

text_3 = "## 2. Feature Scaling"

code_3 = """features = ['GPA', 'Attendance_Pct', 'Credits_Completed', 'Study_Load']
X = df[features].values

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
print("Scaling done. Shape:", X_scaled.shape)
"""

text_4 = "## 3. K-Means - Elbow Method to Find Optimal k"

code_4 = """inertias = []
silhouettes = []
k_range = range(2, 11)

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, km.labels_))

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Elbow curve
axes[0].plot(list(k_range), inertias, 'bo-', linewidth=2, markersize=8)
axes[0].axvline(x=4, color='red', linestyle='--', label='Optimal k=4')
axes[0].set_xlabel('Number of Clusters (k)', fontsize=12)
axes[0].set_ylabel('Inertia (WCSS)', fontsize=12)
axes[0].set_title('Elbow Method', fontsize=14, fontweight='bold')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# Silhouette scores
axes[1].plot(list(k_range), silhouettes, 'gs-', linewidth=2, markersize=8)
axes[1].set_xlabel('Number of Clusters (k)', fontsize=12)
axes[1].set_ylabel('Silhouette Score', fontsize=12)
axes[1].set_title('Silhouette Scores', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('elbow_silhouette.png', dpi=150, bbox_inches='tight')
plt.show()

opt_k = k_range.start + silhouettes.index(max(silhouettes))
print(f"Optimal k by Silhouette: {opt_k}")
print(f"Best Silhouette Score  : {max(silhouettes):.4f}")
"""

text_5 = "## 4. K-Means Clustering (k=4)"

code_5 = """K = 4
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
df['KMeans_Cluster'] = kmeans.fit_predict(X_scaled)

# PCA for 2D visualization
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df['PCA1'] = X_pca[:,0]
df['PCA2'] = X_pca[:,1]

palette = ['#E63946','#457B9D','#2A9D8F','#E9C46A']

plt.figure(figsize=(10, 7))
for cluster_id in sorted(df['KMeans_Cluster'].unique()):
    mask = df['KMeans_Cluster'] == cluster_id
    plt.scatter(df.loc[mask,'PCA1'], df.loc[mask,'PCA2'],
                c=palette[cluster_id], label=f'Cluster {cluster_id}',
                alpha=0.6, s=25, edgecolors='none')
plt.xlabel(f'PC1 ({pca.explained_variance_ratio_[0]*100:.1f}% variance)', fontsize=12)
plt.ylabel(f'PC2 ({pca.explained_variance_ratio_[1]*100:.1f}% variance)', fontsize=12)
plt.title('K-Means Student Clusters (PCA 2D)', fontsize=14, fontweight='bold')
plt.legend(title='Cluster', fontsize=10)
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('kmeans_clusters_pca.png', dpi=150, bbox_inches='tight')
plt.show()
print("K-Means cluster counts:")
print(df['KMeans_Cluster'].value_counts().sort_index())
"""

text_6 = "## 5. Cluster Profile Analysis"

code_6 = """cluster_profile = df.groupby('KMeans_Cluster')[features].mean().round(3)
print("Cluster Profiles (Mean Feature Values):")
print(cluster_profile.to_string())

# Radar / bar comparison
cluster_profile_norm = (cluster_profile - cluster_profile.min()) / (cluster_profile.max() - cluster_profile.min())

fig, axes = plt.subplots(2, 2, figsize=(14, 10))
axes = axes.flatten()

for idx, feat in enumerate(features):
    vals = cluster_profile[feat]
    bars = axes[idx].bar([f'Cluster {i}' for i in vals.index], vals.values,
                         color=palette, edgecolor='black', alpha=0.85)
    axes[idx].set_title(f'Average {feat}', fontsize=12, fontweight='bold')
    axes[idx].set_ylabel(feat)
    for bar, v in zip(bars, vals.values):
        axes[idx].text(bar.get_x()+bar.get_width()/2, bar.get_height()+0.01*vals.max(),
                       f'{v:.2f}', ha='center', va='bottom', fontsize=9)
    axes[idx].grid(axis='y', alpha=0.3)

plt.suptitle('Cluster Feature Profiles', fontsize=15, fontweight='bold')
plt.tight_layout()
plt.savefig('cluster_profiles.png', dpi=150, bbox_inches='tight')
plt.show()
"""

text_7 = "## 6. Risk Analysis - Label Each Cluster"

code_7 = """# Assign risk labels based on GPA and attendance profile
risk_labels = {}
for cid, row in cluster_profile.iterrows():
    if row['GPA'] >= 3.0 and row['Attendance_Pct'] >= 75:
        risk_labels[cid] = 'High Achievers'
    elif row['GPA'] >= 2.0 and row['Attendance_Pct'] >= 60:
        risk_labels[cid] = 'Average Performers'
    elif row['GPA'] >= 1.5:
        risk_labels[cid] = 'Struggling Students'
    else:
        risk_labels[cid] = 'At-Risk Students'

df['Risk_Label'] = df['KMeans_Cluster'].map(risk_labels)

print("Risk Segmentation:")
print(df['Risk_Label'].value_counts())

# Pie chart
label_counts = df['Risk_Label'].value_counts()
plt.figure(figsize=(8, 8))
plt.pie(label_counts.values, labels=label_counts.index,
        autopct='%1.1f%%', colors=['#2A9D8F','#457B9D','#E9C46A','#E63946'],
        startangle=140, textprops={'fontsize': 12})
plt.title('Student Risk Segmentation', fontsize=14, fontweight='bold')
plt.tight_layout()
plt.savefig('risk_segmentation_pie.png', dpi=150, bbox_inches='tight')
plt.show()
"""

text_8 = "## 7. Hierarchical Clustering (Dendrogram)"

code_8 = """# Use a sample of 300 students for readable dendrogram
sample_idx = np.random.choice(len(X_scaled), size=300, replace=False)
X_sample = X_scaled[sample_idx]

linked = linkage(X_sample, method='ward')

plt.figure(figsize=(18, 7))
dendrogram(linked, truncate_mode='lastp', p=30,
           leaf_rotation=45, leaf_font_size=10,
           color_threshold=0.7*max(linked[:,2]))
plt.title('Hierarchical Clustering Dendrogram (Ward Linkage)', fontsize=14, fontweight='bold')
plt.xlabel('Student Index (or cluster size)', fontsize=11)
plt.ylabel('Distance', fontsize=11)
plt.axhline(y=8, color='red', linestyle='--', label='Cut line (k=4)')
plt.legend()
plt.tight_layout()
plt.savefig('dendrogram.png', dpi=150, bbox_inches='tight')
plt.show()
print("Dendrogram saved.")
"""

text_9 = "## 8. Agglomerative Clustering Comparison"

code_9 = """agg = AgglomerativeClustering(n_clusters=4, linkage='ward')
df['Agg_Cluster'] = agg.fit_predict(X_scaled)

# 2D PCA scatter for Agglomerative
plt.figure(figsize=(10, 7))
for cluster_id in sorted(df['Agg_Cluster'].unique()):
    mask = df['Agg_Cluster'] == cluster_id
    plt.scatter(df.loc[mask,'PCA1'], df.loc[mask,'PCA2'],
                c=palette[cluster_id], label=f'Cluster {cluster_id}',
                alpha=0.6, s=25, edgecolors='none')
plt.xlabel('PC1', fontsize=12)
plt.ylabel('PC2', fontsize=12)
plt.title('Agglomerative Clustering (PCA 2D)', fontsize=14, fontweight='bold')
plt.legend(title='Cluster', fontsize=10)
plt.grid(True, alpha=0.2)
plt.tight_layout()
plt.savefig('agglomerative_clusters_pca.png', dpi=150, bbox_inches='tight')
plt.show()

agg_sil = silhouette_score(X_scaled, df['Agg_Cluster'])
km_sil  = silhouette_score(X_scaled, df['KMeans_Cluster'])
print(f"K-Means Silhouette     : {km_sil:.4f}")
print(f"Agglomerative Silhouette: {agg_sil:.4f}")
"""

text_10 = """## 9. Summary

| Method | Clusters | Silhouette Score | Best Use |
|---|---|---|---|
| K-Means | 4 | Computed above | Fast, scalable |
| Agglomerative | 4 | Computed above | Richer hierarchy view |

### Risk Segments Identified
| Segment | Characteristics |
|---|---|
| High Achievers | GPA >= 3.0, Attendance >= 75% |
| Average Performers | GPA 2.0-3.0, Attendance 60-75% |
| Struggling Students | Low GPA but moderate attendance |
| At-Risk Students | Low GPA + Low attendance - need intervention |
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
]

nb['cells'] = cells

with open('University_Clustering.ipynb', 'w', encoding='utf-8') as f:
    nbf.write(nb, f)

print("Notebook 'University_Clustering.ipynb' generated.")
