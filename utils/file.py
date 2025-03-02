import json
import os
import pandas as pd

def read_json(file_path):
	with open(file_path, 'r') as f:
		return json.load(f)

def save_json(file_path, data):
	with open(file_path, 'w') as f:
		json.dump(data, f, indent=4, ensure_ascii=False)

def save_csv(file_path, data, header=None):
	data = pd.DataFrame(data)
	data.to_csv(file_path, index=False, header=header)

def save_excel(file_path, data, header=None, sheet_name='Sheet1'):
	data = pd.DataFrame(data)
	data.to_excel(file_path, index=False, header=header, sheet_name=sheet_name)

def read_excel_to_dict(file_path, sheet_name='Sheet1'):
	# Check if file exists, if not then return 
	if not os.path.exists(file_path):
		return []

	# Read excel file
	data = pd.read_excel(file_path, sheet_name=sheet_name)

	# Convert value of "video_id" to string to avoid scientific notation
	if "video_id" in data.columns:
		data["video_id"] = data["video_id"].astype(str)

	# Convert to list of dictionaries
	return data.to_dict(orient='records')
