import pandas as pd

FILE_PATH = r"C:\Users\ASUS\Desktop\TezCalismalar\Earthquakes\Earthquakes_USGS.csv"

print("Veri seti yükleniyor... (Bu işlem 2GB dosya için 1-2 dakika sürebilir)")

try:
    # Veriyi SADECE 'time' sütununu alarak yükle (daha hızlı)
    df = pd.read_csv(FILE_PATH, usecols=['time'])
    
    print("Yükleme tamamlandı.")
    print("-" * 30)
    
    print(f"Toplam {len(df):,} adet deprem kaydı bulundu.")
    print("-" * 30)
    
    print("Dosyadaki İLK 5 zaman damgası (Ham hali):")
    print(df['time'].head())
    print("-" * 30)

    print("Dosyadaki SON 5 zaman damgası (Ham hali):")
    print(df['time'].tail())
    print("-" * 30)

    # Şimdi tarihleri parse etmeyi deneyelim
    print("Tarih formatları analiz ediliyor...")
    parsed_times = pd.to_datetime(df['time'], errors='coerce')
    
    null_count = parsed_times.isnull().sum()
    valid_count = len(df) - null_count
    
    print(f"Başarıyla anlaşılan tarih sayısı: {valid_count:,}")
    print(f"Formatı anlaşılamayan (NaT) tarih sayısı: {null_count:,}")
    
    if null_count > 0:
        print("\nSONUÇ: Evet, veriler dosyada mevcut ancak formatı bozuk olduğu için")
        print(f"uygulama tarafından {null_count:,} adet satır siliniyor.")
    else:
        print("\nSONUÇ: Tüm tarihler başarıyla okundu.")

except Exception as e:
    print(f"Bir hata oluştu: {e}")