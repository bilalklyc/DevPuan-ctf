# DevPuan CTF - Writeup & Remediation

> 💡 **Detaylı Analiz:** Bu projenin hikayeleştirilmiş sömürü adımları ve görsel destekli okuması için [Medium Makalemi Buradan Okuyabilirsiniz](#) *()*.

---

## 🚀 Hızlı Özet

### 🚩 Flag 1: Business Logic Flaw (Negative Quantity)
* **Zafiyet:** `/api/add-to-cart` uç noktasında `quantity` parametresi için negatif değer kontrolü yapılmamaktadır.
* **Exploit:** Burp Suite ile `quantity` değeri `-50000` yapılarak sepet toplamı negatif (`-1.000.000 DP`) hale getirilir. Bakiyeden bu eksi değer çıkarıldığında (`50 - (-1.000.000)`) hesap bakiyesi 1.000.050 DP'ye yükselir.
* **Bayrak:** `TUGA{st4jy3r_4hm3t_c30_r0z3t1n1_k4pt1_981a}`

### 🚩 Flag 2: UPDATE Statement SQL Injection
* **Zafiyet:** `/ik-payroll` formundan gelen `salary` parametresi doğrudan f-string ile SQL sorgusuna (`UPDATE employees SET salary = {requested_salary}...`) gömülmektedir.
* **Exploit:** `is_real_ceo` sütunu keşfedildikten sonra, `salary` parametresine `1000000, is_real_ceo = 1 WHERE emp_code = 'EMP104' --` payload'u gönderilir. `--` operatörü sistemin asıl kısıtlamasını devreden çıkarır.
* **Bayrak:** `TUGA{sql1_1l3_c30_y3tk1s1_v3_m44s_ucuruldu_77b}`

---

## 📖 Detaylı Senaryo ve Sömürü Adımları

### 📌 Senaryo Özeti
Bu CTF senaryosunda, "DevPuan" adlı şirket içi ödül sistemine giriş yapan Stajyer Ahmet'in rolünü üstleniyoruz. Hesabımızda sadece 50 DevPuan (DP) bulunuyor. Görevimiz, sistemdeki mantıksal zafiyetleri ve veri işleme hatalarını sömürerek önce 1.000.000 DP'lik CEO Odası giriş kartını almak (Flag 1), ardından da İK sistemini manipüle ederek gerçek CEO yetkilerine sahip olmak (Flag 2).

### 🚩 Bölüm 1: CEO Odası Giriş Kartı (Flag 1)
**Zafiyet Türü:** İş Mantığı Hatası (Business Logic Flaw / Negative Quantity)

**Keşif:**
Sisteme giriş yaptığımızda mağazada çeşitli ürünler bulunuyor. CEO Makam Odası kartının fiyatı 1.000.000 DP iken bizim bakiyemiz yalnızca 50 DP. Normal şartlarda bu ürünü satın almamız imkansızdır.
Sepete ürün ekleme ve satın alma mekanizmasını analiz etmek için Burp Suite ile araya giriyoruz. Sepete ekleme işlemi `/api/add-to-cart` uç noktasına bir JSON isteği atarak gerçekleşiyor.

**Zafiyet ve Sömürü (Exploitation):**
Burp Suite üzerinden giden isteği incelediğimizde, sepete eklenecek ürün miktarını belirleyen `quantity` parametresinin, sunucu tarafında pozitif bir tam sayı olup olmadığının kontrol edilmediğini (Input Validation eksikliği) fark ediyoruz.

Bu zafiyeti sömürmek için Burp Suite üzerinden şu adımları izliyoruz:
1. Intercept ayarını 'on' yapıp ucuz bir ürünün (Örn: ID 1 - Kupa) miktarını negatif bir değer (`-50000`) olarak gönderiyoruz. Kupanın birim fiyatı 20 DP olduğu için arka planda sistem şu hesabı yapıyor: `20 DP * (-50000) = -1.000.000 DP` (Toplam Sepet Tutarı).
2. Ödeme aşamasına geçtiğimizde sistem bakiyemizden sepet tutarını çıkarmaya çalışıyor. Formül `Yeni Bakiye = Mevcut Bakiye - Sepet Tutarı` şeklinde çalıştığı için matematiksel bir çöküş yaşanıyor: `50 DP - (-1.000.000 DP) = 1.000.050 DP`.
3. Input Validation (Girdi Doğrulama) eksikliği yüzünden sistem bizden para tahsil etmek yerine hesabımıza 1 Milyon DP yatırıyor. Bu devasa bakiye ile CEO Rozetini normal bir şekilde sepete ekleyip satın alıyor ve 1. Bayrağı elde ediyoruz.

**Flag 1:** `TUGA{st4jy3r_4hm3t_c30_r0z3t1n1_k4pt1_981a}`

### 🚩 Bölüm 2: Gerçek CEO Yetkisine Ulaşmak (Flag 2)
**Zafiyet Türü:** SQL Injection (SQLi)

**Keşif:**
Birinci bayrağı alıp terminale girdikten sonra bizi İK Bordro ve Yetkilendirme konsolu (`/ik-payroll`) karşılıyor. Ekranda sistemin işleyişine dair çok kritik bir ipucu (uyarı) bulunuyor: *"Gerçek CEO yetkisi kesinlikle verilmeyecektir!"*

Aldığımız hatanın ardından SQL Injection şüphesiyle, girdi alanına tek tırnak (`'`) göndererek veritabanı tepkisini ölçtük. Hata mesajından yola çıkarak uygulamanın tek tırnak (`'`) karakterini filtrelemediğini doğruladık. İşlemleri hızlandırmak için HTTP isteğini Burp Suite Repeater'a aktardık.

**Zafiyetin Sömürülmesi (Exploitation):**
Hedefimiz Ahmet'in yetkisini yükseltmek ancak arka plandaki yetki sütununun adını bilmiyoruz. Arayüzdeki "Gerçek CEO Yetkisi" tablosundan yola çıkarak `UPDATE` sorgusunun içine sızmak (UPDATE Injection) için sırasıyla `role`, `is_ceo`, ve `is_real_ceo` gibi isimleri denedik.

`is_real_ceo` parametresini kullandığımızda sistemin hata vermediğini gördük ve nihai payload'umuzu HTTP gövdesindeki (body) `salary` parametresine şu şekilde enjekte ettik:

`salary=1000000, is_real_ceo = 1 WHERE emp_code = 'EMP104' --`

**Payload Analizi:**
* **`1000000`:** İstenen maaş miktarını ayarlar.
* **`, is_real_ceo = 1`:** `SET` bloğunun içine sızarak kendi yetki atamamızı yaparız.
* **`WHERE emp_code = 'EMP104'`:** Değişikliğin sadece Stajyer Ahmet'i etkilemesini garantiye alırız.
* **`--`:** SQL'de yorum satırı operatörüdür. Kodun orijinalinde bulunan, bizi engelleyen (Örn: `, is_real_ceo = 0 WHERE...`) kısmını devre dışı bırakır.

Sorguyu gönderdiğimizde veritabanı manipüle ediliyor, kısıtlamalar atlatılıyor ve Ahmet gerçek CEO yetkisine kavuşarak 2. Bayrağı ekrana yazdırıyor.

**Flag 2:** `TUGA{sql1_1l3_c30_y3tk1s1_v3_m44s_ucuruldu_77b}`

---
