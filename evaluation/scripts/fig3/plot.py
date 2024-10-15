import pandas as pd
import matplotlib.pyplot as plt

# Set the font family
plt.rcParams['font.family'] = 'candara'

# Load the data for the first plot
csv_adult = r"./evaluation/scripts/fig3/adult_labels.csv"
csv_child = r"./evaluation/scripts/fig3/child_labels.csv"
df_adult = pd.read_csv(csv_adult)
df_child = pd.read_csv(csv_child)
# Create the first subplot
ax1 = plt.subplot(1, 2, 1)
df_adult.plot(kind='scatter',x='width',y='height', label='Adult',color = 'grey', ax=ax1) # scatter plot
df_child.plot(kind='scatter',x='width',y='height',color = 'black', ax=ax1 ,  label='Child') # scatter plot
plt.title("Adult and Child \nDistribution",fontdict={'fontweight':'bold','fontsize':20})
# Set the legend
plt.legend(loc='lower right', prop={'weight': 'bold', 'size': 17})
# Load the data for the second plot
csv_detected = r"./evaluation/scripts/fig3/detected.csv"
csv_miss = r"./evaluation/scripts/fig3/undetected.csv"
df_detected = pd.read_csv(csv_detected)
df_miss = pd.read_csv(csv_miss)

# Create the second subplot
ax2 = plt.subplot(1, 2, 2, sharex=ax1, sharey=ax1)
df_detected.plot(kind='scatter',x='Width',y='Height', label='Detected', color = 'grey', ax=ax2) # scatter plot
df_miss.plot(kind='scatter',x='Width',y='Height',color = 'black', ax=ax2, label='Undetected') # scatter plot

# Set the legend
plt.legend(loc='lower right', prop={'weight': 'bold', 'size': 17})
plt.title("Deteced and Undeteced \nDistribution", fontdict={'fontweight':'bold','fontsize':20})

# Set the axis labels and tick labels
ax1.set_xlabel('Width', fontweight='bold', fontsize = 17)
ax1.set_ylabel('Height', fontweight='bold', fontsize = 17)
ax2.set_xlabel('Width', fontweight='bold', fontsize = 17)
ax2.set_ylabel('Height', fontweight='bold', fontsize = 17)

ax1.set_xticklabels(ax1.get_xticklabels(), fontdict = {'weight':'bold','fontsize':15})
ax1.set_yticklabels(ax1.get_yticklabels(), fontdict = {'weight':'bold','fontsize':15})
ax2.set_xticklabels(ax2.get_xticklabels(), fontdict = {'weight':'bold','fontsize':15})
ax2.set_yticklabels(ax2.get_yticklabels(), fontdict = {'weight':'bold','fontsize':15})

ax1.set_xticklabels(ax1.get_xticks(), fontdict = {'weight':'bold'})
ax1.set_yticklabels(ax1.get_yticks(), fontdict = {'weight':'bold'})
ax2.set_xticklabels(ax2.get_xticks(), fontdict = {'weight':'bold'})
ax2.set_yticklabels(ax2.get_yticks(), fontdict = {'weight':'bold'})

ax1.xaxis.set_major_formatter(plt.FormatStrFormatter("%d"))
ax1.yaxis.set_major_formatter(plt.FormatStrFormatter("%d"))
ax2.xaxis.set_major_formatter(plt.FormatStrFormatter("%d"))
ax2.yaxis.set_major_formatter(plt.FormatStrFormatter("%d"))

plt.gcf().set_size_inches(10,7.5)
# Show the merged plot
plt.savefig("Distribution Deteced and Age.png", dpi = 600)
