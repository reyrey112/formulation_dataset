import matplotlib.pyplot as plt
import seaborn as sns

# put df_residules and feature names all in one fucntoin or class so that it can be nputted at once

class model_accuracy_plotting():
    def __init__(self):
        pass        

    def title_to_filename(self,title):
        new_title = title.split(" ")
        filename = "_".join(new_title)

        return filename

    def save_model(self, title):
        filename = self.title_to_filename(title)

        plt.savefig(f"plots/{filename}.png")

        plt.close()

    def graph_accuracy(self, data):
        title = "Comparison of Accuracy Between Models"

        plt.figure(figsize=(15, 10))
        plt.style.use("default")
        sns.barplot(x="Model", y="Score", hue="Feature Set", data=data)
        plt.title(
            title,
            fontdict={"size": 18, "fontweight": "bold"},
        )
        plt.xlabel("Model", fontdict={"size": 14, "fontweight": "bold"})
        plt.ylabel("Accuracy", fontdict={"size": 14, "fontweight": "bold"})
        plt.legend(loc="lower right")

        self.save_model(title)

    def graph_residuals(self, residuals, feature_names, model_names):
        plt.figure()
        plt.style.use("classic")
        colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
        plt.style.use("default")
        plt.rcParams["axes.prop_cycle"] = plt.cycler(color=colors)
        plt.rcParams["axes.spines.right"] = False
        plt.rcParams["axes.spines.top"] = False

        for i,names in enumerate(feature_names):
            title = f"Residuals for {names}"

            plt.figure(i)

            plt.hist(residuals[names], edgecolor="black", linewidth=0.5, stacked=True)
            plt.tick_params(colors="#4d504f")
            plt.legend(labels=model_names, reverse=True, fontsize=10, loc="right", shadow=True)
            plt.title(title, fontdict={"size": 18, "weight": "bold"}, loc="center", pad=0)
            plt.xlabel(
                "Residual Value",
                fontdict={"fontname": "Times New Roman", "size": 14, "fontweight": "bold"},
            )
            plt.ylabel(
                "Count of Residuals",
                fontdict={"fontname": "Times New Roman", "size": 14, "fontweight": "bold"},
            )

            self.save_model(title)


# def plotting(df_score):

#     # Plotting Comparisoin of Model Accuracy Bar graph

#     plt.figure(figsize=(15, 10))
#     plt.style.use("default")
#     sns.barplot(x="Model", y="Score", hue="Feature Set", data=df_score)
#     plt.title(
#         "Comparison of Accuracy Between Models",
#         fontdict={"size": 18, "fontweight": "bold"},
#     )
#     plt.xlabel("Model", fontdict={"size": 14, "fontweight": "bold"})
#     plt.ylabel("Accuracy", fontdict={"size": 14, "fontweight": "bold"})
#     plt.legend(loc="lower right")
#     plt.show()

#     # Setting Plot Parameters

#     plt.figure()
#     plt.style.use("classic")
#     colors = plt.rcParams["axes.prop_cycle"].by_key()["color"]
#     plt.style.use("default")
#     plt.rcParams["axes.prop_cycle"] = plt.cycler(color=colors)
#     plt.rcParams["axes.spines.right"] = False
#     plt.rcParams["axes.spines.top"] = False

#     # Bar Charts of # of Residual vs Residual Value for Each Feature Set and Model

#     for i in feature_names:

#         plt.hist(df_residuals[i], edgecolor="black", linewidth=0.5, stacked=True)
#         plt.tick_params(colors="#4d504f")
#         plt.legend(labels=labels, reverse=True, fontsize=10, loc="right", shadow=True)
#         plt.title(f"Residuals for {i}", fontdict={"size": 18, "weight": "bold"}, loc="center", pad=0)
#         plt.xlabel(
#             "Residual Value",
#             fontdict={"fontname": "Times New Roman", "size": 14, "fontweight": "bold"},
#         )
#         plt.ylabel(
#             "Count of Residuals",
#             fontdict={"fontname": "Times New Roman", "size": 14, "fontweight": "bold"},
#         )
#         plt.show()
