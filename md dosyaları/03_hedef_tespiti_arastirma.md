# 03_hedef_tespiti_arastirma

## Amaç ve yarışma bağlamı

Bu not, İnsansız Kara Aracı yarışmasındaki **otonom atış / hedef tespiti** görevi için klasik görüntü işleme tabanlı yöntemleri karşılaştırır. Yarışma şartnamesine göre atış, minimum **10 m** uzaklıktaki A3 kâğıt boyutundaki hedefe yapılır; nişan alma lazer kapalıyken kameralarla yapılır, lazer yalnızca atış anında açılır ve aktif olduktan sonra en az **1 s** hedefte kalmalıdır. Araçlarda ileri, geri ve nişan kamerası olmak üzere en az 3 kamera ve nişan alma düzeneği üzerinde lazer işaretleyici bulunması gerekir; lazer nokta çapı 10 m mesafede **1,5 cm’den büyük olmamalıdır**.

Bu yüzden hedef tespiti sistemi şu işi yapmalıdır:

1. Nişan kamerasından hedefi bulmak.
2. Hedef merkezini veya istenen puan halkasını hesaplamak.
3. Kamera görüntüsündeki hedef merkezi ile lazer/nişangâh merkezi arasındaki piksel hatasını bulmak.
4. Pan-tilt mekanizması, servo veya araç üstü lazer yönlendiriciyi bu hata sıfıra yaklaşana kadar hareket ettirmek.
5. Lazer açılmadan önce hedefte kararlı hizalanmayı doğrulamak.

---

## Araştırma özeti
   
| Algoritma / yöntem             | Ne için uygun?                                                          | Yarışmada kullanılabilir mi? | Önerilen rol |
|---                             |---                                                                      |---:                          |---           |
| OpenCV Thresholding            | Hedefteki siyah/beyaz/kırmızı gibi renk-parlaklık ayrımı                | Evet                         | Ön işleme ve maskeleme |
| OpenCV Contour Detection       | Hedef halkalarının, tabelaların, lazer noktasının dış sınırlarını bulma | Evet                         | Ana hedef adaylarını bulma |
| Hough Circle Transform         | Dairesel hedef halkalarını bulma                                        | Kısmen evet                  | Hedef tamamen dairesel görünüyorsa destekleyici yöntem |
| Ellipse Detection / fitEllipse | Perspektiften dolayı elipse dönüşen hedef halkalarını bulma             | Evet                         | Atış hedefi için güçlü yöntem |
| Camera Crosshair Alignment     | Kamera merkez çizgisi ile hedef merkezini hizalama                      | Evet                         | Nişan alma kontrol mantığı |
| Visual Servoing                | Görsel hatayı servo hareketine dönüştürme                               | Evet                         | Otonom nişan alma kapalı çevrim kontrolü |
| Laser Pointer Detection        | Lazer noktasını algılayıp kalibrasyon/geri besleme alma                 | Evet, dikkatli kullanılmalı  | Kalibrasyon, manuel test ve atış sonrası doğrulama |

---

## 1. OpenCV Thresholding

### Algoritma adı

**Thresholding / Eşikleme**  
OpenCV fonksiyonları: `cv2.threshold`, `cv2.adaptiveThreshold`, `cv2.inRange`, Otsu thresholding.

### Ne işe yarıyor?

Görüntüdeki pikselleri belirli bir parlaklık veya renk aralığına göre ayırır. Hedef tespitinde arka planı bastırmak, siyah hedef halkalarını çıkarmak, kırmızı/beyaz parkur tabelalarını maskelemek veya lazer noktasını parlak renk olarak ayırmak için kullanılır.

### Nasıl çalışıyor?

Temel eşikleme mantığında görüntü gri seviyeye çevrilir. Piksel değeri eşikten büyükse beyaz, küçükse siyah yapılır. Renk tabanlı tespitte görüntü genellikle HSV renk uzayına çevrilir ve `cv2.inRange()` ile belirli renk aralığındaki pikseller maske olarak çıkarılır.

