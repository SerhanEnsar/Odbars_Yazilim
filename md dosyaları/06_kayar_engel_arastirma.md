# 06 - Kayar Engel Algoritma Araştırması

## 1. Şartname Özeti ve Problem Tanımı

TEKNOFEST 2026 İnsansız Kara Aracı şartnamesinde kayar engel aşaması için şu isterler tanımlıdır:

- Parkur üzerinde genişliği **1 metre** olan ve tamamen parkur dışına çıkabilen **1 adet kayar engel** bulunacaktır.
- Engel sağa ve sola doğru **20 cm/s** hızla sürekli rejimde git-gel hareketi yapacaktır.
- Engel parkur dışına çıktığı noktada beklemeden ters yönde hareketine devam edecektir.
- Takımın kayar engelin **pozisyonunu** ve **hareket yönünü** tespit edip engele temas etmeden geçmesi beklenmektedir.
- Kayar engel aşaması, temassız geçilmesi durumunda **50 puan** değerindedir.

Bu nedenle algoritmanın temel görevi, aracın ileri görüş kamerasından kayar engeli algılamak, engelin görüntüdeki merkez konumunu takip etmek, hareket yönünü kestirmek ve geçiş için güvenli zaman aralığını hesaplamaktır.

## 2. Araştırılan Yaklaşımlar

### 2.1 Moving Object Detection - OpenCV

**Amaç:** Videoda hareket eden bölgeleri tespit etmek.

OpenCV tarafında hareketli nesne tespiti genellikle arka plan çıkarma yöntemleriyle yapılır. En yaygın yöntemler:

- `BackgroundSubtractorMOG2`
- `BackgroundSubtractorKNN`
- frame differencing
- eşikleme + kontur çıkarımı

**Çalışma mantığı:**

1. Kamera görüntüsünden arka plan modeli oluşturulur.
2. Yeni karede arka plandan farklı pikseller hareketli bölge olarak işaretlenir.
3. Gürültü azaltma için morfolojik işlemler uygulanır.
4. Konturlar çıkarılır.
5. En uygun kontur kayar engel adayı olarak seçilir.

**Avantajları:**

- YOLO eğitimi gerektirmeden hızlı prototip yapılabilir.
- CPU üzerinde çalışabilir.
- Engel sabit renk/şekil özelliklerine sahipse basit ve hızlıdır.

**Dezavantajları:**

- Araç hareket ettiği için kamera da hareket eder; bu durum arka plan çıkarma yöntemlerini zorlaştırır.
- Titreşim, ışık değişimi, gölge ve su/zemin yansımaları yanlış pozitif üretebilir.
- Engel dışında hareket eden başka bölgeler varsa ayrım zorlaşır.

**Kayar engel için değerlendirme:**

Bu yöntem tek başına ana çözüm olarak yeterince güvenilir görülmemelidir. Ancak YOLO tespitine yardımcı olacak ikincil doğrulama yöntemi olarak kullanılabilir. Örneğin YOLO ile bulunan kutunun gerçekten hareket edip etmediği OpenCV frame differencing ile kontrol edilebilir.

---

### 2.2 Optical Flow

**Amaç:** Ardışık karelerde piksel veya özellik noktalarının hareket vektörlerini hesaplamak.

Optical flow, nesnenin iki kare arasındaki görünür hareketini vektör alanı olarak verir. Kayar engel yatay doğrultuda hareket ettiği için özellikle yatay akış bileşeni değerlidir.

Kullanılabilecek yöntemler:

- Lucas-Kanade sparse optical flow
- Farneback dense optical flow
- pyramidal Lucas-Kanade

**Çalışma mantığı:**

1. Kayar engel ROI bölgesi belirlenir.
2. Bu ROI içinde takip edilecek köşe/özellik noktaları seçilir.
3. Ardışık karelerde bu noktaların yeni konumu hesaplanır.
4. Ortalama yatay yer değiştirme `dx` hesaplanır.
5. `dx > eşik` ise sağa, `dx < -eşik` ise sola hareket kararı verilir.

