import numpy as np
import matplotlib.pyplot as plt
from sklearn.datasets import load_wine


class PCA:
    def __init__(self, n_components=2, normalize=False):
        self.n_components = n_components
        self.components = None
        self.mean = None
        self.normalize = normalize

    def fit(self, X):
        if self.normalize:
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X = scaler.fit_transform(X)
            # X=(X-np.mean(X, axis=0)) / np.std(X,axis=0)

        # Center the data
        self.mean = np.mean(X, axis=0)
        X = X - self.mean
        # Compute Variance Matrix
        cov = np.cov(X, rowvar=False)

        eigenvalues, eigenvectors = np.linalg.eigh(cov)

        # Sort the eigenvalues and eigenvectors in decreasing order
        idx = np.argsort(eigenvalues)[::-1]
        eigenvalues = eigenvalues[idx]
        eigenvectors = eigenvectors[:, idx]

        self.components = eigenvectors[:, : self.n_components]

    def transform(self, X):
        if self.normalize:
            from sklearn.preprocessing import StandardScaler
            scaler = StandardScaler()
            X = scaler.fit_transform(X)
            # X=(X-np.mean(X, axis=0)) / np.std(X,axis=0)

        X = X - self.mean
        # Project the data onto the principal components
        X_transformed = np.dot(X, self.components)
        return X_transformed


wine_data = load_wine()
X, y = wine_data.data, wine_data.target

pca = PCA(n_components=2)
pca.fit(X)
X_low = pca.transform(X)
plot = plt.scatter(X_low[:, 0], X_low[:, 1], c=y)
plt.legend(handles=plot.legend_elements()[0],
           labels=list(wine_data.target_names))
plt.title("Custom PCA Low")
plt.show()

pca = PCA(n_components=2, normalize=True)
pca.fit(X)
X_low = pca.transform(X)
plot = plt.scatter(X_low[:, 0], X_low[:, 1], c=y)
plt.legend(handles=plot.legend_elements()[0],
           labels=list(wine_data.target_names))
plt.title("Custom PCA Normalized Low")
plt.show()

from sklearn.decomposition import PCA as sklearnPCA

X_low = sklearnPCA(n_components=2).fit_transform(X)
plot = plt.scatter(X_low[:, 0], X_low[:, 1], c=y)
plt.legend(handles=plot.legend_elements()[0],
           labels=list(wine_data.target_names))
plt.title("Sklearn PCA Low")
plt.show()

from sklearn.preprocessing import StandardScaler

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_low = sklearnPCA(n_components=2).fit_transform(X)
plot = plt.scatter(X_low[:, 0], X_low[:, 1], c=y)
plt.legend(handles=plot.legend_elements()[0],
           labels=list(wine_data.target_names))
plt.title("Sklearn PCA Normalized Low")

plt.show()
