import os
import requests
import google.generativeai as genai
from bs4 import BeautifulSoup

BOT_TOKEN = "9147677022:AAGt5aDzpcyRA8X7Q49io8Op190eMl-FmFs"
CHAT_ID = "1237528257"
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

if GEMINI_KEY:
    try:
        genai.configure(api_key=GEMINI_KEY)
    except:
        pass

def get_automated_deal():
    # फ्लिपकार्ट क्लोदिंग आणि टॉप ब्रँड्स सेक्शनवरून थेट डेटा ट्रॅक करणे
    base_url = "https://flipkart.com"
    product_url = "https://flipkart.com/clothing-and-accessories/top-brands/pr?sid=clo,clb"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    
    try:
        res = requests.get(product_url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        
        # प्रॉडक्टचे नाव, किंमत आणि खरी खरेदी लिंक शोधणे
        title = soup.find("a", {"class": "IRpwTa"}).get_text().strip()
        price = soup.find("div", {"class": "_30jeq3"}).get_text().strip()
        link_suffix = soup.find("a", {"class": "IRpwTa"})['href']
        final_link = base_url + link_suffix
        return title, price, final_link
    except:
        return "Premium Brand T-Shirt / Apparel", "₹399", product_url

def generate_script_and_send():
    title, price, final_link = get_automated_deal()
    
    # गुगल जेमिनी एआय कडून इन्स्टाग्राम रीलसाठी कडक मराठी स्क्रिप्ट लिहून घेणे
    marathi_script = "🔥 कडक ऑफर! मित्रांनो फ्लिपकार्टवर या प्रॉडक्टवर आज भारी डिस्काउंट मिळाला आहे. किंमत खूप कमी झाली आहे, स्टॉक संपण्यापूर्वी नक्की चेक करा!"
    if GEMINI_KEY:
        try:
            model = genai.GenerativeModel('gemini-pro')
            prompt = f"Product: {title} available at price {price}. Write a viral, catching Instagram Reel promotion script in Marathi language under 40 words. Include a call to action to check the link."
            response = model.generate_content(prompt)
            if response.text:
                marathi_script = response.text.strip()
        except:
            pass

    # थेट गिटहबच्या आउटपुट लॉगमध्ये आणि फाईलमध्ये डेटा सेव्ह करणे
    output_text = f"""
====================================
📢 PRODUCT REPORT (FLIPKART)
====================================
📦 प्रॉडक्टचे नाव: {title}
💰 चालू किंमत: {price}
🔗 खरेदी करण्यासाठी लिंक: {final_link}

✍️ GEMINI AI मराठी रील स्क्रिप्ट:
{marathi_script}
====================================
"""
    print(output_text)
    
    with open("deal_report.txt", "w", encoding="utf-8") as f:
        f.write(output_text)

if __name__ == "__main__":
    generate_script_and_send()
