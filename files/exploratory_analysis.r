library(tidyverse)
library(ggplot2)
library(corrplot)

saveplot <- function(name, vect) {
    path <- paste("plots/", name, ".png", sep = "")
    
    vect <- append(vect, path)

    ggsave(
        filename = path,
        units = "cm",
        dpi = 300,
        width = 40,
        height = 29
    )
    return(vect)
}

# create vector to store paths of plots

plot_paths <- c()

# Load Data

df <- read.csv("csv_data_files/interim/01_no_outliers.csv")

view(df)
# Data Preparation for Correlation Chart

cor <- cor(df)
cor <- cor[
    c("Mixing_Time", "Active_1", "Active_2", "Active_3", "Active_4", "Water", "Crashout", "Viscosity"),
    c("Mixing_Time", "Active_1", "Active_2", "Active_3", "Active_4", "Water", "Crashout", "Viscosity")
]

# Plot Correlation Chart

corrplot(cor,
    addCoef.col = "black",
    outline = TRUE,
    method = "square",
    type = "lower",
    tl.pos = "ld",
    tl.col = "black",
    tl.cex = 1.2,
    tl.srt = 45,
    diag = FALSE
)

# Box and Whiskers of Mixing time vs Viscocity

df |>
    ggplot(aes(as_factor(Mixing_Time), Viscosity, fill = as_factor(Mixing_Time))) +
    stat_boxplot(geom = "errorbar", width = 0.5, linewidth = 0.5) +
    geom_boxplot(linewidth = 0.3, alpha = 1, show.legend = T) +
    theme_bw() +
    theme_classic() +
    scale_y_continuous(breaks = c(2500, 5000, 6500, 7500, 8000, 10000)) +
    labs(
        x = "Mixing Time (Minutes)",
        y = "Viscosity (cP)",
        title = "Viscosity with Varying Mixing Times",
        fill = "Mixing Times"
    ) +
    theme(
        legend.position = "top",
        legend.justification = "left",
        legend.title = element_text(face = "bold", size = 16),
        legend.text = element_text(face = "bold", size = 12),
        legend.background = element_rect(fill = "transparent"),
        panel.grid.major = element_blank(),
        panel.grid.minor = element_blank(),
        plot.title = element_text(face = "bold", size = 30, hjust = 0, family = "serif"),
        axis.title = element_text(size = 12, face = "bold"),
        axis.text = element_text(face = "bold", family = "sans", size = 12, color = "black")
    ) +
    annotate("text", x = 1, y = 8400, label = "Target Viscosity Range\n(6500cP - 8000cP)", color = "black", family = "serif", fontface = "bold", size = 5) +
    annotate("rect", xmin = 0.5, xmax = 1.5, ymin = 8000, ymax = 8800, alpha = 0.2) +
    annotate("rect", xmin = 0, xmax = 5.6, ymin = 6500, ymax = 8000, alpha = 0.2, fill = "yellow")

plot_paths <- saveplot("ex_box_viscosity_mixingtime", plot_paths)

# Mixing Time vs Crashout as Function of Active_1

df |>
    ggplot(aes(Mixing_Time, Crashout, color = as_factor(Active_1))) +
    geom_smooth(level = 0.1) +
    geom_point() +
    theme_bw()

plot_paths <- saveplot("ex_line_mixingtime_active1", plot_paths)

# Density Plot of Crashout

df |>
    ggplot(aes(Viscosity)) +
    geom_density(alpha = 0.5) +
    theme_bw()

plot_paths <- saveplot("ex_density_crashout", plot_paths)

# Box and Whiskers of Crashout vs Active_1

df |>
    ggplot(aes(as_factor(Active_1), Crashout)) +
    geom_boxplot() +
    theme_bw()

plot_paths <- saveplot("ex_box_crashout_active1", plot_paths)

#write.csv(plot_paths, file = "plots/exploratory_plot_paths.csv")