# Yapay Zeka Ajanları İçin Proje Talimatnamesi (AI Agents Guidelines)

Merhaba Meslektaşım (AI Agent),

Bu doküman, "TEKNOFEST 2026 Havacılıkta Yapay Zeka" projesi üzerinde çalışan iki farklı AI ajanı (ben ve sen) arasındaki senkronizasyonu sağlamak için oluşturulmuştur. Lütfen her göreve başlamadan önce bu dokümanı ve aynı klasördeki `CURRENT_STATE.md` dosyasını dikkatlice oku.

## 1. Mimari ve Kurallar
- **Modülerlik**: Proje kesinlikle modüler olmak zorundadır. Görüntü işleme kodları `/vision`, yer kontrol arayüzü kodları `/panel` klasöründe yer alır. Ortak dökümanlar `/docs` altındadır.
- **Git Kullanımı**: ASLA doğrudan `main` veya `develop` branch'lerine kod yazma. Kullanıcın (User) bir özellik istediğinde her zaman `feature/ozellik-adi` veya `bugfix/hata-adi` şeklinde yeni bir branch aç.
- **Dil**: Kod içi yorum satırları anlaşılır ve temiz olmalıdır. Tercihen İngilizce veya temiz Türkçe.

## 2. İletişim Protokolü
- İki ajan olarak birbirimizle haberleşmemizin tek yolu Git geçmişi (commit'ler) ve bu `agent` klasöründeki dosyalardır.
- Bir görevi (feature) bitirip pull request veya merge aşamasına getirdiğinde, lütfen `agent/CURRENT_STATE.md` dosyasını güncelle. Böylece ben (diğer ajan) projeyi çektiğimde senin neyi tamamladığını ve projenin neresinde kaldığımızı anlayabilirim.

## 3. Görev Dağılımı
- Genel olarak **Yer Kontrol İstasyonu (GCS - Panel)** ve **Görüntü İşleme Entegrasyonu** üzerine çalışıyoruz.
- `/docs/plans/` altındaki `.md` dosyalarında planlarımız yer almaktadır. Bir geliştirme yapmadan önce ilgili plan dosyasını kontrol et.

Başarılar dilerim! Birlikte harika bir iş çıkaracağız.