Örnek işlem zinciri:

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
blur = cv2.GaussianBlur(gray, (5, 5), 0)
_, mask = cv2.threshold(blur, 80, 255, cv2.THRESH_BINARY_INV)
```

Renk için:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
mask_red = cv2.inRange(hsv, lower_red, upper_red)
```

### Avantajları

- Çok hızlıdır; Raspberry Pi, Jetson Nano veya düşük güçlü bilgisayarlarda gerçek zamanlı çalışabilir.
- Kodlaması kolaydır.
- Contour detection ve ellipse fitting için iyi bir ön işlem üretir.
- Hedef yüksek kontrastlıysa çok başarılıdır.
- Lazer noktası parlak ve tek renkliyse tespit kolaylaşır.

### Dezavantajları

- Işık değişimlerine duyarlıdır.
- Gölge, parlama, yağmur, toz ve kamera pozlaması sonucu yanlış maske oluşabilir.
- Sabit threshold değeri her ortamda çalışmayabilir.
- Hedef arka planla benzer renkteyse başarısız olabilir.
- Lazer noktası parlak yüzeyde yansıyorsa birden fazla nokta oluşabilir.

### Bizim yarışmada kullanılabilir mi?

**Evet.** Tek başına hedef tespiti için yeterli olmayabilir, ancak sistemin ilk katmanı olarak çok uygundur. Özellikle hedefin siyah halkalarını beyaz zeminden ayırmak, kırmızı referans çizgileri/halkaları çıkarmak veya lazer noktasını yakalamak için kullanılabilir.

### Yarışma için öneri

- Atış hedefi için gri seviye + ters threshold kullanılabilir.
- Lazer noktası için HSV renk aralığı kullanılmalıdır.
- Sabit threshold yerine mümkünse adaptif threshold veya Otsu threshold denenmelidir.
- Maskeden sonra `morphologyEx`, `erode`, `dilate` gibi morfolojik işlemlerle gürültü temizlenmelidir.

Kaynaklar: OpenCV thresholding dokümantasyonu: https://docs.opencv.org/4.x/d7/d4d/tutorial_py_thresholding.html, OpenCV temel thresholding işlemleri: https://docs.opencv.org/4.x/db/d8e/tutorial_threshold.html

---

## 2. OpenCV Contour Detection

### Algoritma adı

**Contour Detection / Kontur Tespiti**  
OpenCV fonksiyonları: `cv2.findContours`, `cv2.drawContours`, `cv2.contourArea`, `cv2.boundingRect`, `cv2.minEnclosingCircle`, `cv2.moments`.

### Ne işe yarıyor?

Binary görüntüdeki bağlı şekillerin sınırlarını bulur. Hedef halkaları, tabelalar, siyah-beyaz alanlar, lazer noktası veya dairesel/oval şekiller kontur olarak çıkarılabilir.

### Nasıl çalışıyor?

Önce görüntü threshold veya edge detection ile binary hale getirilir. Daha sonra `findContours()` beyaz bölgelerin sınırlarını listeler. Her kontur için alan, çevre, merkez, dikdörtgen sınır, dairesellik ve hiyerarşi bilgileri hesaplanabilir.

Örnek işlem zinciri:

```python
contours, hierarchy = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

for cnt in contours:
    area = cv2.contourArea(cnt)
    if area < 100:
        continue

    M = cv2.moments(cnt)
    if M["m00"] != 0:
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
```

### Avantajları

- Hızlı ve açıklanabilir bir yöntemdir.
- Hedefin merkezini momentlerle bulabilir.
- Alan, oran, çevre, dairesellik gibi filtrelerle yanlış tespitler azaltılabilir.
- Hedef halkaları iç içe konturlar oluşturduğu için `RETR_TREE` hiyerarşi bilgisi faydalıdır.
- Sonuçlar debug etmek ve raporlamak kolaydır.

### Dezavantajları

- Binary maske kötü ise konturlar da kötü olur.
- Gürültü, kopuk çizgiler ve parlamalar yanlış konturlar üretir.
- Kamera çok eğik bakarsa halka konturları bozulabilir.
- Hedef uzak olduğunda kontur küçük kalabilir.
- Arka plandaki benzer şekiller yanlış aday oluşturabilir.

