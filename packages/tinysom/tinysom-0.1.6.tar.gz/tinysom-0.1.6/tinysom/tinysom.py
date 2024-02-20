#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt
from tqdm.auto import tqdm


class SOM(object):
    """Self-Organising Map (SOM) training and analysis on a rectangular grid.

    Attributes
    ----------
    bmus : ndarray
        1D array of Best Matching Units (BMUs) for each training instance.
    wts: ndarray
        SOM weights (codebook). Rows correspond to neurons, columns to
        weights in feature space.
    inertia_: float
        The sum of squared distances between each data point and its BMU.
    """

    def __init__(self, n_rows, n_cols, neighbourhood='gaussian', metric='cosine',
                 n_epochs=10, kernelwt_Rmax=0.1, initial='pca'):
        """Class constructor.
        
        Parameters
        ----------
        n_rows : int
            Number of rows in SOM.
        n_cols : int
            Number of columns in SOM.
        neighbourhood : str, optional
            Form of neighbourhood function on SOM. Options are
            `gaussian` (default), `exponential`, `linear`, `bubble`.
        metric : str
            Metric used to calculate BMUs. Options are
            'cosine' (default) or 'euclidean'.
        n_epochs : int, optional
            Number of training epochs. Defaults to 10.
        kernelwt_Rmax : float, optional
            Kernel weight at maximum inter-neuron distance. Defaults to 0.1.
        initial : str, optional
            Weights initialisation method. Options are
            `pca` (default) or `random`.
        """

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.neighbourhood = neighbourhood
        self.metric = metric
        self.n_epochs = n_epochs
        self.kernelwt_Rmax = kernelwt_Rmax
        self.initial = initial
        self.bmus = None
        self.wts = None
        self.inertia_ = None

        # Calculate distance**2 matrix for neuron array
        ixs = np.arange(n_rows*n_cols)       
        rows, cols = ixs % n_cols, ixs // n_cols
        self.d2mat = (rows[:,None]-rows[None,:])**2 + (cols[:,None]-cols[None,:])**2

        # Define kernels based on neighbourhood function and neuron distance matrix
        self.make_kernels()

    def calc_BMUs(self, X):
        """Calculate Best-Matching Units (BMUs) for training data array X.
        
        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.
        """
        if self.metric == 'cosine':
            return ((self.wts @ X.T) / np.outer(np.linalg.norm(self.wts, axis=1),
                                                np.linalg.norm(X, axis=1))
                   ).argmax(axis=0)
        elif self.metric == 'euclidean':
            return ((X[:,None]-self.wts)**2).sum(axis=2).argmin(axis=1)
        else:
            return None

    def make_kernels(self):
        """Generate kernels for all epochs. 
        
        User-defined kernel weights at the maximum radius Rmax for the
        first epoch, and unit radius R1 at the final epoch.
        """ 

        # Define kernels based on neighbourhood function
        if self.neighbourhood == 'bubble':
            Rmax = np.sqrt(self.d2mat.max())
            sigs = np.linspace(Rmax, 0.5, self.n_epochs)
            self.kernels = np.where(np.sqrt(self.d2mat)[None,:,:]<=sigs[:,None,None], 1, 1e-12)
        elif self.neighbourhood == 'linear':
            Rmax = np.sqrt(self.d2mat.max())
            sigs = np.linspace(Rmax, 0.5, self.n_epochs)
            self.kernels = np.clip(1 - np.sqrt(self.d2mat[None,:,:])/sigs[:,None,None], 1e-12, 1)
        elif self.neighbourhood == 'exponential':
            Rmax = -np.sqrt(self.d2mat.max())/(2*np.log(self.kernelwt_Rmax))
            sigs = np.linspace(Rmax, 0.5, self.n_epochs)
            self.kernels = np.exp(-(np.sqrt(self.d2mat[None,:,:])/(2*sigs[:,None,None])))
        elif self.neighbourhood == 'gaussian':
            Rmax = -self.d2mat.max()/(2*np.log(self.kernelwt_Rmax))
            sigs = np.linspace(Rmax, 0.5, self.n_epochs)
            self.kernels = np.exp(-(self.d2mat[None,:,:]/(2*sigs[:,None,None])))
        else:
            print('Invalid neighbourhood')
            return None
    
    def fit(self, X, y=None):
        """Train SOM on input data array X using the batch algorithm.
        
        Input array X should be in the standard format, i.e.
        rows (axis 0) are instances, columns (axis 1) are features.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.
            y : Ignored
                Not used, present here for API consistency by convention.
        """
        
        # Initialise SOM weights as a random array or using PCA
        n_samp, n_feat = X.shape
        if self.initial == 'random':
            self.wts = np.random.random(size=(self.n_rows*self.n_cols, n_feat))
        elif self.initial == 'pca':
            X_mean = X.mean(axis=0)
            X_zm = X - X_mean
            covmat = (X_zm.T @ X_zm)/n_samp
            eigvals, eigvecs = np.linalg.eigh(covmat)

            # Variance explained by PCs beyond the first two
            resid_variance = eigvals[:-2].sum()
            
            # Generate Gaussian noise to make up variance
            noise = np.random.normal(loc=0, scale=np.sqrt(resid_variance), 
                                     size=(self.n_rows, self.n_cols, n_feat))
            
            # Ranges of row PCs (for EOF1) and column PCs (for EOF2) over SOM
            row_facs = np.linspace(-eigvals[-1], eigvals[-1], self.n_rows)
            col_facs = np.linspace(-eigvals[-2], eigvals[-2], self.n_cols)
            col_facs, row_facs = np.meshgrid(col_facs, row_facs)
            
            self.wts = ((row_facs[:,:,None] * eigvecs[:,-1]) + 
                        (col_facs[:,:,None] * eigvecs[:,-2]) + 
                        noise + X_mean
                       ).reshape((self.n_rows*self.n_cols, -1))
        else:
            print('initial must be random or pca')
            return None

        for i in tqdm(range(self.n_epochs)):
            # Calculate BMUs for all training vectors
            bmus = self.calc_BMUs(X)
            
            # Calculate numerator (BMU kernel-weighted sum of training data)
            num = (X[:,None] * self.kernels[i][bmus][:,:,None]).sum(axis=0)
            
            # Calculate denominator (sum of BMU weights for training data) and update weights
            denom = self.kernels[i][bmus].sum(axis=0)
            self.wts = num/denom[:,None]
            
        # Update BMUs
        self.bmus = self.calc_BMUs(X)
        
        # Calculate distance matrix of neurons in feature space
        self.dmat = np.sqrt(((self.wts[:,None] - self.wts)**2).sum(axis=2))

        # Update inertia
        self.inertia_ = ((X - self.wts[self.bmus])**2).sum()

    def predict(self, X):
        """Calculate Best-Matching Units (BMUs) for training data array X.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.

        Returns
        -------
            bmus : ndarray
                BMUs.
        """

        if self.wts is None:
            print('Train SOM before classifying')
            return None
        return self.bmus

    def umatrix(self, figsize=(6,6)):
        """Plot U-matrix."""

        # Create empty U-matrix of appropriate dimensions
        umat = np.zeros((self.n_rows*2-1, self.n_cols*2-1))

        fig, ax = plt.subplots(1, 1, figsize=figsize)

        # Loop over neurons
        for i in range(self.n_rows * self.n_cols):
            row, col = i // self.n_cols, i % self.n_cols

            # Calculate means of distances in feature space to immediate neighbours
            dmat_neighbours = np.where((self.d2mat>0) & (self.d2mat<=2), self.dmat, np.nan
                                      )[i].reshape((self.n_rows, self.n_cols))
            dmat_neighbours_mean = np.nanmean(dmat_neighbours)
            umat[row*2, col*2] = dmat_neighbours_mean

            # Plot each neuron
            ax.plot([col*2], [row*2], marker='o', color='k', markersize=2)

            # Subset row, column coordinates of neighbours and calculate offset
            rows_alt, cols_alt = np.where(~np.isnan(dmat_neighbours))
            rows_offset, cols_offset = rows_alt - row, cols_alt - col

            # Fill between-neuron distances in U-matrix
            umat[row*2+rows_offset, col*2+cols_offset] = dmat_neighbours[rows_alt, cols_alt]

        # Save and plot U-matrix
        self.umat = umat
        ax.imshow(umat, cmap='Reds')
        ax.tick_params(labelbottom=False,labeltop=True)
        plt.tight_layout()

    def component_planes(self, i=None, cmap='viridis_r', figsize=(6,6)):
        """Plot component planes.
        
        Parameters
        ----------
            i : int, list or ndarray
                Index or indices of neuron weights to visualise.
            cmap : str
                Matplotlib colourmap.
        """

        if i is None:
            to_loop = range(self.wts.shape[1])
        elif isinstance(i, int):
            to_loop = [i]
        else:
            to_loop = i

        # Loop over dimensions of codebook
        for i in to_loop:
            arr = self.wts[:,i].reshape((self.n_rows, self.n_cols))
            fig, ax = plt.subplots(1, 1, figsize=figsize)
            ax.imshow(arr, cmap=cmap)


