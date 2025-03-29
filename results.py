import os
import re
import pandas as pd

# Root directory where all logs are stored (including subfolders)
root_dir = "C:/Users/Sanal/Documents/Important/Workspace/EEEM071-Coursework/logs"

# Regular expressions for extracting data
map_pattern = re.compile(r"mAP:\s*([\d\.]+)%")
rank1_pattern = re.compile(r"Rank-1\s*:\s*([\d\.]+)%")
elapsed_pattern = re.compile(r"Elapsed\s*(\d+):(\d+):(\d+)")  # Matches HH:MM:SS

# List to store extracted results
results = []

# Walk through all subdirectories
for subdir, _, files in os.walk(root_dir):
    for filename in files:
        # if filename == "log_train.txt":  # Check for specific log file
            file_path = os.path.join(subdir, filename)

            # Extract the subfolder name (experiment name)
            subfolder_name = os.path.basename(subdir)

            # Read and process the log file
            with open(file_path, "r", encoding="utf-8") as file:
                log_content = file.read()

            # Extract metrics using regex
            map_match = map_pattern.search(log_content)
            rank1_match = rank1_pattern.search(log_content)
            elapsed_match = elapsed_pattern.search(log_content)

            # Extract values if found, otherwise set to None
            map_value = float(map_match.group(1)) if map_match else None
            rank1_value = float(rank1_match.group(1)) if rank1_match else None
            elapsed_time = (
                int(elapsed_match.group(1)) * 3600 +
                int(elapsed_match.group(2)) * 60 +
                int(elapsed_match.group(3))
            ) if elapsed_match else None

            # Store results, modifying filename in the output but not in storage
            results.append({
                "Subfolder": subfolder_name,
                "Filename (Modified)": f"{subfolder_name}_log_train.txt",
                "Original Filename": filename,
                "mAP (%)": map_value,
                "Rank-1 Accuracy (%)": rank1_value,
                "Elapsed Time (seconds)": elapsed_time
            })

# Convert results to a Pandas DataFrame
df = pd.DataFrame(results)

# Save to CSV for further analysis
df.to_csv("vehicle_reid_results.csv", index=False)

# Print results
print(df)
print(f"Results saved to vehicle_reid_results.csv")