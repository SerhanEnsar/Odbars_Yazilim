# 04_tabela_tanima_arastirma

## Amaç

Bu araştırmanın amacı, İnsansız Kara Aracı yarışma parkurunda yer alan aşama tabelalarının kamera görüntüsü üzerinden tespit edilmesi ve tabela içindeki görev numarasının okunması için uygulanabilecek algoritma seçeneklerini değerlendirmektir.

Şartnameye göre parkur kenarında her aşamayı belirtmek için dış çapı 60 cm olan, yazı tipi olarak **Arial Black** kullanan tabelalar bulunacaktır. Otonom görevlerde araç bu tabelaları tanıyarak ilgili parkura geldiğini algılamalıdır. Örnek tabela kırmızı dış halka, beyaz iç alan ve siyah görev numarası biçimindedir.

## Problem Tanımı

Tabela tanıma problemi iki alt göreve ayrılabilir:

1. **Tabela tespiti:** Görüntü içinde tabelanın konumunun bulunması.
2. **Görev numarası okuma:** Bulunan tabelanın içindeki rakamın sınıflandırılması veya OCR ile okunması.

Bu nedenle sistem, tek aşamalı bir sınıflandırmadan ziyade iki kademeli bir algı hattı olarak tasarlanmalıdır:

```text
Kamera görüntüsü
      ↓
Tabela tespiti
      ↓
Tabela kırpma / hizalama
      ↓
Rakam okuma
      ↓
Görev numarası
```

## Araştırılan Başlıklar

### 1. Traffic sign detection YOLO

YOLO tabanlı nesne tespit modelleri, trafik işareti veya tabela gibi küçük nesnelerin gerçek zamanlı olarak bulunması için yaygın biçimde kullanılmaktadır. YOLO ailesinin avantajı, görüntüdeki nesneyi tek geçişte konumlandırması ve gömülü sistemlerde çalışabilecek küçük model varyantlarının bulunmasıdır.

Tabela tespiti için YOLO yaklaşımı şu şekilde kullanılabilir:

- Tabela sınıfı için veri seti hazırlanır.
- Farklı mesafe, ışık, açı, bulanıklık ve arka plan koşullarında tabela görüntüleri toplanır.
- Model sadece “tabela” sınıfını tespit edecek şekilde eğitilebilir.
- Model çıktısı olarak bounding box alınır.
- Bounding box içindeki alan kırpılarak rakam okuma aşamasına gönderilir.

**Avantajları**

- Gerçek zamanlı çalışmaya uygundur.
- Tabela farklı açılarda veya kısmen küçük görünse bile öğrenme tabanlı olduğu için dayanıklıdır.
- Kırmızı halka, dairesel şekil ve rakam birlikte öğrenilebilir.
- OpenCV tabanlı klasik yöntemlere göre karmaşık arka planlarda daha kararlı olabilir.

**Dezavantajları**

- Eğitim verisi gerektirir.
- Gömülü donanımda model boyutu ve FPS dikkate alınmalıdır.
- Yanlış pozitifleri azaltmak için yarışma ortamına benzer veri toplanmalıdır.

**Uygunluk değerlendirmesi**

Bu proje için tabela tespiti tarafında en uygun ana yöntem YOLO’dur. Özellikle YOLOv8n / YOLOv11n gibi küçük modeller veya benzer hafif nesne tespit mimarileri gerçek zamanlı kullanım için değerlendirilebilir.

### 2. Traffic sign recognition CNN

CNN tabanlı sınıflandırma modelleri, tespit edilmiş ve kırpılmış trafik işareti görüntüsünün hangi sınıfa ait olduğunu belirlemek için kullanılır. Bu proje özelinde CNN, trafik işareti türünü değil, tabela içindeki görev numarasını sınıflandırmak için kullanılabilir.

Önerilen kullanım:

- YOLO ile tabela bulunur.
- Tabela bölgesi kırpılır.
- Görüntü normalize edilir.
- Rakam alanı merkeze alınır.
- Küçük bir CNN modeli ile 0–9 arası rakam sınıflandırılır.

Basit bir CNN mimarisi yeterli olabilir:

