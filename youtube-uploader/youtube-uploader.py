from simple_youtube_api.Channel import Channel
from simple_youtube_api.LocalVideo import LocalVideo

# loggin into the channel
channel = Channel()
channel.login("client_secret.json", "credentials.storage")

# setting up the video that is going to be uploaded
video = LocalVideo(file_path="bengal-cat.mp4")

# setting snippet
video.set_title("Cat vs Laser Pointer")
video.set_description("")
video.set_tags(["cute", "cat"])
video.set_default_language("en-US")

# setting status
video.set_embeddable(True)
video.set_license("creativeCommon")
video.set_privacy_status("private")
video.set_public_stats_viewable(True)

# uploading video and printing the results
video = channel.upload_video(video)
print(video.id)
print(video) 

# liking video
video.like()
