from datetime import datetime

headers = ["video_id", "created_at", "crawled_at", "reaction_count", "comment_count", "collect_count", "share_count", "play_count", "author_id", "author_follower_count", "author_heart_count", "author_video_count",  "url", "content", "hashtags"]

def process_id_dict(data):
	output = {}

	for el in data:
		output[el["video_id"]] = True

	return output

def process_video_data(data):
	created_at = datetime.fromtimestamp(data["createTime"]).strftime("%d/%m/%Y %H:%M:%S")
	crawled_at = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

	hashtags = list(map(lambda x: x["hashtagName"], data["textExtra"])) if "textExtra" in data else []
	hashtags = '#' + ' #'.join(hashtags) if len(hashtags) > 0 else ""

	result = {
		"video_id": str(data["id"]),
		"created_at": created_at,
		"crawled_at": crawled_at,
		"reaction_count": data["stats"]["diggCount"],
		"comment_count": data["stats"]["commentCount"],
		"collect_count": data["stats"]["collectCount"],
		"share_count": data["stats"]["shareCount"],
		"play_count": data["stats"]["playCount"],
		"author_id": data["author"]["uniqueId"],
		"author_follower_count": data["authorStats"]["followerCount"],
		"author_heart_count": data["authorStats"]["heartCount"],
		"author_video_count": data["authorStats"]["videoCount"],
		"url": f"https://www.tiktok.com/@{data['author']['uniqueId']}/video/{data['id']}",
		"content": data["desc"],
		"hashtags": hashtags,
	}

	return result
