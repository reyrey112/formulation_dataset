library(tidyverse)

#Import the Dataset in

#R init file?
#make the dataset import form python import file once its been setup
df <- read.csv("csv_data_files/raw/Formulations.csv")


#make it into function and then have main in the same folder to call? or have main with the other mains to call?    
#Dropping unnesscary coloumns

df <- df |> select(-c(Formulation_Number,Main_Formulation_Number,Sub_Formulation_Number))

#Numerical Outlier Removal

summa <- df |>
    group_by(Mixing_Time) |>
    summarize(Q3 = quantile(Viscosity, probs = 0.75),
            Q1 = quantile(Viscosity, probs = 0.25))

upper_0.5 <- as.numeric(summa[1,'Q3'] + (1.5 * (summa[1,'Q3'] -  summa[1,'Q1'])))
lower_0.5 <- as.numeric(summa[1,'Q1'] - (1.5 * (summa[1,'Q3'] -  summa[1,'Q1'])))
upper_1 <- as.numeric(summa[2,'Q3'] + (1.5 * (summa[2,'Q3'] -  summa[2,'Q1'])))
lower_1 <- as.numeric(summa[2,'Q1'] - (1.5 * (summa[2,'Q3'] -  summa[2,'Q1'])))
upper_1.5 <- as.numeric(summa[3,'Q3'] + (1.5 * (summa[3,'Q3'] -  summa[3,'Q1'])))
lower_1.5 <- as.numeric(summa[3,'Q1'] - (1.5 * (summa[3,'Q3'] -  summa[3,'Q1'])))
upper_2 <- as.numeric(summa[4,'Q3'] + (1.5 * (summa[4,'Q3'] -  summa[4,'Q1'])))
lower_2 <- as.numeric(summa[4,'Q1'] - (1.5 * (summa[4,'Q3'] -  summa[4,'Q1'])))
upper_2.5 <- as.numeric(summa[5,'Q3'] + (1.5 * (summa[5,'Q3'] -  summa[5,'Q1'])))
lower_2.5 <- as.numeric(summa[5,'Q1'] - (1.5 * (summa[5,'Q3'] -  summa[5,'Q1'])))

df_out <- df |> filter(
    (Mixing_Time == 0.5 & Viscosity < upper_0.5 & Viscosity > lower_0.5) |
    (Mixing_Time == 1 & Viscosity < upper_1 & Viscosity > lower_1) |
    (Mixing_Time == 1.5 & Viscosity < upper_1.5 & Viscosity > lower_1.5) |
    (Mixing_Time == 2 & Viscosity < upper_2 & Viscosity > lower_2) |
    (Mixing_Time == 2.5 & Viscosity < upper_2.5 & Viscosity > lower_2.5))

#Exporting Dataset

write.csv(df_out, row.names = FALSE, file = "csv_data_files/interim/01_no_outliers.csv")