**Avantajları:**

- Hareket yönünü doğrudan ölçer.
- YOLO tespitleri arasında yön kestirimini destekler.
- Engel kısa süreli kısmen kapanırsa hareket bilgisi devam ettirilebilir.

**Dezavantajları:**

- Kamera titreşimi ve aracın kendi hareketi optical flow’u bozabilir.
- ROI doğru seçilmezse zemin hareketi de hesaplamaya katılır.
- Düşük dokulu veya tek renkli engelde özellik noktası az olabilir.

**Kayar engel için değerlendirme:**

Optical flow, ana nesne algılama yöntemi olmaktan çok yön tahminini kararlı hale getiren destekleyici yöntem olarak uygundur. YOLO bounding box içindeki optical flow vektörlerinin ortalaması alınarak hareket yönü daha güvenilir hale getirilebilir.

---

### 2.3 Kalman Filter Object Tracking

**Amaç:** Tespit edilen nesnenin konumunu gürültülü ölçümlere rağmen kararlı biçimde takip etmek ve bir sonraki konumunu tahmin etmek.

Kayar engel için basit bir sabit hızlı hareket modeli yeterlidir. Durum vektörü şu şekilde tanımlanabilir:

```text
x = [cx, cy, vx, vy]
```

Burada:

- `cx`: bounding box merkezinin x koordinatı
- `cy`: bounding box merkezinin y koordinatı
- `vx`: x yönündeki hız
- `vy`: y yönündeki hız

Kayar engel pratikte yatay hareket ettiği için `vx` kritik değişkendir. Hareket yönü şu şekilde tahmin edilir:

```text
vx > +eşik  -> sağa hareket
vx < -eşik  -> sola hareket
|vx| <= eşik -> yön belirsiz / dönüş noktası
```

**Avantajları:**

- YOLO tespitlerindeki kutu zıplamalarını yumuşatır.
- Nesne 1-2 kare algılanmasa bile tahmin üretmeye devam eder.
- Hız ve yön bilgisi doğrudan elde edilir.
- Basit ve gerçek zamanlıdır.

**Dezavantajları:**

- Yanlış YOLO tespiti Kalman durumunu bozabilir.
- Dönüş noktalarında hız işareti değiştiği için kısa süreli kararsızlık oluşabilir.
- İyi performans için süreç gürültüsü ve ölçüm gürültüsü ayarlanmalıdır.

**Kayar engel için değerlendirme:**

Kalman filter, bu görev için güçlü ve düşük maliyetli bir kararlılık katmanıdır. İlk prototipte YOLO merkez koordinatı + kayan ortalama kullanılabilir; ikinci aşamada Kalman filter eklenmesi önerilir.

---

### 2.4 YOLO Object Tracking

**Amaç:** Kayar engelin görüntüdeki bounding box konumunu nesne tespiti ile bulmak ve ardışık karelerde takip etmek.

YOLO, tek karede nesne tespiti yapar. Kayar engel için özel bir sınıf eğitilebilir:

```text
class: sliding_obstacle
```

Her karede şu bilgiler alınır:

- bounding box: `(x1, y1, x2, y2)`
- merkez: `(cx, cy)`
- güven skoru: `confidence`
- sınıf: `sliding_obstacle`

Hareket yönü, ardışık karelerde merkez x koordinatındaki değişimle bulunur:

```text
dx = cx_t - cx_(t-1)
```

Karar:

```text
dx_avg > +T  -> sağa hareket
dx_avg < -T  -> sola hareket
aksi halde   -> belirsiz / dönüş bölgesi
```

**Avantajları:**

- Arka plan, ışık ve kamera hareketinden klasik yöntemlere göre daha az etkilenir.
- Engel farklı konumlarda ve farklı açılarda tespit edilebilir.
- Ultralytics YOLO içinde takip modlarıyla ByteTrack veya BoT-SORT kullanılabilir.
- Tek nesne için bile güvenilir kutu takibi sağlar.

