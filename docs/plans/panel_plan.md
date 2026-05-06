# Yer Kontrol İstasyonu (GCS Panel) Planlaması

## 1. Temel Bileşenler
- **Acil Durdurma (Emergency Stop)**: Şartnamede zorunlu tutulan ve aracın tüm motorlarını anında durduran donanımsal butona ek olarak yazılımsal Acil Durdurma özelliği.
- **Çoklu Video Akışı (Multi-Camera Feed)**: İleri Sürüş, Geri Sürüş ve Nişan kameralarından gelen akışların ekranda izlenebilmesi (Ön plana istenen kameranın alınabilmesi).
- **Manuel Kontrol (Teleoperation)**: Yarışmanın "Uzaktan Kontrollü" (Manuel) koşusunda aracı klavye veya harici bir gamepad/joystick ile yönlendirme ekranı. Atış sırasında lazerin aktif edilmesi (tetik) özelliği.
- **Telemetri ve Durum Göstergesi**: Eğim (Pitch/Roll) verileri, hız, batarya (BMS verileri) ve motor sıcaklığı gibi kritik verilerin anlık takibi.
- **Otonom Durum Göstergesi**: Araç "Tam-Otonom" moda alındığında tespit ettiği engellerin (koni, hedef vb.) bounding box olarak panel üzerinden izlenebilmesi.

## 2. Tasarım Prensipleri
- **Karanlık Mod (Dark Mode)**: Sahada güneş altında görünürlüğü ve operatör odağını maksimize edecek, yüksek kontrastlı "askeri/taktik" düzey tasarım.
- **Modüler Widget'lar**: Kameranın, telemetrinin ve haritanın boyutlarının ayarlanabileceği modern dashboard yapısı.

## 3. Kullanılacak Teknolojiler
- HTML5, CSS3, JavaScript / WebSocket / WebRTC.
- Gelişmiş veri görselleştirme için dinamik UI framework'leri.