### Bizim yarışmada kullanılabilir mi?

**Evet.** Bu yarışmada hedef, kontrastlı halkalardan oluştuğu için kontur tespiti en pratik ana yöntemlerden biridir. Hedef tespitinden sonra merkez hesaplama, hata vektörü çıkarma ve servo kontrol için yeterli veri sağlar.

### Yarışma için öneri

Kontur filtresi şu kriterlerle yapılabilir:

- Alan aralığı: çok küçük ve çok büyük konturlar elenir.
- En-boy oranı: hedef perspektifte elips olacağı için makul oran aralığı seçilir.
- Dairesellik/ovallik: `4*pi*area/perimeter^2` ile kontrol edilir.
- Hiyerarşi: iç içe konturlar hedef halkalarını doğrulamak için kullanılır.
- Merkez yakınlığı: birden fazla halka aynı merkeze yakınsa hedef güven skoru artırılır.

Kaynaklar: OpenCV contour başlangıç dokümantasyonu: https://docs.opencv.org/3.4/d4/d73/tutorial_py_contours_begin.html, OpenCV contour özellikleri: https://docs.opencv.org/4.x/dd/d49/tutorial_py_contour_features.html

---

## 3. Hough Circle Transform

### Algoritma adı

**Hough Circle Transform / Hough Daire Dönüşümü**  
OpenCV fonksiyonu: `cv2.HoughCircles`.

### Ne işe yarıyor?

Görüntüdeki dairesel şekilleri bulur. Atış hedefindeki iç daire ve halkalar kamera görüntüsünde daireye yakın görünüyorsa merkez ve yarıçap tespiti için kullanılabilir.

### Nasıl çalışıyor?

Hough dönüşümü kenar piksellerini kullanarak olası daire merkezleri ve yarıçapları için oy toplar. Belirli bir merkez ve yarıçap yeterince çok kenar pikseli tarafından desteklenirse daire olarak kabul edilir.

Örnek:

```python
gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
gray = cv2.medianBlur(gray, 5)

circles = cv2.HoughCircles(
    gray,
    cv2.HOUGH_GRADIENT,
    dp=1.2,
    minDist=40,
    param1=100,
    param2=30,
    minRadius=10,
    maxRadius=120
)
```

### Avantajları

- Dairesel hedefler için doğrudan merkez ve yarıçap verir.
- Konturlar kopuk olsa bile kenar bilgisi yeterliyse çalışabilir.
- Parametreler doğru ayarlanırsa hedef halkalarını bulabilir.
- Hedef merkezini hesaplamak kolaydır.

### Dezavantajları

- Perspektif etkisinde daireler elipse dönüştüğünde performans düşer.
- Parametre ayarı hassastır: `param1`, `param2`, `minRadius`, `maxRadius`.
- Gürültü ve arka plandaki dairesel nesneler yanlış tespit üretebilir.
- Uzak hedefte yarıçap küçük olduğunda kararsızlaşabilir.
- Gerçek zamanlı çalışsa da contour yöntemine göre daha maliyetli olabilir.

### Bizim yarışmada kullanılabilir mi?

**Kısmen evet.** Kamera hedefe yaklaşık dik bakıyorsa ve hedef görüntüde daireye yakınsa kullanılabilir. Ancak araç rampada, eğimde veya hedefe açılı bakarken hedef elips gibi görüneceği için tek ana algoritma olarak seçilmemelidir.

### Yarışma için öneri

- Hough Circle, contour/ellipse yöntemiyle birlikte ikinci doğrulama katmanı olarak kullanılmalıdır.
- Hedef ilk bulunduğunda sadece ROI içinde çalıştırılmalıdır; tüm görüntüde çalıştırmak gereksiz yük oluşturur.
- Hough sonucu ile ellipse/contour merkezi benzerse güven skoru artırılmalıdır.

Kaynak: OpenCV Hough Circle Transform dokümantasyonu: https://docs.opencv.org/4.x/da/d53/tutorial_py_houghcircles.html

---

## 4. Ellipse Detection / fitEllipse

### Algoritma adı

