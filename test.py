import youtube_dl

url="https://www.youtube.com/watch?v=2sW08zLO8S8"

ydl_opts={
    "format":"worstaudio",
    "postprocessors":[{
        "key":"FFmpegExtractAudio",
        "preferredcodec":"mp3",
        "preferredquality":"50",
    }],
}
                
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])




