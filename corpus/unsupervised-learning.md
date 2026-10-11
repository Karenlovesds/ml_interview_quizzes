# Unsupervised Learning

## Clustering

- **k-means**: minimizes within-cluster sum of squares. Needs `k`, assumes
  spherical clusters, sensitive to initialization (use k-means++).
- **DBSCAN**: density-based, finds arbitrary shapes, detects outliers, no `k`.
- **Hierarchical / agglomerative**: builds a dendrogram; cut at a height.
- **Gaussian Mixture Models**: soft, probabilistic clustering via EM.

## Dimensionality reduction

- **PCA**: linear projection onto directions of maximum variance
  (eigenvectors of the covariance matrix). Unsupervised, preserves global
  structure. Use the explained-variance ratio to pick components.
- **t-SNE / UMAP**: non-linear, mainly for visualization; distances between
  far clusters are not reliable in t-SNE.

## Anomaly detection

Isolation Forest, One-Class SVM, and autoencoder reconstruction error flag
points that deviate from the learned normal distribution.

## When to use which

| Goal | Method |
|---|---|
| Compact linear features | PCA |
| Visualize high-dim clusters | t-SNE / UMAP |
| Arbitrary-shaped clusters + noise | DBSCAN |
| Soft cluster membership | GMM |
