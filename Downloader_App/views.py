from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
import instaloader
import os
from pathlib import Path

DownloadFolder = str(Path.home() / "Downloads" / "Instagram")

# Ensure the folder exists
os.makedirs(DownloadFolder, exist_ok=True)

def Home(request):
    return render(request, "insert.html")

def download(request):
    if request.method == "GET":
        post_url = request.GET.get("url", None)
        print(post_url)
        
        if not post_url:
            return JsonResponse({"error": "No URL provided"}, status=400)

        try:
            loader = instaloader.Instaloader(download_pictures=False, download_video_thumbnails=False)

            shortcode = post_url.split("/")[-2]

            if not shortcode:
                return JsonResponse({"error": "Invalid URL provided"}, status=400)

            post = instaloader.Post.from_shortcode(loader.context, shortcode)
            
            os.chdir(DownloadFolder)
            
            loader.download_post(post, target="videos") 
            
            listOFDirectory = os.listdir(path=str(Path.home() / "Downloads" / "Instagram" / "videos"))
            print("listOFDirectory--> ", listOFDirectory)
            
            for file in listOFDirectory:
                path = str(Path.home() / "Downloads" / "Instagram" / "videos")
                try:
                    if not file.endswith(".mp4"):
                        file_path = os.path.join(path, file)
                        os.remove(path=file_path)
                except Exception as e:
                    return JsonResponse({"Error": str(e)})
                    
            return JsonResponse({
                "message": f"✅ Video downloaded successfully in '{DownloadFolder}/' folder!", 
                "path": str(DownloadFolder)
            })
            
        except instaloader.exceptions.InstaloaderException as e:
            return JsonResponse({"error": f"❌ Download failed: {str(e)}"}, status=500)

        except Exception as e:
            return JsonResponse({"error": f"⚠️ Unexpected error: {str(e)}"}, status=500)
        
    return render(request, "insert.html")