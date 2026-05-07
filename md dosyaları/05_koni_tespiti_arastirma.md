# 05 — Koni Tespiti Algoritma Araştırması

## 1. Amaç ve yarışma bağlamı

Bu doküman, İnsansız Kara Aracı projesinde **trafik konilerinin kamera görüntüsünden tespit edilmesi** için kullanılabilecek yöntemleri araştırır ve uygulanabilir bir teknik karar önerir.

TEKNOFEST İnsansız Kara Aracı şartnamesine göre trafik konileri:

- **40 cm ± 10 cm x 40 cm ± 10 cm** kare tabanlı,
- **75 cm ± 5 cm** yükseklikte,
- **kırmızı-beyaz** veya **turuncu-beyaz** renkte olacaktır.

Araçtan beklenen davranış, koni engellerine **dokunmadan ilerlemek**tir. Ayrıca konilerin yerleşimi yarışma sırasında hakem heyeti tarafından belirleneceği için sistemin ezberlenmiş konumlara değil, gerçek zamanlı algılamaya dayanması gerekir.

## 2. Araştırılan başlıklar

Araştırma aşağıdaki başlıklara göre yapılmıştır:

1. `traffic cone detection YOLO`
2. `traffic cone detection OpenCV HSV`
3. `autonomous vehicle cone detection`

## 3. İlk karar

Koni tespiti için **YOLO tabanlı nesne tespiti ana yöntem** olarak değerlendirilecektir.

**HSV renk segmentasyonu** ise aşağıdaki amaçlarla **yedek veya destekleyici yöntem** olarak incelenecektir:

- YOLO güven skoru düşük çıktığında ek doğrulama yapmak,
- Eğitim verisi az olduğunda ilk prototipi hızlı kurmak,
- Turuncu/kırmızı-beyaz renk bilgisini kullanarak yanlış pozitifleri azaltmak,
- Basit güvenlik kontrolü veya debug çıktısı üretmek.

## 4. Yöntem 1 — YOLO tabanlı nesne tespiti

### 4.1. Genel yaklaşım

YOLO ailesi, görüntüdeki nesneleri tek geçişte tespit eden gerçek zamanlı nesne tespit modelleridir. Trafik konisi tespitinde YOLO modeli, her koni için:

- sınıf etiketi: `cone`, `traffic_cone`, `orange_cone`, vb.
- sınırlayıcı kutu: `x_min, y_min, x_max, y_max`,
- güven skoru: `confidence`

üretir.

Bu çıktı, otonom sürüş tarafında şu bilgilere dönüştürülebilir:

- Koninin görüntü merkezi,
- Koninin yaklaşık açısal konumu,
- Stereo kamera / derinlik kamerası / LiDAR varsa yaklaşık mesafe,
- Koniler arası güvenli geçiş hattı,
- Temas riskine göre durma veya rota düzeltme kararı.

### 4.2. Neden YOLO ana yöntem olmalı?

YOLO tabanlı yöntemler, yarışma şartları açısından avantajlıdır:

| Kriter | YOLO değerlendirmesi |
|---|---|
| Değişken aydınlatma | HSV’ye göre daha dayanıklı olabilir. |
| Kırmızı-beyaz / turuncu-beyaz farklılığı | Eğitim verisine eklenirse her iki tipi öğrenebilir. |
| Kısmi kapanma | Uygun eğitim verisiyle kısmen kapanmış konileri tespit edebilir. |
| Gerçek zamanlı çalışma | Küçük modeller Jetson, mini PC veya GPU destekli sistemlerde gerçek zamanlı çalışabilir. |
| Yanlış pozitif kontrolü | Confidence threshold, NMS, alan/oran filtresi ve takip algoritmasıyla iyileştirilebilir. |
| Otonom sürüş entegrasyonu | Bounding box çıktısı rota planlama modülüne kolay aktarılır. |

Özellikle otonom araç literatüründe trafik konisi tespiti, Formula Student Driverless ve otonom yarış araçları bağlamında sık çalışılmıştır. FSOCO veri seti, Formula Student / FSAE takımlarının kamera tabanlı koni algılama sistemleri geliştirmesi için oluşturulmuştur. Bu, bizim senaryoya oldukça yakın bir alandır.

### 4.3. Model seçimi

Başlangıç için önerilen modeller:

