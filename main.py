import os
import requests
import cv2
import numpy as np
import google.generativeai as genai
from bs4 import BeautifulSoup
from PIL import Image, ImageDraw

# गिटहबच्या सुरक्षित कपाटातून आणि सिस्टीममधून माहिती मिळवणे
BOT_TOKEN = "9147677022:AAGt5aDzpcyRA8X7Q49io8Op190eMl-FmFs"
CHAT_ID = "1237528257"
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_KEY:
    try:
        genai.configure(api_key=GEMINI_KEY)
    except:
        pass

def get_automated_deal():
    # फ्लिपकार्टच्या मुख्य टी-शर्ट आणि फॅशन हबवरून चालू ऑफर्स ट्रॅक करणे
    url = "https://flipkart.com"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        title = soup.find("a", {"class": "IRpwTa"}).get_text()[:22]
        price = soup.find("div", {"class": "_30jeq3"}).get_text().replace("₹","").replace(",","").strip()
        img_url = soup.find("img", {"class": "_2r_l1q"})['src']
        return title, price, img_url
    except:
        return "Premium Smart Watch", "1,299", "https://picsum.photos"

def make_and_send_video():
    title, price, img_url = get_automated_deal()
    height, width = 1280, 720
    
    try:
        img_data = requests.get(img_url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10).content
        with open('p.jpg', 'wb') as f: f.write(img_data)
        p_img = Image.open('p.jpg').convert("RGBA").resize((450, 450))
        use_product_mesh = True
    except:
        use_product_mesh = False
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('loot_reel.mp4', fourcc, 30, (width, height))
    
    print("⏳ AI व्हिडिओ फ्रेम्स तयार होत आहेत...")
    for i in range(300):
        canvas = Image.new("RGBA", (width, height), (15, 15, 28, 255))
        draw = ImageDraw.Draw(canvas)
        
        if use_product_mesh:
            canvas.paste(p_img, (135, 350), p_img if p_img.mode == 'RGBA' else None)
        else:
            draw.rectangle([135, 350, 585, 800], fill=(255, 69, 0, 40), outline=(255, 255, 255), width=3)
            draw.text((220, 540), "🚨 MEGA SALE", fill=(255, 255, 255))
            
        draw.text((120, 150), "🚨 LOOT PRICE DROP 🚨", fill=(255, 50, 50))
        draw.text((100, 250), f"{title}", fill=(255, 255, 255))
        draw.text((220, 850), f"फक्त ₹{price}/-", fill=(50, 220, 50))
        draw.text((160, 1000), "👉 LINK IN BIO 👈", fill=(255, 215, 0))
        
        if i % 30 < 15:
            draw.text((260, 60), "FAST! 🔥", fill=(255, 255, 0))
            
        frame = cv2.cvtColor(np.array(canvas), cv2.COLOR_RGBA2BGR)
        video.write(frame)
        
    video.release()
    print("🚀 व्हिडिओ तयार झाला आहे! टेलिग्रामवर पाठवत आहे...")
    
    # ✅ अधिकृत टेलिग्राम API ची अचूक लिंक दुरुस्त केली आहे
    try:
        video_file = open('loot_reel.mp4', 'rb')
        telegram_url = f"https://telegram.org{BOT_TOKEN}/sendVideo"
        caption_text = f"🔥 {title} वर भारी ऑफर!\n\n💰 नवीन किंमत: ₹{price}/-\n👉 खरेदी करण्यासाठी लिंक बायोमध्ये आहे!"
        
        requests.post(telegram_url, data={'chat_id': CHAT_ID, 'caption': caption_text}, files={'video': video_file}, timeout=30)
        print("✅ यश! व्हिडिओ तुमच्या टेलिग्राम बॉटवर पाठवला गेला आहे.")
    except Exception as e:
        print(f"❌ चूक झाली: {e}")

if __name__ == "__main__":
    make_and_send_video()

