# 08 - Model Sınıfları

Bu doküman, ilk nesne algılama modeli için kullanılacak başlangıç sınıflarını ve ilerleyen aşamalarda eklenebilecek sınıfları tanımlar.

## İlk Model İçin Başlangıç Sınıfları

İlk modelde sınıf sayısı gereksiz yere artırılmamalıdır. Amaç, parkur görevleri için en kritik nesneleri güvenilir şekilde algılayan sade ve hızlı bir model oluşturmaktır.

| Sınıf Adı | Açıklama |
|---|---|
| `stage_sign` | Parkur aşama tabelası |
| `traffic_cone` | Trafik konisi |
| `target` | Atış hedefi |
| `sliding_obstacle` | Kayar engel |
| `stop_marker` | Stop noktası / stop işareti |

## Sonradan Eklenebilecek Sınıflar

İlk model kararlı çalıştıktan ve yeterli veri toplandıktan sonra aşağıdaki sınıflar eklenebilir:

| Sınıf Adı | Açıklama |
|---|---|
| `barrier` | Yol bariyeri |
| `road_boundary` | Yol sınırı / parkur kenarı |
| `water_area` | Su geçiş alanı |
| `gravel_area` | Taşlı / çakıllı yol bölgesi |
| `bump` | Tümsek / engebeli arazi elemanı |

## Sınıf Seçim Stratejisi

- İlk model yalnızca yarışma başarısını doğrudan etkileyen nesnelere odaklanmalıdır.
- Başlangıç sınıfları, otonom sürüş ve otonom görev kararları için temel algılama ihtiyaçlarını karşılamalıdır.
- Ek sınıflar, modelin ilk sürümü sahada test edildikten sonra veri kalitesi ve görev ihtiyacına göre eklenmelidir.
- Sınıf sayısının erken aşamada fazla artırılması, veri toplama yükünü büyütür ve modelin kararlılığını düşürebilir.
