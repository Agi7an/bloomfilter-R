#Plotting p against n, m:
library(ggplot2)
library(plotly)
library(hrbrthemes)


n.values = 10000
m.values = n.values * 32

k.values = seq(from = 1, to = 31, 1)
p0 = ((1 - (1 / m.values)) ^ (k.values * n.values))
p.values = ((1 - p0) ^ k.values)

plotts <- ggplot(data = data.frame(k = k.values, p = p.values),
                 mapping = aes(x = k, y = p)) + labs(x = "No. of Hash Functions", y = "False Probability Rate(log Scale)", title = "k Vs p Plot")
plotts <- plotts + scale_y_continuous(trans='log') + geom_point() + theme_ipsum()
ggplotly(plotts)

