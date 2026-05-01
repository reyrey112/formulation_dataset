library(tidyverse)
library(ggplot2)
library(ggtext)
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

palette_colors <- c("#7577ec", "#1DB87E", "#F5A623", "#E84855", "#150074")

df |>
  ggplot(aes(as_factor(Mixing_Time), Viscosity,
             fill = as_factor(Mixing_Time),
             color = as_factor(Mixing_Time))) +

  annotate("rect",
    xmin = 0, xmax = 5.6, ymin = 6500, ymax = 8000,
    fill = "#F5A623", alpha = 0.08, color = "#F5A623",
    linewidth = 0.4, linetype = "dashed") +

  geom_boxplot(
    linewidth = 0.45,
    width = 0.55,
    alpha = 0.30,       
    outlier.shape = 21,
    outlier.size = 1.8,
    outlier.stroke = 0.4,
    show.legend = TRUE
  ) +

  annotate("label",
    x = 5.45, y = 7250,
    label = "Target range\n6500–8000 cP",
    hjust = 1, vjust = 0.5,
    fill = "#FFF8EC", color = "#BA7517",
    label.size = 0, label.padding = unit(0.35, "lines"),
    size = 3.2, lineheight = 1.3
  ) +

  scale_fill_manual(values = palette_colors) +
  scale_color_manual(values = palette_colors) +
  scale_y_continuous(
    breaks = c(2500, 5000, 6500, 7500, 8000, 10000),
    labels = scales::comma,
    expand = expansion(mult = c(0.02, 0.05))
  ) +
  scale_x_discrete(expand = expansion(add = 0.6)) +

  labs(
    x = "Mixing time (minutes)",
    y = "Viscosity (cP)",
    title = "Viscosity vs. mixing time",
    subtitle = "Shaded band shows target viscosity range (6500–8000 cP)",
    fill = "Mixing time",
    color = "Mixing time"
  ) +

  theme_minimal(base_size = 13) +
  theme(
    plot.title    = element_text(face = "bold", size = 18,
                                   color = "#1A1A2E", margin = margin(b = 4)),
    plot.subtitle = element_text(size = 11, color = "#666",
                                   margin = margin(b = 14)),
    plot.title.position = "plot",

    axis.title    = element_text(size = 11, color = "#555"),
    axis.text     = element_text(size = 10, color = "#444"),
    axis.ticks    = element_blank(),
    axis.line     = element_blank(),

    panel.grid.major.y = element_line(color = "#EBEBEB", linewidth = 0.4),
    panel.grid.major.x = element_blank(),
    panel.grid.minor   = element_blank(),

    legend.position      = c(0.01, 0.99),
    legend.justification = c(0, 1),
    legend.title         = element_text(size = 10, face = "bold"),
    legend.text          = element_text(size = 9),
    legend.key.size      = unit(0.55, "cm"),
    legend.background    = element_rect(fill = "white",
                              color = "#E0E0E0", linewidth = 0.3),

    plot.background  = element_rect(fill = "white", color = NA),
    panel.background = element_rect(fill = "white", color = NA),
    plot.margin      = margin(16, 20, 12, 16)
  )

plot_paths <- saveplot("outliers_box_viscosity_mixingtime", plot_paths)
