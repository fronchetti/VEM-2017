require("effsize")

data <- read.csv("plotly_committer.txt")
wilcox.test(count ~ response, data) # p-value
cliff.delta(count ~ response, data) # effect size
