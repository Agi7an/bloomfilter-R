library("reshape2")
library(ggplot2)
library(plotly)
library(hrbrthemes)

data <- read.table(file = "../Data/predictionData.txt", sep = ",")
colnames(data) <- c("m", "n")

model = lm(n ~ m, data = data)

slope = model$coefficients[2]
intercept = model$coefficients[1]

n.pred <- predict(model, newdata = data.frame(m = 1500))

plt <- ggplot(data = data) + labs(x = "No. of bits in the bit array", y = "No. of entries before first collision", title = "Prediction Model")
plt <- plt + 
  geom_point(aes(x = m, y = n), size = 0.15, color = "black") + 
  geom_abline(intercept = intercept, slope = slope, color = "red", size = 0.8) + 
  theme_ipsum() + geom_point(aes(x = 1500, y = n.pred), color = "blue")
ggplotly(plt)



