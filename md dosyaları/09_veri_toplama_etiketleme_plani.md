# 09 - Veri Toplama ve Etiketleme Planı

Bu doküman, İnsansız Kara Aracı yarışması için geliştirilecek görüntü işleme ve yapay zekâ tabanlı algılama sistemlerinde kullanılacak veri toplama ve etiketleme planını tanımlar.

## Toplanacak Veri

Aşağıdaki veri grupları öncelikli olarak toplanmalıdır:

- Parkur tabelası görüntüleri
- Farklı açılardan koni görüntüleri
- Atış hedefi görüntüleri
- Kayar engel videoları
- Stop noktası görüntüleri

## Etiketleme Aracı

Etiketleme sürecinde aşağıdaki araçlardan biri veya birkaçı kullanılabilir:

- Roboflow
- CVAT
- LabelImg

## Veri Çeşitliliği

Modelin gerçek parkur koşullarında daha kararlı çalışabilmesi için veri seti yalnızca ideal görüntülerden oluşmamalıdır. Aşağıdaki çeşitlilikler özellikle sağlanmalıdır:

- Farklı ışık koşulları
- Farklı uzaklıklar
- Farklı kamera açıları
- Hareket bulanıklığı
- Su/yağmur sonrası görüntüler

## Veri Toplama Yaklaşımı

- Görüntüler mümkün olduğunca aracın yarışmada kullanacağı gerçek kameralarla toplanmalıdır.
- İleri sürüş kamerası, geri sürüş kamerası ve nişan kamerasından ayrı veri toplanmalıdır.
- Kayar engel için yalnızca tek kare görüntüler değil, hareket yönünü anlamaya yarayacak kısa video sekansları da kaydedilmelidir.
- Tabela ve stop işaretleri için yakın, orta ve uzak mesafeden örnekler alınmalıdır.
- Atış hedefi için hedefin merkezde, kenarda, kısmen eğik ve farklı uzaklıklarda göründüğü görüntüler toplanmalıdır.

## Etiketleme Kuralları

- Her nesne, görünür sınırlarını kapsayacak şekilde sıkı bounding box ile etiketlenmelidir.
- Kısmen görünen nesneler de etiketlenmelidir.
- Çok bulanık veya tanınamayacak durumda olan nesneler ayrı bir kalite kontrol sürecinde değerlendirilmelidir.
- Sınıf isimleri `08_model_siniflari.md` dosyasındaki adlarla birebir aynı kullanılmalıdır.
- Etiketleme sonrası veri seti mutlaka kontrol edilmeli; yanlış sınıf, eksik kutu ve taşan kutular temizlenmelidir.

## Veri Seti Bölme Önerisi

Başlangıç için veri seti aşağıdaki oranlarda bölünebilir:

| Bölüm | Oran |
|---|---:|
| Eğitim | %70 |
| Doğrulama | %20 |
| Test | %10 |

## İlk Hedef

İlk hedef, az sınıflı fakat güvenilir çalışan bir model üretmektir. Bu nedenle başlangıçta `stage_sign`, `traffic_cone`, `target`, `sliding_obstacle` ve `stop_marker` sınıflarına odaklanılmalıdır.
