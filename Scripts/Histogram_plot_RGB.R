library(arrow)
library("tidyverse")
path <- "C:/Users/PardoEA/Downloads/RGB_data"

data <- open_dataset(path)

data_long <- data |>
  select(ID, month, year, R,G,B) |> 
  collect() |> sample_n(1000000) |>
  pivot_longer(
    cols = c(R, G, B),
    names_to = "Channel",
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

data_long$Channel <- factor(
  data_long$Channel,
  levels = c("R", "G", "B")
)



colors <- c("chocolate", "gray", "black", "yellow", "orange")

ggplot(data_long, aes(x = Value, color = month_year)) +
  geom_density() +
  scale_color_manual(values = colors) +
  facet_wrap(~ID + Channel, ncol = 3) +
  xlab("Pixel intensity (0-255)") +
  ylab("Frequency of observations") +
  theme_classic()
