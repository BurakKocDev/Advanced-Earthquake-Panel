import streamlit as st
import pandas as pd
import plotly.express as px
import datetime
import json
import urllib.request
import plotly.graph_objects as go
import numpy as np
from sklearn.cluster import DBSCAN  # DBSCAN import'unda görünmez karakter hatası düzeltildi

# --- Sayfa Yapılandırması ---
st.set_page_config(layout="wide")

# --- Veri Yolları ---
FILE_PATH = r"C:\Users\ASUS\Desktop\TezCalismalar\Earthquakes\Earthquakes_USGS.csv"
GEOJSON_URL = "https://raw.githubusercontent.com/fraxen/tectonicplates/master/GeoJSON/PB2002_boundaries.json"


@st.cache_data
def load_data(file_path):
    """
    CSV dosyasını yükler, 'time' sütununu KARIŞIK formatları deneyecek şekilde
    tarih/saat formatına çevirir ve sütun adlarını basitleştirir.
    """
    try:
        with st.spinner(f"Lütfen bekleyin... 4.3 Milyon satırlık deprem verisi yükleniyor..."):
            df = pd.read_csv(file_path)
        
        df.rename(columns={
            'latitude': 'lat',
            'longitude': 'lon',
            'mag': 'magnitude'
        }, inplace=True, errors='ignore')

        with st.spinner("Tüm zaman formatları analiz ediliyor... (Bu işlem birkaç dakika sürebilir)"):
            df['time'] = pd.to_datetime(df['time'], format='mixed', errors='coerce', utc=True)

        original_count = len(df)
        df.dropna(subset=['time', 'lat', 'lon', 'magnitude', 'depth'], inplace=True)
        cleaned_count = len(df)
        dropped_count = original_count - cleaned_count
        
        st.success(f"Veri işleme tamamlandı. Toplam {cleaned_count:,} adet geçerli deprem kaydı yüklendi.")
        if dropped_count > 0:
            st.warning(f"UYARI: {dropped_count:,} adet satır, eksik veya bozuk tarih/konum bilgisi nedeniyle atlandı.")
        
        if cleaned_count == 0:
            st.error("HATA: Hiç geçerli veri bulunamadı. CSV dosyanızın içeriğini kontrol edin.")
            return None
            
        return df
        
    except FileNotFoundError:
        st.error(f"HATA: Dosya bulunamadı. Lütfen '{FILE_PATH}' yolunu kontrol edin.")
        return None
    except Exception as e:
        st.error(f"Veri yüklenirken bir hata oluştu: {e}")
        return None

# --- GeoJSON (Tektonik Plaka) Yükleme Fonksiyonu ---
@st.cache_data
def load_geojson(url):
    """
    Verilen URL'den GeoJSON verisini yükler.
    """
    try:
        with st.spinner("Tektonik plaka sınırları yükleniyor..."):
            with urllib.request.urlopen(url) as response:
                geojson_data = json.loads(response.read())
        return geojson_data
    except Exception as e:
        st.error(f"HATA: Tektonik plaka verisi yüklenemedi: {e}")
        return None

# --- Ana Uygulama Başlangıcı ---

# Veriyi yükle
df = load_data(FILE_PATH)
geojson_data = load_geojson(GEOJSON_URL)

if df is None or geojson_data is None:
    st.stop()

# --- Başlık ---
st.title("🌎 Gelişmiş Etkileşimli Deprem Panosu (1900-2025)")
st.markdown("Bu pano, USGS veri setini kullanarak sismik aktiviteleri, tektonik plakaları, "
            "enerji salınımını, frekansları ve **Makine Öğrenimi (ML)** ile kümelenmiş fay hatlarını görselleştirir.")

# --- KENAR ÇUBUĞU (Sidebar) - Filtreler ---
st.sidebar.header("Filtreleme Seçenekleri")

# 1. Tarih Aralığı Filtresi
st.sidebar.subheader("Tarih Aralığı")
min_date = df['time'].min().date()
max_date = df['time'].max().date()

st.sidebar.info(f"Veri Aralığı: **{min_date}** ile **{max_date}** arası.")

