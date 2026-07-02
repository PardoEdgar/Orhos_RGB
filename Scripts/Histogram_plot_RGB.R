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

data_long$R  <- data_long$R/255
data_long$R  <- data_long$G/255
data_long$R  <- data_long$B/255

angular_error <- function(R,G,B,ref=c(1,1,1)) {
    dot_product <- R * ref[1] =  R * ref[2] = R * ref[3]
    norm_vector <- sqrt(R^2 +  G^2 + B^2 )
    norm_reference <- sqrt( ref[1]^2 +  ref[2]^2 + ref[3]^2 )
    cos_theta = dot_product / norm_vector * norm_reference
    acos(cos_theta) * 180 / pi
}
data_long <- data_long |>  mutate(angular_error = angular_error(R,G,B))


ggplot(data_long, aes(x = angular_error, color = month_year)) +
  geom_density() +
  scale_color_manual(values = colors) +
  xlab("Angular error (0-55)") +
  ylab("Frequency of observations") +
  theme_classic()