**Ellipse Detection / Elips Tespiti**  
OpenCV fonksiyonları: `cv2.fitEllipse`, `cv2.ellipse`, `cv2.minAreaRect`.

### Ne işe yarıyor?

Görüntüdeki oval/eliptik şekillerin merkezini, eksen uzunluklarını ve dönüş açısını bulur. Gerçek dünyada daire olan hedef, kamera perspektifi nedeniyle görüntüde çoğu zaman elips olarak görüneceği için bu yöntem atış hedefi için çok uygundur.

### Nasıl çalışıyor?

Önce hedefe ait konturlar bulunur. Her kontur yeterli sayıda noktaya sahipse `fitEllipse()` ile bu noktalara en uygun elips oturtulur. Sonuç olarak elips merkezi `(cx, cy)`, eksen boyutları ve açı elde edilir.

Örnek:

```python
for cnt in contours:
    if len(cnt) < 5:
        continue

    ellipse = cv2.fitEllipse(cnt)
    (cx, cy), (major, minor), angle = ellipse

    ratio = min(major, minor) / max(major, minor)
    if ratio < 0.25:
        continue
```

### Avantajları

- Perspektif bozulmasına Hough Circle’a göre daha dayanıklıdır.
- Hedef merkezini doğrudan verir.
- İç içe elipslerin merkezlerinin yakın olması hedefi doğrulamak için güçlü bir ipucudur.
- Rampa, eğim ve kamera açısı değişiminde daha esnektir.
- Atış hedefindeki halka yapısına uygundur.

### Dezavantajları

- Kontur kalitesi kötüyse elips de hatalı çıkar.
- En az 5 kontur noktasına ihtiyaç duyar.
- Hedefin sadece küçük kısmı görünüyorsa yanlış elips oturabilir.
- Benzer oval nesneler yanlış aday olabilir.
- Çok fazla konturda çalıştırılırsa işlem yükü artabilir.

### Bizim yarışmada kullanılabilir mi?

**Evet, güçlü aday.** Atış hedefi dairesel halkalardan oluşsa bile kameranın hedefe tam dik bakması beklenmemelidir. Bu nedenle ellipse fitting, hedef merkezini bulmak için contour detection ile birlikte ana yöntem olarak seçilmelidir.

### Yarışma için öneri

Hedef güven skoru şu şekilde hesaplanabilir:

- Aynı bölgede birden fazla elips var mı?
- Elips merkezleri birbirine yakın mı?
- Elips eksen oranı makul mü?
- Elips alanı hedef mesafesi için beklenen aralıkta mı?
- Hedefin kırmızı/siyah/beyaz renk yapısı maskeyle uyumlu mu?

Kaynaklar: OpenCV rotated boxes and ellipses dokümantasyonu: https://docs.opencv.org/4.x/de/d62/tutorial_bounding_rotated_ellipses.html, OpenCV fitEllipse örneği: https://docs.opencv.org/3.4/d9/d73/samples_2cpp_2fitellipse_8cpp-example.html

---

## 5. OpenCV Camera Crosshair Alignment

### Algoritma adı

**Camera Crosshair Alignment / Kamera Nişangâh Hizalama**

### Ne işe yarıyor?

Kamera görüntüsünün merkezi veya önceden kalibre edilmiş lazer vurma noktası ile hedef merkezi arasındaki piksel farkını hesaplar. Bu fark pan-tilt servo, lazer yönlendirici veya araç üstü nişan mekanizması için hata sinyali olarak kullanılır.

### Nasıl çalışıyor?

Önce kameranın görüntü merkezi veya kalibrasyonla bulunan lazer referans noktası belirlenir:

```python
crosshair_x = frame_width // 2
crosshair_y = frame_height // 2
```

Daha sonra hedef merkezi bulunur:

```python
error_x = target_x - crosshair_x
error_y = target_y - crosshair_y
```

Servo kontrolü bu hataya göre yapılır:

```python
pan_cmd  = Kp_x * error_x
tilt_cmd = Kp_y * error_y
```

Daha iyi sistemde kamera merkezi yerine gerçek lazerin görüntüde vurduğu nokta kullanılır. Çünkü kamera optik ekseni ile lazer ekseni aynı olmayabilir. Buna **camera-laser calibration** denir.