start_date = st.sidebar.date_input("Başlangıç Tarihi", min_date, min_value=min_date, max_value=max_date)
end_date = st.sidebar.date_input("Bitiş Tarihi", max_date, min_value=start_date, max_value=max_date)

# 2. Büyüklük (Magnitude) Filtresi
st.sidebar.subheader("Büyüklük (Magnitude)")
min_mag = 0.0
max_mag = float(pd.to_numeric(df['magnitude'], errors='coerce').max())

mag_range = st.sidebar.slider(
    "Büyüklük Aralığı Seçin",
    min_value=min_mag,
    max_value=max_mag,
    value=(6.5, max_mag),  # Başlangıçta 6.5 ve üzerini göster
    step=0.1
)

# --- YENİ EKLEME: 3. Makine Öğrenimi (ML) Görünüm Seçeneği ---
st.sidebar.subheader("Harita Görünümü Seçin")
color_by = st.sidebar.radio(
    "Haritadaki noktaları renklendir:",
    ("Büyüklük", "Sismik Küme (DBSCAN)"),
    index=0, # Varsayılan olarak "Büyüklük" seçili gelsin
    help="Sismik Küme, depremlerin konumlarına göre yoğunlaştığı bölgeleri (fay hatlarını) "
         "otomatik olarak bulan bir ML modelidir."
)
# --- YENİ EKLEME SONU ---


# --- Veriyi Filtreleme ---
start_datetime = pd.to_datetime(start_date, utc=True)
end_datetime = pd.to_datetime(end_date, utc=True) + datetime.timedelta(days=1)

filtered_df = df[
    (df['time'] >= start_datetime) &
    (df['time'] < end_datetime) &
    (pd.to_numeric(df['magnitude'], errors='coerce') >= mag_range[0]) &
    (pd.to_numeric(df['magnitude'], errors='coerce') <= mag_range[1])
]

# --- Performans Uyarısı ---
MAX_POINTS_TO_DISPLAY = 50000
st.sidebar.info(f"Filtre sonucu {len(filtered_df):,} deprem bulundu.")

if len(filtered_df) > MAX_POINTS_TO_DISPLAY:
    st.sidebar.warning(
        f"Çok fazla sonuç ({len(filtered_df):,}). Tarayıcı performansını korumak için "
        f"haritada rastgele {MAX_POINTS_TO_DISPLAY:,} nokta gösteriliyor."
    )
    display_df = filtered_df.sample(MAX_POINTS_TO_DISPLAY)
else:
    display_df = filtered_df.copy() # .copy() ile 'SettingWithCopyWarning' önlenir

# --- Yıllık Frekans ve Enerji Analizi için Veri Hazırlama ---
if not filtered_df.empty:
    filtered_df['year'] = filtered_df['time'].dt.year
    yearly_counts = filtered_df.groupby('year').size().reset_index(name='count')
    
    analysis_df = filtered_df[['time', 'magnitude']].copy()
    analysis_df['energy'] = np.power(10, 1.5 * pd.to_numeric(analysis_df['magnitude'], errors='coerce'))
    analysis_df = analysis_df.sort_values(by='time')
    analysis_df['cumulative_energy'] = analysis_df['energy'].cumsum()
    
else:
    yearly_counts = pd.DataFrame(columns=['year', 'count'])
    analysis_df = pd.DataFrame(columns=['time', 'cumulative_energy'])