```text
Input: 64x64 gri seviye veya RGB tabela/rakam görüntüsü
Conv2D + ReLU + MaxPool
Conv2D + ReLU + MaxPool
Flatten
Dense
Softmax: 0–9 sınıfı
```

**Avantajları**

- OCR’a göre daha kontrollü bir problemdir.
- Sadece rakam sınıfları gerektiği için model küçük tutulabilir.
- Yarışmadaki tabela fontu sabit olduğundan yüksek doğruluk beklenir.
- Eğitim verisi sentetik olarak üretilebilir.

**Dezavantajları**

- Rakam kırpma ve hizalama kalitesi önemlidir.
- Eğitim verisi yetersiz olursa ışık ve açı değişimlerinde hata yapabilir.

**Uygunluk değerlendirmesi**

Görev numarası tanıma için küçük CNN sınıflandırıcı güçlü bir adaydır. OCR’a göre daha deterministik ve daha hızlı olabilir. Yarışmada kullanılacak fontun Arial Black olması, sentetik veri üretimini kolaylaştırır.

### 3. Hough Circle traffic sign detection

Hough Circle Transform, görüntüde dairesel şekilleri tespit etmek için kullanılan klasik bir görüntü işleme yöntemidir. Yarışmadaki tabela dış formu dairesel olduğundan bu yöntem yardımcı veya yedek tespit yöntemi olarak değerlendirilebilir.

Örnek işlem hattı:

```text
RGB görüntü
      ↓
HSV renk uzayına dönüşüm
      ↓
Kırmızı renk maskesi
      ↓
Gürültü azaltma
      ↓
Canny edge detection
      ↓
Hough Circle Transform
      ↓
Dairesel tabela adayları
```

**Avantajları**

- Eğitim verisi gerektirmez.
- Tabelanın dairesel ve kırmızı halkalı olması nedeniyle uygulanabilir.
- YOLO başarısız olduğunda yedek kontrol olarak kullanılabilir.
- Tespit sonucunda daire merkezi ve yarıçap alınabilir.

**Dezavantajları**

- Işık değişimlerine, gölgeye, bulanıklığa ve kısmi kapanmaya duyarlıdır.
- Parametre ayarı hassastır.
- Kamera açısı arttıkça tabela elips gibi görünebilir; daire varsayımı zayıflar.
- Arka planda başka kırmızı/dairesel nesneler varsa yanlış pozitif üretebilir.

**Uygunluk değerlendirmesi**

Hough Circle ana yöntem yerine yardımcı yöntem olarak kullanılmalıdır. Örneğin YOLO tespitini doğrulamak, kırpma merkezini iyileştirmek veya düşük veri durumunda prototip geliştirmek için faydalıdır.

### 4. OCR digit recognition

OCR, görüntüdeki metni veya rakamı karakter olarak okumak için kullanılır. Bu proje özelinde OCR sadece tabela içindeki tek veya az sayıda rakamı okumak için değerlendirilebilir.

Önerilen OCR işlem hattı:

```text
Tabela kırpması
      ↓
Perspektif düzeltme
      ↓
Gri seviye dönüşüm
      ↓
Threshold / adaptive threshold
      ↓
Morfolojik temizleme
      ↓
Rakam bölgesi kırpma
      ↓
OCR veya digit classifier
```

OCR için iki seçenek vardır:

1. **Hazır OCR motoru:** Tesseract gibi bir OCR motoru sadece rakam modu ile çalıştırılabilir.
2. **Özel rakam sınıflandırıcı:** OCR yerine MNIST benzeri ama tabela fontuna uyarlanmış küçük CNN modeli kullanılabilir.

**Avantajları**

- Hazır OCR araçları ile hızlı prototip yapılabilir.
- Tek rakamlı görev numarası varsa problem basitleşir.
- OCR çıktısına güven skoru eklenebilir.

**Dezavantajları**

- Tesseract genel amaçlı OCR olduğu için küçük, eğik veya bulanık tabela görüntülerinde kararsız olabilir.
- Sadece tek rakam okunacaksa genel OCR fazla karmaşık kalabilir.
- Ön işleme kalitesi sonucu ciddi şekilde etkiler.

**Uygunluk değerlendirmesi**

