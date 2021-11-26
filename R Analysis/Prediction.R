library("reshape2")
library(ggplot2)
library(plotly)
library(hrbrthemes)

data.names <- read.table(file = "../Data/facebook-firstnames.txt", sep = "\n")[1:2e4, ]

p <- seq(1e-04, 1, 0.01)
first_collisions <- data.frame(p = p)
col.names <- c()
for (k in seq(4, 32, 4)){
  data <- read.table(file = paste0("first_collision_k", k), sep = "\n")
  first_collisions <- cbind(first_collisions, data)
  col.names <- c(col.names, paste0("k", k))
}
colnames(first_collisions) <- c("p", col.names)

reshaped <- melt(first_collisions, id = "p")
plott <- ggplot(data = reshaped, aes(x = p, y = value, color = variable))
plott <- plott + scale_x_continuous(trans='log') + geom_line(size = 1)
plott <- plott  + labs(colour = "No.of\nhash\nfunctions\n\n", fill = "Number of Hash Functions", x = "False Probability Rate", y = "No. of entries before first collision", title = "Are Bloom Filters Good?")
ggplotly(plott)
