import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import colorsys

# make it so on initilization it takes models to train from main file
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.tree import DecisionTreeRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.feature_selection import SequentialFeatureSelector

from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.model_selection import train_test_split
from sklearn import metrics


class model_training:

    def __init__(
        self,
        data,
        models,
        cv_dict,
        cv_params
    ):
        self.data = data
        self.models = models
        self.cv_dict = cv_dict
        self.cv_params = cv_params
        self.__create_labels()

    # move to separate file ventually
    def __create_labels(self):
        # self.labels = [str(x())[:-2] for x in self.models]
        self.labels = {str(self.models[i]()): str(regressor())[:-2] for i, regressor in enumerate(self.models)}

    def color_generator(self):

        rgb = (
            random.randrange(25, 75, 5) / 100,
            random.randrange(25, 75, 5) / 100,
            random.randrange(25, 75, 5) / 100
        )

        return rgb

    def rgb_shift(self):
        rgb = self.color_generator()

        h, s, v = colorsys.rgb_to_hsv(*rgb)

        up_v = v + 0.25
        down_v = v - 0.25

        up_rgb = colorsys.hsv_to_rgb(h,s,up_v)
        down_rgb = colorsys.hsv_to_rgb(h, s, down_v)

        if any(up_rgb) < 0 or any(down_rgb) < 0 or any(up_rgb) > 1 or any(down_rgb) > 1: 
            self.rgb_shift()

        return rgb, up_rgb, down_rgb

    def title_to_filename(self, title):
        new_title = title.split(" ")
        filename = "_".join(new_title)

        return filename

    def save_model(self, title):
        filename = self.title_to_filename(title)

        plt.savefig(f"plots/{filename}.png")

        plt.close()

    def graph_discrete_variable_split(self, x_train, x_test, *discrete_variables):
        df = self.data

        for i, varible_name in enumerate(discrete_variables):
            title = f"Data split for {str(varible_name)}"

            rgb, up_rgb, down_rgb = self.rgb_shift()

            fig, ax = plt.subplots(figsize=(10, 5))
            df[discrete_variables[i]].value_counts().plot(
                kind="bar", ax=ax, color=up_rgb, label="Total"
            )
            x_train[discrete_variables[i]].value_counts().plot(
                kind="bar", ax=ax, color=rgb, label="Train"
            )
            x_test[discrete_variables[i]].value_counts().plot(
                kind="bar", ax=ax, color=down_rgb, label="Test"
            )
            plt.title(title, fontdict={"fontname": "Times New Roman", "size": 14, "fontweight": "bold"}, loc="center", pad=0)
            plt.ylabel(
                "Count", fontdict={"fontname": "Times New Roman", "size": 14, "fontweight": "bold"}
            )
            plt.xlabel(discrete_variables[i], fontdict={"size": 12, "fontweight": "bold"})
            plt.legend()
            
            self.save_model(title)

    def forward_feature_selection(self, x_train, y_train):
        dt = DecisionTreeRegressor()
        sfs = SequentialFeatureSelector(dt)

        sfs.fit(x_train, y_train)
        forward_DT_features = sfs.get_feature_names_out()

        return forward_DT_features

    def model_train(self, regressor, x_train, y_train):
        self.model = regressor()

        if self.cv_dict[regressor] != "none":
            model = self.model_train_cv(self.model, regressor, x_train, y_train)

        model = self.model

        model.fit(x_train, y_train)

        return model

    def model_train_cv(self, model, regressor, x_train, y_train):
        if self.cv_dict[regressor] == "grid":
            val_model = GridSearchCV(model, self.cv_params[regressor])
        elif self.cv_dict[regressor] == "random": 
            val_model = RandomizedSearchCV(model, self.cv_params[regressor])

        val_model.fit(x_train, y_train)
        best_params = val_model.best_params_

        new_model = regressor(**best_params)

        return new_model

    def model_pred(self, model, x_test):
        y_pred = model.predict(x_test)

        return y_pred

    def calc_residuals(self, y_pred, y_test):    
        residuals = np.subtract(y_test, y_pred)

        return residuals

    def score_data_collect(self, model, iteration, set_num , x_test, y_test, feature_names):
        i = iteration

        new_score = pd.DataFrame()

        new_score.loc[i, "Model"] = self.labels[str(model)]
        new_score.loc[i, "Score"] = model.score(x_test, y_test)
        new_score.loc[i, "R2 Score"] = metrics.r2_score(y_test, self.model_pred(model, x_test))
        new_score.loc[i, "Feature Set"] = feature_names[set_num]
        new_score.loc[i, "Hypertuned"] = "GridSearchCV"

        return new_score


# # Reading Data in from Files

# df = pd.read_csv("../../CSV Data Files/processed/01_PCA.csv")

