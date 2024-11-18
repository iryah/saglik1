from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os
import re

app = Flask(__name__)

class AIAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def format_response(self, response):
    # Temizleme işlemi
    text = response
    if "ContentBlock(text=" in text:
        text = text.split("ContentBlock(text=")[1]
        text = text.rsplit(", type='text')", 1)[0]
        text = text.strip('"').strip("'")
    
    text = text.replace("\\n", "\n")
    
    # Kartlı görünüm oluştur
    html = '<div class="space-y-4">'  # Kartlar arası boşluk
    
    sections = []
    current_section = {"title": "", "content": []}
    
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
            
        if line.startswith('#') or line.isupper():
            if current_section["title"]:
                sections.append(current_section)
                current_section = {"title": "", "content": []}
            current_section["title"] = line.strip('# ')
        else:
            if line.startswith('*'):
                line = f"• {line.strip('* ')}"
            current_section["content"].append(line)
    
    if current_section["title"]:
        sections.append(current_section)
    
    # Her bölüm için kart oluştur
    for section in sections:
        html += f"""
            <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
                <div class="text-lg font-bold text-blue-600 mb-3">
                    {section["title"]}
                </div>
                <div class="text-gray-700 space-y-2">
                    {"<br>".join(f'<div class="ml-4">{line}</div>' for line in section["content"])}
                </div>
            </div>
        """
    
    html += '</div>'
    return html

    def get_prompt(self, service_type, user_input):
        prompts = {
            'symptom_analysis': f"""
                Bir doktor asistanı olarak aşağıdaki semptomları değerlendir:
                
                SEMPTOMLAR: {user_input}
                
                # İLK DEĞERLENDİRME
                [Semptomların detaylı analizi]
                
                # OLASI DURUMLAR
                [Göz önünde bulundurulması gereken durumlar]
                
                # ÖNERİLER
                * İlk yapılması gerekenler
                * Yaşam tarzı önerileri
                * Dikkat edilmesi gerekenler
                
                # ACİLİYET DURUMU
                [Durumun aciliyeti ve hastaneye gitme gerekliliği]
                
                # UZMAN YÖNLENDİRMESİ
                [Hangi uzmana başvurulmalı]
            """,
            'mental_health': f"""
                Bir psikolojik danışman olarak aşağıdaki durumu değerlendir:
                
                DURUM: {user_input}
                
                # DURUM ANALİZİ
                [Psikolojik durumun değerlendirmesi]
                
                # BAŞA ÇIKMA STRATEJİLERİ
                * Önerilen teknikler
                * Günlük uygulamalar
                * Yaşam tarzı değişiklikleri
                
                # PROFESYONEL DESTEK
                [Uzman desteği gerekli mi?]
                
                # SONRAKİ ADIMLAR
                [Atılması gereken adımlar]
            """,
            'nutrition': f"""
                Bir beslenme uzmanı olarak aşağıdaki durumu değerlendir:
                
                DURUM: {user_input}
                
                # BESLENME ANALİZİ
                [Mevcut durumun değerlendirmesi]
                
                # ÖNERİLER
                * Besin grupları
                * Öğün düzeni
                * Dikkat edilecekler
                
                # HEDEFLER
                [Beslenme hedefleri]
                
                # TAKİP PLANI
                [Önerilen takip süreci]
            """
        }
        return prompts.get(service_type, f"Sağlık danışmanı olarak şu konuyu değerlendir: {user_input}")

    def generate_response(self, service_type, user_input):
        try:
            prompt = self.get_prompt(service_type, user_input)
            response = self.client.messages.create(
                model="claude-3-sonnet-20240229",
                messages=[{
                    "role": "user", 
                    "content": prompt
                }],
                max_tokens=4000
            )
            return {
                'success': True,
                'response': self.format_response(str(response.content))
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/service', methods=['POST'])
def process_service():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'error': 'Veri bulunamadı'})
        
        assistant = AIAssistant()
        result = assistant.generate_response(
            data.get('service_type'),
            data.get('input')
        )
        
        return jsonify(result)
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
