import os
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH

def add_student_details(doc):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p.add_run("Name: Pranav Lamkhade\nRoll No: 42\nBatch: A3\nPRN: 202401120062")
    run.font.size = Pt(10)
    run.bold = True
    doc.add_paragraph() # spacing

def add_heading(doc, text, level=1):
    h = doc.add_heading(text, level)
    run = h.runs[0]
    run.font.color.rgb = RGBColor(0, 51, 102)

def add_code(doc, text):
    p = doc.add_paragraph()
    run = p.add_run(text)
    run.font.name = 'Consolas'
    run.font.size = Pt(9)
    # Add a slight background or border if possible, but standard is fine

def create_clustering_doc(output_path):
    doc = Document()
    add_student_details(doc)
    
    add_heading(doc, 'Part 4: Clustering - Student Segmentation & Risk Analysis', 0)
    
    doc.add_heading('Objective', level=2)
    doc.add_paragraph('Segment students into meaningful groups using GPA, Attendance Percentage, Credits Completed, and Study Load. Techniques used include K-Means Clustering (with Elbow Method) and Hierarchical (Agglomerative) Clustering (with Dendrogram).')

    # Step 1 & 2 & 3
    doc.add_heading('1. Data Preparation, Feature Scaling, and K-Means Elbow Method', level=2)
    add_code(doc, '''features = ['GPA', 'Attendance_Pct', 'Credits_Completed', 'Study_Load']
X = df[features].values
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

inertias = []
silhouettes = []
k_range = range(2, 11)

for k in k_range:
    km = KMeans(n_clusters=k, random_state=42, n_init=10)
    km.fit(X_scaled)
    inertias.append(km.inertia_)
    silhouettes.append(silhouette_score(X_scaled, km.labels_))
''')
    
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part4_Clustering\elbow_silhouette.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(6.0))
        
    # Step 4
    doc.add_heading('2. K-Means Clustering (k=4)', level=2)
    add_code(doc, '''K = 4
kmeans = KMeans(n_clusters=K, random_state=42, n_init=10)
df['KMeans_Cluster'] = kmeans.fit_predict(X_scaled)

pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)
df['PCA1'] = X_pca[:,0]
df['PCA2'] = X_pca[:,1]
''')
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part4_Clustering\kmeans_clusters_pca.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(5.0))
        
    # Step 5
    doc.add_heading('3. Cluster Profile Analysis', level=2)
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part4_Clustering\cluster_profiles.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(6.0))

    # Step 6
    doc.add_heading('4. Risk Analysis - Segment Labels', level=2)
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part4_Clustering\risk_segmentation_pie.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(4.0))

    # Step 7
    doc.add_heading('5. Hierarchical Clustering (Dendrogram)', level=2)
    add_code(doc, '''sample_idx = np.random.choice(len(X_scaled), size=300, replace=False)
X_sample = X_scaled[sample_idx]
linked = linkage(X_sample, method='ward')
dendrogram(linked, truncate_mode='lastp', p=30)
''')
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part4_Clustering\dendrogram.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(6.0))

    # Step 8
    doc.add_heading('6. Agglomerative Clustering', level=2)
    add_code(doc, '''agg = AgglomerativeClustering(n_clusters=4, linkage='ward')
df['Agg_Cluster'] = agg.fit_predict(X_scaled)
''')
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part4_Clustering\agglomerative_clusters_pca.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(5.0))

    doc.add_heading('Conclusion', level=2)
    doc.add_paragraph('Both K-Means and Agglomerative Clustering identified 4 optimal segments: High Achievers, Average Performers, Struggling Students, and At-Risk Students. This segmentation enables targeted interventions for students based on their behavioral and academic profiles.')

    doc.save(output_path)
    print(f"Saved: {output_path}")

def create_ann_doc(output_path):
    doc = Document()
    add_student_details(doc)
    
    add_heading(doc, 'Part 5: ANN - Academic Performance Forecasting', 0)
    
    doc.add_heading('Objective', level=2)
    doc.add_paragraph('Predict Dropout Risk using a Feedforward Neural Network and compare performance with traditional ML models (Logistic Regression, Random Forest, Gradient Boosting).')

    doc.add_heading('1. Data Normalization & Network Initialization', level=2)
    add_code(doc, '''features = ['attendance_pct', 'internal_marks', 'course_load', 'hist_pass_rate', 'faculty_interaction']
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(X)

ann = MLPClassifier(
    hidden_layer_sizes=(128, 64, 32),
    activation='relu',
    solver='adam',
    learning_rate_init=0.001,
    max_iter=200,
    random_state=42
)
ann.fit(X_train, y_train)
''')

    doc.add_heading('2. Training Loss Curve', level=2)
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part5_ANN\ann_loss_curve.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(5.0))

    doc.add_heading('3. Model Comparison & ROC Curves', level=2)
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part5_ANN\roc_curves.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(5.0))

    doc.add_heading('4. ANN Confusion Matrix', level=2)
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part5_ANN\ann_confusion_matrix.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(4.0))

    doc.add_heading('5. Model Performance Metrics', level=2)
    img_path = r'c:\Users\prana_b2roblq\Downloads\university Analytics\Part5_ANN\model_comparison.png'
    if os.path.exists(img_path):
        doc.add_picture(img_path, width=Inches(6.0))

    doc.add_heading('Conclusion', level=2)
    doc.add_paragraph('The ANN successfully modeled dropout risk with high accuracy and ROC-AUC. While traditional models like Gradient Boosting provide strong competition, the Multi-Layer Perceptron (128-64-32) effectively learns non-linear patterns between attendance, GPA, and historical performance.')

    doc.save(output_path)
    print(f"Saved: {output_path}")

if __name__ == "__main__":
    clustering_path = r"c:\Users\prana_b2roblq\Downloads\university Analytics\Part4_Clustering\Clustering_Assignment.docx"
    ann_path = r"c:\Users\prana_b2roblq\Downloads\university Analytics\Part5_ANN\ANN_Assignment.docx"
    create_clustering_doc(clustering_path)
    create_ann_doc(ann_path)

    import sys
    try:
        import docx2pdf
        docx2pdf.convert(clustering_path)
        docx2pdf.convert(ann_path)
        print("PDFs generated successfully.")
    except ImportError:
        print("docx2pdf not installed, please run: pip install docx2pdf")
    except Exception as e:
        print("Error during PDF conversion:", e)
