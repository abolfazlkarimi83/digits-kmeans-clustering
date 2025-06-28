"""
Title: Iris Dataset Clustering with KMeans
Description: Clustering the Digits dataset using KMeans algorithm and comparing it with true labels.
Author: Abolfazl Karimi
GitHub: https://github.com/abolfazlkarimi83
License: MIT
"""

from sklearn.datasets import load_digits
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import confusion_matrix, accuracy_score
from scipy.stats import mode
import numpy as np
import seaborn as sns

# ثابت برای reproducibility
RANDOM_STATE = 42

# بارگذاری دیتاست ارقام دست‌نویس
digits = load_digits()
X = digits.data
Y = digits.target

print(f"Shape of X: {X.shape}")  # (1797, 64)
print(f"Shape of Y: {Y.shape}")  # (1797,)

# نمایش 10 نمونه از تصاویر با برچسب‌ها و ذخیره تصویر نمونه
plt.figure(figsize=(10, 4))
for i in range(10):
    plt.subplot(2, 5, i + 1)
    plt.imshow(digits.images[i], cmap='gray')
    plt.title(f"Label: {digits.target[i]}")
    plt.axis('off')
plt.tight_layout()
plt.savefig('sample_digits.png')  # ذخیره تصویر نمونه‌ها
plt.show()

# اجرای الگوریتم KMeans با 10 خوشه
kmeans = KMeans(n_clusters=10, random_state=RANDOM_STATE)
kmeans.fit(X)

# برچسب‌های پیش‌بینی شده خوشه‌ها
predicted_labels = kmeans.labels_
print(f"Predicted Cluster Labels for First 20 Samples:\n{predicted_labels[:20]}")

# تغییر برچسب خوشه‌ها به برچسب‌های واقعی با استفاده از mode
new_labels = np.zeros_like(predicted_labels)
for i in range(10):
    mask = (predicted_labels == i)
    if np.any(mask):
        new_labels[mask] = mode(Y[mask], keepdims=True)[0]

# محاسبه دقت خوشه‌بندی
acc = accuracy_score(Y, new_labels)
print(f"Clustering Accuracy: {acc:.4f}")

# محاسبه ماتریس درهم‌ریختگی
conf_mat = confusion_matrix(Y, new_labels)

# رسم ماتریس درهم‌ریختگی با seaborn
plt.figure(figsize=(8, 6))
sns.heatmap(conf_mat, annot=True, fmt='d', cmap='viridis', cbar=True, linewidths=0.5)
plt.xlabel('Predicted Labels')
plt.ylabel('True Labels')
plt.title('Confusion Matrix - KMeans Clustering')
plt.tight_layout()
plt.savefig('Kmeans_confusion_matrix.png')  # ذخیره تصویر ماتریس درهم‌ریختگی
plt.show()

# تست برای تعداد خوشه‌ها از 1 تا 10 و ذخیره مقدار SSE (inertia)
inertias = []
k_values = range(1, 11)

for k in k_values:
    model = KMeans(n_clusters=k, random_state=RANDOM_STATE)
    model.fit(X)
    inertias.append(model.inertia_)

# رسم نمودار Elbow برای تعیین تعداد خوشه بهینه
plt.figure(figsize=(8, 5))
plt.plot(k_values, inertias, 'bo-', linewidth=2)
plt.xlabel('Number of Clusters (k)')
plt.ylabel('Inertia (SSE)')
plt.title('Elbow Method for Optimal k')
plt.grid(True)
plt.tight_layout()
plt.savefig('elbow_method.png')  # ذخیره نمودار Elbow
plt.show()
