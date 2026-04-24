import os
import google.generativeai as genai
import pandas as pd
import requests
from io import StringIO

API_KEY = "Insert your GOOGLE API"

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-3-flash-preview')


URL_GOOGLE_SHEET = "https://docs.google.com/spreadsheets/d/e/2PACX-1vR08YhIPbj8h-rHU2MTdiEujoTMcyvEMeVMYPUlx6m36ufPQDNjEA-K1oBbxFXCSdnYBt04sthJ6PF8/pub?gid=0&single=true&output=csv"

def ambil_data_cloud():
    try:
        response = requests.get(URL_GOOGLE_SHEET)
        response.raise_for_status()
        
        data_csv = StringIO(response.text)
        df = pd.read_csv(data_csv, encoding='utf-8')
        
        return "\n--- DATA STOK & HARGA (CLOUD) ---\n" + df.to_string(index=False)
    except Exception as e:
        print(f"⚠️ Gagal ambil data cloud: {e}")
        return ""

def muat_data_lokal():
    if os.path.exists("data.txt"):
        with open("data.txt", "r", encoding='utf-8') as file:
            return "\n--- INFO UMUM (ALAMAT & LAYANAN) ---\n" + file.read()
    return ""

def petshop_bot():
    print("--- 🚀 Bot Petshop Comppy Real-Time Cloud Aktif! ---")
    print("(Ketik 'keluar' untuk berhenti)\n")
    
    while True:
        user_input = input("Pelanggan: ")
        if user_input.lower() == 'keluar':
            break
            
        try:
            
            stok_harga = ambil_data_cloud()
            info_umum = muat_data_lokal()
            
            context = f"{info_umum}\n{stok_harga}"

            prompt = (
                f"Kamu adalah admin Petshop Comppy yang ceria. 🐾🐈\n"
                f"Gunakan DATA REFERENSI di bawah untuk menjawab.\n"
                f"Data Alamat/Layanan ada di INFO UMUM.\n"
                f"Data Stok/Harga ada di DATA CLOUD.\n\n"
                f"Jika tiba bisa menjawab maka tanyakan Admin dengan menyertai No WAnya. \n\nS"
                f"DATA REFERENSI:\n{context}\n\n"
                f"PERTANYAAN: {user_input}\n"
                f"JAWABAN:"
            )
            
            response = model.generate_content(prompt)
            print(f"AI: {response.text}")
            
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    petshop_bot()