### Avantajları

- Uygulaması çok basittir.
- Hedef merkezine kilitlenme mantığını net şekilde sağlar.
- Hata değeri doğrudan kontrol algoritmasına verilebilir.
- Debug ekranında crosshair çizilerek kolay test edilir.
- Manuel ve otonom atış modunda ortak kullanılabilir.

### Dezavantajları

- Kamera merkezi ile lazer noktası aynı kabul edilirse kalibrasyon hatası oluşabilir.
- Kamera-lazer eksenleri paralel değilse mesafeye bağlı hata oluşur.
- Servo backlash, mekanik boşluk ve titreşim nişanı bozabilir.
- Lens distorsiyonu düzeltilmezse görüntü kenarlarında hata artar.
- Araç hareketliyken görüntü bulanıklığı ve titreşim hatayı büyütür.

### Bizim yarışmada kullanılabilir mi?

**Evet.** Hedef tespitinden sonra nişan alma için temel yöntem budur. Ancak sadece görüntü merkezi kullanılmamalı; gerçek lazer düzeneği kamera ile kalibre edilmelidir.

### Yarışma için öneri

- Kamera kalibrasyonu yapılmalı: `cameraMatrix`, `distCoeffs`.
- Lazerin görüntüdeki gerçek vurma noktası farklı mesafelerde ölçülmeli.
- Crosshair noktası mesafeye göre düzeltilebilir.
- Hedefe kilitlenme için hata toleransı belirlenmelidir, örneğin `abs(error_x) < 5 px` ve `abs(error_y) < 5 px`.
- 1 saniyelik atış öncesi kararlılık için hata birkaç frame boyunca tolerans içinde kalmalıdır.

---

## 6. Visual Servoing

### Algoritma adı

**Visual Servoing / Görsel Geri Beslemeli Servo Kontrol**

### Ne işe yarıyor?

Kameradan alınan hedef konumuna göre servo veya motor komutlarını otomatik üretir. Amaç, görüntü düzlemindeki hedef merkezini crosshair/lazer referans noktasına getirmektir.

### Nasıl çalışıyor?

Bu yarışma için en pratik yaklaşım **Image-Based Visual Servoing (IBVS)** mantığıdır. 3B hedef pozunu tam hesaplamak yerine görüntüdeki 2B piksel hatası kullanılır.

Temel döngü:

1. Kameradan görüntü al.
2. Hedef merkezini bul.
3. Hedef merkezi ile crosshair arasındaki piksel hatasını hesapla.
4. Hatayı PID veya P kontrolcüye ver.
5. Servo açılarını güncelle.
6. Hata küçük ve kararlıysa lazer atışına izin ver.

Basit kontrol:

```python
error_x = target_x - laser_ref_x
error_y = target_y - laser_ref_y

pan_angle  += Kp_x * error_x
tilt_angle += Kp_y * error_y
```

Daha kararlı kontrol:

```python
pan_angle  += Kp_x * error_x + Ki_x * sum_error_x + Kd_x * delta_error_x
tilt_angle += Kp_y * error_y + Ki_y * sum_error_y + Kd_y * delta_error_y
```

### Avantajları

- Hedef ve nişangâh aynı görüntüdeyse doğrudan kapalı çevrim kontrol sağlar.
- Mekanik hata, küçük kalibrasyon hatası ve titreşim kısmen telafi edilebilir.
- Hedefe kilitlenme otomatik yapılır.
- Otonom atış görevi için en uygun kontrol yaklaşımıdır.
- Hedef kayarsa sistem tekrar hizalayabilir.

### Dezavantajları

- Kontrol kazançları yanlış seçilirse sistem salınım yapabilir.
- Görüntü işleme gecikmesi servo kontrolünü bozabilir.
- Kamera FPS düşükse tepki yavaş olur.
- Titreşimli platformda hedef merkezi zıplayabilir.
- Hedef kaybolduğunda güvenli duruma geçmek gerekir.

### Bizim yarışmada kullanılabilir mi?

