import os
import datetime
from functions.archive_path import TheArchivePath
import matplotlib.pyplot as plt
import matplotlib as mpl

# Directory to search for files
directory = TheArchivePath()

# Search string to filter files
search_string = " 20"

# Create a dictionary to store the created counts for each month
created_counts = {}

# Get the current year and month
now = datetime.datetime.now()
current_year = now.year
current_month = now.month

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file contains the search string
    if search_string in filename:
        # Get the creation date of the file
        # ctime = os.path.getctime(os.path.join(directory, filename))
        # cdate = datetime.datetime.fromtimestamp(ctime)
        # Extract the year and month from the filename
       
        year_month = filename[-15:-9]
        year = int(year_month[:4])
        if year_month[:-2] == '0':
            month_str = year_month[5:7].lstrip('0')
            month = int(month_str) if month_str else 1 
        else:
            month = int(year_month[-2:])         

        # Create a datetime object from the year and month
        cdate = datetime.datetime(year, month, 1)



        # Group the files by year and month, and increment the count
        key = (cdate.year, cdate.month)
        created_counts[key] = created_counts.get(key, 0) + 1

# Create a dictionary to store the modified counts for each month
modified_counts = {}

# Loop through all files in the directory
for filename in os.listdir(directory):
    # Check if the file contains the search string
    if search_string in filename:
        # Get the modification date of the file
        mtime = os.path.getmtime(os.path.join(directory, filename))
        mdate = datetime.datetime.fromtimestamp(mtime)
        # Group the files by year and month, and increment the count
        key = (mdate.year, mdate.month)
        modified_counts[key] = modified_counts.get(key, 0) + 1

# Merge the created and modified counts into a single dictionary
counts = {}
for key in set(created_counts.keys()) | set(modified_counts.keys()):
    counts[key] = (created_counts.get(key, 0), modified_counts.get(key, 0))

# Sort the dictionary by year and month
sorted_counts = sorted(counts.items())

# Display the sorted dictionary
# for (year, month), (created_count, modified_count) in sorted_counts:
#     print(f"{year}-{month}: {created_count} created, {modified_count} modified")

# Loop through the counts and print the output for the relevant months
now = datetime.datetime.now()
counts_list = []
for year in range(2021, now.year + 1):
    if year < now.year:
        for month in range(1, 13):
            created_count, modified_count = counts.get((year, month), (0, 0))
            counts_list.append((f"{year}-{month}", created_count, modified_count))
    elif year == now.year:
        for month in range(1, now.month + 1):
            created_count, modified_count = counts.get((year, month), (0, 0))
            counts_list.append((f"{year}-{month}", created_count, modified_count))
                # print(f"{year}-{month}: {created_count} created, {modified_count} modified")

# Set the default size of the graph to 1500 x 800
mpl.rcParams['figure.figsize'] = (15, 8)

# Create a bar chart of the counts for each month
labels = [label for label, _, _ in counts_list]
created_counts = [created_count for _, created_count, _ in counts_list]
modified_counts = [modified_count for _, _, modified_count in counts_list]
width = .95
x = list(range(len(labels)))
x = [i - width/2 for i in x]
fig, ax = plt.subplots()
rects1 = ax.bar(x, created_counts, width, label='Created', color=(0.98, 0.76, 0.25))
rects2 = ax.bar(x, modified_counts, width, bottom=created_counts, label='Modified', color=(0.4, 0.4, 0.4))
ax.set_xticks(x)
ax.set_xticklabels(labels, rotation=90)
ax.legend()

# Add text labels to the bars
for i, rect in enumerate(rects1):
    ax.text(rect.get_x() + rect.get_width() / 2.0, rect.get_height() / 2.0, str(created_counts[i]), ha='center', va='center', color='black')
    
y_offset = [0] * len(modified_counts)
for i, rect in enumerate(rects2):
    y = created_counts[i] + rect.get_height() / 2.0 + y_offset[i]
    ax.text(rect.get_x() + rect.get_width() / 2.0, y, str(modified_counts[i]), ha='center', va='center', color='white')
    y_offset[i] += rect.get_height()

# Add a title to the chart
ax.set_title('Counts of Created and Modified Notes/Ideas by Month', fontsize=16)

plt.show()