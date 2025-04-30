# Formulation Dataset Analysis

This repo contains the functions and classes for performing exploratory data analysis and applying machine learning modeling to make predictive models. 

## Project Organization

### files

Contains Python packages and R scripts. The R scripts are run from Python using subprocess and the command line, the Python files are imported as classes when needed.

### csv_data_files

Contains 3 folders:
raw: For the initial raw dataset
interim: For the dataset after removal of outliers
processed: For the dataset after PCA transformation. The final model accuracy and residuals are also housed here.

### plot

A landing spot for the plots made from the R scripts and Python functions. Saved as PNGs.

### models

A landing spot for the trained models. Saved as pkl files.

## Usage

The main.py file contains a helper class called "analysis", which contains functions for running each part of the analysis:

```python

    # class to run the different scripts such as removing outliers and graphical analysis
    helper = analysis()

    # Run R script to view outliers in box plot form. Saves graphs
    helper.view_outliers()
    
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

```

--------

