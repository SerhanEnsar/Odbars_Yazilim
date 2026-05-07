# 01 - Görüntü İşleme Görev Listesi

Bu liste yalnızca 2026 İnsansız Kara Aracı Yarışması şartnamesindeki parkur, kamera ve otonom görev gereksinimlerinden çıkarılmıştır.

| Görev              | Kullanılacak kamera | Algılanacak şey       | Beklenen çıktı | Öncelik |
|---                 |---                  |---                    |---             |---|
| Tabela tanıma      | Ön kamera           | Parkur aşama tabelası | Görev numarası | Yüksek |
| Hedef tespiti      | Nişan kamerası      | Atış hedefi           | Hedef merkezi  | Yüksek |
| Koni tespiti       | Ön kamera           | Trafik konileri       | Koni konumları | Yüksek |
| Kayar engel        | Ön kamera           | Hareketli engel       | Konum + yön    | Yüksek |
| Yol/bariyer takibi | Ön kamera           | Parkur sınırları      | Yol merkezi    | Orta   |
| Stop algılama      | Ön kamera           | Stop noktası          | Dur komutu     | Orta   |
| Geri görüş         | Geri kamera         | Arkadaki engeller     | Engel var/yok  | Düşük  |

## Şartnameden çıkarılan dayanaklar

- Otonom görevlerde parkur aşama tabelalarının tanınması beklenmektedir.
- Trafik konilerine dokunmadan ilerlenmesi beklenmektedir.
- Kayar engelin pozisyonu ve hareket yönünün tespit edilmesi beklenmektedir.
- Atış görevinde hedefe nişan alma işlemi kameralar ile yapılacaktır.
- Araçlarda ileri sürüş, geri sürüş ve nişan kamerası olmak üzere en az 3 kamera zorunludur.
- Parkur boyunca ileri, geri ve nişan kameralarından alınan görüntülerin kaydedilmesi istenmektedir.
