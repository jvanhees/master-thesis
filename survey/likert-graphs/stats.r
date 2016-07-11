require(likert)

# MySQL Query custom graph:
# SELECT results.information_without as 'without', results.information_with as 'with', COUNT(results.information_with) as count 
# FROM results, sessions WHERE results.session_id = sessions.id AND sessions.imagetype = 'video'
# GROUP BY results.information_without, results.information_with ORDER BY results.information_without, results.information_with




# all <- read.csv("all.csv", sep="\t", header=TRUE, colClasses=c('character', 'factor', 'factor', 'factor', 'factor'))
all <- read.csv("concat.csv", sep="\t", header=TRUE, colClasses=c('factor', 'factor', 'factor', 'factor'))

scale <- factor(c("Strongly disagree", "Disagree", "Neutral", "Agree", "Strongly agree"))

all$information <- factor(all$information, levels = scale)
all$engagement <- factor(all$engagement, levels = scale)

# testset <- informationCSV[which(informationCSV$without == 'Strongly disagree'),]
static <- all[which(all$imagetype == 'static'),]
video <- all[which(all$imagetype == 'video'),]

print(nrow(static[which(static$thumbnail == 'with'),]))
print(nrow(static[which(static$thumbnail == 'without'),]))

staticLikert <- likert(static[,c('information', 'engagement'), drop=FALSE], grouping = static$thumbnail)
videoLikert <- likert(video[,c('information', 'engagement'), drop=FALSE], grouping = video$thumbnail)

plot(staticLikert)
plot(videoLikert)
