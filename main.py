import subprocess
from pickle import dump

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from files.pca_transformation import pca_transformation
from files.script_preparation import script_preparation
from files.model_training import model_training
from files.model_accuracy_plotting import model_accuracy_plotting

from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor

from sklearn.model_selection import train_test_split


class analysis(script_preparation):
    def __init__(self):
        super().__init__()
        self.set_parent(__file__)

    def get_specific_files(self, sep):
        files = self.get_files_list("plots")

        new_files = [i for i in files if i[:3] == sep]

        return new_files

    def get_feature_names(self, df):
        feature_names = []
        columns_names = df.columns.values

        for i in columns_names[0:]:
            feature_names.append(i)

        return feature_names

    def get_model_names(self, df):
        labels = []

        for i in df["Model"]:
            if i in labels:
                break
            labels.append(i)

        return labels

    def remove_outliers(self):
        remove_outliers = subprocess.run(
            f'"{self.get_R_script()}" "{self.back_to_forward_slash_switch(str(self.get_parent())) + "/files/outlier_removal.r"}"',
            shell=True,
            capture_output=True,
            text=True,
        )

    def exploratory_analysis(self):
        exploratory_analysis = subprocess.run(
            f'"{self.get_R_script()}" "{self.back_to_forward_slash_switch(str(self.get_parent())) + "/files/exploratory_analysis.r"}"',
            shell=True,
            capture_output=True,
            text=True,
        )

    def pca_analysis(self):
        df = pd.read_csv("csv_data_files/interim/01_no_outliers.csv")
        pca = pca_transformation(df)

        # plot explained variance to find best # of componenets with elbow method

        pca.plot_explained_variance()

        # create feature sets with principal components

        for i in [4, 5]:
            x_pca = pca.transform_x(i)
            col_names = pca.create_coloumn_names(i)
            df_x_pca = pd.DataFrame(x_pca, columns=col_names)
            df = pd.concat([df, df_x_pca], axis=1)

        # export dataset

        df.to_csv("csv_data_files/processed/01_PCA.csv", index=False)

    def train_models(self):
        df = pd.read_csv("csv_data_files/processed/01_PCA.csv")

        # Define all of the inputs necessary to model the data
        model_list = [
            LinearRegression,
            RandomForestRegressor,
            DecisionTreeRegressor,
            KNeighborsRegressor,
            GradientBoostingRegressor,
        ]
        model_labels = {
            LinearRegression: "Linear Regressor",
            RandomForestRegressor: "Random Forest Regressor",
            DecisionTreeRegressor: "Decision Tree Regressor",
            KNeighborsRegressor: "KNeighbors Regressor",
            GradientBoostingRegressor: "Gradient Boosting Regressor",
        }
        knr_cv_params = {
            "n_neighbors": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 15, 20],
            "metric": ["euclidean", "manhattan", "minkowski"],
        }
        rf_cv_params = {
            "n_estimators": [50, 75, 100, 125, 150],
            "max_depth": list(range(1, 10)),
        }
        gbr_cv_params = {
            "criterion": ["squared_error", "friedman_mse"],
            "learning_rate": [0.1, 0.15, 0.2, 0.25],
            "max_depth": [2, 3, 4, 5],
            "max_features": ["sqrt", None],
            "max_leaf_nodes": list(range(2, 10)),
            "n_estimators": list(range(50, 500, 50)),
            "subsample": [0.8, 0.9, 1.0],
        }
        all_cv_params = {
            KNeighborsRegressor: knr_cv_params,
            GradientBoostingRegressor: gbr_cv_params,
            RandomForestRegressor: rf_cv_params,
        }
        model_cv_dict = {
            LinearRegression: "none",
            DecisionTreeRegressor: "none",
            KNeighborsRegressor: "grid",
            GradientBoostingRegressor: "random",
            RandomForestRegressor: "grid",
        }

        # creating x labels for feature sets of data to see what the models train on the best
        feature_names = [
            "Original Feature Set",
            "4 PCA Feature Set",
            "5 PCA Feature Set",
            "Original + 4 PCA Feature Set",
            "Original + 5 PCA Feature Set",
            "Original + 4 PCA + 5 PCA Feature Set",
            "Forward DT Feature Set",
        ]
        original_features = [
            "Mixing_Time",
            "Active_1",
            "Active_2",
            "RM_3",
            "RM_4",
            "Active_3",
            "RM_6",
            "RM_7",
            "RM_8",
            "Active_4",
            "Water",
            "Crashout",
        ]
        pca_4_features = ["PC_1-4", "PC_2-4", "PC_3-4", "PC_4-4"]
        pca_5_features = ["PC_1-5", "PC_2-5", "PC_3-5", "PC_4-5", "PC_5-5"]

        original_features_set = original_features
        pca4_components_features = pca_4_features
        pca5_components_features = pca_5_features
        original_pca4_features = list(set(original_features + pca_4_features))
        original_pca5_features = list(set(original_features + pca_5_features))
        original_pca4_pca5_features = list(
            set(original_features + pca_4_features + pca_5_features)
        )

        # defining x and y and creating the modeling object instance before defining the feature_sets to use forward feature selection
        x = df.drop(["Viscosity"], axis=1)
        y = df["Viscosity"]

        x_train, x_test, y_train, y_test = train_test_split(
            x, y, test_size=0.25, stratify=x["Active_1"], random_state=7565
        )

        m = model_training(
            data=df, models=model_list, cv_dict=model_cv_dict, cv_params=all_cv_params
        )

        feature_sets = [
            original_features_set,
            pca4_components_features,
            pca5_components_features,
            original_pca4_features,
            original_pca5_features,
            original_pca4_pca5_features,
            m.forward_feature_selection(x_train=x_train, y_train=y_train),
        ]

        # Due to small dataset, graphing the number of elements for each discrete value to ensure an even split in test and train set
        m.graph_discrete_variable_split(x_train, x_test, "Mixing_Time", "Active_1")

        for feature_set_number, name in zip(range(len(feature_sets)), feature_names):
            if feature_set_number == 0:
                df_score = pd.DataFrame()
                df_residuals = pd.DataFrame()
                list_residuals = list(range(len(model_list)))

            print(
                f"Current Feature set: {name} {feature_set_number+1}/{len(feature_sets)}"
            )
            x_train_features = x_train[feature_sets[feature_set_number]]
            x_test_features = x_test[feature_sets[feature_set_number]]

            for i, regressor in enumerate(model_list):
                print(f"Model Currently Being Trained: {model_labels[regressor]}")

                trained_model = m.model_train(regressor, x_train_features, y_train)
                
                with open(f"models/{model_labels[regressor]} for {name}.pkl", "wb") as f:
                    dump(trained_model, f, protocol=5)
                
                y_pred = m.model_pred(trained_model, x_test_features)
                list_residuals[i] = abs(m.calc_residuals(y_pred=y_pred, y_test=y_test))

                new_score = m.score_data_collect(
                    model=trained_model,
                    iteration=i,
                    set_num=feature_set_number,
                    x_test=x_test_features,
                    y_test=y_test,
                    feature_names=feature_names,
                )

                df_score = pd.concat([df_score, new_score])

                print("Done Training")

            df_residuals[feature_names[feature_set_number]] = list_residuals

            if feature_set_number + 1 == len(feature_sets):
                print("Done Training All Models on All Feature Sets")

        df_score.sort_values(by="Score", ascending=False)

        df_score.to_csv("csv_data_files/processed/01_Model_Accuracy_Scores.csv")
        df_residuals.to_pickle("csv_data_files/processed/01_model_residuals")

    def graph_accuracy_residuals(self):
        model_plots = model_accuracy_plotting()

        df_model_scores = pd.read_csv(
            "csv_data_files/processed/01_Model_Accuracy_Scores.csv"
        )
        df_residuals = pd.read_pickle("csv_data_files/processed/01_model_residuals")

        model_plots.graph_accuracy(data=df_model_scores)

        model_plots.graph_residuals(
            residuals=df_residuals,
            feature_names=self.get_feature_names(df_residuals),
            model_names=self.get_model_names(df_model_scores),
        )


def main():

    # class to run the different scripts such as removing outliers and graphical analysis
    helper = analysis()

    # Run R script to remove outliers. Saves modified CSV file
    helper.remove_outliers()

    # Run R script to perform exploratoyr analysis. Saves graphs
    helper.exploratory_analysis()

    # Perform PCA analsysis with pca_tranformation class. Saves modified csv file
    helper.pca_analysis()

    # Train models with model_training class. Saves models as pickles
    helper.train_models()

    # Plot model accuracy and residuals for each feature set and model. Saves graphs
    helper.graph_accuracy_residuals()
    
main()