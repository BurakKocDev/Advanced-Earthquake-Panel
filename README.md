# Advanced-Earthquake-Panel

Gelişmiş Etkileşimli Deprem Analiz Panosu (1900-2025)

Bu proje, 1900-2025 yılları arasındaki 4.3 milyondan fazla deprem kaydını içeren devasa bir USGS veri setini işleyen, analiz eden ve görselleştiren gelişmiş bir interaktif web uygulamasıdır.

Bu pano, sadece ham veriyi bir haritada göstermekle kalmaz, aynı zamanda jeolojik bağlam (tektonik plakalar), bilimsel analiz (enerji salınımı) ve makine öğrenimi (kümeleme) tekniklerini kullanarak sismik desenleri ortaya çıkarır.

🚀 Temel Özellikler

İnteraktif Coğrafi Görselleştirme:

Dağılım Haritası (Scatter Plot): Büyüklüğe göre dinamik boyutlandırma.

Yoğunluk Haritası (Heatmap): Sismik aktivitenin coğrafi yoğunluğu.

Jeolojik Bağlam (Tektonik Plakalar):

Tüm haritalara ana tektonik plaka sınırları eklenmiştir. Bu, "Ateş Çemberi" (Ring of Fire) gibi sismik kuşakların neden var olduğunu anında görselleştirir.

Makine Öğrenimi (DBSCAN Kümeleme):

DBSCAN algoritması (Haversine metriği ile) kullanılarak, sadece deprem konumlarına bakarak ana fay hatlarını ve sismik bölgeleri (kümeleri) otomatik olarak "keşfeder".

Bilimsel Analiz (Kümülatif Enerji Salınımı):

Seçilen filtre aralığı için zaman içindeki kümülatif sismik enerji salınımını (Benioff Strain) gösteren bir çizgi grafiği sunar ($Enerji \propto 10^{1.5 \times M}$).

İstatistiksel Analiz (Yıllık Frekans):

Seçilen filtre aralığındaki depremlerin yıllara göre dağılımını gösteren bir çubuk (bar) grafik sunar.

Dinamik Filtreleme ve Optimizasyon:

Tarih Aralığı ve Büyüklük (Magnitude) bazında filtreleme.

50.000+ nokta için rastgele örnekleme (.sample()) ile tarayıcı çökmesi engellenir.

💻 Teknik Yığın

Uygulama: Streamlit

Veri İşleme: Pandas

Görselleştirme: Plotly, Plotly Express

Bilimsel Hesaplama: Numpy

Makine Öğrenimi: Scikit-learn (sklearn)

🔧 Kurulum ve Çalıştırma

Bu depoyu klonlayın.

Veri Seti (ÖNEMLİ): Bu proje, ~2GB boyutunda bir veri seti kullanmaktadır. GitHub dosya limiti nedeniyle veri seti buraya dahil edilmemiştir (.gitignore ile yoksayılmıştır). Lütfen veri setini aşağıdaki Kaggle linkinden indirin:

Veri Kaynağı: Earthquakes Around the World from 1900-2025 (Kaggle)

İndirdiğiniz Earthquakes_USGS.csv dosyasını projenin ana klasörüne (app.py'nin yanına) yerleştirin.

Terminali açın ve gerekli kütüphaneleri kurun:

pip install -r requirements.txt


Uygulamayı başlatın:

streamlit run app.py
