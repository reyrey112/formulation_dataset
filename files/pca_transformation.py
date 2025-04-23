import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# scale at initilization
# definie which coloumns to take, autoatcally on the ones i hav eset
# import data in the main

class pca_transformation:
    def __init__(
        self,
        data
    ):
        self.data = data
        self.x_scaled = self.stan_scale_data()

    def title_to_filename(self, title):
        new_title = title.split(" ")
        filename = "_".join(new_title)

        return filename

    def save_model(self, title):
        filename = self.title_to_filename(title)

        plt.savefig(f"plots/{filename}.png")

        plt.close()

    def stan_scale_data(self):

        df = self.data

        # Create x axis data set

        # define outside (input the x in main or use df.drop? in main)
        x = df.loc[:, "Mixing_Time":"Crashout"]

        # Apply Scaler and PCA Transformations

        scaler = StandardScaler()
        x_scaled = scaler.fit_transform(x)

        return x_scaled

    def transform_x(self, n_components = None):
        pca = PCA(n_components=n_components)
        x = pca.fit_transform(self.x_scaled)

        return x

    def plot_explained_variance(self):

        # Plot Explained Variance

        pca = PCA()
        pca.fit(self.x_scaled)

        ev = pca.explained_variance_ratio_

        title = "Elbow Method for Optimal Component Number"

        plt.plot(range(1, len(ev) + 1), np.cumsum(ev), marker = 'o')
        plt.xlabel("Number of Componenets")
        plt.ylabel("Cumulated Explaed Varience")
        plt.title(title)
        plt.grid(True)

        self.save_model(title)

    def create_coloumn_names(self, n_components):
        column_names = [f"PC_{i+1}-{n_components}" for i in range(n_components)]

        return column_names
