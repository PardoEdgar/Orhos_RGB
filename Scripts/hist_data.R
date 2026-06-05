library(ggplot2)
path <- "C:/Users/jandr/Downloads/RGB_data.csv"
data <- read_csv(path)

data_long <- data |>
  pivot_longer(
    cols = c(R, G, B, meanRGB),
    names_to = "Channel",
    values_to = "Value"
  )
data_long$Channel <- factor(
  data_long$Channel,
  levels = c("R", "G", "B", "meanRGB")
)

data_long$Date <- factor(
  data_long$Date,
  levels = c("March", "September", "January")
)

colors <- c("chocolate", "gray", "black")
ggplot(data_long, aes(x = Value, color = Date)) +
  geom_density(aes(y = after_stat(count))) +
  scale_color_manual(values = colors) +
  facet_grid(~Channel) +
  xlab("Pixel intensity (0-255)") +
  ylab("Frequency of observations") +
  theme_classic()