| Model | Kullanım nedeni |
|---|---|
| YOLOv8n / YOLOv8s | Hafif, kolay eğitilir, yaygın kaynak ve örnek var. |
| YOLOv11n / YOLOv11s veya güncel Ultralytics küçük modelleri | Daha güncel denemeler için uygun. |
| YOLOv5n / YOLOv5s | Eski ama stabil; çok sayıda örnek proje var. |

**İlk prototip önerisi:** `YOLOv8n` veya `YOLOv8s`

- `n` modeli daha hızlıdır.
- `s` modeli genellikle daha yüksek doğruluk verir.
- Donanım güçlü değilse önce `n`, doğruluk yetmezse `s` denenmelidir.

### 4.4. Eğitim verisi

Koni tespiti için veri kaynakları:

1. **Kendi yarışma verimiz**  
   En değerli veri kaynağıdır. Gerçek parkura benzer koniler, benzer kamera yüksekliği ve benzer zeminle çekilmelidir.

2. **FSOCO — Formula Student Objects in Context**  
   Formula Student Driverless için hazırlanmış, koni tespiti odaklı açık veri setidir. Başlangıç eğitimi için kullanılabilir.

3. **TraCon veri seti / trafik konisi veri setleri**  
   Trafik konisi tespiti için hazırlanmış farklı açık veri kaynakları modelin çeşitliliğini artırabilir.

4. **Roboflow benzeri veri setleri**  
   Hızlı başlangıç için kullanılabilir; ancak lisans, veri kalitesi ve sınıf tutarlılığı kontrol edilmelidir.

### 4.5. Veri toplama planı

Kendi veri setimiz için önerilen çekim senaryoları:

- Güneşli açık alan,
- Bulutlu hava,
- Gölge / ters ışık,
- Islak zemin,
- Koniye yakın ve uzak mesafeler,
- Viraj ve düz yol,
- Kısmen kadraj dışı koniler,
- Kırmızı-beyaz ve turuncu-beyaz koniler,
- Bariyer, tabela ve kırmızı-beyaz nesnelerle karışabilecek sahneler,
- Araç titreşimi varken hareketli görüntü.

Önerilen minimum veri hedefi:

| Aşama | Görüntü sayısı | Amaç |
|---|---:|---|
| Hızlı prototip | 300–500 | İlk modelin çalıştığını görmek |
| Yarışmaya yakın deneme | 1.000–2.000 | Farklı ışık ve mesafe koşullarını kapsamak |
| Sağlam model | 3.000+ | Genelleme ve yanlış pozitifleri azaltmak |

### 4.6. Etiketleme standardı

Önerilen sınıf yapısı:

```yaml
names:
  0: cone
```

Başlangıçta tek sınıf kullanmak daha güvenlidir. Renk ayrımı gerekiyorsa ikinci aşamada şu yapı denenebilir:

```yaml
names:
  0: orange_white_cone
  1: red_white_cone
```

Ancak yarışma görevi açısından renk sınıfı değil, **koninin güvenli şekilde algılanması ve koniye temas edilmemesi** kritiktir. Bu nedenle ilk sürümde tek sınıf `cone` önerilir.

### 4.7. Eğitim komutu örneği

```bash
yolo detect train \
  model=yolov8n.pt \
  data=cone_dataset.yaml \
  imgsz=640 \
  epochs=100 \
  batch=16 \
  device=0
```

### 4.8. Çıkarım komutu örneği

```bash
yolo detect predict \
  model=runs/detect/train/weights/best.pt \
  source=video.mp4 \
  imgsz=640 \
  conf=0.35
```

### 4.9. Model değerlendirme metrikleri

Kullanılacak temel metrikler:

| Metrik | Anlamı |
|---|---|
| Precision | Tespit edilen konilerin ne kadarı gerçekten koni? |
| Recall | Gerçek konilerin ne kadarı tespit edildi? |
| mAP50 | IoU 0.50 seviyesinde ortalama başarı |
| mAP50-95 | Daha sıkı IoU aralığında genel başarı |
| FPS | Gerçek zamanlı çalışma hızı |
| Latency | Bir kare için işlem süresi |

Yarışma açısından **recall** çok önemlidir. Koni kaçırmak doğrudan temas riskini artırır. Ancak precision da önemlidir; yanlış koni tespiti rota planlamayı bozabilir.

