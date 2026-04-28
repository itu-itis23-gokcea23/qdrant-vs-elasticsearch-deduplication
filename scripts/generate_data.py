"""
generate_data.py
----------------
Generates 200 fake Turkish customer complaints.
Includes 15 categories, each containing complaints written with different wording.
Goal: To test whether complaints expressing the same issue with different words can be found semantically.
"""

import json
import random

# Set seed for reproducibility
random.seed(42)

# Complaint templates for each category with different linguistic expressions
COMPLAINT_TEMPLATES = {
    "hasarli_ayipli_urun": [
        "Ürün resmen paramparça geldi, kutuyu açınca şok oldum.",
        "Kapağı çatlamış, içindeki sıvı her yere sızmış.",
        "İkinci el ürün mü gönderiyorsunuz? Üstü çizik ve leke içinde.",
        "Dikişleri ilk günden söküldü, kalitesi yerlerde.",
        "Cam kısımları tuzla buz olmuş, paketleme çok yetersiz.",
        "Elektronik ürünün ekranı kırık çıktı, görüntü gelmiyor.",
        "Ürün paslanmış halde ulaştı, belli ki nemli yerde kalmış.",
        "Yüzeyinde derin çizikler var, sıfır ürün olduğuna inanmıyorum.",
        "Plastik aksamı yamulmuş, yerine oturmuyor.",
        "Ürünün her yeri toz ve kir içinde, iğrenç bir görüntü.",
        "Gelen ayakkabının tabanı açılmış, yapışkanı sökük.",
        "Kumaşı çok kalitesiz, resmen şeffaf gibi iç gösteriyor.",
        "Cihazın düğmeleri basılı kalıyor, mekanizması bozuk.",
        "Paketi açtığımda ağır bir koku vardı, ürün rutubetli.",
        "Ürünün bir parçası ezilmiş, estetik olarak çok kötü duruyor.",
        "Boya hataları var, her yeri dalgalı duruyor.",
        "Eski, kullanılmış ürünü paketleyip göndermişsiniz.",
        "Aynası çatlak geldi, kargoda başına gelmeyen kalmamış.",
        "Üstünde parmak izleri ve yağ lekeleri vardı.",
        "Kutusu sağlam ama içindeki ürünün her yeri deforme olmuş."
    ],
    "lojistik_teslimat": [
        "2 hafta oldu tık yok, kargom nerede kardeşim?",
        "Kurye zile bile basmadan 'evde yok' notu düşüp kaçmış.",
        "Tahmini teslimat tarihini 15 gün geçtiniz, ayıp.",
        "Ürünüm başka bir şehirdeki şubede takılı kaldı, ilerlemiyor.",
        "Kargocu paketi bahçeye fırlatmış, yağmurda ıslanmış her şey.",
        "Sipariş hala 'hazırlanıyor' gözüküyor, iptal mi ettiniz?",
        "Takip numarası geçersiz diyor, ürünüm uzayda mı?",
        "Aynı gün teslimat dediniz, 4 gün oldu hala bekliyorum.",
        "Komşuya bırakılmış ama haberim yok, tesadüfen öğrendim.",
        "Kargo şirketi telefonu açmıyor, muhatap bulamıyorum.",
        "Yanlış adrese teslim edilmiş, imza bana ait değil.",
        "Transfer merkezinde 1 haftadır bekliyor, neden hareket etmiyor?",
        "Ürünüm kaybolmuş, kargo firması topu size atıyor.",
        "Acil ihtiyacım vardı ama kargo kaplumbağa hızında geliyor.",
        "Dağıtıma çıktı dediler akşam oldu hala gelen giden yok.",
        "Kargo poşeti yırtılmış, içindekiler dökülmek üzereydi.",
        "Şehir dışına çıkacağım ama kargo hala ulaşmadı, mağdurum.",
        "Sürekli erteleme mesajı geliyor, bıktım artık beklemekten.",
        "Sistemde teslim edildi yazıyor ama kapıma gelen olmadı.",
        "Kurye kaba bir tavırla paketi elime tutuşturup gitti."
    ],
    "yanlis_eksik_urun": [
        "Mavi istedim pembe göndermişsiniz, hiç mi bakmıyorsunuz?",
        "İçinden şarj kablosu çıkmadı, eksik parça var.",
        "Kutuda 2 tane olması gerekiyordu ama sadece 1 tane çıktı.",
        "Başka birinin faturası ve ürünü bana geldi, karışıklık var.",
        "Sitedeki fotoğrafta metal görünüyordu, gelen ürün plastik.",
        "38 numara ayakkabı yerine 42 numara yollamışlar, şaka gibi.",
        "Montaj kılavuzu ve vidalar eksik, kurulum yapamıyorum.",
        "Ürünün yanında hediye verileceği yazıyordu ama gelmedi.",
        "Sipariş ettiğim markayla gelen marka tamamen farklı.",
        "Açıklamada 1 TB yazıyor ama gelen cihaz 500 GB çıktı.",
        "Model numaraları uyuşmuyor, eski versiyonu yollamışsınız.",
        "Kutu tam ama içindeki ana gövde eksik, kullanamıyorum.",
        "Pamuklu diye aldım etiketi %100 polyester çıktı.",
        "Tanıtım videosundaki özelliklerin hiçbiri bu üründe yok.",
        "Yanlış ürün gönderimi yüzünden iadeyle uğraşıyorum, yazık.",
        "Eksik parçaları tamamlayın yoksa tüketici haklarına gideceğim.",
        "Görseldeki renk çok canlıydı, gelen ürün soluk ve mat.",
        "Aparatları eksik olduğu için ürünü çalıştıramadım.",
        "Siparişimdeki 3 üründen sadece 2'si geldi, diğeri nerede?",
        "Yanlış model gelmiş, benim istediğim bu değildi."
    ],
    "finansal_ve_iade": [
        "İade ettim ama para hala banka hesabıma yatmadı.",
        "Kredi kartımdan aynı tutarı iki kez çekmişsiniz, düzeltin.",
        "İndirim kuponu tanımlanmadı, fazla ödeme yaptım.",
        "Fatura gelmedi, mail kutumda da yok, muhasebeye lazım.",
        "İade talebim reddedilmiş, kutusu bile açılmamıştı oysa.",
        "Taksitli alım yapmıştım ama ekstremde tek çekim görünüyor.",
        "Para iadesi yapıldı diyorlar ama bakiyemde artış yok.",
        "Cüzdan hesabımdaki para buhar oldu, kimseye ulaşamıyorum.",
        "Faturadaki isim hatalı yazılmış, şirket adına kesilmemiş.",
        "Ödeme sayfasında hata verdi ama para hesabımdan çekildi.",
        "KDV oranı yanlış hesaplanmış, tutar uyuşmuyor.",
        "İade kargosu karşı ödemeli olacaktı benden ücret aldılar.",
        "Promosyon kodu uygulanmadı, aradaki farkı iade edin.",
        "Siparişimi iptal ettim ama hala provizyonda bekliyor.",
        "Ödeme yaparken sistem dondu, 3 kez onay kodu geldi.",
        "İade süreci çok yavaş, 1 aydır paramı bekliyorum.",
        "Fatura adresi yerine teslimat adresi yazılmış.",
        "Müşteri puanlarım yüklenmemiş, sistem hatası veriyor.",
        "Ücret iadesi eksik yapılmış, kargo bedeli neden kesildi?",
        "Banka dekontu gönderdim ama hala ödeme onaylanmadı diyor."
    ],
    "destek_ve_hesap": [
        "Müşteri hizmetlerine bağlanmak ölüm, müzik dinletip kapatıyorlar.",
        "Temsilci suratıma telefon kapattı, böyle saygısızlık görmedim.",
        "Canlı destek botu sürekli aynı şeyleri söylüyor, çözüm yok.",
        "Şifremi unuttum maili 3 saattir gelmiyor, giriş yapamıyorum.",
        "Hesabım durduk yere askıya alınmış, nedenini bilen yok.",
        "Şikayet yazdım ama sadece otomatik cevap yolladılar.",
        "Temsilci 'yapacak bir şey yok' diyerek beni başından savdı.",
        "Adresimi güncellemek istiyorum ama sistem sürekli hata veriyor.",
        "Maillere asla geri dönüş yapılmıyor, kara delik gibi site.",
        "Üyeliğimi silmek istiyorum ama öyle bir buton koymamışlar.",
        "Giriş yaparken SMS kodu telefonuma bir türlü ulaşmıyor.",
        "Yardım merkezi makaleleri çok eski, güncel bilgi yok.",
        "Temsilci sorunu anlamamakta direniyor, robotla mı konuşuyorum?",
        "Beni hattan hatta aktardılar, sonunda telefon düştü.",
        "Kişisel verilerimin güvenliğinden endişe ediyorum, sızıntı mı var?",
        "Premium üyeliğim aktifleşmedi ama parası çekildi.",
        "Uygulama sürekli çöküyor, sepetimdeki ürünler siliniyor.",
        "Gece yarısı arandım, böyle bir çalışma saati mi olur?",
        "Destek ekibi çok yetersiz, teknik konularda bilgileri sıfır.",
        "Mail adresimi değiştiremiyorum, hata kodu alıyorum."
    ]
}
def generate_complaints():
    """
    Constructs the list of complaint dictionaries based on the templates.
    """
    complaints = []
    complaint_id = 1

    # Iterate through each category and its specific complaint texts
    for category, templates in COMPLAINT_TEMPLATES.items():
        for text in templates:
            complaints.append({
                "id": complaint_id,
                "category": category,
                "text": text
            })
            complaint_id += 1

    # Shuffle the list to randomize data order
    random.shuffle(complaints)
    
    # Re-assign unique IDs after shuffling to keep them sequential
    for i, c in enumerate(complaints):
        c["id"] = i + 1

    return complaints


if __name__ == "__main__":
    # Generate the dataset
    complaints = generate_complaints()

    # Save to JSON file with UTF-8 encoding
    with open("data/complaints.json", "w", encoding="utf-8") as f:
        json.dump(complaints, f, ensure_ascii=False, indent=2)

    print(f"✅ {len(complaints)} complaints generated → data/complaints.json")

    # Display distribution of complaints per category
    from collections import Counter
    cats = Counter(c["category"] for c in complaints)
    for cat, count in sorted(cats.items()):
        print(f"  {cat}: {count} complaints")