# # Creating Trainign and Test set
# # Create funciton to ensure trianing set it a certain pecent uniformell ==y distrubted

# x = df.drop(["Viscosity"], axis=1)
# y = df["Viscosity"]

# x_train, x_test, y_train, y_test = train_test_split(
#     x, y, test_size=0.25, stratify=x["Active_1"], random_state=7565
# )

# # Plotting Value counts to ensure evenly distrubuted split

# fig, ax = plt.subplots(figsize=(10, 5))
# df["Mixing_Time"].value_counts().plot(kind="bar", ax=ax, color="#F88379", label="Total")
# x_train["Mixing_Time"].value_counts().plot(kind="bar", ax=ax, color="red", label="Train")
# x_test["Mixing_Time"].value_counts().plot(kind="bar", ax=ax, color="#880808", label="Test")
# plt.ylabel("Count", fontdict={"fontname": "Times New Roman", "size": 14, "fontweight": "bold"})
# plt.xlabel("Mixing Time", fontdict={"size": 12, "fontweight": "bold"})
# plt.legend()
# plt.show()

# fig, ax = plt.subplots(figsize=(10, 5))
# df["Active_1"].value_counts().plot(kind="bar", ax=ax, color="#00FFFF", label="Total")
# x_train["Active_1"].value_counts().plot(kind="bar", ax=ax, color="#0096FF", label="Train")
# x_test["Active_1"].value_counts().plot(kind="bar", ax=ax, color="#0000FF", label="Test")
# plt.ylabel("Count", fontdict={"fontname": "Times New Roman", "size": 14, "fontweight": "bold"})
# plt.xlabel("Active 1", fontdict={"size": 12, "fontweight": "bold"})
# plt.legend()
# plt.show()

# # Creating Feature Sets

# original_features = [
#     "Mixing_Time",
#     "Active_1",
#     "Active_2",
#     "RM_3",
#     "RM_4",
#     "Active_3",
#     "RM_6",
#     "RM_7",
#     "RM_8",
#     "Active_4",
#     "Water",
#     "Crashout",
# ]
# pca_4_features = ["PC_1-4", "PC_2-4", "PC_3-4", "PC_4-4"]
# pca_5_features = ["PC_1-5", "PC_2-5", "PC_3-5", "PC_4-5", "PC_5-5"]

# original_features_set = original_features
# pca4_components_features = pca_4_features
# pca5_components_features = pca_5_features
# original_pca4_features = list(set(original_features + pca_4_features))
# original_pca5_features = list(set(original_features + pca_5_features))
# original_pca4_pca5_features = list(set(original_features + pca_4_features + pca_5_features))

# # Forward feature selection using DecisionTree


# dt = DecisionTreeRegressor()
# sfs = SequentialFeatureSelector(dt)

# sfs.fit(x_train, y_train)
# forward_DT_features = sfs.get_feature_names_out()

# # Creating Objects for  Iterations

# feature_sets = [
#     original_features_set,
#     pca4_components_features,
#     pca5_components_features,
#     original_pca4_features,
#     original_pca5_features,
#     original_pca4_pca5_features,
#     forward_DT_features,
# ]
# feature_names = [
#     "Original Feature Set",
#     "4 PCA Feature Set",
#     "5 PCA Feature Set",
#     "Original + 4 PCA Feature Set",
#     "Original + 5 PCA Feature Set",
#     "Original + 4 PCA + 5 PCA Feature Set",
#     "Forward DT Feature Set",
# ]
# models = [
#     LinearRegression,
#     RandomForestRegressor,
#     DecisionTreeRegressor,
#     KNeighborsRegressor,
#     GradientBoostingRegressor,
# ]

# labels = [str(x())[:-2] for x in models]

# # Defining Model Parameters

# knr_params = {
#     "n_neighbors": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 13, 15, 20],
#     "metric": ["euclidean", "manhattan", "minkowski"],
# }
# search_params = {
#     LinearRegression: "none",
#     DecisionTreeRegressor: "none",
#     KNeighborsRegressor: "grid",
#     GradientBoostingRegressor: "random",
#     RandomForestRegressor: "grid",
# }
# rf_params = {"n_estimators": [50, 75, 100, 125, 150], "max_depth": list(range(1, 10))}
# gbr_params = {
#     "criterion": ["squared_error", "friedman_mse"],
#     "learning_rate": [0.1, 0.15, 0.2, 0.25],
#     "max_depth": [2, 3, 4, 5],
#     "max_features": ["sqrt", None],
#     "max_leaf_nodes": list(range(2, 10)),
#     "n_estimators": list(range(50, 500, 50)),
#     "subsample": [0.8, 0.9, 1.0],
# }
# cv_params = {
#     KNeighborsRegressor: knr_params,
#     GradientBoostingRegressor: gbr_params,
#     RandomForestRegressor: rf_params,
# }

