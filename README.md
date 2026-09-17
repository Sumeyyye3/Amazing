*This project has been created as part of the 42 curriculum by sumdogan, basakall.*

# A-Maze-ing 🌀 — This is the way

Python ile yazılmış, konfigürasyon dosyasından okuduğu ayarlara göre labirent (maze) üreten, terminalde görselleştiren ve giriş-çıkış arasındaki en kısa yolu bulan bir proje.

---

## 📖 Açıklama

A-Maze-ing, verilen bir `config.txt` dosyasını okuyup iki farklı modda labirent üretebilen bir Python programıdır:

- **`PERFECT=True`** modunda, giriş ile çıkış arasında **tek bir yol** bulunan, hiç döngüsü (loop) olmayan klasik bir "perfect maze" üretir.
- **`PERFECT=False`** modunda (varsayılan), Pac-Man tarzı bir oyun tahtası olarak kullanılabilecek, **birden fazla bağımsız rotası** olan, dört köşesi ve merkezi açık, mümkün olduğunca az çıkmaz sokağa (dead-end) sahip "oynanabilir" bir labirent üretir.

Üretilen labirent hem terminalde ASCII sanatıyla gösterilir hem de hexadecimal duvar kodlamasıyla bir çıktı dosyasına yazılır. Program ayrıca girişten çıkışa giden **en kısa yolu** (BFS algoritmasıyla) hesaplar ve hem çıktı dosyasına hem de ekrana (isteğe bağlı olarak) çizer. Etkileşimli bir menü üzerinden labirent yeniden üretilebilir, çözüm yolu gösterilip gizlenebilir ve duvar renkleri değiştirilebilir.

---

## ⚙️ Talimatlar

