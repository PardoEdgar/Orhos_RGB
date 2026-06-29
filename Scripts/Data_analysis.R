library("tidyverse")
path <- "C:/Users/PardoEA/Downloads/Data_pixels.csv"
data <- read.csv(path)
data_long <- pivot_longer(
  data,
  names_to = "RGB",
  cols = c(R, G, B),
  values_to = "Value"
) |>
  mutate(
    month_year = factor(
      paste(month, year),
      levels = c(
        "August 2022",
        "March 2023",
        "August 2023",
        "September 2023",
        "January 2024"
      )
    )
  )
stat_summary <- data_long |>
  group_by(month, year, Type, RGB) |>
  summarise(
    mean = mean(Value),
    sd = sd(Value),
    SE = sd / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    month_year = factor(
      paste(month, year),
      levels = c(
        "August 2022",
        "March 2023",
        "August 2023",
        "September 2023",
        "January 2024"
      )
    )
  )

colors <- c("darkorange", "yellow", "gray", "purple", "darkred")

ggplot(
  data_long,
  aes(
    x = data_long$month_year,
    y = data_long$Value,
    color = data_long$month_year
  )
) +
  geom_violin(alpha = 1) +
  geom_jitter(size = 0.5, alpha = 0.1, width = 0.2) +
  geom_boxplot(
    width = 0.2,
    position = position_identity(),
    color = "black",
    alpha = 0.5
  ) +
  geom_errorbar(
    data = stat_summary,
    aes(x = month_year, ymax = mean + SE, ymin = mean - SE),
    width = 0.1,
    inherit.aes = FALSE
  ) +
  geom_point(
    data = stat_summary,
    aes(x = month_year, y = mean),
    color = "darkred",
    size = 2,
    inherit.aes = FALSE
  ) +
  facet_wrap(~ Type + RGB, nrow = 2) +
  scale_color_manual(values = colors) +
  theme_classic() +
  xlab("month year") +
  ylab("Pixel intensity (0-255)") +
  labs(title = "12 colonies automated RGB plot", color = "month year") +
  theme(
    legend.position = "top",
    title = element_text(size = 20)
  )


ggplot(
  data_long,
  aes(
    x = Value,
    color = month_year
  )
) +
  geom_density() +
  facet_wrap(~ Type + RGB, nrow = 2) +
  scale_color_manual(values = colors) +
  theme_classic() +
  xlab("Month Year") +
  ylab("Value") +
  labs(title = "Automated", color = "Month & year") +
  theme(
    legend.position = "top",
    title = element_text(size = 20)
  )
data_type_3 <- data_long |> dplyr::filter(Type == "Type 3")

kruskal.test(Value ~ month, data_type_3)


########################################## Plot con smooth
data_long_num <- pivot_longer(
  data,
  names_to = "RGB",
  cols = c(R, G, B),
  values_to = "Value"
) |>
  mutate(
    month_year = factor(
      paste(month, year),
      levels = c(
        "August 2022",
        "March 2023",
        "August 2023",
        "September 2023",
        "January 2024"
      )
    )
  ) |>  mutate(month_numeric = case_when(month == "August"~ 6,month == "March"~ 3,month == "January"~ 1,month == "September"~ 7))

stat_summary_num <- data_long_num |>
  group_by(month, year, Type, RGB) |>
  summarise(
    mean = mean(Value),
    sd = sd(Value),
    SE = sd / sqrt(n()),
    .groups = "drop"
  ) |>
  mutate(
    month_year = factor(
      paste(month, year),
      levels = c(
        "August 2022",
        "March 2023",
        "August 2023",
        "September 2023",
        "January 2024"
      ) 
    )
  ) |>  mutate(month_numeric = case_when(month == "August"~ 6,month == "March"~ 3,month == "January"~ 1,month == "September"~ 7))

ggplot(
  data_long_num,
  aes(
    x = data_long_num$month_year,
    y = data_long_num$Value,
    color = data_long_num$month_year
  )
) +
  geom_violin(alpha = 1) +
  geom_jitter(size = 0.5, alpha = 0.1, width = 0.2) +
  geom_boxplot(
    width = 0.2,
    position = position_identity(),
    color = "black",
    alpha = 0.5
  ) +
  geom_errorbar(
    data = stat_summary_num,
    aes(x = month_year, ymax = mean + SE, ymin = mean - SE),
    width = 0.1,
    inherit.aes = FALSE
  ) +
  geom_point(
    data = stat_summary_num,
    aes(x = month_year, y = mean),
    color = "darkred",
    size = 2,
    inherit.aes = FALSE
  ) +
  facet_wrap(~ Type + RGB, nrow = 2) +
  scale_color_manual(values = colors) +
  theme_classic() +
  xlab("month year") +
  ylab("Pixel intensity (0-255)") +
  labs(title = "12 colonies automated RGB plot", color = "month year") +
  theme(
    legend.position = "top",
    title = element_text(size = 20)
  )


kruskal.test(Value ~ month, data_type_3)
