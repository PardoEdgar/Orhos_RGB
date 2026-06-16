library(arrow)
library("tidyverse")
path <- "C:/Users/PardoEA/Downloads/dataset_pixels"

data <- open_dataset(path)

data_long <- data |>
  select(ID, Date, R,G,B) |> 
  collect() |> sample_n(1000000) |>
  pivot_longer(
    cols = c(R, G, B),
    names_to = "Channel",
    values_to = "Value"
  )

data_long$Channel <- factor(
  data_long$Channel,
  levels = c("R", "G", "B")
)

data_long$Date <- factor(
  data_long$Date,
  levels = c("February","January", "September", "August")
)

colors <- c("chocolate", "gray", "black", "yellow")

ggplot(data_long, aes(x = Value, color = Date)) +
  geom_density() +
  scale_color_manual(values = colors) +
  facet_wrap(~ID + Channel, ncol = 3) +
  xlab("Pixel intensity (0-255)") +
  ylab("Frequency of observations") +
  theme_classic()
