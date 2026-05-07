# 07 - Model Eğitimi İhtiyacı

Bu doküman, İnsansız Kara Aracı yarışması için görüntü işleme / yapay zekâ tabanlı algılama bileşenlerinde model eğitimi gerekip gerekmediğini netleştirir.

| Sistem | Model gerekli mi? | Önerilen yöntem |
|---|---|---|
| Tabela | Evet | YOLO + OCR/sınıflandırıcı |
| Koni | Evet | YOLO |
| Kayar engel | Evet | YOLO + tracking |
| Hedef | Şart değil | OpenCV / YOLO destekli |
| Nişangâh sapması | Hayır | Geometrik hesap |
| Yol/bariyer | Belki | OpenCV veya segmentation |
| Stop | Belki/Evet | YOLO veya OCR |

## Notlar

- **Tabela algılama** için model eğitimi önerilir. Tabelanın önce nesne olarak tespit edilmesi, ardından üzerindeki aşama numarasının OCR veya sınıflandırıcı ile okunması uygundur.
- **Trafik konileri** parkurda temas edilmeden geçilmesi gereken kritik engellerdir. Bu nedenle güvenilir tespit için YOLO tabanlı nesne algılama önerilir.
- **Kayar engel** yalnızca tespit edilmemeli, aynı zamanda konumu ve hareket yönü takip edilmelidir. Bu nedenle YOLO + tracking yaklaşımı tercih edilmelidir.
- **Hedef tespiti** için OpenCV ile daire / merkez / kontur tabanlı yöntemler yeterli olabilir. Ancak farklı ışık koşullarında kararlılık için YOLO destekli çözüm eklenebilir.
- **Nişangâh sapması** görüntüde hedef merkezi ile lazer / nişangâh merkezi arasındaki piksel farkından geometrik olarak hesaplanabilir; ayrıca model eğitimi gerekmez.
- **Yol ve bariyer algılama** için klasik görüntü işleme yeterli olabilir. Ancak su, yağmur, çakıl, eğim ve gölge gibi durumlarda segmentation modeli gerekebilir.
- **Stop işareti / noktası** için metin okunacaksa OCR, nesne olarak tespit edilecekse YOLO kullanılabilir.