Proje bağımlılıkları [Poetry](https://python-poetry.org/) ile yönetiliyor ve bir `Makefile` üzerinden çalıştırılıyor.

```bash
# Bağımlılıkları kur (flake8, mypy, poetry sanal ortamı)
make install

# Programı varsayılan config.txt ile çalıştır
make run

# pdb ile debug modunda çalıştır
make debug

# flake8 . ve mypy . ile tüm projeyi denetle
make lint

# __pycache__, .mypy_cache gibi geçici dosyaları temizle
make clean

# Sanal ortamı da silip sıfırdan kurar (fclean + install)
make re
```

Manuel çalıştırmak istersen:

```bash
python3 a_maze_ing.py config.txt
```

- `a_maze_ing.py` proje ana dosyasıdır, adı değiştirilemez.
- `config.txt` tek argümandır; farklı bir isimle başka bir konfigürasyon dosyası da verilebilir.

Program çalıştığında labirenti terminale çizer ve şu menüyü sunar:

```
=== A-Maze-ing ===
1. Re-generate a new maze
2. Show / Hide the shortest path
3. Rotate the wall colours
4. Quit
```

---

## 🗂️ Config Dosyası Formatı

`config.txt` her satırda bir `KEY=VALUE` çifti içerir. `#` ile başlayan satırlar ve satır sonu yorumları yok sayılır.

| Key | Açıklama | Zorunlu mu? | Örnek |
|---|---|---|---|
| `WIDTH` | Labirent genişliği (hücre sayısı) | ✅ | `WIDTH=15` |
| `HEIGHT` | Labirent yüksekliği | ✅ | `HEIGHT=15` |
| `ENTRY` | Giriş koordinatı `x,y` | ✅ | `ENTRY=1,1` |
| `EXIT` | Çıkış koordinatı `x,y` | ✅ | `EXIT=12,13` |
| `OUTPUT_FILE` | Çıktı dosyasının adı | ✅ | `OUTPUT_FILE=print_maze/maze.txt` |
| `PERFECT` | `True`/`False` — tek yollu mu, oynanabilir board mu | ✅ | `PERFECT=False` |
| `SEED` | Rastgele üretimi sabitlemek için tohum değeri | İsteğe bağlı | `SEED=42` |

Repo kökündeki `config.txt`, bu formatı kullanan hazır bir örnektir:

```
WIDTH = 15
HEIGHT = 15
ENTRY = 1,1
EXIT = 12,13
OUTPUT_FILE = print_maze/maze.txt
PERFECT = False
```

### Çıktı Dosyası Formatı

Her hücre, hangi duvarların kapalı olduğunu tek bir hexadecimal rakamla kodlar (bit 0=Kuzey, 1=Doğu, 2=Güney, 3=Batı; bit 1 ise duvar kapalı demektir). Satırlar art arda yazılır, ardından boş bir satırdan sonra sırasıyla giriş koordinatı, çıkış koordinatı ve en kısa yolun `N`/`E`/`S`/`W` harfleriyle gösterimi gelir.

---

## 🧠 Maze Üretim Algoritması

### Neden Kruskal + Union-Find?

Labirent üretimi, **rastgele Kruskal algoritması** ile **Union-Find (Disjoint-Set)** veri yapısı kullanılarak yapılıyor:

1. Her hücre arasındaki tüm potansiyel duvarlar bir liste haline getirilip rastgele karıştırılır.
2. Sırayla her duvar için, duvarın ayırdığı iki hücre zaten aynı "kümede" (birbirine bağlı) değilse duvar kırılır ve iki küme birleştirilir.
3. Sonuç, grid üzerindeki bütün hücreleri **tam olarak bir kez** birbirine bağlayan bir **spanning tree** — yani hiç döngüsü olmayan, "perfect" bir labirent.

Bu algoritmayı seçme sebebimiz: Kruskal, DFS tabanlı (backtracking) üreticilere göre daha az "uzun koridor" eğilimi gösterip daha dengeli, keşfedilmesi ilginç labirentler üretiyor; Union-Find ile birleştirme/arama işlemleri neredeyse O(1) olduğu için büyük labirentlerde de hızlı kalıyor; ve **tam bağlantı garantisi** matematiksel olarak spanning tree'nin doğasından geliyor, ayrıca doğrulama gerektirmiyor.

### `PERFECT=False` — Oynanabilir Board

`PERFECT=False` olduğunda, önce yukarıdaki Kruskal algoritmasıyla temel bir spanning tree kuruluyor (tam bağlantı garantisi buradan geliyor), sonra üzerine iki aşamalı bir işlem uygulanıyor:

1. Kalan kapalı duvarların bir kısmı rastgele kırılarak labirente **döngüler (loop)** ekleniyor — her kırılan duvarın koridoru 2 hücreden geniş bir "oda" haline getirip getirmediği kontrol ediliyor, getiriyorsa geri kapatılıyor.
2. Ardından kalan **çıkmaz sokaklar (dead-end)** tek tek tespit edilip, yine "geniş koridor" kuralını bozmayacak şekilde birer duvar daha kırılarak elenmeye çalışılıyor.

Sonuç, subject'in `maze_analyzer.py` scripti ile doğrulanan, dört köşesi ve merkezi açık, en az iki bağımsız rotası olan ve gerçek dead-end'i olmayan (bonus seviyesinde "braided") bir board.

### En Kısa Yol — BFS

Labirentteki her geçiş eşit maliyetli (ağırlıksız bir graf) olduğu için, en kısa yolu bulmak için **BFS (Breadth-First Search)** kullanıyoruz. BFS, girişten başlayıp katman katman yayılarak bir hücreye ilk ulaştığı anda oraya olan en kısa yoldan gelmiş olduğunu garanti eder; bu yüzden Dijkstra gibi ağırlıklı-graf algoritmalarına hiç gerek yok, BFS hem en basit hem de burada en doğru seçim.

---

## ♻️ Yeniden Kullanılabilir Kısım

`kruskal/` paketindeki `generate_kruskal_maze` fonksiyonu ve `pathfinder/` paketindeki `find_shortest_path` fonksiyonu, projenin geri kalanından bağımsız, saf Python modülleri olarak yazıldı — başka bir projeye doğrudan kopyalanıp import edilebilir:

```python
from kruskal import generate_kruskal_maze
from pathfinder import find_shortest_path

# Sabit bir seed ile üret, böylece her çalıştırmada aynı labirent çıkar
maze = generate_kruskal_maze(
    cells: List[List[Dict[str, bool]]],
    width: int,
    height: int,
    blocked_cells: Set[Tuple[int, int]],
) -> List[List[Dict[str, bool]]]:

# maze, cells[y][x] formatında bir liste; her hücre {"N","E","S","W"} anahtarlı
# bir dict, True ise o yönde duvar kapalı demektir.
path = find_shortest_path(maze, entry=(0, 0), exit_pos=(9, 9))
# path, "EESSN..." gibi bir string döner
```

`blocked_cells` parametresiyle belirli hücreler (örn. "42" deseni) tamamen kapalı/dokunulmamış bırakılabilir.

---

## 👥 Takım ve Proje Yönetimi

### Roller

**Sümeyye Doğan**
- Kruskal algoritmasının ve Union-Find veri yapısının yazımı (`kruskal/kruskal.py`)
- `PERFECT=True` modunun uçtan uca kurulması
- `config.txt` parse işlemleri (`parse/parse_config.py`) — zorunlu alan kontrolü, tip dönüşümü, sınır doğrulaması
- Repo'daki `config.txt` örneğinin hazırlanması
- `Makefile`'ın ilk yazımı

**Barış Sakallı**
- En kısa yol algoritmasının (BFS, `pathfinder/pathfinder.py`) tasarımı ve yazımı
- `Makefile` ve `.gitignore` üzerinde iyileştirmeler
- `README.md`'nin hazırlanması
- "42" deseninin labirente yerleştirilmesi (`fourty_two.py`)

**Ortak**
- `PERFECT=False` modunun (`generate_false.py`) — döngü ekleme ve çıkmaz sokak azaltma algoritması — birlikte tasarlanması ve yazılması

### Planlama Süreci

Proje, subject'in Chapter III–VIII'inde sıralanan zorunlu adımlar takip edilerek aşamalı şekilde ilerledi: önce config parse + temel Kruskal üretimi (mandatory çekirdek), ardından en kısa yol algoritması, sonra "42" deseni ve `PERFECT=False` modu, en son da terminal menüsü ve görsel iyileştirmeler. İlerledikçe iki kişinin ayrı yazdığı modüller birleştirilirken koordinat sistemi (grid'in `(satır, sütun)` mi yoksa config'in `(x, y)` mi kullandığı) konusunda birkaç kez uyumsuzluk çıktı; bunlar test edilerek tek tek bulunup düzeltildi.

### Neler İyi Gitti / Neler Geliştirilebilir

İyi giden: Kruskal + Union-Find çekirdeği baştan sağlam kurulduğu için üzerine `PERFECT=False` ve "42" deseni gibi katmanları eklemek nispeten kolay oldu; `pathfinder` ve `kruskal` modüllerinin bağımsız/yeniden kullanılabilir yazılması entegrasyonu basitleştirdi.

Geliştirilebilir: Farklı modüllerde koordinatların bazen `(x, y)`, bazen `(row, col)` olarak tutulması entegrasyon sırasında birkaç bug'a yol açtı — ileride tek bir konvansiyonun proje genelinde (belki tip takma adlarıyla) daha baştan netleştirilmesi zaman kazandırırdı. Ayrıca `flake8`/`mypy` denetimlerinin her modülde en başından itibaren (yalnızca sona bırakılmadan) çalıştırılması, stil ve tip hatalarının erken yakalanmasını sağlardı.

### Kullanılan Araçlar

- **Poetry** — bağımlılık ve sanal ortam yönetimi
- **flake8** ve **mypy** (`--disallow-untyped-defs --check-untyped-defs` bayraklarıyla) — kod kalitesi ve tip denetimi
- **Claude (Anthropic)** — bkz. aşağıdaki Resources bölümü

---

## 📚 Kaynaklar

- [Kruskal's Algorithm — Wikipedia](https://en.wikipedia.org/wiki/Kruskal%27s_algorithm)
- [Disjoint-Set / Union-Find veri yapısı — Wikipedia](https://en.wikipedia.org/wiki/Disjoint-set_data_structure)
- [Breadth-First Search — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Maze generation algorithms — genel karşılaştırma](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [PEP 257 — Docstring Conventions](https://peps.python.org/pep-0257/)
- [flake8 dokümantasyonu](https://flake8.pycqa.org/)
- [mypy dokümantasyonu](https://mypy.readthedocs.io/)

### Yapay Zeka Kullanımı

- Kod incelemesi: projenin subject'e (bu README'nin ilham aldığı PDF) uygunluğunun bölüm bölüm kontrol edilmesi, ve tespit edilen bug'ların (koordinat sistemi uyuşmazlıkları, eksik tip belirteçleri, stil hataları) düzeltilmesi.
- `flake8`/`mypy` hatalarının giderilmesi ve `Makefile`'ın tüm projeyi (`flake8 .`) taraması için düzeltilmesi.

Tüm kod, üretilmeden önce takım üyeleri tarafından okunup anlaşıldı; yapay zeka bir kod kontrol aracı olarak kullanıldı, tasarım kararları (algoritma seçimi, veri yapıları) takım tarafından alındı.