### 4.10. Otonom sürüşe entegrasyon

YOLO çıktısı doğrudan sürüş kararına bağlanmamalıdır. Önerilen ara katman:

```text
Kamera görüntüsü
    ↓
YOLO koni tespiti
    ↓
Filtreleme: confidence, alan, oran, ROI
    ↓
Takip: basit zaman filtresi / Kalman / SORT benzeri takip
    ↓
Mesafe tahmini: stereo, derinlik kamerası, LiDAR veya geometrik yaklaşım
    ↓
Yerel planlama: koniden kaçınma / güvenli geçiş koridoru
    ↓
Hız ve direksiyon komutu
```

Önerilen güvenlik mantığı:

- Koni çok yakınsa hız düşür.
- Koni merkez hattına yakınsa kaçınma manevrası üret.
- Birden fazla kare boyunca aynı koni görülüyorsa güveni artır.
- Tek karelik tespitlere doğrudan sert manevra verme.

## 5. Yöntem 2 — OpenCV HSV renk segmentasyonu

### 5.1. Genel yaklaşım

HSV yöntemi, görüntüyü BGR/RGB renk uzayından HSV renk uzayına çevirir ve belirlenen renk aralıklarına göre maske üretir.

OpenCV’de tipik işlem hattı:

```python
frame = get_camera_frame()
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask_orange = cv2.inRange(hsv, lower_orange, upper_orange)
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)
mask = mask_orange | mask_red1 | mask_red2
```

Ardından:

- morfolojik açma/kapama,
- kontur bulma,
- alan filtresi,
- dikeylik / en-boy oranı filtresi,
- üçgen/trapez şekil kontrolü,
- beyaz şerit kontrolü

uygulanabilir.

### 5.2. Örnek HSV aralıkları

OpenCV’de Hue aralığı genellikle `0–179` kabul edilir. Başlangıç için denenecek aralıklar:

```python
# Turuncu koniler için başlangıç aralığı
lower_orange = (5, 80, 80)
upper_orange = (25, 255, 255)

# Kırmızı için Hue ekseni iki uca bölündüğü için iki maske gerekir
lower_red1 = (0, 80, 80)
upper_red1 = (10, 255, 255)

lower_red2 = (170, 80, 80)
upper_red2 = (179, 255, 255)
```

Bu değerler kesin değildir. Kamera, beyaz ayarı, ışık ve koni malzemesine göre kalibre edilmelidir.

### 5.3. HSV yönteminin avantajları

| Avantaj | Açıklama |
|---|---|
| Basitlik | Eğitim verisi gerekmez. |
| Hız | CPU’da bile hızlı çalışabilir. |
| Açıklanabilirlik | Hangi renklerin seçildiği kolay görülür. |
| Debug kolaylığı | Maske görüntüsü doğrudan incelenebilir. |
| Yedek sistem | YOLO çalışmazsa basit renk tabanlı uyarı üretilebilir. |

### 5.4. HSV yönteminin dezavantajları

| Dezavantaj | Risk |
|---|---|
| Işığa duyarlılık | Güneş, gölge, kamera pozlaması sonucu eşikler bozulabilir. |
| Benzer renkli nesneler | Turuncu/kırmızı tabelalar veya bariyerler yanlış pozitif olabilir. |
| Uzak koniler | Piksel alanı küçüldükçe kontur kararsızlaşır. |
| Kısmi kapanma | Şekil filtresi başarısız olabilir. |
| Renk farklılığı | Kırmızı-beyaz ve turuncu-beyaz koniler için ayrı eşikler gerekir. |

### 5.5. HSV destekleyici kullanım önerisi

HSV tek başına ana algılama sistemi olarak seçilmemelidir. Ancak şu noktalarda faydalıdır:

1. **YOLO sonrası doğrulama**  
   YOLO’nun verdiği bounding box içinde turuncu/kırmızı piksel oranı hesaplanabilir.

2. **ROI üretimi**  
   HSV ile olası koni bölgeleri çıkarılıp YOLO veya daha basit sınıflandırıcıya verilebilir.

3. **Güvenlik modu**  
   YOLO modeli çökerse veya düşük FPS verirse, HSV basit yakın engel uyarısı üretebilir.

4. **Veri toplama yardımı**  
   HSV maskeleri, otomatik ön etiketleme için kullanılabilir.

