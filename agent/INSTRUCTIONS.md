# Yapay Zeka Ajanları İçin Proje Talimatnamesi (AI Agents Guidelines)

Merhaba Meslektaşım (AI Agent),

Bu doküman, "TEKNOFEST 2026 Havacılıkta Yapay Zeka" projesi üzerinde çalışan iki farklı AI ajanı (ben ve sen) arasındaki senkronizasyonu sağlamak ve hatasız bir CI/CD süreci yürütmek için oluşturulmuştur. Lütfen her göreve başlamadan önce bu dokümanı ve `CURRENT_STATE.md` dosyasını dikkatlice oku.

## 1. Mimari ve Kurallar
- **Modülerlik**: Proje kesinlikle modüler olmak zorundadır. Görüntü işleme kodları `/vision`, yer kontrol arayüzü kodları `/panel` klasöründe yer alır. Ortak dökümanlar `/docs` altındadır.
- **Dil**: Kod içi yorum satırları anlaşılır ve temiz olmalıdır. Tercihen İngilizce veya temiz Türkçe kullanılmalıdır.

## 2. Git ve GitHub Kullanım Kılavuzu (Kritik Kurallar)
Maksimum güvenlik ve kod bütünlüğü için aşağıdaki adımları EKSİKSİZ uygulayacaksın:

1. **İşe Başlarken (Branching)**:
   - ASLA doğrudan `main` veya `develop` branch'lerine commit atma.
   - Her yeni özellik veya bug fix için `main` (veya `develop`) üzerinden güncel kodu çek (`git pull origin main`) ve yeni bir branch oluştur: `git checkout -b feature/ozellik-adi` veya `bugfix/hata-adi`.

2. **Commit Süreci**:
   - Commit mesajlarında "Conventional Commits" formatını kullan (`feat: ...`, `fix: ...`, `docs: ...`).
   - Kodunu pushlamadan önce çalıştığından ve hata vermediğinden emin ol.

3. **Pull Request (PR) Açma ve İletişim**:
   - Geliştirmen bittiğinde branch'ini remote'a pushla: `git push origin feature/ozellik-adi`.
   - Sisteme kurulu olan Github CLI (`gh`) aracını kullanarak bir PR oluştur. Komut: `gh pr create --title "feat: Panel arayüzü eklendi" --body "Bu PR, panel arayüzünü içermektedir. CURRENT_STATE güncellenmiştir."`
   - Bizim iletişim kuracağımız ana noktalardan biri PR'lardır. `gh pr list`, `gh pr view <PR-ID>` ve `gh pr review <PR-ID>` komutları ile benim açtığım PR'ları okuyabilir, yorum yapabilir veya inceleyebilirsin.

4. **Merge (Birleştirme) Süreci**:
   - Kendi PR'ını açtıktan sonra, diğer ajanın (benim) veya kullanıcının onayını bekle.
   - Onay verildikten sonra `gh pr merge <PR-ID> --squash` (veya merge/rebase) ile kodu ana branch'e dahil et.

## 3. Durum Senkronizasyonu
- Bir görevi tamamlayıp PR açacağın zaman mutlaka `agent/CURRENT_STATE.md` dosyasını güncelle.
- Ne üzerinde çalıştığını `Sıradaki Adımlar` (To-Do) veya `Şu An Üzerinde Çalışılanlar` sekmesine yaz ki aynı anda aynı dosyalar üzerinde çakışma (conflict) yaşamayalım.

Başarılar dilerim! Birlikte harika bir iş çıkaracağız.
