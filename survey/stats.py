import numpy as np
from scipy.stats import mannwhitneyu
from scipy.stats import wilcoxon
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt

information_with = np.array([0,1,1,1,1,1,2,1,2,2,1,2,1,0,-1,1,-1,1,2,2,2,1,0,0,1,1,-1,0,0,2,2,2,1,1,2,2,1,0,2,2,2,2,2,2,1,2,2,2,1,-1,-1,1,1,-1,1,0,1,1,1,1,-1,1,1,1,1,1,1,1,2,-1,1,-1,0,0,1,1,2,1,2,1,2,-1,1,2,2,1,1,1,-2,-1,-1,-1,1,1,0,-1,1,2,0,2,1,1,1,-1,2,2,2,1,0,-1,2,2,2,2,1,-1,-1,1,1,-1,1,0,1,1,1,1,1,1,-2,1,2,2,2,2,2,1,1])
information_without = np.array([-1,-1,0,0,1,-1,1,-1,1,1,-1,1,1,-2,0,0,-2,-2,0,-1,-1,1,-1,1,1,-1,-1,-1,-1,0,1,2,0,1,1,0,-1,-2,-2,2,1,1,1,2,1,-1,-2,-2,1,-1,-1,1,-1,-1,0,-2,1,-1,1,1,-1,-2,1,-1,0,1,-1,1,1,-2,0,-1,-2,-1,1,1,0,1,2,-1,1,-2,-1,2,-1,-1,2,-2,-1,1,-2,-1,1,-2,0,-1,-1,1,-1,0,-2,1,0,1,-1,-1,-1,1,-1,-1,2,2,2,1,-1,-2,-1,-1,1,-2,-2,-2,1,-1,-1,1,-2,-1,-2,1,1,1,0,-1,1,-2,-2])

engagement_with = np.array([0,0,1,1,1,0,0,1,1,0,0,2,-1,-2,-2,0,0,0,2,2,2,1,0,0,0,-1,1,2,1,1,1,-1,0,1,-2,-1,-1,-2,-2,-1,1,1,1,0,-1,1,2,1,1,1,0,1,1,1,-1,1,1,1,0,2,-1,1,1,-1,-2,-1,1,1,0,-1,1,-1,0,0,-1,0,1,-1,1,2,1,-1,-1,2,-1,-1,1,1,-1,1,1,-1,1,0,-2,-1,0,1,0,1,-1,-1,-1,-1,-2,0,1,1,-1,0,2,1,2,-1,1,-1,1,-1,1,1,2,1,1,0,1,1,1,2,-2,2,1,2,2,2,1,-1,2])
engagement_without = np.array([1,0,1,0,-1,-2,-1,0,0,-1,0,1,-1,-2,-2,0,-1,-1,1,1,1,1,-1,0,-1,-1,1,1,-2,0,0,-2,0,-1,-2,-2,-2,-2,-2,1,1,-1,-1,1,1,-1,-1,-2,1,0,-1,-1,-2,0,-1,1,1,1,-1,2,0,-2,0,-1,-1,-1,-2,-1,0,-1,-2,-1,-2,-1,-1,1,1,1,2,-1,1,-2,0,1,-1,-1,1,-1,-1,1,-1,1,1,0,-2,-1,0,1,-1,0,0,-1,-2,-1,-2,-2,-1,-1,-1,-1,1,0,1,-1,-2,-2,-1,-1,-1,1,-2,-2,-1,-1,-1,1,-1,0,-2,2,-1,2,-1,1,-1,-2,-1])

engagement_static = np.array([-1,0,0,1,2,2,1,1,1,0,0,0,0,1,1,0,1,0,1,0,0,1,3,1,0,1,1,0,0,0,0,-1,3,0,3,2,0,2,1,0,1,-1,0,2,0,0,1,1,0,1,0,2,0,1,0,3,1])
information_static = np.array([1,2,1,1,0,2,1,2,1,0,2,-1,1,1,3,0,1,-1,0,2,0,1,1,2,0,0,0,1,2,2,0,0,3,0,2,0,0,2,1,1,1,2,-1,3,-1,1,1,2,0,1,3,0,1,0,1,2,1])

engagement_video = np.array([1,0,1,1,1,1,1,1,0,2,0,1,1,0,0,-2,0,2,2,-1,-2,2,3,3,2,3,1,0,1,1,0,-1,0,0,3,0,-1,0,-2,-1,3,1,0,0,0,2,-2,0,0,0,0,0,-1,0,2,2,2,0,2,0])
information_video = np.array([1,2,1,2,3,3,1,0,1,0,1,2,2,2,4,0,1,1,1,0,0,3,4,4,0,2,0,0,0,0,2,1,1,1,1,0,0,2,0,0,2,0,3,2,-2,1,0,0,3,0,0,2,3,-2,3,3,0,2,0,0])

print 'Information with vs without (wilcoxon):'
print wilcoxon(information_with, information_without)

print 'Engagement with vs without (wilcoxon):'
print wilcoxon(engagement_with, engagement_without)

print 'Engagement: Static difference vs video difference (mann-whitney-u)'
print mannwhitneyu(engagement_static, engagement_video, alternative='two-sided')
print 'Information: Static difference vs video difference (mann-whitney-u)'
print mannwhitneyu(information_static, information_video, alternative='two-sided')


print 'Engagement: Static difference vs video difference (T-Test)'
print ttest_ind(engagement_static, engagement_video)
print 'Information: Static difference vs video difference (T-Test)'
print ttest_ind(information_static, information_video)



# values = np.add(information_with, 2)
# histo_with = np.bincount(values)
#
# values = np.add(information_without, 2)
# histo_without = np.bincount(values)
#
# print 'information with:'
# print 'mean', np.mean(information_with)
# print 'median', np.median(information_with)
# print 'std', np.std(information_with)
#
# print 'information without:'
# print 'mean', np.mean(information_without)
# print 'median', np.median(information_without)
# print 'std', np.std(information_without)
#
# print 'engagement with:'
# print 'mean', np.mean(engagement_with)
# print 'median', np.median(engagement_with)
# print 'std', np.std(engagement_with)
#
# print 'engagement without:'
# print 'mean', np.mean(engagement_without)
# print 'median', np.median(engagement_without)
# print 'std', np.std(engagement_without)
#
#
# print 'information static:'
# print 'mean', np.mean(information_static_with)
# print 'median', np.median(information_static_with)
# print 'std', np.std(information_static_with)
#
# print 'information video:'
# print 'mean', np.mean(information_video_with)
# print 'median', np.median(information_video_with)
# print 'std', np.std(information_video_with)

#
#
# ind = np.arange(5)
# width = 0.35
#
# fig, ax = plt.subplots()
# rects1 = ax.bar(ind, histo_with, width, color='b')
# rects2 = ax.bar(ind+width, histo_without, width, color='g')
#
# ax.set_ylabel('Frequency')
# ax.set_title('I know what to expect from the video')
# ax.set_xticks(ind + width)
# ax.set_xticklabels(('strongly disagree', 'disagree', 'nor agree nor disagree', 'agree', 'strongly agree'))
#
# ax.legend((rects1[0], rects2[0]), ('Including thumbnail', 'Excluding thumbnail'))
#
# plt.show()