# --- YENİ EKLEME: DBSCAN Kümeleme Hesaplaması ---
if color_by == "Sismik Küme (DBSCAN)" and not display_df.empty:
    with st.spinner("Makine öğrenimi modeli (DBSCAN) çalıştırılıyor... Yoğun sismik bölgeler hesaplanıyor..."):
        # 1. Veriyi hazırla: DBSCAN, Haversine metriği için radyan bekler
        coords = np.radians(display_df[['lat', 'lon']].values)
        
        # 2. Modeli ayarla
        # eps = 0.03 (Radyan cinsinden. Yaklaşık 190km'lik bir yarıçap)
        # min_samples = 25 (Bir bölgeyi "yoğun" kabul etmek için min. deprem sayısı)
        db = DBSCAN(eps=0.03, min_samples=25, metric='haversine', n_jobs=-1)
        
        # 3. Modeli çalıştır ve kümeleri al
        clusters = db.fit_predict(coords)
        
        # 4. Kümeleri 'display_df'ye ekle (Plotly için string'e çevir)
        # -1 = Gürültü (Noise) olarak etiketlenir
        display_df['cluster'] = [f"Küme {c}" if c != -1 else "Gürültü (Noise)" for c in clusters]
        
        num_clusters = len(set(clusters)) - (1 if -1 in clusters else 0)
        st.sidebar.success(f"ML modeli {num_clusters} adet ana sismik küme buldu.")

elif 'cluster' in display_df.columns:
    # Eğer kullanıcı Büyüklük'e geri dönerse, eski sütunu temizle
    display_df = display_df.drop(columns=['cluster'])
# --- YENİ EKLEME SONU ---


# --- Ana Panel (Dashboard) - Görselleştirmeler ---

st.header("Coğrafi Dağılım Analizi")
tab1, tab2 = st.tabs(["Deprem Dağılım Haritası (Scatter Plot)", "Deprem Yoğunluk Haritası (Heatmap)"])

with tab1:
    # --- GÜNCELLENDİ: Harita başlığı ve çizimi artık ML seçeneğine duyarlı ---
    if color_by == "Sismik Küme (DBSCAN)":
        st.subheader("Makine Öğrenimi ile Sismik Kümeleme (DBSCAN)")
        st.markdown("Noktalar, ML modelinin bulduğu **Sismik Kümelere** göre renklendirilmiştir. "
                    "Tektonik plakaları bilmeden bile ana deprem kuşaklarını (Ateş Çemberi vb.) görebilirsiniz.")
    else:
        st.subheader("Deprem Dağılımı ve Tektonik Plakalar")
        st.markdown("Noktaların **rengi ve boyutu** depremin büyüklüğü ile orantılıdır. "
                    "**Kırmızı çizgiler** ana tektonik plaka sınırlarını gösterir.")
    # --- GÜNCELLEME SONU ---
    
    if not display_df.empty:
        
        # --- GÜNCELLENDİ: Hangi renklendirmeyi kullanacağımıza karar ver ---
        if color_by == "Sismik Küme (DBSCAN)" and 'cluster' in display_df.columns:
            fig_scatter = px.scatter_geo(
                display_df,
                lat='lat',
                lon='lon',
                color='cluster',        # Renklendirme kümelere göre
                hover_name='place',      
                hover_data={'lat': ':.2f', 'lon': ':.2f', 'depth': ':.1f km', 'magnitude': ':.1f'},
                projection="natural earth", 
                title=f"Sismik Kümeler ({start_date.year} - {end_date.year})",
                color_discrete_sequence=px.colors.qualitative.Vivid # Ayrı kümeler için belirgin renkler
            )
        else: # Varsayılan: Büyüklüğe göre
            fig_scatter = px.scatter_geo(
                display_df,
                lat='lat',
                lon='lon',
                color='magnitude',       # Renklendirme büyüklüğe göre
                size='magnitude',        # Boyutlandırma büyüklüğe göre
                hover_name='place',      
                hover_data={           
                    'lat': ':.2f',
                    'lon': ':.2f',
                    'depth': ':.1f km',
                    'time': True,
                    'magnitude': ':.1f'
                },
                projection="natural earth", 
                title=f"Deprem Dağılımı ({start_date.year} - {end_date.year})",
                color_continuous_scale=px.colors.sequential.OrRd 
            )
        # --- GÜNCELLEME SONU ---
        
        # Plaka Sınırlarını Ekleme (Bu kod her iki harita için de ortak)
        for feature in geojson_data['features']:
            coords = feature['geometry']['coordinates']
            lons, lats = zip(*coords)
            fig_scatter.add_trace(
                go.Scattergeo(
                    lon = lons,
                    lat = lats,
                    mode = 'lines',
                    line = dict(color='red', width=2),
                    name = 'Plaka Sınırı',
                    showlegend = False  # <--- 1. DÜZELTME BURADA
                )
            )
        
        # --- 2. DÜZELTME BURADA ---
        # Efsaneyi sadece ML Kümeleme görünümündeyken göster
        show_legend_for_clusters = (color_by == "Sismik Küme (DBSCAN)")
        fig_scatter.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0}, showlegend=show_legend_for_clusters) 
        # --- DÜZELTME SONU ---
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    else:
        st.warning("Bu filtre kriterlerine uyan veri bulunamadı.")


