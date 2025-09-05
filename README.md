```markdown
# Presensi Scanner (QR HID + IoT)

Proyek ini adalah daemon Python berbasis Docker untuk membaca **QR Scanner USB (mode HID/keyboard)** di perangkat Orange Pi (Ubuntu console).  
Setiap kali QR code discan, hasilnya otomatis dikirim ke endpoint API kehadiran (CityNet).

---

## 🚀 Fitur
- Baca input langsung dari device `/dev/input/eventX`
- Kirim data ke API endpoint dengan format:
```

GET [https://dev.zeneight.xyz/absensi-be/absensi/siswa/{id}](https://dev.zeneight.xyz/absensi-be/absensi/siswa/{id})

````
- Logging ke file dengan timestamp (`./logs/presensi.log`)
- Otomatis jalan saat boot (via `docker-compose restart:always`)

---

## 📦 Persiapan

1. **Pastikan scanner terdeteksi**
 ```bash
 lsusb
 ls /dev/input/
````

Gunakan `evtest` untuk mengetahui event number:

```bash
sudo apt install -y evtest
sudo evtest
```

Saat scan QR, akan terlihat output `KEY_1, KEY_2, ...` → catat device event (misal `/dev/input/event0`).

2. **Install Docker & Docker Compose**

   ```bash
   sudo apt update
   sudo apt install -y docker.io docker-compose
   sudo systemctl enable docker
   sudo systemctl start docker
   ```

---

## ⚙️ Konfigurasi

### 1. Clone Repository

```bash
git clone https://github.com/username/presensi-scanner.git
cd presensi-scanner
```

### 2. Sesuaikan device scanner

Edit `docker-compose.yml`:

```yaml
devices:
  - "/dev/input/event0:/dev/input/event0"
```

Ganti `event0` sesuai device scanner kamu.

---

## ▶️ Jalankan

### Build image

```bash
docker-compose build
```

### Start service

```bash
docker-compose up -d
```

### Cek log

```bash
docker-compose logs -f
```

Log juga tersimpan di file:

```
./logs/presensi.log
```

---

## 🔧 Debugging

Jika scanner tidak terbaca:

* Cek `ls /dev/input/` setelah colok scanner
* Gunakan `evtest` untuk pastikan event number benar
* Pastikan sudah mapping device yang tepat di `docker-compose.yml`

---

## 📂 Struktur Repo

```
presensi-scanner/
├── Dockerfile
├── docker-compose.yml
├── presensi.py
├── requirements.txt
├── logs/                # auto generated log
└── README.md
```

---

## 📜 Lisensi

MIT License © 2025

```

---

👉 Dengan README ini, repo kamu sudah **self-documented**.  
Siapa pun yang clone repo bisa langsung jalanin di Orange Pi cukup dengan `docker-compose up -d`.  

Mau saya sekalian bikinkan **contoh isi `logs/presensi.log`** (sample output hasil scan + response API) biar lebih jelas dokumentasinya?
```
