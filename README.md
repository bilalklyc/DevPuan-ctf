<div align="center">
  <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExM3BqMndrM2VnMGc2aGZjZ2ZqMnhqM2NqZ2JqMnhqM2NqZ2JqMnhqMyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/L1R1tvI9svkIWwpVYr/giphy.gif" alt="Hacking Animation" width="150"/>

# 🚀 DevPuan CTF Lab

**Stajyer Ahmet'in CEO Olma Mücadelesi**

[![Python](https://img.shields.io/badge/Python-3.11-blue.svg?style=for-the-badge\&logo=python)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-2.x-lightgrey.svg?style=for-the-badge\&logo=flask)](https://flask.palletsprojects.com/)
[![Docker](https://img.shields.io/badge/Docker-Supported-2496ED.svg?style=for-the-badge\&logo=docker)](https://www.docker.com/)
[![Vulnerabilities](https://img.shields.io/badge/Vulnerabilities-Logic%20Flaw%20%7C%20SQLi-red.svg?style=for-the-badge)](#)

</div>

---

## 📖 Senaryo

**DevPuan**, şirket çalışanlarının performans puanlarıyla yan haklar satın alabildiği kapalı devre bir alışveriş ve İK portalıdır.

Sisteme sadece **50 DevPuan (DP)** sahibi **Stajyer Ahmet** olarak giriş yapıyorsunuz. Ancak Ahmet'in gözü yükseklerde: O, **1.000.000 DP** değerindeki **CEO Odası Giriş Kartı'nı** istiyor.

### 🎯 Göreviniz

Sistemdeki güvenlik zafiyetlerini keşfederek:

1. 🏢 CEO odası kapı şifresini ele geçirip **Flag 1'i** bulun.
2. 💼 İK Bordro sistemine sızarak Ahmet'in yetkilerini ve maaşını CEO seviyesine çıkarıp **Flag 2'yi** bulun.

---

## 🎯 İçerdiği Zafiyetler

> ⚠️ **Spoiler:** Laboratuvarın içerdiği zafiyetleri görmek istiyorsanız aşağıdaki bölümü açın.

<details>
<summary>🔓 Zafiyetleri görmek için tıklayın</summary>

<br>

### 🛒 Business Logic Flaw — Negative Quantity

Ödeme ve sepet sisteminde kullanıcı tarafından gönderilen ürün miktarının yeterince doğrulanmaması nedeniyle **negatif miktar** değerleri kullanılabilmektedir.

Bu durum, fiyat hesaplama mantığının manipüle edilmesine ve başlangıçta yalnızca **50 DevPuan** bulunan kullanıcının yüksek değerli ürünleri satın alabilmesine yol açmaktadır.

**Temel problem:**

```text
Ürün Fiyatı × Negatif Miktar
        ↓
Negatif toplam
        ↓
Bakiye manipülasyonu
        ↓
Yetkisiz ürün satın alma
```

### 💉 UPDATE Statement SQL Injection

İK portalındaki maaş güncelleme mekanizmasında kullanıcı girdisinin güvenli şekilde işlenmemesi nedeniyle **SQL Injection** meydana gelmektedir.

`UPDATE` sorgusunun parametrik olmayan şekilde oluşturulması, saldırganın sorgunun yapısını manipüle ederek veritabanındaki maaş ve yetki bilgilerinin değiştirilmesine olanak sağlamaktadır.

Bu zafiyet sonucunda:

* Maaş bilgisi manipüle edilebilir.
* Kullanıcı yetkileri değiştirilebilir.
* **Privilege Escalation** gerçekleştirilebilir.

</details>

---

## 🛠️ Kurulum

Projeyi ayağa kaldırmanın en izole ve güvenli yolu **Docker** kullanmaktır.

### Ön Koşullar

* [Docker](https://docs.docker.com/get-docker/)
* [Docker Compose](https://docs.docker.com/compose/install/)

### 1. Repoyu Klonlayın

```bash
git clone https://github.com/bilalklyc/devpuan-ctf.git
cd devpuan-ctf
```

### 2. Laboratuvarı Başlatın

```bash
docker-compose up --build -d
```

### 3. Uygulamaya Erişin

Tarayıcınızdan:

```text
http://localhost:5000
```

Laboratuvarı durdurmak için:

```bash
docker-compose down
```

---

## 🎮 Hedefler — Flags

Sistemi analiz ederken bulmanız gereken **2 adet flag** bulunmaktadır:

* [ ] **Flag 1:** `TUGA{...}`
  Mağaza sistemindeki iş mantığı hatasını keşfedin ve CEO odası şifresine ulaşın.

* [ ] **Flag 2:** `TUGA{...}`
  İK sistemindeki SQL Injection zafiyetini keşfedin ve yetki yükseltme gerçekleştirin.

> 💡 **İpucu:** HTTP isteklerini analiz etmek ve manipüle etmek için **Burp Suite** veya **OWASP ZAP** kullanmanız şiddetle tavsiye edilir.

---

## 🧪 Önerilen Araçlar

| Araç              | Kullanım                                       |
| ----------------- | ---------------------------------------------- |
| 🦋 **Burp Suite** | HTTP request/response analizi ve manipülasyonu |
| 🛡️ **OWASP ZAP** | Web uygulaması güvenlik testleri               |
| 🐳 **Docker**     | İzole laboratuvar ortamı                       |
| 🐍 **Python**     | Kod analizi ve yardımcı scriptler              |

---

## ⚠️ Disclaimer

Bu proje yalnızca **eğitim, CTF ve yetkili güvenlik testi** amacıyla hazırlanmıştır.

Laboratuvar içerisindeki zafiyetler kasıtlı olarak oluşturulmuştur. Gerçek sistemlerde, sistem sahibinin açık izni olmadan bu tekniklerin uygulanması uygun değildir.

---

## 👨‍💻 Author

**Bilal Kalaycı**

Software Engineering Student | Cybersecurity Enthusiast

* 🔐 Offensive Security
* 🕵️ Red Team / Pentesting
* 🌐 Web Application Security
* 🐍 Python
