<div align="center">

# Advanced Earthquake Panel

### 1900–2025 küresel deprem kayıtları için etkileşimli Streamlit analiz panosu

Türkçe · [English](README.en.md)

![Streamlit](https://img.shields.io/badge/Streamlit-Dashboard-FF4B4B?logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-Data%20Analysis-3776AB?logo=python&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-Interactive%20Charts-3F4F75?logo=plotly&logoColor=white)
![scikit-learn](https://img.shields.io/badge/scikit--learn-DBSCAN-F7931E?logo=scikitlearn&logoColor=white)
![USGS Data](https://img.shields.io/badge/Data-USGS%20Earthquakes-2E7D32)

</div>

---

## Proje Hakkında

**Advanced Earthquake Panel**, geniş ölçekli küresel deprem kayıtlarını tarih ve büyüklük aralıklarına göre filtreleyen; coğrafi dağılımı, yoğunluğu, yıllık frekansı ve kümülatif sismik enerji göstergesini etkileşimli grafiklerle sunan bir Streamlit uygulamasıdır.

Proje, yaklaşık 4,3 milyon kayıt içerdiği belirtilen **Earthquakes Around the World from 1900–2025** veri seti için hazırlanmıştır. Deprem noktaları tektonik plaka sınırlarıyla birlikte gösterilir ve isteğe bağlı DBSCAN görünümüyle yoğun sismik konum kümeleri keşifsel olarak analiz edilir.

---

## Temel Özellikler

### Etkileşimli Filtreleme

- Başlangıç ve bitiş tarihine göre filtreleme
- Minimum ve maksimum deprem büyüklüğü seçimi
- Filtre sonucu bulunan kayıt sayısının gösterilmesi
- Büyük sonuç kümelerinde tarayıcı performansını korumak için en fazla 50.000 noktanın örneklenmesi

### Coğrafi Görselleştirme

- Büyüklüğe göre renklendirilen ve boyutlandırılan küresel deprem dağılım haritası
- Deprem yoğunluk haritası
- Ana tektonik plaka sınırlarının GeoJSON üzerinden haritalara eklenmesi
- Konum, derinlik, zaman ve büyüklük bilgilerini içeren etkileşimli araç ipuçları

### Keşifsel Kümeleme

- Haversine uzaklık metriğiyle DBSCAN
- Coğrafi koordinatların radyan cinsinden işlenmesi
- Yoğun sismik bölgelerin küme etiketleriyle görselleştirilmesi
- Küme dışı noktaların gürültü olarak işaretlenmesi

### İstatistiksel ve Zamansal Analiz

- Yıllara göre deprem sayısı
- Zamana göre kümülatif sismik enerji göstergesi
- Seçilen tarih ve büyüklük aralığına bağlı dinamik grafikler

---

## Analiz Yaklaşımı

### DBSCAN Kümeleme

Uygulama, görüntülenecek deprem koordinatları üzerinde aşağıdaki yapılandırmayla DBSCAN çalıştırır:

```text
metric      = haversine
eps         = 0.03 radians
min_samples = 25
```

Bu yaklaşım, birbirine coğrafi olarak yakın ve yoğun deprem noktalarını aynı kümede toplar. Çıktı, bilinen fay hatlarının bilimsel olarak doğrulanması değil; konumsal yoğunluk örüntülerini incelemek için kullanılan keşifsel bir görselleştirmedir.

### Kümülatif Enerji Göstergesi

Uygulamadaki göreli enerji değeri şu büyüklük ilişkisiyle hesaplanır:

```text
relative_energy = 10^(1.5 × magnitude)
```

Kayıtlar zamana göre sıralanır ve değerlerin kümülatif toplamı çizilir. Bu grafik, filtrelenen dönem içindeki büyük depremlerin göreli etkisini karşılaştırmaya yardımcı olur; kalibre edilmiş fiziksel enerji ölçümü veya doğrudan Benioff strain hesabı değildir.

---

## Veri Kaynakları

### Deprem Verisi

Proje aşağıdaki Kaggle veri seti için hazırlanmıştır:

```text
Earthquakes Around the World from 1900–2025
```

GitHub dosya boyutu sınırları nedeniyle yaklaşık 2 GB boyutundaki `Earthquakes_USGS.csv` repository içinde yer almamaktadır.

Beklenen temel kolonlar:

```text
time
latitude
longitude
mag
depth
place
```

Uygulama yükleme sırasında:

- `latitude` kolonunu `lat`
- `longitude` kolonunu `lon`
- `mag` kolonunu `magnitude`

olarak yeniden adlandırır ve geçersiz tarih, konum, büyüklük veya derinlik değerlerini temizler.

### Tektonik Plaka Verisi

Plaka sınırları uygulama çalışırken aşağıdaki açık GeoJSON kaynağından alınır:

```text
https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json
```

Bu nedenle tektonik plaka katmanının yüklenebilmesi için internet bağlantısı gerekir.

---

## Teknoloji Yığını

- **Python**
- **Streamlit**
- **Pandas**
- **NumPy**
- **Plotly**
- **Plotly Express**
- **scikit-learn**
- **GeoJSON**
- **USGS tabanlı deprem verisi**

---

## Proje Yapısı

```text
Advanced-Earthquake-Panel/
├── app.py
├── requirements.txt
└── README.md
```

Veri seti yerel olarak aşağıdaki şekilde eklenmelidir:

```text
Advanced-Earthquake-Panel/
├── Earthquakes_USGS.csv
├── app.py
├── requirements.txt
└── README.md
```

---

## Kurulum

### 1. Repository'yi klonlayın

```bash
git clone https://github.com/BurakKocDev/Advanced-Earthquake-Panel.git
cd Advanced-Earthquake-Panel
```

### 2. Veri setini ekleyin

Kaggle üzerinde `Earthquakes Around the World from 1900–2025` veri setini bulun ve `Earthquakes_USGS.csv` dosyasını `app.py` ile aynı klasöre yerleştirin.

### 3. CSV yolunu güncelleyin

`app.py` içindeki eski, bilgisayara özel yolu:

```python
FILE_PATH = r"C:\Users\ASUS\Desktop\TezCalismalar\Earthquakes\Earthquakes_USGS.csv"
```

aşağıdaki göreli yolla değiştirin:

```python
FILE_PATH = "Earthquakes_USGS.csv"
```

### 4. Bağımlılıkları kurun

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS / Linux:

```bash
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

### 5. Uygulamayı çalıştırın

```bash
streamlit run app.py
```

---

## Performans Notları

- Veri setinin tamamının belleğe yüklenmesi yüksek RAM kullanabilir.
- Tarih dönüşümü ve veri temizleme ilk çalıştırmada birkaç dakika sürebilir.
- Haritada gösterilecek kayıt sayısı 50.000 ile sınırlandırılır; istatistiksel grafikler filtrelenen tam veri üzerinden hesaplanır.
- DBSCAN yalnızca görüntüleme için seçilen örnek veri üzerinde çalışır.
- Aynı filtrelerle tekrar çalıştırılan veri ve GeoJSON yüklemeleri Streamlit cache mekanizmasından yararlanır.

---

## Sınırlılıklar

- Deprem verisi repository içinde bulunmaz ve kullanıcı tarafından ayrıca indirilmelidir.
- Kaynak kodda bulunan CSV yolu varsayılan hâliyle bilgisayara özeldir.
- Tektonik plaka katmanı harici bir internet kaynağına bağlıdır.
- Rastgele örnekleme nedeniyle haritadaki noktalar her çalıştırmada farklı olabilir.
- DBSCAN kümeleri doğrudan jeolojik fay hattı veya tektonik yapı doğrulaması olarak yorumlanmamalıdır.
- Göreli enerji formülü kalibre edilmiş fiziksel enerji hesabı değildir.
- Uygulama gerçek zamanlı deprem uyarısı, risk tahmini veya erken uyarı sistemi değildir.
- Proje eğitim, veri analizi ve portföy amacıyla geliştirilmiştir.

---

## Amaç

Advanced Earthquake Panel; büyük ölçekli jeo-uzamsal verinin temizlenmesi, filtrelenmesi, etkileşimli olarak görselleştirilmesi ve keşifsel makine öğrenmesi yöntemleriyle analiz edilmesini tek bir web panosunda birleştirir.
