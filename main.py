from TikTokApi import TikTokApi
from datetime import datetime
import asyncio
import os

import utils.file as file
from configs import config
from utils.data_processor import (
	process_video_data, process_id_dict,
	headers
)

ms_token = os.environ.get("MS_TOKEN", None)

def get_video_generator(api, key, type, size=1):
	if type == "hashtag":
		hashtag = api.hashtag(name=key)
		return hashtag.videos(count=size)
	elif type == "sound":
		sound = api.sound(id=key)
		return sound.videos(count=size)
	else:
		raise Exception("Invalid type")

async def fetch_video(config, key, crawled_ids, output, size=1):
	id = config["id"]
	output_path = f"./output/{id}.xlsx"

	print("=" * 20)
	print("Fetching data for id:", id, key)
	print(config)

	# Convert to start of day and end of day of parrameter (fornmat is DD/MM/YYYY)
	start = config.get("start", None)
	end = config.get("end", None)

	start_date = datetime.strptime(start, "%d/%m/%Y") if start else None
	end_date = datetime.strptime(end, "%d/%m/%Y") if end else None
	end_date = end_date.replace(hour=23, minute=59, second=59) if end_date else None

	async with TikTokApi() as api:
		await api.create_sessions(ms_tokens=[ms_token], num_sessions=1, sleep_after=3)

		videos = get_video_generator(api, key, config["type"], size)
		async for video in videos:
			# Check if video is already crawled
			if video.id in crawled_ids:
				print("Video is already crawled", video.id)
				continue

			# Check if the video is in the range
			if start_date and video.create_time < start_date:
				continue
			if end_date and video.create_time > end_date:
				continue

			# Check if download address is available
			download_addr = video.as_dict.get("video", {}).get("downloadAddr", None)
			if not download_addr:
				print("Download address is not available", video.id)
				continue

			# Process video data
			print("Processing video data...", len(output) + 1, key, video.id)
			video_info = process_video_data(video.as_dict)
			output.append(video_info)
			crawled_ids[video_info["video_id"]] = True

			# Save video file
			try:
				video_path = f"./output/{id}/{video.id}.mp4"
				if not os.path.exists(f"./output/{id}"):
					os.makedirs(f"./output/{key}")

				# Check if file exists
				if os.path.exists(video_path):
					print("Video file exists", video_path)
					continue

				# video_bytes = await video.bytes()
				video_new = api.video(url=video_info['url'])
				await video_new.info()
				video_bytes = await video_new.bytes()

				with open(video_path, 'wb') as file_output:
					file_output.write(video_bytes)

				print("Saved video file", video_path)

				# sleep for 1 second to avoid being blocked
				await asyncio.sleep(1)
			except Exception as e:
				print("Failed to save video file", video.id, e)

			# Save file every 10 videos
			if len(output) > 0 and len(output) % 10 == 0:
				file.save_excel(output_path, output, headers, id)
				print("Saved to file", len(output), "videos", id)

				# sleep for 2 seconds to avoid being blocked
				await asyncio.sleep(2)


	# Save to file
	file.save_excel(output_path, output, headers, id)
	print("Saved to file", len(output), "videos", id)
	print("Done fetching data", len(output), "videos", id)

if __name__ == "__main__":
	output_path = f"./output/{config['id']}.xlsx"
	output = file.read_excel_to_dict(output_path, sheet_name=config["id"])
	crawled_ids = process_id_dict(output)

	for key in config["keys"]:
		asyncio.run(
			fetch_video(
				key=key,
				config=config,
				output=output,
				crawled_ids=crawled_ids,
				size=500
			)
		)
