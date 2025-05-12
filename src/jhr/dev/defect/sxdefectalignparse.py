import pandas as pd
import re

entries = []

with open("correction_output.txt", "r") as file:
    for line in file:
        line = line.strip()

        # Skip empty or decorative lines
        if not line or set(line) in [{'='}, {'-'}, {'+'}]:
            continue

        # Case 1: Match "Key: value unit"
        match_colon = re.match(r'^([\w\s\+\-().]+):\s+(-?\d+\.?\d*)\s*([a-zA-Z]*)', line)
        if match_colon:
            key = match_colon.group(1).strip().lower().replace(" ", "_")
            value = float(match_colon.group(2))
            unit = match_colon.group(3) if match_colon.group(3) else ""
            entries.append({"parameter": key, "value": value, "unit": unit})
            continue

        # Case 2: Match "Key = value unit"
        match_equal = re.match(r'^([\w\s\+\-().]+)=\s*(-?\d+\.?\d*)\s*([a-zA-Z]*)', line)
        if match_equal:
            key = match_equal.group(1).strip().lower().replace(" ", "_")
            value = float(match_equal.group(2))
            unit = match_equal.group(3) if match_equal.group(3) else ""
            entries.append({"parameter": key, "value": value, "unit": unit})
            continue

        # Case 3: "key = string" (non-numeric)
        if '=' in line:
            parts = line.split('=', 1)
            key = parts[0].strip().lower().replace(" ", "_")
            val = parts[1].strip()
            entries.append({"parameter": key, "value": val, "unit": ""})
            continue

        # Case 4: "key: string" (non-numeric)
        if ':' in line:
            parts = line.split(':', 1)
            key = parts[0].strip().lower().replace(" ", "_")
            val = parts[1].strip()
            entries.append({"parameter": key, "value": val, "unit": ""})
            continue

# Create DataFrame (long format)
df = pd.DataFrame(entries)

# Display the result
print(df)
