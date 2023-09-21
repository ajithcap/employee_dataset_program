import pandas as pd
import matplotlib.pyplot as plt
import sqlite3

conn = sqlite3.connect('Employee.db')

# Replace 'your_timeeries_query_here' with your SQL query for the Timeseries table
Timeseries_query = "SELECT employee_id, time_in_stamp, time_out_stamp, year, month, day FROM Timeseries"

df_Timeseries = pd.read_sql_query(Timeseries_query, conn)


# Define a custom function to parse the time data
def custom_time_parser(time_str):
    # Split the time string to separate hours, minutes, and AM/PM
    time_parts = time_str.split(':')
    hours = int(time_parts[0])
    minutes = int(time_parts[1])

    # Check if it's AM or PM and adjust the hours accordingly
    if "PM" in time_str:
        hours += 12

    # Create a datetime object with fixed seconds and microseconds
    return pd.Timestamp(year=2000, month=1, day=1, hour=hours, minute=minutes, second=0, microsecond=0)


# Use the custom parser to convert time columns
df_Timeseries['time_in_stamp'] = df_Timeseries['time_in_stamp'].apply(custom_time_parser)
df_Timeseries['time_out_stamp'] = df_Timeseries['time_out_stamp'].apply(custom_time_parser)

# Define the time ranges
normal_start = pd.Timestamp(year=2000, month=1, day=1, hour=8, minute=0, second=0, microsecond=0)
normal_end = pd.Timestamp(year=2000, month=1, day=1, hour=16, minute=0, second=0, microsecond=0)

# Calculate work duration per employee per day
df_Timeseries['work_duration'] = df_Timeseries['time_out_stamp'] - df_Timeseries['time_in_stamp']

# Calculate total work hours per employee per day in seconds
df_Timeseries['total_work_hours'] = df_Timeseries['work_duration'].dt.total_seconds() / 3600  # Convert to hours

# Create a DataFrame to track employees who worked overtime (over 8 hours), worked less than 8 hours, and arrived early
df_work_status = df_Timeseries.groupby(['employee_id', 'year', 'month', 'day']).agg(
    total_work_hours=('total_work_hours', 'sum'),
    early_arrival=('time_in_stamp', lambda x: any(x <= normal_start)),
).reset_index()

# Create a grouped bar chart with color-coded bars
plt.figure(figsize=(12, 8))
bar_width = 0.2
index = df_work_status.index

# Define color coding based on conditions
colors = []
labels = []
for _, row in df_work_status.iterrows():
    if 0 <= row['total_work_hours'] <= 8:
        colors.extend(['green', 'orange', 'red', 'blue'])
        labels.extend(['0-8 hours', 'Overtime', 'Less than 8 hours', 'Early Arrival'])
    elif row['total_work_hours'] > 8:
        colors.extend(['green', 'orange', 'red', 'blue'])
        labels.extend(['0-8 hours', 'Overtime', 'Less than 8 hours', 'Early Arrival'])
    elif row['early_arrival']:
        colors.extend(['blue', 'green', 'red', 'orange'])
        labels.extend(['Early Arrival', '0-8 hours', 'Less than 8 hours', 'Overtime'])
    else:
        colors.extend(['red', 'green', 'blue', 'orange'])
        labels.extend(['Less than 8 hours', '0-8 hours', 'Early Arrival', 'Overtime'])

# Create grouped bars
plt.bar(index - bar_width, df_work_status['total_work_hours'], bar_width, color=colors)
plt.xlabel('Employee and Date Index')
plt.ylabel('Total Work Hours')
plt.title('Employee Work Hours (Grouped Bar)')
plt.xticks(index, [f"Emp {row['employee_id']}, {row['year']}-{row['month']}-{row['day']}" for _, row in
                   df_work_status.iterrows()], rotation=90)
plt.tight_layout()

# Customize legend
legend_labels = [plt.Line2D([0], [0], color=color, lw=4, label=label) for color, label in zip(colors, labels)]
plt.legend(handles=legend_labels)

# Show the plot
plt.show()

# Close the database connection
conn.close()