**Evet.** Otonom atış için hedef tespiti tek başına yeterli değildir; tespit edilen hedefe lazer yönlendirmek gerekir. Bu nedenle visual servoing, hedef tespit sisteminin kontrol katmanı olmalıdır.

### Yarışma için öneri

- İlk sürümde sadece P kontrolcü kullanılmalı.
- Daha sonra küçük D terimi eklenerek salınım azaltılmalı.
- Servo komutları sınırlandırılmalı.
- Hedef kaybolursa lazer kesinlikle kapalı kalmalı.
- Hedef kilit kararı için son 10-20 frame ortalama hata kullanılmalı.
- Atış anında araç ve lazer yönlendirici hareket ettirilmemelidir.

Kaynaklar: OpenCV calibration/pose refinement dokümantasyonunda visual servoing kavramı geçer: https://docs.opencv.org/4.x/d9/d0c/group__calib3d.html, visual servoing öğretici kaynak: https://sir.upc.edu/projects/ris_tutorials/advanced/visual_servoing/visual_servoing.html

---

## 7. Laser Pointer Detection

### Algoritma adı

**Laser Pointer Detection / Lazer Noktası Tespiti**

### Ne işe yarıyor?

Kamera görüntüsünde lazer noktasını bulur. Bu yöntem hedef tespiti değil, daha çok lazer-kamera kalibrasyonu, atış sonrası doğrulama ve manuel test için kullanılır. Yarışma kuralı gereği nişan alma lazer kapalıyken yapılmalıdır; bu yüzden lazer noktasını nişan alma boyunca sürekli açık tutmak uygun değildir.

### Nasıl çalışıyor?

Lazer genellikle kırmızı veya yeşil parlak bir nokta olarak görünür. HSV renk uzayında lazerin renk aralığı maskelenir. Ardından en parlak ve küçük alanlı kontur seçilir.

Örnek:

```python
hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

mask_laser = cv2.inRange(hsv, lower_laser, upper_laser)
mask_laser = cv2.morphologyEx(mask_laser, cv2.MORPH_OPEN, kernel)

contours, _ = cv2.findContours(mask_laser, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

laser_point = None
if contours:
    cnt = max(contours, key=cv2.contourArea)
    M = cv2.moments(cnt)
    if M["m00"] != 0:
        laser_point = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
```

### Avantajları

- Kamera-lazer kalibrasyonu için çok faydalıdır.
- Lazerin gerçekten nereye vurduğunu görmeye yarar.
- Atış sonrası kayıt analizinde puan halkası kontrolü yapılabilir.
- Parlak renkli nokta olduğu için iyi pozlamada tespiti kolaydır.
- Manuel testlerde hızlı geri bildirim sağlar.

### Dezavantajları

- Yarışma sırasında nişan alma bitmeden lazer açmak kurala aykırı olabilir.
- Parlak güneş, yansıma ve hedef yüzeyi tespiti zorlaştırabilir.
- Kamera pozlaması lazer noktasını doyurabilir.
- Kırmızı hedef çizgileri veya ışıklar yanlış tespit olabilir.
- Lazer açıkken araca/lazere hareket verilmemesi gerektiği için kontrol döngüsünde dikkatli kullanılmalıdır.

### Bizim yarışmada kullanılabilir mi?

**Evet, ancak sınırlı ve dikkatli.** Lazer pointer detection ana nişan alma algoritması olmamalıdır. Asıl nişan alma hedef tespiti + crosshair alignment + visual servoing ile lazer kapalıyken yapılmalıdır. Lazer tespiti daha çok kalibrasyon ve test aşamasında kullanılmalıdır.

### Yarışma için öneri

- Test alanında lazer açılarak kamera-lazer referans noktası kalibre edilmeli.
- Yarışma modunda lazer sadece atış komutunda açılmalı.
- Lazer açıldıktan sonra hareket komutu kilitlenmeli.
- Kayıt edilen görüntüde lazer noktası sonradan analiz edilerek sistem başarısı ölçülmeli.

---

## Önerilen birleşik sistem mimarisi

### A. Görüntü işleme hattı

