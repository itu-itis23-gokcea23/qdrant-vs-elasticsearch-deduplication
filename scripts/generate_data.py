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
    "kirli_urun": [
        "Ürün çok kirli bir şekilde geldi, iğrenç haldeydi.",
        "Paket açıldığında içindeki ürün lekeliydi.",
        "Teslim aldığım ürünün üzerinde pislik vardı.",
        "Ürün hijyenik değildi, kirlenmiş halde ulaştı.",
        "Aldığım ürün temiz değildi, üzerinde leke mevcuttu.",
        "Ürünün ambalajı açık ve içi kirli gelmişti.",
        "Gelen ürünün yüzeyi kirli ve pis görünümlüydü.",
        "Kutunun içindeki ürün kullanılmış gibi kirli çıktı.",
        "Hijyen konusunda ciddi sorun yaşadım, ürün kirliydi.",
        "Ürün bana temiz gelmedi, üzerinde leke ve iz vardı.",
        "Sipariş ettiğim ürün kirli haldeydi, kullanmaktan çekindim.",
        "Ürün paketlenmeden önce temizlenmemiş olmalı, lekeli geldi.",
        "Kutu içindeki ürün pis ve kirli durumdaydı.",
    ],
    "kirik_urun": [
        "Kutu açılınca ürünün çatlak olduğunu fark ettim.",
        "Teslim aldığımda ürün kırık haldeydi.",
        "Ürün hasar görmüş olarak elime ulaştı.",
        "Ambalaj açıldığında içindeki parça kırılmıştı.",
        "Ürünün bir köşesi ezilmiş ve çatlamış geldi.",
        "Kargo sürecinde ürün zarar görmüş, kırık teslim edildi.",
        "Aldığım ürünün gövdesi çatlamıştı.",
        "Paket açtığımda ürün paramparçaydı.",
        "Ürünün camı kırık çıktı, kullanılamaz durumdaydı.",
        "Sipariş ettiğim ürün hasarlı ve çatlak şekilde geldi.",
        "Kutu içindeki ürün ezilmiş, deforme olmuştu.",
        "Teslimat sırasında ürüne zarar verilmiş, kırık geldi.",
        "Ürünün plastik kapağı kırılmış haldeydi.",
    ],
    "gec_teslimat": [
        "Siparişim üç haftadır hâlâ gelmedi.",
        "Kargo çok geç ulaştı, beklediğimden 10 gün fazla sürdü.",
        "Ürünü zamanında teslim alamadım, çok gecikmeli geldi.",
        "Teslimat tarihi geçmesine rağmen kargo hâlâ yolda.",
        "Siparişim bir ayı aşkın süredir kapıma ulaşmadı.",
        "Kargo firması ürünü çok geç getirdi.",
        "Beklenen teslimat tarihinin çok ötesine geçildi.",
        "Sipariş vereli 3 hafta oldu, ürün hâlâ elime ulaşmadı.",
        "Tahmini teslimat tarihini 2 hafta aştılar.",
        "Ürünüm çok gecikmeli geldi, neredeyse iptal edecektim.",
        "Kargo süreci inanılmaz uzun sürdü, çok bekledim.",
        "Teslimat bu kadar geç olmaz, kabul edilemez bir durum.",
        "Sipariş ettiğim ürün haftalar geçmesine rağmen gelmedi.",
    ],
    "yanlis_urun": [
        "Sipariş ettiğimden farklı bir renk geldi.",
        "Başka bir model teslim edildi, yanlış ürün göndermişler.",
        "Aldığım ürün siparişimdeki ürün değildi.",
        "Farklı beden gönderilmiş, seçtiğimle uyuşmuyor.",
        "Yanlış ürün gönderildi, iade etmek zorunda kaldım.",
        "Sipariş ettiğim markadan farklı bir marka geldi.",
        "Ürünün rengi ve modeli hiç uymuyordu siparişime.",
        "Bana başka birinin siparişi gönderilmiş gibi.",
        "Seçtiğim ürün yerine tamamen farklı bir şey geldi.",
        "Gönderilen ürün sipariş formundaki ile eşleşmiyordu.",
        "Yanlış beden ve yanlış renk geldi, hiçbiri doğru değil.",
        "Sipariş numaramla eşleşmeyen bir ürün teslim edildi.",
        "Tamamen yanlış ürün geldi, hiç benzemiyordu siparişime.",
    ],
    "fatura_sorunu": [
        "Fatura tutarı ödediğimden farklı çıktı.",
        "KDV yanlış hesaplanmış, fazla ücretlendirildim.",
        "Makbuz eksik gönderildi, fatura alamadım.",
        "Faturada ürün adı yanlış yazılmıştı.",
        "İndirim faturaya yansıtılmamış, fazla para ödedim.",
        "Fatura bilgilerim hatalı yazılmış.",
        "Vergi numaramı yanlış kesmişler faturaya.",
        "Aldığım fatura tutarı sipariş tutarıyla uyuşmuyor.",
        "Fatura gönderilmedi, defalarca talep etmem gerekti.",
        "Faturada eksik bilgi var, muhasebemize işletemiyoruz.",
        "Çift fatura kesilmiş, iki kez ödeme yapılmış gibi görünüyor.",
        "Fatura üzerindeki tarih yanlış, sorun çıkıyor.",
        "E-fatura sistemine düşmedi, tekrar istemek zorunda kaldım.",
    ],
    "musteri_hizmetleri": [
        "Müşteri temsilcisi çok kaba davrandı.",
        "Destek hattı sorularıma hiç cevap vermedi.",
        "Şikayetimi ilettim ama kimse geri dönmedi.",
        "Müşteri hizmetleri telefonu açmıyor.",
        "Saatlerce beklettiler, sorunum hâlâ çözülmedi.",
        "Temsilci ilgisiz ve umursamaz bir tavır sergiledi.",
        "Geri dönüş sözü verdiler ama aramadılar.",
        "Canlı destek bağlanamıyor, sürekli hata veriyor.",
        "Şikayetim kayıt altına alınmadı, hiçbir işlem yapılmadı.",
        "Müşteri temsilcisi sorunu anlayamadı ve yanlış yönlendirdi.",
        "Destek ekibi çözüm üretmek yerine geçiştirdi.",
        "Çağrı merkezinde defalarca aktarıldım, sorun çözülmedi.",
        "Müşteri hizmetleri çalışanı sabırsız ve saygısızdı.",
    ],
    "iade_sorunu": [
        "İade talebim kabul edilmedi, haksız yere reddedildi.",
        "İade sürecim bir aydır sonuçlanmadı.",
        "Para iadesi hesabıma yatmadı.",
        "İade için kargo gönderdim ama ürünü teslim almadılar.",
        "İade formunu doldurdum, hiçbir geri dönüş olmadı.",
        "İade politikası sitede yazdığından farklı uygulandı.",
        "İade ettiğim ürünün parası eksik yatırıldı.",
        "Ürünü iade etmek istedim ama sistem izin vermedi.",
        "İade sürecinde ürün kayboldu, hiç izlenemedi.",
        "İade talebimi gönderdim, onaylansın diye haftalar bekliyorum.",
        "İade ettiğim ürün teslim alındı ama para iadesi gelmedi.",
        "İade politikasını anlamak için defalarca aramak zorunda kaldım.",
        "Para iadesi 3 iş günü denmişti, 3 haftadır bekliyorum.",
    ],
    "ambalaj_sorunu": [
        "Ürün çok kötü paketlenmişti, dağınık haldeydi.",
        "Ambalaj tamamen açık ve hasarlı geldi.",
        "Kutu ezilmiş ve içindeki ürün korumasız kalmıştı.",
        "Paketleme çok yetersizdi, ürün zarar gördü.",
        "Naylon poşete sarılı geldi, hiç uygun değil.",
        "Kırılabilir ürün balonlu naylon olmadan gönderilmişti.",
        "Kutu üzerinde çok sayıda ezik ve delik vardı.",
        "Ambalaj malzemesi yetersizdi, ürün içinde sallanıyordu.",
        "Kutu içinde dolgu malzemesi yoktu, ürün hasarlı geldi.",
        "Paket açılmış gibi bantlanmıştı, güven vermedi.",
        "Ambalaj sızdırmaz değildi, içindeki sıvı dışarı çıkmıştı.",
        "Kırılabilir ibaresi olmasına rağmen özensiz paketlenmişti.",
        "Kutu tamamen ezilmişti, ürünü zor çıkardım.",
    ],
    "urun_aciklamasi": [
        "Ürün sitedeki açıklamayla hiç uyuşmuyordu.",
        "Özellikleri yanlış yazılmış, aldatıcı bir açıklama.",
        "Sitede gösterilen ürün ile gelen ürün farklıydı.",
        "Ürünün boyutları açıklamadaki gibi değildi.",
        "Malzeme bilgisi yanlış, cotton dendi polyester çıktı.",
        "Ürün görseli gerçeği yansıtmıyor.",
        "Ağırlık bilgisi hatalı yazılmıştı.",
        "Garanti süresi açıklamadan farklı çıktı.",
        "Teknik özellikler eksik ve yanıltıcı yazılmış.",
        "Ürün renkli gösterilmiş ama siyah beyaz geldi.",
        "Aksesuar ürünle birlikte gelir denmiş ama gelmedi.",
        "Ürün açıklaması çok yanıltıcı, mağdur oldum.",
        "Kapasitesi açıklamada farklı, gerçekte çok daha az.",
    ],
    "odeme_sorunu": [
        "Kredi kartımdan fazla ücret çekildi.",
        "Çift ödeme yapıldı, iki kez para çıktı hesabımdan.",
        "Ödeme onaylandı ama sipariş oluşmadı.",
        "Ödeme sayfasında hata alıyorum, ödeyemiyorum.",
        "İndirim kodu uygulanmadı ama ödeme alındı.",
        "Kapıda ödeme seçeneği çalışmıyor.",
        "Taksit seçeneği sözünden döndüler, tek çekim yapıldı.",
        "Ödeme iade edilmesi gerekirken hâlâ çekildi.",
        "Banka hareketi gözüküyor ama sipariş sistemde yok.",
        "3D Secure sayfasında takılı kaldım, ödeme geçmedi.",
        "Farklı bir tutarda ödeme kesildi, ne olduğunu anlamadım.",
        "Ödeme başarısız dedi ama hesabımdan para çıktı.",
        "Promosyon indirimi ödeme aşamasında düşülmedi.",
    ],
    "urun_kalitesi": [
        "Ürün çok düşük kaliteli, fiyatına değmez.",
        "Sadece bir kullanımda bozuldu, dayanıksız.",
        "Malzeme kalitesi çok kötü, ucuz hissettiriyor.",
        "İki gün içinde rengi soldu, kalitesiz bir ürün.",
        "Ürün görüntüsü güzeldi ama kalitesi çok kötü çıktı.",
        "Dikiş kalitesi berbat, ilk giyişte söküldü.",
        "Ürün plastik kısımları çok ince ve kırılgan.",
        "Çok pahalı bir ürün ama kalitesi piyasa malından beter.",
        "Kısa sürede deforme oldu, beklentimin çok altında.",
        "Ürünün kokusu çok rahatsız ediciydi, kalitesiz malzeme.",
        "Yüzey kaplaması ilk temizlikte döküldü.",
        "Ürünün vidaları gevşek çıktı, montaj kalitesi sıfır.",
        "Bu fiyata bu kalite kabul edilemez.",
    ],
    "eksik_parca": [
        "Kutu içinde bazı parçalar eksikti.",
        "Montaj kılavuzu ürünle birlikte gönderilmemişti.",
        "Setin bir parçası eksik, kullanamıyorum.",
        "Kablo gelmedi, ürünü çalıştıramıyorum.",
        "Ürünle birlikte olması gereken adaptör yoktu.",
        "Garanti belgesi kutu içinde çıkmadı.",
        "Pil dahil denmişti ama pil gelmedi.",
        "Ürünün vida takımı eksikti, montaj yapamadım.",
        "Setin tamamı gelmemiş, bir parça kayıp.",
        "Şarj kablosu kutuda yoktu, ürün işe yaramıyor.",
        "Ürün manualsiz geldi, nasıl kullanacağımı bilemedim.",
        "Kutu içindeki kontrol listesinde tik atılmış ama parça yok.",
        "Birden fazla parça eksik çıktı, çok mağdur oldum.",
    ],
    "kargo_firmasi": [
        "Kargo görevlisi kapıyı çalmadan gitmişti.",
        "Kargo firması ürünü yanlış adrese bırakmış.",
        "Teslimat saati bildirilmedi, evde beklemek zorunda kaldım.",
        "Kargo görevlisi çok kaba davrandı.",
        "Ürün kargo deposunda kaybolmuş.",
        "Kargo takip numarası çalışmıyor, nerede olduğunu bilmiyorum.",
        "Görevli ürünü eşiğe fırlatıp gitti.",
        "Kargo şirketi teslim ettiğini söylüyor ama ürün yok.",
        "Aynı gün teslimat vaat edildi, 3 gün sonra geldi.",
        "Teslimat randevusu verildi ama o gün gelmedi.",
        "Kargo firması ürünü hasarlı teslim etti.",
        "Görevli ürünü komşuya bırakmış, haberim olmadı.",
        "Kargo deposu çok uzak, ürünü almaya gidemiyorum.",
    ],
    "uyelik_hesap": [
        "Hesabım sebepsiz yere kapatıldı.",
        "Şifremi sıfırlayamıyorum, link çalışmıyor.",
        "Üyeliğimi iptal etmek istiyorum ama seçenek yok.",
        "Kişisel bilgilerim yanlış kayıt edilmiş.",
        "Adres bilgilerimi güncelleyemiyorum.",
        "Siparişlerim hesabımda görünmüyor.",
        "E-posta adresimi değiştirmek istiyorum ama sistem hata veriyor.",
        "Hesabım hacklendi, güvenlik açığı var.",
        "Giriş yapamıyorum, şifrem doğru olmasına rağmen.",
        "Üyelik bilgilerimin değiştirildiğini fark ettim.",
        "Hesabım doğrulanmadı, e-posta gelmiyor.",
        "Telefon numaram başkasına kayıtlı görünüyor sistemde.",
        "Hesabımı silmek istiyorum ama nasıl yapacağımı bulamıyorum.",
    ],
    "urun_stok": [
        "Ürün stokta var gözüküyordu ama sonra iptal edildi.",
        "Siparişimi verdikten sonra stokta kalmadığını söylediler.",
        "Satın aldığım ürün stoktan düştü, çok mağdur oldum.",
        "Stok bilgisi hatalı, ürün yokken var gözüküyordu.",
        "Kampanyalı ürünü sepete ekledim, stok bitti denildi.",
        "Siparişim onaylandı ama bir hafta sonra stok yok denildi.",
        "Ürün sitede görünüyor ama temin edilemiyor.",
        "Stok takibi çok kötü, aldatıcı bilgi veriliyor.",
        "Ürün var diye ödedim, sonra para iade edildi.",
        "Flash indirimde stok tükendi ama sayfa kapanmadı.",
        "Siparişim 2 kez iptal edildi stok gerekçesiyle.",
        "Gerçek stok durumu sitede yansıtılmıyor.",
        "Ürünü rezerve ettim ama yine de stoktan düştü.",
    ],
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