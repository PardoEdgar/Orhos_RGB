library("tidyverse")
path <- "C:/Users/jandr/Downloads/Data_pixels.csv"
data <- read.csv(path)
View(data)
data_long <- pivot_longer(
  data,
  names_to = "RGB",
  cols = c(h, s, v),
  values_to = "Value"
)
View(data_long)
colors <- c("darkorange", "yellow", "gray")
ggplot(data_long, aes(x = data_long$Value, fill = data_long$month)) +
  geom_histogram() +
  facet_wrap(~ data_long$Type + data_long$RGB, nrow = 2) +
  scale_fill_manual(values = colors)

data_type_3 <- data_long |> dplyr::filter(Type == "Type 3")

kruskal.test(Value ~ month, data_type_3)
