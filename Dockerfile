FROM python:3.11-slim

# Install dependencies
RUN apt-get update && apt-get install -y \
    libevdev2 \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements & install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy script
COPY presensi.py .

# Buat folder logs
RUN mkdir /logs

# Jalankan script
CMD ["python", "presensi.py"]
