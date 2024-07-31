import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd


class ViolinPlotInput:
    def __init__(self, name, ibis):
        self.name = name
        self.ibis = ibis


# Sample data: two lists of IBIs
# ibi_list1 = [800, 850, 830, 870, 860, 840, 820, 810, 880, 850]
# ibi_list2 = [750, 780, 760, 790, 770, 755, 765, 785, 780, 770]


# Combine data into a DataFrame for seaborn

def violin_plots(ibis_list: [ViolinPlotInput]):
    all_ibis = []
    all_groups = []
    for plot in ibis_list:

        ibis = plot.ibis
        name = plot.name
        all_ibis.extend(ibis)
        all_groups.extend([name] * len(ibis))

    data = {
        'IBI': all_ibis,
        'Group': all_groups
    }
    df = pd.DataFrame(data)

    # Create the violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Group', y='IBI', data=df)

    # Add title and labels
    plt.title('Comparison of IBIs')
    plt.xlabel('Group')
    plt.ylabel('IBI (ms)')

    # Show the plot
    plt.show()

#
# ibi_lists = [
#     [800, 850, 830, 870, 860, 840, 820, 810, 880, 850],
#     [750, 780, 760, 790, 770, 755, 765, 785, 780],
#     [900, 920, 910, 930, 915, 925, 935],
#     # Add more lists as needed
# ]
#
# # Flatten the list of lists and create corresponding group labels
# all_ibi = []
# all_groups = []
#
# for idx, ibi_list in enumerate(ibi_lists):
#     all_ibi.extend(ibi_list)
#     all_groups.extend([f'Group {idx + 1}'] * len(ibi_list))
#
# # Combine data into a DataFrame for seaborn
# data = {
#     'IBI': all_ibi,
#     'Group': all_groups
# }
# df = pd.DataFrame(data)
#
# # Create the violin plot
# plt.figure(figsize=(12, 8))
# sns.violinplot(x='Group', y='IBI', data=df)
#
# # Add title and labels
# plt.title('Comparison of IBIs between Multiple Groups')
# plt.xlabel('Group')
# plt.ylabel('IBI (ms)')
#
# # Show the plot
# plt.show()
