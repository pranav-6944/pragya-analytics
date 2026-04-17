import os, shutil

BASE = r'c:\Users\prana_b2roblq\Downloads\university Analytics'

structure = {
    'Part1_Data_Preprocessing': [
        'University_Predictive_Analysis.ipynb',
        'Processed_University_Data.xlsx',
        'generate_preprocessing_notebook.py',
        'inspect_data.py',
    ],
    'Part2_Association_Rule_Mining': [
        'University_Association_Mining.ipynb',
        'generate_arm_notebook.py',
    ],
    'Part3_Classification': [
        'University_Classification.ipynb',
        'generate_classification_notebook.py',
        'confusion_matrices.png',
        'model_accuracy_comparison.png',
        'feature_importances.png',
    ],
    'Part4_Clustering': [
        'University_Clustering.ipynb',
        'generate_clustering_notebook.py',
        'elbow_silhouette.png',
        'kmeans_clusters_pca.png',
        'agglomerative_clusters_pca.png',
        'cluster_profiles.png',
        'dendrogram.png',
        'risk_segmentation_pie.png',
    ],
    'Part5_ANN': [
        'University_ANN.ipynb',
        'generate_ann_notebook.py',
        'ann_loss_curve.png',
        'ann_confusion_matrix.png',
        'roc_curves.png',
        'model_comparison.png',
    ],
    'Part6_Advanced_Analytics': [
        'University_Advanced_Analytics.ipynb',
        'generate_advanced_analytics_notebook.py',
        'advanced_at_risk.png',
        'advanced_course_bottlenecks.png',
        'advanced_dept_performance.png',
        'advanced_unified_dashboard.png',
    ],
    'Part7_Visualization': [
        'University_Visualization.ipynb',
        'generate_visualization_notebook.py',
        'viz_confusion_matrix.png',
        'viz_cluster_plots.png',
        'viz_gpa_distributions.png',
        'viz_attendance_vs_performance.png',
        'viz_master_dashboard.png',
    ],
    'Part8_Final_Deliverable': [
        'University_Final_Deliverable.ipynb',
        'generate_final_notebook.py',
        'final_core_charts.png',
        'final_roc_attendance.png',
    ],
    'Dataset': [
        'University_Management_Curation_Project.xlsx',
    ],
    '_scripts': [
        'generate_notebook.py',
    ],
}

for folder, files in structure.items():
    folder_path = os.path.join(BASE, folder)
    os.makedirs(folder_path, exist_ok=True)
    for f in files:
        src = os.path.join(BASE, f)
        dst = os.path.join(folder_path, f)
        if os.path.exists(src):
            shutil.move(src, dst)
            print(f"  Moved: {f} -> {folder}/")
        else:
            print(f"  SKIP (not found): {f}")

print("\nFolder organised successfully!")
