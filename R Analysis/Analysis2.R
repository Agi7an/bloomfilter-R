library("reshape2")
library(ggplot2)
library(plotly)
library(hrbrthemes)

p <- seq(1e-04, 1, 0.01)
data <- data.frame(p = p)
data.col.names <- c()
for (k in seq(4, 32, 4)){
  m.n <- ((-k) / log(1 - exp(log(p) / k)))
  data <- cbind(data, m.n)
  data.col.names <- c(data.col.names, paste0("k", k))
}
colnames(data) <- c("p", data.col.names)

reshaped <- melt(data, id = "p")
plott <- ggplot(data = reshaped, mapping = aes(x = p, y = value, color = variable)) + labs(x = "False Probability Rate(log Scale)", y = "Bits per Entry", title = "p Vs m/n")
plott <- plott + scale_x_continuous(trans='log') + geom_line(size = 1) + theme_ipsum()
ggplotly(plott)