# # Training Models on Each Feature Set and Collecting Accuracy Values on Test Data
# for i, j in zip(range(len(feature_sets)), feature_names):
#     print(j)

# for i, j in zip(range(len(feature_sets)), feature_names):
#     if i == 0:
#         df_score = pd.DataFrame()
#         df_residuals = pd.DataFrame()
#         list_residuals = list(range(len(models)))

#     print(f"Current Feature set: {j} {i+1}/{len(feature_sets)}")
#     x_train_features = x_train[feature_sets[i]]
#     x_test_features = x_test[feature_sets[i]]

#     for k, p in enumerate(models):
#         if p in (LinearRegression, DecisionTreeRegressor):
#             print(f"Model Currently Being Trained: {labels[k]}")

#             model = p()
#             model.fit(x_train_features, y_train)
#             y_pred = model.predict(x_test_features)

#             residuals = np.subtract(y_test, y_pred)
#             list_residuals[k] = abs(residuals)

#             new_score = pd.DataFrame()

#             new_score.loc[k, "Model"] = labels[k]
#             new_score.loc[k, "Score"] = model.score(x_test_features, y_test)
#             new_score.loc[k, "R2 Score"] = metrics.r2_score(y_test, y_pred)
#             new_score.loc[k, "Feature Set"] = feature_names[i]
#             new_score.loc[k, "Hypertuned"] = "None"

#             df_score = pd.concat([df_score, new_score])

#             print("Done Training")

#         else:
#             if search_params[p] == "grid":
#                 print(f"Model Currently Being Trained: {labels[k]}")

#                 model = p()
#                 cv = GridSearchCV(model, cv_params[p], cv=5)

#                 results = cv.fit(x_train_features, y_train)
#                 results = cv.best_params_

#                 model = p(**results)
#                 model.fit(x_train_features, y_train)
#                 y_pred = model.predict(x_test_features)

#                 residuals = np.subtract(y_test, y_pred)
#                 list_residuals[k] = abs(residuals)

#                 new_score = pd.DataFrame()

#                 new_score.loc[k, "Model"] = labels[k]
#                 new_score.loc[k, "Score"] = cv.best_score_
#                 new_score.loc[k, "R2 Score"] = metrics.r2_score(y_test, y_pred)
#                 new_score.loc[k, "Feature Set"] = feature_names[i]
#                 new_score.loc[k, "Hypertuned"] = "GridSearchCV"

#                 df_score = pd.concat([df_score, new_score])

#                 print("Done Training")

#             elif search_params[p] == "random":
#                 print(f"Model Currently Being Trained: {labels[k]}")

#                 model = p()
#                 cv = RandomizedSearchCV(model, cv_params[p], cv=5)

#                 results = cv.fit(x_train_features, y_train)
#                 results = cv.best_params_

#                 model = p(**results)
#                 model.fit(x_train_features, y_train)
#                 y_pred = model.predict(x_test_features)

#                 residuals = np.subtract(y_test, y_pred)
#                 list_residuals[k] = abs(residuals)

#                 new_score = pd.DataFrame()

#                 new_score.loc[k, "Model"] = labels[k]
#                 new_score.loc[k, "Score"] = cv.best_score_
#                 new_score.loc[k, "R2 Score"] = metrics.r2_score(y_test, y_pred)
#                 new_score.loc[k, "Feature Set"] = feature_names[i]
#                 new_score.loc[k, "Hypertuned"] = "RandomSearchCV"

#                 df_score = pd.concat([df_score, new_score])

#                 print("Done Training")

#             else:
#                 print(f"Model Currently Being Trained: {labels[k]}")

#                 model = p()
#                 model.fit(x_train_features, y_train)
#                 y_pred = model.predict(x_test_features)

#                 residuals = np.subtract(y_test, y_pred)
#                 list_residuals[k] = abs(residuals)

#                 new_score = pd.DataFrame()

#                 new_score.loc[k, "Model"] = labels[k]
#                 new_score.loc[k, "Score"] = model.score(x_train_features, y_train)
#                 new_score.loc[k, "R2 Score"] = metrics.r2_score(y_test, y_pred)
#                 new_score.loc[k, "Feature Set"] = feature_names[i]
#                 new_score.loc[k, "Hypertuned"] = "None"

#                 df_score = pd.concat([df_score, new_score])

#                 print("Done Training")

#     df_residuals[feature_names[i]] = list_residuals

#     if i == len(feature_sets):
#         print("Done Training All Models and Sets")

# df_score.sort_values(by="Score", ascending=False)

# # Exporting Out Modle Accuracy Data

# df_score.to_csv("/CSV Data Files/processed/01_Model_Accuracy_Scores.csv")
