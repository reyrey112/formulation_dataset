library(tidyverse)
library(ggplot2)

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

plot_paths <- c()

df <- read.csv("csv_data_files/raw/Formulations.csv")

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
        axis.title = element_text(size = 14, face = "bold"),
        axis.text = element_text(face = "bold", family = "sans", size = 12, color = "black")
    ) +
    annotate("text", x = 1, y = 8400, label = "Target Viscosity Range\n(6500cP - 8000cP)", color = "black", family = "serif", fontface = "bold", size = 6.5) +
    annotate("rect", xmin = 0.5, xmax = 1.5, ymin = 8000, ymax = 8800, alpha = 0.2) +
    annotate("rect", xmin = 0, xmax = 5.6, ymin = 6500, ymax = 8000, alpha = 0.2, fill = "yellow")

plot_paths <- saveplot("outliers_box_viscosity_mixingtime", plot_paths)