class SOM_cluster(SOM):
    """Subclass of SOM object for supervised or unsupervised clustering.

    Uses SOM twice, first to cluster input data to a general map of arbitrary 
    size, and again to the target number of clusters.

    Attributes
    ----------
    labels_: ndarray
        Cluster labels derived from **unsupervised** clustering, activated by 
        using the `n_clusters` argument.
    """

    def __init__(self, n_clusters, n_rows, n_cols, neighbourhood='gaussian',
                 metric='cosine', n_epochs=10, kernelwt_Rmax=0.1, initial='pca'):
        """Subclass constructor.

        Parameters
        ----------
            n_clusters : int
                Number of clusters to target for unsupervised clustering.
        """

        super().__init__(n_rows, n_cols, neighbourhood, metric, n_epochs,
                         kernelwt_Rmax, initial)

        self.n_clusters = n_clusters
        self.neuron_to_label = np.empty(self.n_cols*self.n_rows)
        self.neuron_to_label[:] = np.nan
        self.labels_ = None

    def fit(self, X, y=None):
        """Modified fit function for clustering.

        Input array X should be in the standard format, i.e.
        rows (axis 0) are instances, columns (axis 1) are features.
        If training data y is passed to this function, the `n_clusters`
        attribute is overridden.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.
            y : ndarray or list
                Labels of training data for supervised training.
        """

        super().fit(X)

        # Unsupervised clustering
        if y is None:
            # A linear SOM instance to cluster the weights vectors
            som = SOM(1, self.n_clusters)
            som.fit(self.wts)
            self.neuron_to_label[:] = som.bmus
            self.labels_ = som.bmus[self.bmus]
        # Supervised clustering/classification
        else:
            y = np.array(y)

            # Define mapping from neurons to classes using majority vote
            for i in range(self.n_cols*self.n_rows):
                labels_i = y[self.bmus==i]
                values, counts = np.unique(labels_i, return_counts=True)
                if counts.size > 0:
                    self.neuron_to_label[i] = values[np.argmax(counts)]

            # Backfill nans in neuron_to_label with the closest non-nan neuron
            # Fill all nan neurons columns in feature distance matrix with large number
            dmat_nonan = np.where(np.isnan(self.neuron_to_label), np.inf, self.dmat)
            
            # Get column indices of nearest neurons for all rows and backfill
            nearest_nonan = dmat_nonan.argsort(axis=1)[:,0]
            self.neuron_to_label = np.where(np.isnan(self.neuron_to_label), 
                                            self.neuron_to_label[nearest_nonan], 
                                            self.neuron_to_label)

    def predict(self, X):
        """Predict classes of data.

        Unsupervised clusers unless model was trained supervised.

        Parameters
        ----------
            X : ndarray
                Training data, with rows as instances, columns as features.

        Returns
        -------
            predicted : ndarray
                Predicted labels.
        """

        if np.isnan(self.neuron_to_label).all():
            print('Fit SOM clusterer/classifier before predicting')
            return None

        bmus = self.calc_BMUs(X)
        return self.neuron_to_label[bmus]
