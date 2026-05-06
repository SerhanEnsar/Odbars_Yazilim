# Git Workflow & Sistematik Çalışma Prensipleri

## Branch Stratejisi (Feature Branching)
Proje tamamen modüler olarak yürütülecek ve ana branch her zaman çalışır kod içerecektir.

- `main` branch: Sadece stabil, test edilmiş ve yarışma şartlarını sağlayan kodları barındırır.
- `develop` branch: Entegrasyonların yapıldığı ana geliştirme branch'i.
- *Feature Branchler*: Her bir yeni özellik için oluşturulacak alt branch'ler.
  - Örnek: `feature/vision-yolo-setup`
  - Örnek: `feature/panel-ui-design`
  - Örnek: `feature/api-connection`
  - Örnek: `bugfix/json-parsing-error`

## Geliştirme Süreci
1. Özellik belirle ve ilgili `.md` plan dosyasını güncelle.
2. `develop` üzerinden yeni bir branch oluştur (`git checkout -b feature/isim`).
3. Kodu geliştir. İlgili `vision` veya `panel` klasörü altında çalış.
4. Commit'leri anlaşılır ve Conventional Commits formatında at (`feat: ...`, `fix: ...`, `docs: ...`).
5. Özellik tamamlanınca GitHub üzerinde PR (Pull Request) aç ve review sonrası `develop` branch'ine birleştir (merge).
6. Hazır sistem yarışma simülasyonu ile test edildikten sonra `develop` -> `main` merge'i gerçekleştir.
