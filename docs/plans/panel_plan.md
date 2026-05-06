# Yer Kontrol İstasyonu (GCS Panel) Yol Haritası ve Planlaması

Bu doküman kullanıcı tarafından iletilen detaylı İKA Yer Kontrol Paneli isterlerini barındırır. Proje geliştirimi bu maddeler üzerinden modüler olarak yapılacaktır.

## 1. Kullanılacak Teknolojiler ve İzlenecek Yol
- **Framework**: React (Vite ile başlatılması önerilir).
- **Stil ve Tasarım**: Tailwind CSS. (Savunma sanayii, Rover Control, Drone GCS vb. Taktik Arayüz "Dark Mode" konsepti benimsenecek).
- **Prototipleme**: React arayüzü kodlanmadan önce Figma ile konsept tasarım yapılabilir.
- **Veri Akışı**: Geliştirme sürecinin ilk aşamalarında tüm widget'lar için "Sahte Veriler (Dummy Data)" kullanılacak. Panel bu sayede arka plandan bağımsız olarak test edilebilecek.

## 2. Ana Gösterge Maddeleri (Layout & Widgets)

### Merkez Ekran (Görev / Parkur Yönetim)
- **Etap Listesi**: Yarışma etapları TODO LİST şeklinde sıralanacak (tamamlandı, aktif, hata, pas hakkı kullanıldı).
- **Zamanlayıcılar**: 15dk genel görev sayacı ve koşu süresi.
- **Puan Durumu**: Ceza Puanları, geçerli puan tahmini (opsiyonel) ve pas hakkı durumu.

### Kamera Paneli (3+1 Yapı)
- İleri Sürüş, Geri Sürüş ve Nişan Kamerası akışları.
- AI Detection Overlay (Görüntü İşleme Katmanı): Koni, tabela, kayar engel, hedef tespiti ve atış nişan merkezi doğrudan ekrana bindirilecek.

### Otonomi Durum Paneli
- Aktif Mod göstergesi (Otonom / Manuel).
- Mevcut görev durumu.
- Yeniden planlama (re-planning) durumu.
- Karar Log'u: Aracın kurtarma stratejisi, "bekleme seçildi" gibi aldığı otonom kararların akan log ekranı.

### Görev Özelinde Widget'lar
- **Dik Eğim**: Stop doğrulama modülü (Geri sayımlı 2sn bekleme sayacı).
- **Kayar Engel**: Tahmin paneli (Kayma hızı, tahmini geçiş penceresi, güvenli geçiş zamanlaması).
- **Atış Paneli / Nişangah**: Hedefe kilitlenildi, lazer nişanlandı, atış penceresi hazır ibareleri. Ayrıca 2. atış denemesine yönelik vuruş geribildirim ekranı.

### Telemetri & Araç Sağlığı
- **Bileşenler**: Pil, Motor Durumu, IMU, Eğim (Pitch/Roll), CPU, GPU.
- **Bağlantı**: Bağlantı kalitesi, Paket Kaybı.
- **Sensör Durumu**: Lidar, GPS, Kamera 1/2/3 ve ana iletişim modüllerinin anlık "Sağlık (Health)" durumu.

### Güvenlik Paneli / Fail-Safe
- Acil Durdurma (E-Stop).
- Bağlantı Kayıp Monitörü.
- Arıza Emniyeti Devre Durumu.
- Fren Kilidi.
- Manuel Engelleme (Sistemi zorla kapatma/devralma).

### Mod Geçiş Paneli
- Araç çalışma modunu seçme düğmeleri: Manuel, Otonom, Hibrit Hata Ayıklama (Hybrid Debug).