OCR, ilk prototip için denenebilir; ancak yarışma sistemi için küçük ve özel eğitilmiş bir rakam sınıflandırıcı daha güvenilir olabilir. OCR yedek yöntem veya karşılaştırma yöntemi olarak tutulmalıdır.

### 5. Template matching OpenCV

Template matching, önceden hazırlanmış şablon görüntünün giriş görüntüsü üzerinde kaydırılarak en benzer bölgenin bulunmasıdır. OpenCV’de `cv.matchTemplate()` fonksiyonu ile uygulanabilir.

Bu proje için iki şekilde kullanılabilir:

- Tabela şekli şablonu ile tabela tespiti.
- Rakam şablonları ile görev numarası okuma.

**Avantajları**

- Basit ve hızlı uygulanır.
- Eğitim gerektirmez.
- Font, renk ve ölçek sabit kalırsa iyi sonuç verebilir.
- Erken prototip ve doğrulama için uygundur.

**Dezavantajları**

- Ölçek, açı, perspektif, ışık ve bulanıklık değişimlerine hassastır.
- Gerçek yarışma ortamında kamera açısı değişeceği için tek başına güvenilir değildir.
- Her görev numarası için ayrı şablon hazırlanması gerekir.

**Uygunluk değerlendirmesi**

Template matching ana yöntem olarak önerilmez. Ancak sabit kamera açısı ve sabit mesafe testlerinde hızlı prototip veya CNN/OCR sonucunu doğrulama amacıyla kullanılabilir.

## Yöntem Karşılaştırması

| Yöntem | Kullanım Yeri | Güçlü Yanı | Zayıf Yanı | Proje İçin Rol |
|---|---|---|---|---|
| YOLO | Tabela tespiti | Gerçek zamanlı, dayanıklı | Eğitim verisi ister | Ana tespit yöntemi |
| CNN | Rakam sınıflandırma | Küçük, hızlı, özelleştirilebilir | Veri ve hizalama ister | Ana rakam okuma yöntemi |
| Hough Circle | Daire tespiti | Eğitim gerektirmez | Işık/açı hassas | Yedek/doğrulama |
| OCR | Rakam okuma | Hızlı prototip | Küçük/eğik görüntüde kararsız | Alternatif/yedek |
| Template Matching | Şablon eşleştirme | Basit | Ölçek/açı hassas | Prototip/doğrulama |

## Önerilen Mimari

Bu proje için önerilen tabela tanıma mimarisi:

```text
Kamera görüntüsü
      ↓
YOLO ile tabela tespiti
      ↓
Bounding box kırpma
      ↓
Kırpılan tabela üzerinde:
  - daire merkezi / kırmızı halka kontrolü
  - perspektif ve ölçek düzeltme
      ↓
Rakam bölgesinin çıkarılması
      ↓
Küçük CNN sınıflandırıcı veya OCR
      ↓
Görev numarası
      ↓
Otonom görev karar sistemi
```

## Uygulama Planı

### Aşama 1: Veri Toplama

- Şartnamedeki örnek tabela tasarımına uygun yapay tabela görüntüleri üretilecek.
- Arial Black fontu ile 0–9 rakamları için sentetik veri oluşturulacak.
- Farklı ölçek, döndürme, bulanıklık, parlaklık, gölge ve perspektif bozulmaları eklenecek.
- Gerçek kamera ile farklı mesafelerden tabela görüntüleri alınacak.

### Aşama 2: Tabela Tespiti

- İlk prototip için OpenCV renk maskesi + Hough Circle denenebilir.
- Ana çözüm için YOLO modeli eğitilecek.
- Model sadece tabela sınıfını tespit edecek şekilde sade tutulabilir.
- Başarım ölçütleri:
  - mAP
  - precision / recall
  - FPS
  - yanlış pozitif sayısı

### Aşama 3: Rakam Okuma

- Tabela kırpması normalize edilecek.
- Rakam alanı maskeleme veya merkez kırpma ile çıkarılacak.
- İlk deneme için Tesseract OCR yalnız rakam modu ile test edilecek.
- Ana çözüm olarak 0–9 sınıflı küçük CNN modeli eğitilecek.
- Başarım ölçütleri:
  - rakam doğruluğu
  - karışıklık matrisi
  - düşük ışık ve hareket bulanıklığında doğruluk

