# 🚇 MetroExpressSim

> **Yerel (Local) + Ekspres (Express) metro işletmesini istasyon içi geçiş cepleri kullanarak simüle eden Python tabanlı metro işletme simülatörü.**

Bu proje, İstanbul Büyükşehir Belediyesi'nin **Bütçe Senin** platformuna sunduğum **"MetroEkspres: İstasyon İçi Geçiş Cepleri ile Kesintisiz ve Hızlı Metro Hattı İşletim Modeli"** önerisinin teknik olarak simülasyon ortamında test edilmesi amacıyla geliştirilmiştir.

Amacım yalnızca bir fikir sunmak değil, bu fikrin gerçek işletme koşullarında uygulanabilirliğini algoritmalar ve simülasyon yardımıyla analiz etmektir.

---

# 🎯 Projenin Amacı

Uzun metro hatlarında;

- 🚇 Yerel (Local) trenler
- 🚄 Ekspres (Express) trenler

aynı hat üzerinde birlikte çalıştırılarak;

- Yolculuk sürelerinin azaltılması
- Hat kapasitesinin korunması
- İşletme verimliliğinin artırılması
- Ekspres işletmenin uygulanabilirliğinin analiz edilmesi

hedeflenmektedir.

İlk simülasyon modeli **M5 Üsküdar – Sultanbeyli Metro Hattı** üzerinden geliştirilmektedir.

---

# 🚄 İşletme Modeli

Simülasyonda;

- **30 tren/saat**
- **15 Local**
- **15 Express**

işletmesi modellenmektedir.

Yerel trenler tüm istasyonlarda durmaktadır.

Ekspres trenler ise yalnızca ana aktarma ve yüksek yolcu talebine sahip istasyonlarda durmaktadır.

---

# 🚉 İstasyon İçi Geçiş Cepleri

Modelin temelini her istasyonda bulunduğu varsayılan **Passing Track (Cep Hattı)** oluşturmaktadır.

Her istasyonda;

- Ana Hat
- Cep Hattı

bulunmaktadır.

Yerel trenler cep hattına girerek yolcu indirip bindirirken;

Ekspres trenler ana hattan durmaksızın geçebilmektedir.

Bu sayede aynı hatta iki farklı servis tipi birlikte işletilebilmektedir.

---

# 🚦 Dispatcher (Trafik Kontrol Sistemi)

Simülasyonun en önemli bileşeni **Dispatcher** sistemidir.

Dispatcher her saniye bütün trenleri analiz ederek aşağıdaki kararları vermektedir.

## İşletme Kuralları

- Yerel tren her istasyonda cep hattına girer.
- Yolcu iniş-binişi başladıktan sonra arkadaki ekspres tren kontrol edilir.
- Eğer belirlenen mesafe içerisinde yaklaşan bir ekspres tren varsa yerel tren ana hatta çıkmaz.
- Bekleme süresince kapılar açık kalır ve yolcu alımı devam eder.
- Ekspres tren yaklaşırken yerel tren kapılarını kapatır ve kalkış hazırlığına başlar.
- Ekspres tren ana hattan geçer geçmez yerel tren minimum bekleme süresiyle ana hatta bağlanarak seferine devam eder.
- Böylece ekspres tren hiçbir zaman yerel tren nedeniyle hızını düşürmek zorunda kalmaz.
- Eğer ekspres trenin de durduğu bir ana arter istasyondaysa, ekspres tren de istasyona gireceği için yerel tren arkasını kontrol etmeden standart kalkış prosedürüyle ana hatta bağlanabilir.

---

# 💻 Kullanılan Teknolojiler

- Python
- Object-Oriented Programming (OOP)
- CSV tabanlı hat modeli
- Ayrık Zamanlı Simülasyon
- Pygame
- Dispatcher tabanlı trafik yönetimi

---

# 📁 Proje Yapısı

```text
MetroExpressSim/
│
├── data/
│   ├── stations.csv
│   └── segments.csv
│
├── src/
│   ├── dispatcher.py
│   ├── line.py
│   ├── simulation.py
│   ├── station.py
│   ├── train.py
│   └── visualizer.py
│
├── main.py
├── README.md
└── requirements.txt
```

---

# 💡 İlham Kaynağı

Bu proje, **İBB Bütçe Senin** platformuna sunduğum **"MetroEkspres: İstasyon İçi Geçiş Cepleri ile Kesintisiz ve Hızlı Metro Hattı İşletim Modeli"** önerisinin teknik olarak simülasyon ortamında doğrulanmasını amaçlamaktadır.

---