**Dezavantajları:**

- Kayar engel için veri seti oluşturmak ve etiketlemek gerekir.
- Eğitim kalitesi veri çeşitliliğine bağlıdır.
- GPU/edge AI donanımı gerekebilir.
- Çok yakın mesafe, motion blur veya kısmi görünürlükte tespit kaçabilir.

**Kayar engel için değerlendirme:**

Ana karar olarak YOLO ile nesne tespiti seçilmelidir. Engel merkezinin zamana göre değişimi ile hareket yönü tahmini yapılmalıdır. İlk karar bu görev için uygundur.

---

### 2.5 ByteTrack

**Amaç:** Tespit kutularını ardışık karelerde ID ile ilişkilendirmek.

ByteTrack, yüksek güvenli tespitlerin yanında düşük güvenli tespitleri de ilişkilendirme sürecine dahil ederek parçalanan izleri azaltmayı hedefler. Bu özellik, kısmi kapanma, motion blur veya düşük güven skorlu karelerde faydalıdır.

**Avantajları:**

- YOLO ile doğrudan entegre edilebilir.
- Tespit güveni kısa süreli düşse bile takip ID’si korunabilir.
- Gerçek zamanlı uygulamalara uygundur.
- Tek kayar engel için oldukça yeterli ve hafiftir.

**Dezavantajları:**

- Yanlış düşük skorlu tespitler takip zincirine girebilir.
- Çok basit tek nesne senaryosunda manuel merkez takibi + Kalman’a göre fazla karmaşık olabilir.
- Parametre ayarı gerekir: `track_high_thresh`, `track_low_thresh`, `match_thresh`.

**Kayar engel için değerlendirme:**

YOLO tespitlerinin zaman içinde ID ile korunması isteniyorsa ByteTrack iyi bir seçenektir. Tek engel olsa bile tespit kaçırma durumlarına karşı kararlılığı artırır. Ultralytics YOLO’da `bytetrack.yaml` ile hızlıca denenebilir.

---

### 2.6 SORT Tracking Algorithm

**Amaç:** Nesne tespit kutularını Kalman filter ve Hungarian assignment ile gerçek zamanlı takip etmek.

SORT, tracking-by-detection yaklaşımıdır. Her karede YOLO gibi bir dedektörden bounding box alınır. SORT bu kutuları mevcut izlerle eşleştirir.

Temel bileşenler:

- Kalman filter ile hareket tahmini
- IoU tabanlı eşleştirme
- Hungarian algoritması ile optimum atama

**Avantajları:**

- Basit, hızlı ve anlaşılırdır.
- Kayar engel gibi sınırlı sayıda nesne olan görevlerde yeterlidir.
- Kalman filter içerdiği için kısa süreli tespit gürültüsünü azaltır.

**Dezavantajları:**

- Görsel özellik kullanmadığı için benzer nesneler arasında ID değişimi olabilir.
- Uzun süreli kapanma veya tespit kaybında ByteTrack/DeepSORT kadar dayanıklı değildir.
- Performansı dedektör kalitesine çok bağlıdır.

**Kayar engel için değerlendirme:**

Tek kayar engel senaryosunda SORT yeterli olabilir. Daha sade bir sistem istenirse YOLO + SORT tercih edilebilir. Ancak Ultralytics tarafında ByteTrack hazır ve yaygın olduğu için uygulama kolaylığı açısından ByteTrack daha avantajlıdır.

---

## 3. Yöntem Karşılaştırması

| Yöntem | Pozisyon Tespiti | Hareket Yönü | Gerçek Zaman | Kamera Hareketine Dayanım | Uygunluk |
|---|---:|---:|---:|---:|---:|
| OpenCV background subtraction | Orta | Orta | Yüksek | Düşük | Yardımcı yöntem |
| Optical flow | Düşük-Orta | Yüksek | Orta-Yüksek | Orta-Düşük | Yön doğrulama |
| YOLO detection | Yüksek | Orta | Orta-Yüksek | Yüksek | Ana yöntem |
| YOLO + Kalman | Yüksek | Yüksek | Yüksek | Yüksek | Önerilen temel çözüm |
| YOLO + SORT | Yüksek | Yüksek | Yüksek | Yüksek | Alternatif çözüm |
| YOLO + ByteTrack | Yüksek | Yüksek | Yüksek | Yüksek | En kararlı çözüm adayı |