## 6. Yöntem 3 — Otonom araçlarda koni tespiti yaklaşımları

Otonom araçlarda koni tespiti yalnızca 2B kutu bulma problemi değildir. Yarışma için asıl ihtiyaç, konilere temas etmeden yol almak olduğundan algı çıktısı rota planlama ile birleşmelidir.

### 6.1. Kamera tabanlı 2B tespit

En basit kurulumdur:

```text
Monoküler kamera → YOLO → bounding box → görüntü tabanlı kaçınma
```

Avantajı düşük maliyettir. Dezavantajı mesafe tahmininin zor olmasıdır.

### 6.2. Stereo / derinlik kamera ile 3B konum

Stereo kamera veya derinlik kamerası varsa:

```text
YOLO bounding box → kutu merkezi → derinlik haritası → 3B koni konumu
```

Bu yöntem, koniden kaçınma ve rota planlama için daha uygundur. Literatürde YOLOv8 + ZED 2 + Jetson Orin kullanan Formula Student çalışmaları bulunmaktadır.

### 6.3. Kamera + LiDAR füzyonu

Daha sağlam ama daha karmaşık yöntemdir:

```text
YOLO 2B tespit + LiDAR nokta bulutu → 3B koni konumu → yerel harita
```

Avantajı mesafe ve konum doğruluğudur. Dezavantajı kalibrasyon, maliyet ve yazılım karmaşıklığıdır.

### 6.4. Takip ve zamansal filtreleme

Koni tespitleri tek kareye bağlı kalmamalıdır. Önerilen yaklaşım:

- Son 3–5 karede görülen koniler saklanır.
- Aynı bölgede tekrar görülen konilerin güveni artırılır.
- Tek karelik düşük güvenli tespitler sürüş kararında sınırlı etki yapar.
- Yakın koniler için daha düşük hız limiti uygulanır.

## 7. Karşılaştırma tablosu

| Kriter | YOLO | HSV | Kamera + LiDAR / Derinlik |
|---|---|---|---|
| Eğitim verisi ihtiyacı | Var | Yok | Var / orta |
| Gerçek zamanlılık | İyi, donanıma bağlı | Çok iyi | Orta-iyi |
| Işık değişimine dayanıklılık | Orta-iyi | Zayıf-orta | İyi |
| Kısmi kapanma dayanımı | İyi | Zayıf | İyi |
| Uzak koni tespiti | İyi | Zayıf-orta | İyi |
| Mesafe bilgisi | Ek yöntem gerekir | Ek yöntem gerekir | Doğrudan/kolay |
| Uygulama karmaşıklığı | Orta | Düşük | Yüksek |
| Yarışma için ana yöntem uygunluğu | Yüksek | Düşük-orta | Yüksek ama karmaşık |

## 8. Önerilen nihai mimari

Yarışma için önerilen algılama mimarisi:

```text
Kamera
  ↓
YOLOv8n/s cone detector
  ↓
Bounding box filtreleri
  - confidence > 0.35 veya testlerle belirlenecek değer
  - minimum alan filtresi
  - en-boy oranı filtresi
  - yol ROI filtresi
  ↓
HSV destek kontrolü
  - kutu içinde turuncu/kırmızı piksel oranı
  - beyaz şerit/renk kontrolü
  ↓
Zamansal takip
  - son N karede süreklilik
  - yanlış pozitif bastırma
  ↓
Mesafe / konum tahmini
  - stereo/derinlik varsa 3B
  - yoksa kutu yüksekliği + kamera kalibrasyonu ile yaklaşık mesafe
  ↓
Yerel kaçınma ve hız kontrolü
```

## 9. Uygulama adımları

### Aşama 1 — Hızlı prototip

- Hazır YOLO modeli ve açık veri setleriyle ilk deneme yapılır.
- Kamera görüntüsünde koniler işaretlenir.
- FPS ve gecikme ölçülür.
- HSV maskeleme ayrı bir debug ekranı olarak hazırlanır.

### Aşama 2 — Kendi veri seti

- Yarışmaya benzer konilerle görüntü toplanır.
- Görüntüler YOLO formatında etiketlenir.
- Eğitim / doğrulama / test bölünmesi yapılır.
- Farklı ışık koşulları özellikle eklenir.

Önerilen bölünme:

