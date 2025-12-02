#!/bin/bash

# ===============================
# VisionLingua macOS Setup Script
# ===============================

# 1️⃣ Virtual muhit yaratish
echo "✅ Virtual muhit yaratilyapti..."
python3 -m venv venv

# 2️⃣ Virtual muhitni faollashtirish
source venv/bin/activate

# 3️⃣ Python paketlarini o'rnatish
echo "✅ Python paketlari o'rnatilyapti..."
pip install --upgrade pip
pip install -r requirements.txt
pip install deep-translator
pip install spacy
pip install konlpy
pip install pytesseract opencv-python pillow

# 4️⃣ spaCy ingliz modelini yuklash
echo "✅ spaCy ingliz modeli yuklanyapti..."
python -m spacy download en_core_web_sm

# 5️⃣ Homebrew orqali Tesseract OCR o'rnatish
if ! command -v brew &> /dev/null
then
    echo "Homebrew topilmadi, o'rnatilyapti..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

echo "✅ Tesseract OCR o'rnatilyapti..."
brew install tesseract
brew install tesseract-lang

# 6️⃣ Java JDK (KoNLPy uchun)
echo "✅ Java JDK o'rnatilyapti..."
brew install openjdk
echo 'export PATH="/opt/homebrew/opt/openjdk/bin:$PATH"' >> ~/.zprofile
source ~/.zprofile

# 7️⃣ Tesseract va Java tekshirish
echo "Tesseract versiyasi:"
tesseract --version

echo "Java versiyasi:"
java -version

echo "✅ VisionLingua dependencies tayyor!"