with tab2:
    st.subheader("Deprem Yoğunluk Haritası (Heatmap) ve Tektonik Plakalar")
    st.markdown("Bu harita, depremlerin coğrafi yoğunluğunu gösterir. 'Ateş Çemberi' **kırmızı plaka sınırları** ile çok daha net görülebilir.")

    if not display_df.empty:
        fig_heatmap = px.density_mapbox(
            display_df,
            lat='lat',
            lon='lon',
            z='magnitude',           
            radius=10,               
            center=dict(lat=0, lon=180), 
            zoom=0.5,
            mapbox_style="carto-positron", 
            title=f"Deprem Yoğunluk Haritası ({start_date.year} - {end_date.year})"
        )
        
        # Plaka Sınırlarını Mapbox Haritasına Ekleme
        fig_heatmap.update_layout(
            mapbox_layers=[
                {
                    "source": geojson_data,
                    "type": "line",
                    "color": "red",
                    "line": {"width": 2}
                }
            ]
        )
        
        fig_heatmap.update_layout(height=600, margin={"r":0,"t":40,"l":0,"b":0})
        st.plotly_chart(fig_heatmap, use_container_width=True)
    else:
        st.warning("Bu filtre kriterlerine uyan veri bulunamadı.")


# --- Kümülatif Enerji Grafiği ---
st.header("Kümülatif Sismik Enerji Salınımı (Benioff Strain)")
st.markdown("Seçtiğiniz filtreye göre zaman içinde salınan *toplam* sismik enerjinin birikimi. "
            "Grafikteki dik sıçramalar, büyük depremleri temsil eder.")

if not analysis_df.empty:
    fig_energy = px.line(
        analysis_df, 
        x='time', 
        y='cumulative_energy', 
        title="Zaman İçinde Kümülatif Enerji Salınımı",
        labels={'time': 'Tarih', 'cumulative_energy': 'Göreceli Kümülatif Enerji'} 
    )
    fig_energy.update_layout(xaxis_title="Tarih", yaxis_title="Göreceli Toplam Enerji")
    st.plotly_chart(fig_energy, use_container_width=True)
else:
    st.warning("Enerji analizi için bu filtre kriterlerine uyan veri bulunamadı.")


# --- Yıllık Frekans Grafiği ---
st.header("Yıllık Deprem Frekans Analizi")
st.markdown("Seçtiğiniz filtrelere uyan depremlerin yıllara göre dağılımı.")

if not yearly_counts.empty:
    fig_bar = px.bar(
        yearly_counts, 
        x='year', 
        y='count', 
        title="Yıllara Göre Deprem Sayısı",
        labels={'year': 'Yıl', 'count': 'Deprem Sayısı'} 
    )
    fig_bar.update_layout(xaxis_title="Yıl", yaxis_title="Toplam Deprem Sayısı")
    st.plotly_chart(fig_bar, use_container_width=True)
else:
    st.warning("Yıllık analiz için bu filtre kriterlerine uyan veri bulunamadı.")


# --- Veri Tablosu ---
st.header("Filtrelenmiş Ham Veri (İlk 1000 satır)")
# Analiz için eklediğimiz sütunları son tabloda göstermeye gerek yok
columns_to_drop = ['year']
if 'cluster' in filtered_df.columns:
    columns_to_drop.append('cluster')
if 'year' in filtered_df.columns:
    st.dataframe(filtered_df.drop(columns=columns_to_drop, errors='ignore').head(1000))
else:
     st.dataframe(filtered_df.head(1000))

