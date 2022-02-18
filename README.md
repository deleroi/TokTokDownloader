# TikTok video player and downloader

### What does this app do?
Through the socket from the client to the server, we send the TikTok video URL. The server downloads the video, 
converts it to jpg frames, creates an archive with frames, and sends it back to the client. On the client, the frames open in the browser and play as video.

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
