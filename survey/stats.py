import numpy as np
from scipy.stats import mannwhitneyu
from scipy.stats import wilcoxon

engagement_static_with = np.array([0,0,2,2,2,2,1,-1,0,1,-2,-1,-1,-2,-2,-1,1,1,1,0,-1,1,2,1,1,1,1,1,0,1,-1,-2,0,-1,1,-1,0,1,-1,1,2,2,-1,-1,1,1,-1,1,0,-2,-1,0,-1,-1,0,1,2,1,2,1,-1,1,1,-2])
engagement_static_without = np.array([-1,0,1,1,1,1,0,-2,0,-1,-2,-2,-2,-2,-2,1,1,-1,-1,1,1,-1,-1,-2,-1,-2,0,1,-1,0,-1,-1,0,-1,-2,-1,1,1,1,2,-1,1,-1,-1,1,-1,1,1,0,-2,-1,0,0,-1,-2,-1,1,0,1,-1,-1,-1,1,-2])
engagement_video_with = np.array([0,0,1,1,1,0,0,1,1,-1,-2,-2,0,0,0,1,0,0,0,-1,1,2,1,1,1,1,0,-1,1,1,2,-1,1,-1,1,1,-1,0,0,1,-1,-1,1,1,-1,1,0,1,-1,-1,-2,1,-1,0,-1,1,-1,1,2,1,1,0,1,1,1,2,2,1])
engagement_video_without = np.array([1,0,1,0,-1,-2,-1,0,0,-1,-2,-2,0,-1,-1,1,-1,0,-1,-1,1,1,-2,0,1,0,-1,-1,1,1,2,0,-2,-1,-2,-1,-1,-2,-1,1,-2,0,1,-1,-1,1,-1,0,-1,-2,-2,-1,-1,-1,-1,-2,-2,1,-2,-2,-1,-1,-1,1,-1,0,2,-1])

information_static_with = np.array([2,1,2,2,2,2,2,2,1,1,2,2,1,0,2,2,2,2,2,2,1,2,2,2,1,1,-1,1,1,1,1,1,2,-1,1,1,1,2,1,2,1,2,2,1,-1,-1,-1,1,1,0,-1,1,1,-1,2,2,2,2,2,-1,1,1,0,-2])
information_static_without = np.array([1,-1,1,0,-1,-1,1,2,0,1,1,0,-1,-2,-2,2,1,1,1,2,1,-1,-2,-2,1,-1,-1,1,1,1,-1,0,1,-2,0,1,1,0,1,2,-1,2,-1,-1,1,-2,-1,1,-2,0,-1,-1,-2,1,-1,-1,2,2,2,-1,-1,1,0,-2])
information_video_with = np.array([0,1,1,1,1,1,2,1,2,1,0,-1,1,-1,1,1,0,0,1,1,-1,0,0,2,1,-1,-1,1,0,1,1,-1,1,1,1,1,-1,0,0,2,-1,1,1,1,-2,2,0,2,1,1,2,1,0,-1,2,1,-1,-1,1,0,1,1,1,1,1,1,1,2])
information_video_without = np.array([-1,-1,0,0,1,-1,1,-1,1,1,-2,0,0,-2,-2,1,-1,1,1,-1,-1,-1,-1,0,1,-1,-1,0,-2,-1,1,-1,-2,1,-1,1,-1,-2,-1,1,-2,-1,2,-2,-1,1,-1,0,1,0,-1,1,-1,-1,1,-1,-2,-2,-2,-2,1,-1,-1,1,-2,-1,1,1])

information_video_without_item1 = np.array([1,0,1,2,-1,2,1,2,1,1,1,1,1,1,2,1,1,-2,1,2,-1,0,-2])
information_static_without_item1 = np.array([-1,0,1,1,0,1,1,-1,1,0,1,1,-1,1,2,1,1,1,1,-2,1,1,1])

information_video_without_item2 = np.array([-1,-1,0,1,-2,1,1,-1,-1,1,-1,-2,1,2,-1,-2,0,-1,-1,2,-1])
information_static_without_item2 = np.array([-1,-1,1,-2,-2,-1,-1,-1,-1,-2,-1,-1,-2,-2,-2,-1,0,-1,-1,-2,-1,-2,1])

information_video_without_item3 = np.array([1,-1,1,0,-2,1,-2,-2,-1,0,0,0,-1,-1,-1,-1,-2,-1,2,1])
information_static_without_item3 = np.array([0,-1,1,0,-2,1,-1,0,-1,-1,-2,1,-1,-1,-1,0,-1,-1,-2,-2,-1,-1])

print 'Engagement:'
print 'static with versus static witouth (wilcoxon)'
print wilcoxon(engagement_static_with, engagement_static_without)
print ''
print 'video with versus video witouth (wilcoxon)'
print wilcoxon(engagement_video_with, engagement_video_without)
print ''
print 'static with versus video with (mann-whitney-u)'
print mannwhitneyu(engagement_static_with, engagement_video_with, alternative='two-sided')
print ''
print 'static without versus video without (mann-whitney-u)'
print mannwhitneyu(engagement_static_without, engagement_video_without, alternative='two-sided')
print ''
print ''
print 'Information:'
print 'static with versus static witouth (wilcoxon)'
print wilcoxon(information_static_with, information_static_without)
print ''
print 'video with versus video witouth (wilcoxon)'
print wilcoxon(information_video_with, information_video_without)
print ''
print 'static with versus video with (mann-whitney-u)'
print mannwhitneyu(information_static_with, information_video_with, alternative='two-sided')
print ''
print 'static without versus video without (mann-whitney-u)'
print mannwhitneyu(information_static_without, information_video_without, alternative='two-sided')