1. Kamera görüntüsünü al.
2. Lens distorsiyon düzeltmesi uygula.
3. Gürültü azalt: Gaussian/median blur.
4. HSV veya gri seviye threshold ile hedef maskesi çıkar.
5. Morfolojik temizleme uygula.
6. Konturları bul.
7. Konturlardan elips/dairesel adayları çıkar.
8. İç içe halka yapısını ve merkez tutarlılığını kontrol et.
9. En yüksek güven skoruna sahip hedefi seç.
10. Hedef merkezini hesapla.

### B. Nişan alma hattı

1. Hedef merkezi `(target_x, target_y)` bulunur.
2. Lazer referans/crosshair noktası `(ref_x, ref_y)` alınır.
3. Piksel hatası hesaplanır: `error_x = target_x - ref_x`, `error_y = target_y - ref_y`.
4. Visual servoing kontrolcüsü servo komutunu üretir.
5. Hata tolerans içine girene kadar lazer kapalı kalır.
6. Hata belirli sayıda frame boyunca küçük kalırsa sistem “kilitlendi” durumuna geçer.
7. Araç ve lazer yönlendirici hareketi durdurulur.
8. Lazer 1 saniye aktif edilir.

### C. Güvenlik ve kural uyumu

- Hedef yoksa lazer kapalı.
- Hedef güven skoru düşükse lazer kapalı.
- Servo hareket ediyorsa lazer kapalı.
- Lazer aktifken servo ve araç hareket komutu kilitli.
- Atıştan önce son hata değeri ve hedef güven skoru loglanmalı.
- Kamera görüntüleri kaydedilmeli.

---

## Önerilen algoritma seçimi

### Minimum çalışan sistem

- Thresholding
- Contour detection
- `fitEllipse`
- Crosshair alignment
- P kontrollü visual servoing

Bu kombinasyon düşük işlem gücüyle çalışır ve yarışmanın otonom atış hedefi için yeterli başlangıç sağlar.

### Daha sağlam sistem

- HSV + adaptif threshold
- Contour detection
- Ellipse fitting
- Hough Circle ile doğrulama
- Hedef güven skoru
- Kalman/EMA filtre ile merkez yumuşatma
- PID visual servoing
- Kamera-lazer kalibrasyonu
- Lazer nokta tespiti ile test/doğrulama

---

## Hedef güven skoru önerisi

Aşağıdaki puanlama ile hedef tespit kararı daha güvenilir yapılabilir:

| Kriter | Puan |
|---|---:|
| Kontur alanı beklenen aralıkta | +1 |
| Elips eksen oranı makul | +1 |
| İç içe en az 2 halka bulundu | +2 |
| Halka merkezleri birbirine yakın | +2 |
| Hedef rengi/kontrastı beklenen yapıda | +1 |
| Hedef son frame’lerde aynı bölgede | +1 |
| Hough Circle/ellipse merkezi uyumlu | +1 |
| Toplam | 9 |

Örnek karar:

- 0-3: hedef yok / güvensiz
- 4-6: hedef adayı var, lazer açma
- 7-9: hedef güvenilir, servo hizalama yapılabilir

---

## Yarışma için kısa sonuç

Bu yarışma için en mantıklı hedef tespiti yaklaşımı, tek bir algoritmaya güvenmek yerine **thresholding + contour detection + ellipse detection** birleşimidir. Hough Circle Transform destekleyici doğrulama olarak kullanılabilir, ancak perspektif sebebiyle ana yöntem olmamalıdır. Nişan alma kısmında **camera crosshair alignment** ve **visual servoing** kullanılmalıdır. **Laser pointer detection** ise yarışma sırasında nişan alma için değil, kalibrasyon ve doğrulama için kullanılmalıdır.

Önerilen ana sistem:

```text
Kamera
  -> Threshold / HSV mask
  -> Contour detection
  -> fitEllipse
  -> Hedef merkezi
  -> Crosshair hata hesabı
  -> Visual servoing
  -> Hedef kilit
  -> Lazer atış
```

Bu mimari hem açıklanabilir hem hızlı hem de yarışma şartnamesindeki otonom hedef tespiti ve lazerle temsilî atış görevine uygundur.
