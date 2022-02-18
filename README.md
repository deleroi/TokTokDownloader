# TikTok video player and downloader

### What does this app do?
Through the socket from the client to the server, we send the TikTok video ID. The server downloads the video, converts it to jpg frames, creates an archive with frames, and sends it back to the client. On the client, the frames open in the browser and play as video.

### Where can I get the video ID?
Video id can be obtained from URL , numbers after /video
**video/9374597983427587543**

> ### Installing 
>>Installing Server
>>```sh
>> pip install TikTokApi
>> python -m playwright install
>> ```

>> ### Installing Client
>>```sh
>>pip install Flask
>> ```

### Run
```sh
python3.10 TikTokServer/get_video.py
python3.10 TikTokClient/app.py
```