## 4. Önerilen Algoritma Mimarisi

İlk karar doğrultusunda önerilen çözüm:

```text
Kamera görüntüsü
      |
      v
YOLO kayar engel tespiti
      |
      v
Bounding box merkezi hesaplama: cx, cy
      |
      v
Merkez geçmişini tutma: cx[t-N ... t]
      |
      v
Kalman filter / SORT / ByteTrack ile takip
      |
      v
Hareket yönü tahmini: sağ / sol / belirsiz
      |
      v
Geçiş stratejisi: bekle / ilerle / yavaşla
```

### 4.1 Temel Merkez Takibi

Her karede:

```python
cx = (x1 + x2) / 2
cy = (y1 + y2) / 2
```

Son `N` kare için merkez x değerleri saklanır:

```python
dx_avg = mean(cx[-k:] - cx[-k-1:-1])
```

Karar:

```python
if dx_avg > T:
    direction = "right"
elif dx_avg < -T:
    direction = "left"
else:
    direction = "unknown_or_turning"
```

### 4.2 Kalman Filter Durum Modeli

Durum:

```text
[cx, cy, vx, vy]
```

Ölçüm:

```text
[cx, cy]
```

Kayar engelde beklenen hareket yatay olduğu için `vx` ana karar değişkenidir. `vy` küçük kalmalıdır; büyük `vy` değeri yanlış takip veya kamera sarsıntısı göstergesi olabilir.

### 4.3 Hareket Yönü Karar Filtresi

Anlık `dx` yerine çoğunluk oylaması kullanılmalıdır:

```text
son 7 karenin 5'inde sağa hareket varsa -> sağ
son 7 karenin 5'inde sola hareket varsa -> sol
aksi halde -> belirsiz
```

Bu yaklaşım dönüş noktalarında ve YOLO kutu zıplamalarında yanlış kararları azaltır.

## 5. Geçiş Stratejisi İçin Kullanılabilecek Bilgiler

Kayar engel 20 cm/s hızla git-gel yaptığı için görüntüden tahmin edilen hareket yönü geçiş planlamada kullanılabilir.

Algoritmanın çıkarması gereken bilgiler:

- Engel görüntüde hangi tarafta?
- Engel parkurun içine doğru mu hareket ediyor, dışına doğru mu?
- Engel merkezi yol geçiş hattından uzaklaşıyor mu, yaklaşıyor mu?
- Engel ile araç arasındaki tahmini güvenli boşluk yeterli mi?

Basit geçiş kararı:

```text
Eğer engel geçiş hattından uzaklaşıyorsa ve güvenli mesafe oluşuyorsa -> ilerle
Eğer engel geçiş hattına yaklaşıyorsa -> bekle / yavaşla
Eğer yön belirsizse -> bekle ve 3-5 kare daha gözlemle
```

## 6. Veri Seti ve Test Planı

### 6.1 Veri Seti

YOLO eğitimi için önerilen veri çeşitliliği:

- Engel parkurun solunda, ortasında, sağında
- Engel hareket ederken motion blur içeren görüntüler
- Farklı ışık koşulları
- Farklı kamera açıları
- Araç yaklaşırken farklı mesafeler
- Engel kısmen parkur dışına çıkmışken görüntüler
- Dönüş noktalarına yakın görüntüler

Etiket sınıfı:

```text
sliding_obstacle
```

### 6.2 Test Senaryoları

- Engel sağa hareket ederken tespit ve yön tahmini
- Engel sola hareket ederken tespit ve yön tahmini
- Engel yön değiştirirken belirsiz durum üretme
- YOLO 1-3 kare tespit kaçırdığında Kalman/SORT/ByteTrack davranışı
- Kamera titreşiminde yanlış yön üretme oranı
- Farklı mesafelerde bounding box kararlılığı

