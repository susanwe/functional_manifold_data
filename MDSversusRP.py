import scms
import get_auto_isomap_gdist as gaig
from sklearn import  datasets
from sklearn.manifold import MDS
from sklearn import random_projection
import numpy as np
import matplotlib.pyplot as plt

# load data
n = 1500
X, color = datasets.samples_generator.make_swiss_roll(n_samples=n)
dg_true = gaig.get_auto_isomap_gdist(X)

# Random projection to reduce dimension, then shift to density ridge
P = 1000
RP_error = []
dg_RP_matrix = np.empty((0, n**2))
for i in range(P):
    # embed into lower dimension using RP
    n_components = 2
    transformer = random_projection.GaussianRandomProjection(n_components=n_components)
    X_transformed_RP = transformer.fit_transform(X)
    # compute density ridge
    sigma = 0.5
    projected_RP = scms.scms(X_transformed_RP, sigma, n_iterations=5)
    # geodesic distance
    dg_RP = gaig.get_auto_isomap_gdist(projected_RP)
    dg_RP_matrix = np.vstack((dg_RP_matrix, dg_RP.flatten()))
    # calculate error
    diff = dg_RP - dg_true
    RP_error = np.append(RP_error, (diff ** 2).mean())

# calculate elementwise median for dg_RPs
dg_RP_median = np.median(dg_RP_matrix,axis=0)
# calculate errors
diff = dg_RP_median - dg_true.flatten()
RP_median_error = (diff ** 2).mean()


# embed into lower dimensions using MDS
n_components = 2
embedding = MDS(n_components=n_components)
X_transformed_MDS = embedding.fit_transform(X)
# compute respective density ridges
sigma = 0.5
projected_MDS = scms.scms(X_transformed_MDS, sigma, n_iterations=5)
# geodesic distance estimators
dg_MDS = gaig.get_auto_isomap_gdist(projected_MDS)
# calculate errors
diff = dg_MDS - dg_true
MDS_error = (diff ** 2).mean()

# plot histogram of RP errors with MDS and median RP as references
plt.hist(RP_error, bins=20, color='c', edgecolor='k', alpha=0.65,label='individual RP error')
plt.axvline(MDS_error, color='k', linestyle='dashed', linewidth=1,label='MDS error')
plt.axvline(RP_median_error, color='r', linestyle='dashed', linewidth=1,label='median RP error')
plt.legend()
plt.show()