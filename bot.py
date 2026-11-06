import os
import requests

ACCESS_TOKEN = os.getenv("FB_ACCESS_TOKEN")
PAGE_ID = os.getenv("FB_PAGE_ID")
BASE_MEDIA_DIR = r"E:\herologo"

POST_CAPTION = """🎬 剧集《爱无止境》现已在 HeroDrama 平台上线！
📲 可在 Google Play 和 App Store 下载，立即观看最新热播内容，享受超高清画质！
👉 下载 HeroDrama，精彩不间断！

#HeroDrama #爱无止境 #热门短剧 #追剧 #高清画质 #短剧推荐 #好剧推荐 #必看剧集 #GooglePlay #AppStore #下载观看 #电视剧"""

def get_next_episode():
    if not os.path.exists(BASE_MEDIA_DIR):
        return None, None

    for category in os.listdir(BASE_MEDIA_DIR):
        cat_path = os.path.join(BASE_MEDIA_DIR, category)
        if os.path.isdir(cat_path):
            for drama_series in sorted(os.listdir(cat_path)):
                series_path = os.path.join(cat_path, drama_series)
                if os.path.isdir(series_path):
                    episodes = sorted(os.listdir(series_path))
                    for ep in episodes:
                        ep_path = os.path.join(series_path, ep)
                        if os.path.isfile(ep_path) and ep.lower().endswith(('.mp4', '.mov', '.jpg', '.png')):
                            return ep_path, drama_series
    return None, None

def post_to_facebook():
    if not ACCESS_TOKEN or not PAGE_ID:
        print("بيانات الاتصال بفيسبوك غير متوفرة.")
        return

    file_path, series_name = get_next_episode()
    if not file_path:
        print("انتهت جميع الحلقات، لا توجد ملفات جديدة.")
        return

    print(f"جاري رفع مسلسل: {series_name} - ملف: {os.path.basename(file_path)}")

    url = f"https://graph.facebook.com/{PAGE_ID}/feed"
    full_message = f"【 {series_name} 】\n\n{POST_CAPTION}"
    
    payload = {
        "message": full_message,
        "access_token": ACCESS_TOKEN
    }
    
    response = requests.post(url, data=payload)
    if response.status_code == 200:
        print(f"تم بنجاح نشر حلقة من مسلسل: {series_name}")
        os.remove(file_path)
    else:
        print(f"فشل النشر: {response.text}")

if __name__ == "__main__":
    post_to_facebook()
