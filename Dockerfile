# Stage 1: Builder (Untuk kompilasi)
FROM python:3.11-slim as builder

# Instal tools kompilasi dan header files yang dibutuhkan evdev
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    linux-libc-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

# Build wheels untuk semua dependencies (termasuk evdev)
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt


# Stage 2: Final (Image yang akan dijalankan di Orange Pi)
FROM python:3.11-slim

# Tetap butuh libevdev2 untuk runtime
RUN apt-get update && apt-get install -y \
    libevdev2 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Ambil hasil kompilasi dari stage builder
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .

# Instal dari hasil kompilasi tadi (tanpa perlu kompilasi ulang)
RUN pip install --no-cache-dir /wheels/*

# Copy script presensi Anda
COPY presensi.py .

# Buat folder logs
RUN mkdir -p /logs

# Jalankan script
CMD ["python", "presensi.py"]
