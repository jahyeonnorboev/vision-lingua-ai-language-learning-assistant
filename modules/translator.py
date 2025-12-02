import torch
from deep_translator import GoogleTranslator
from transformers import MarianMTModel, MarianTokenizer

class TranslationEngine:
    def __init__(self):
        """🔸 Tarjima tizimini ishga tushurish"""
        self.marian_models = {}
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def load_marian_model(self, src_lang, tgt_lang):
        """🪄 MarianMT modelini yuklash"""
        model_name = f"Helsinki-NLP/opus-mt-{src_lang}-{tgt_lang}"
        key = f"{src_lang}-{tgt_lang}"

        if key not in self.marian_models:
            try:
                tokenizer = MarianTokenizer.from_pretrained(model_name)
                model = MarianMTModel.from_pretrained(model_name).to(self.device)
                self.marian_models[key] = {
                    'tokenizer': tokenizer,
                    'model': model
                }
                print(f"[✅] MarianMT modeli yuklandi: {model_name}")
            except Exception as e:
                print(f"[❌] MarianMT modelini yuklashda xatolik: {e}")
                return None

        return self.marian_models[key]

    def translate_with_marian(self, text, src_lang='en', tgt_lang='ko'):
        """🪄 MarianMT yordamida tarjima"""
        try:
            model_data = self.load_marian_model(src_lang, tgt_lang)
            if not model_data:
                return None

            tokenizer = model_data['tokenizer']
            model = model_data['model']

            inputs = tokenizer(text, return_tensors="pt", padding=True).to(self.device)
            translated = model.generate(**inputs)
            result = tokenizer.decode(translated[0], skip_special_tokens=True)
            return result

        except Exception as e:
            print(f"[❌] MarianMT tarjima xatosi: {e}")
            return None

    def translate_with_google(self, text, src='en', dest='ko'):
        """🌐 Google Translate (deep-translator)"""
        try:
            if not text or not text.strip():
                return ""
            translated_text = GoogleTranslator(source=src, target=dest).translate(text)
            return translated_text
        except Exception as e:
            print(f"[❌] Google tarjima xatosi: {e}")
            return None

    def translate(self, text, src_lang='en', tgt_lang='ko', method='google'):
        """🔹 Umumiy tarjima funksiyasi"""
        if not text or not text.strip():
            return ""

        if method == 'marian':
            result = self.translate_with_marian(text, src_lang, tgt_lang)
            if result:
                return result
            print("[⚠️] MarianMT ishlamadi, Google Translatega o‘tilmoqda...")

        return self.translate_with_google(text, src=src_lang, dest=tgt_lang)

    def batch_translate(self, texts, src_lang='en', tgt_lang='ko', method='google'):
        """📝 Bir nechta matnlarni ketma-ket tarjima qilish"""
        results = []
        for text in texts:
            translated = self.translate(text, src_lang, tgt_lang, method)
            results.append(translated)
        return results
