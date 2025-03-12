# Mahalle ve İlçe Çekme Scraper

Bu Python scripti, Türkiye'deki mahalle ve ilçe bilgilerini bir web sitesinden çekip, bu verileri bir Excel dosyasından alarak JSON formatına dönüştürür. Veriler, web sitesi üzerinden Excel dosyası olarak indirildikten sonra işlenir, gereksiz bilgiler temizlenir ve mahalle, ilçe ve bağlılık bilgileri düzenli bir şekilde JSON formatında kaydedilir.

## Gereksinimler

Bu scripti çalıştırabilmek için bazı bağımlılıkların kurulması gerekmektedir. Aşağıda, gerekli bağımlılıkların nasıl kurulacağı ve scriptin nasıl çalıştırılacağı hakkında detaylı bilgiler yer almaktadır.

### Bağımlılıkları Kurma

1. **`install_dependencies_first.bat`** dosyasını çalıştırın. Bu dosya, gerekli Python kütüphanelerini yükleyecektir:
    - `selenium`: Web sayfalarından veri çekmek için.
    - `webdriver-manager`: WebDriver'ı otomatik olarak yönetmek için.
    - `pandas`: Excel dosyalarını işlemek ve veri manipülasyonu yapmak için.
    - `openpyxl`: Excel dosyalarını okuma ve yazma işlemleri için.
    - `json`: JSON formatında veri kaydetmek için.

2. **WebDriver Kurulumu**: Script, `Chrome` tarayıcısını kullanmaktadır. Bu nedenle `chromedriver`'ın sisteminizde kurulu olması gerekmektedir. `install_dependencies_first.bat` dosyası, `webdriver-manager` aracılığıyla gerekli sürümü otomatik olarak yükleyecektir.

### Scriptin Çalıştırılması

1. **`run.bat`** dosyasını çalıştırın. Bu dosya, aşağıdaki adımları otomatik olarak gerçekleştirecektir:
   - Web sayfasına bağlanarak mahalle ve ilçe bilgilerini içeren Excel dosyasını indirir.
   - İndirilen dosyayı işler, gereksiz sütunları temizler ve JSON formatında kaydeder.
   - İndirilen Excel dosyasını siler.

## Scriptin Çalışma Adımları

1. **Web Sayfasına Bağlanma**: 
   Script, `https://www.e-icisleri.gov.tr/Anasayfa/MulkiIdariBolumleri.aspx` adresindeki sayfayı açar ve Excel dosyasını indiren butona tıklar.

2. **Excel Dosyasının İndirilmesi**: 
   Excel dosyasının indirilmesi sağlanır ve dosyanın bulunduğu dizin belirlenir.

3. **Excel Dosyasının İşlenmesi**:
   - İndirilen dosya `pandas` ile okunur.
   - Gereksiz sütunlar ve boş satırlar temizlenir.
   - Yalnızca mahalle, ilçe ve bağlılık bilgilerini içeren sütunlar alınır.
   - Veriler, ilçe ve mahalle bilgileri ile birlikte düzgün bir JSON formatına dönüştürülür.

4. **JSON Dosyasının Kaydedilmesi**: 
   Veriler JSON formatında kaydedilir. Eğer daha önce aynı isimde bir dosya varsa, dosya ismi `_1` ekiyle değiştirilir.

5. **Excel Dosyasının Silinmesi**: 
   İndirilen Excel dosyası, işlemler tamamlandıktan sonra silinir.

## Dosya Yapısı

- **`install_dependencies_first.bat`**: Bağımlılıkları yüklemek için kullanılan bat dosyası.
- **`run.bat`**: Scriptin çalıştırılmasını sağlayan bat dosyası.
- **`downloads/`**: İndirilen dosyaların saklandığı klasör.
- **`output/`**: JSON formatında çıktıların kaydedildiği klasör.
- **`mahalleler.json`**: JSON formatındaki çıktı dosyası.

## Önemli Notlar

- Script, başlatıldıktan sonra web tarayıcısının başlatılması ve sayfanın yüklenmesi bir süre alabilir.
- Scriptin çalışabilmesi için `Google Chrome` ve uyumlu bir `chromedriver` sürümü gerekmektedir. Otomatik olarak yükleniyor.