### 6.3 Başarı Metrikleri

- Tespit doğruluğu: precision, recall, mAP
- Takip kararlılığı: ID switch sayısı, tespit kaybı süresi
- Yön doğruluğu: doğru sağ/sol karar oranı
- Gecikme: ms/frame veya FPS
- Geçiş başarısı: temassız geçiş oranı

## 7. Uygulama İçin Önerilen Yol Haritası

### Aşama 1 - Basit Prototip

- YOLO ile `sliding_obstacle` tespiti
- Bounding box merkezinin hesaplanması
- Son 5-10 karede `cx` değişiminden yön tahmini
- Görüntü üzerine bbox, merkez, yön ve güven skoru çizimi

### Aşama 2 - Kararlılık Katmanı

- Kalman filter eklenmesi
- Merkez koordinatlarının yumuşatılması
- `vx` değerinden yön tahmini
- Dönüş noktalarında “belirsiz” kararı eklenmesi

### Aşama 3 - Tracker Karşılaştırması

Aşağıdaki yöntemler aynı video setinde karşılaştırılmalıdır:

1. YOLO + merkez farkı
2. YOLO + Kalman filter
3. YOLO + SORT
4. YOLO + ByteTrack

Karşılaştırma sonucunda en düşük gecikme ve en yüksek yön doğruluğu veren yöntem seçilmelidir.

### Aşama 4 - Otonom Karar Entegrasyonu

- Engel yaklaşma/uzaklaşma kararını hız kontrolüne bağlama
- Belirsiz durumda bekleme kuralı
- Güvenli geçiş penceresi oluştuğunda ilerleme
- Acil durdurma ve güvenlik davranışları

## 8. İlk Teknik Karar

Bu araştırmaya göre ilk karar korunmuştur:

> Kayar engel için YOLO ile nesne tespiti yapılacak, ardından ardışık karelerde bounding box merkez koordinatının değişimine bakılarak hareket yönü tahmin edilecektir.

Daha kararlı takip için önerilen sıra:

1. **YOLO + merkez farkı** ile hızlı prototip
2. **YOLO + Kalman filter** ile kararlı yön tahmini
3. Gerekirse **YOLO + ByteTrack** veya **YOLO + SORT** ile ID tabanlı takip

Pratik öneri:

- Tek kayar engel varsa: **YOLO + Kalman filter** yeterli olabilir.
- Tespit kaçırma veya sahada kararsızlık görülürse: **YOLO + ByteTrack** denenmelidir.
- En sade gerçek zamanlı takip istenirse: **YOLO + SORT** alternatif olarak test edilmelidir.

## 9. Kaynaklar

1. OpenCV Documentation - Background Subtraction: https://docs.opencv.org/4.x/d1/dc5/tutorial_background_subtraction.html
2. OpenCV Documentation - Optical Flow: https://docs.opencv.org/4.x/d4/dee/tutorial_optical_flow.html
3. OpenCV Documentation - KalmanFilter Class Reference: https://docs.opencv.org/3.4/dd/d6a/classcv_1_1KalmanFilter.html
4. OpenCV Documentation - Video Tracking Module: https://docs.opencv.org/4.x/dc/d6b/group__video__track.html
5. Ultralytics YOLO Tracking Documentation: https://docs.ultralytics.com/modes/track/
6. Ultralytics YOLO Tracking Datasets / Available Trackers: https://docs.ultralytics.com/datasets/track/
7. ByteTrack Paper - Multi-Object Tracking by Associating Every Detection Box: https://arxiv.org/abs/2110.06864
8. SORT Paper - Simple Online and Realtime Tracking: https://arxiv.org/abs/1602.00763
9. DeepSORT Paper - Simple Online and Realtime Tracking with a Deep Association Metric: https://arxiv.org/abs/1703.07402