```text
train: %70
val:   %20
test:  %10
```

### Aşama 3 — Model eğitimi

- `YOLOv8n` ile başlanır.
- Doğruluk yetmezse `YOLOv8s` denenir.
- `imgsz=640` ile başlanır.
- Küçük/uzak koniler kaçıyorsa `imgsz=960` denenebilir.
- Donanım yavaş kalırsa TensorRT / ONNX export denenir.

### Aşama 4 — Saha testi

Test senaryoları:

- Koniye düz yaklaşma,
- Konilere çapraz yaklaşma,
- Birden fazla koni arasından geçme,
- Yakın mesafede ani koni görünmesi,
- Gölge ve parlak ışık,
- Islak zemin,
- Kırmızı-beyaz bariyerlerle karışma riski.

### Aşama 5 — Sürüş entegrasyonu

- YOLO çıktısı doğrudan motor komutuna bağlanmaz.
- Önce güvenli geçiş bölgesi hesaplanır.
- Koni yakınsa hız azaltılır.
- Tespit kaybolursa araç hemen hızlanmaz; kısa süreli hafıza kullanılır.

## 10. Riskler ve önlemler

| Risk | Önlem |
|---|---|
| Koni kaçırma | Daha fazla saha verisi, recall odaklı eşik ayarı, düşük confidence uyarısı |
| Yanlış pozitif | HSV doğrulama, ROI filtresi, alan/oran filtresi |
| Düşük FPS | YOLOv8n, TensorRT, düşük çözünürlük, frame skipping |
| Işık değişimi | Veri artırma, farklı saatlerde veri toplama, otomatik pozlama testleri |
| Uzak koni küçük kalıyor | Daha yüksek `imgsz`, tele/uygun lens, veri setinde uzak koni örnekleri |
| Kamera titreşimi | Mekanik izolasyon, kısa pozlama, zamansal filtreleme |
| Koni rengi değişken | Hem kırmızı-beyaz hem turuncu-beyaz örneklerle eğitim |

## 11. Başarı kriterleri

İlk yarışma prototipi için hedefler:

| Kriter | Hedef |
|---|---:|
| FPS | En az 15 FPS, tercihen 25+ FPS |
| Recall | %90+ hedeflenmeli |
| Precision | %85+ hedeflenmeli |
| Yakın koni algılama | 0–5 m aralığında kararlı |
| Orta mesafe algılama | 5–12 m aralığında yeterli |
| Gecikme | 100 ms altında hedeflenmeli |

Bu hedefler saha testlerine göre güncellenmelidir.

## 12. Sonuç ve karar

Araştırma sonucunda koni tespiti için en uygun ana yaklaşım:

> **YOLO tabanlı nesne tespiti + HSV destekli doğrulama + zamansal takip**

olarak belirlenmiştir.

HSV tek başına yarışma koşullarında yeterince güvenilir görülmemektedir; ancak basit, hızlı ve açıklanabilir olduğu için destekleyici modül olarak değerlidir. Ana algılama sorumluluğu YOLO modelinde olmalı, sürüş güvenliği için tespitler filtreleme ve takip katmanından geçirilmelidir.

## 13. Kaynaklar

1. Ultralytics YOLO dokümantasyonu — nesne tespiti, eğitim ve model export süreçleri.  
   https://docs.ultralytics.com/tasks/detect/  
   https://docs.ultralytics.com/modes/train/  
   https://docs.ultralytics.com/modes/export/

2. OpenCV HSV ve `inRange` dokümantasyonu.  
   https://docs.opencv.org/3.4/df/d9d/tutorial_py_colorspaces.html  
   https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

3. FSOCO — Formula Student Objects in Context Dataset.  
   https://fsoco.github.io/fsoco-dataset/  
   https://arxiv.org/abs/2012.07139

4. Dhall et al., “Real-time 3D Traffic Cone Detection for Autonomous Driving”, 2019.  
   https://arxiv.org/abs/1902.02394

5. Katsamenis et al., “TraCon: A novel dataset for real-time traffic cones detection using deep learning”, 2022.  
   https://github.com/ikatsamenis/Cone-Detection

6. Szőnyi et al., “Innovative Cone Clustering and Path Planning for Autonomous Formula Student Race Cars Using Cameras”, 2024.  
   https://www.mdpi.com/2673-4591/79/1/96