### Aşama 4: Sistem Entegrasyonu

- YOLO tespiti güven skoru düşükse Hough Circle veya renk kontrolü ile doğrulama yapılacak.
- Rakam sınıflandırıcı güven skoru düşükse son birkaç karede çoğunluk oylaması uygulanacak.
- Görev numarası birden fazla karede aynı okunmadan karar verilmeyecek.

Örnek karar mantığı:

```text
Son 5 karede okunan görev numaraları:
[8, 8, 8, 3, 8]

Çoğunluk sonucu: 8
Güvenilir karar: evet
```

## Riskler ve Önlemler

| Risk | Etki | Önlem |
|---|---|---|
| Tabela uzakta küçük görünür | YOLO veya OCR hatası | Telefoto/uygun lens, yüksek çözünürlük, küçük nesne eğitimi |
| Hareket bulanıklığı | Rakam okunamaz | Araç hızını düşürme, kısa pozlama, çoklu kare oylama |
| Işık/gölge değişimi | Renk ve OCR hatası | Veri artırma, HSV/CLAHE, adaptif threshold |
| Yan açı/perspektif | Daire elipse dönüşür | YOLO tabanlı tespit, perspektif düzeltme |
| Yanlış tabela tespiti | Yanlış görev kararı | Güven skoru, renk/şekil doğrulama, zamansal filtreleme |
| OCR kararsızlığı | Yanlış rakam | Özel CNN sınıflandırıcı ve çoğunluk oylaması |

## Karar Notu

Tabela tespiti için YOLO ile tabelanın görüntüde bulunması, ardından görev numarasının OCR veya küçük bir sınıflandırıcı model ile okunması değerlendirilecektir.

İlk geliştirme aşamasında OpenCV tabanlı Hough Circle ve template matching yöntemleri hızlı prototip ve doğrulama için kullanılabilir. Nihai sistemde ise ana akışın YOLO + küçük CNN sınıflandırıcı şeklinde kurulması önerilir.

## Kaynaklar

1. Ultralytics, TT100K Dataset dokümantasyonu. Tsinghua-Tencent 100K veri setinin trafik işareti tespiti ve sınıflandırması için 100.000 panoramadan oluşturulmuş büyük ölçekli bir benchmark olduğu belirtilmektedir.  
   https://docs.ultralytics.com/datasets/detect/tt100k/

2. Reveles-Martínez vd., “Benchmarking YOLOv8 to YOLOv11 Architectures for Real-Time Traffic Sign Detection”, 2025. YOLO model varyantlarının gerçek zamanlı trafik işareti tespiti için karşılaştırılmasını ele almaktadır.  
   https://www.mdpi.com/2227-7080/13/11/531

3. Youssouf vd., “Traffic sign classification using CNN and detection using Faster-RCNN and YOLOV4”, 2022. GTSRB üzerinde CNN tabanlı trafik işareti sınıflandırmasını ve YOLO/Faster-RCNN tespit yaklaşımlarını incelemektedir.  
   https://www.sciencedirect.com/science/article/pii/S2405844022030808

4. Uluskan, “Automatic Detection of Regulatory Traffic Signs via Circle Detection”, IJASTECH. Dairesel trafik işaretlerinin tespiti için circle detection yaklaşımını ele almaktadır.  
   https://dergipark.org.tr/en/pub/ijastech/article/709743

5. OpenCV dokümantasyonu, Template Matching. `cv.matchTemplate()` fonksiyonu ile şablonun büyük görüntü üzerinde aranması açıklanmaktadır.  
   https://docs.opencv.org/4.x/d4/dc6/tutorial_py_template_matching.html

6. PyImageSearch, “Detecting and OCR’ing Digits with Tesseract and Python”, 2021. Tesseract ile rakam tespiti ve OCR uygulama adımlarını açıklamaktadır.  
   https://pyimagesearch.com/2021/08/30/detecting-and-ocring-digits-with-tesseract-and-python/

7. TEKNOFEST 2026 İnsansız Kara Aracı Yarışması Şartnamesi. Parkur aşama tabelalarının dış çapı, fontu ve otonom görevlerde tanınması gerekliliği bu dokümandan alınmıştır.
