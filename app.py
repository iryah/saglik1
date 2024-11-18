from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)

class AIAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
  def get_prompt(self, service_type, user_input):
    prompts = {
        'symptom_analysis': f"""
            Bir doktor asistanı olarak aşağıdaki semptomları değerlendir:
            
            SEMPTOMLAR: {user_input}
            
            Lütfen şu başlıklar altında analiz yap:
            
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
        """,
        
        'medical_research': f"""
            Bir sağlık araştırmacısı olarak şu konuyu incele:
            
            KONU: {user_input}
            
            # GÜNCEL BİLGİLER
            [Konu hakkında güncel bilgiler]
            
            # BİLİMSEL VERİLER
            [Araştırma sonuçları]
            
            # TEDAVİ YÖNTEMLERİ
            [Mevcut tedavi yaklaşımları]
            
            # YENİ GELİŞMELER
            [Alandaki son gelişmeler]
        """,
        
        'health_tips': f"""
            Bir sağlık danışmanı olarak şu konuda öneriler sun:
            
            KONU: {user_input}
            
            # GENEL BİLGİLER
            [Konu hakkında temel bilgiler]
            
            # SAĞLIKLI YAŞAM ÖNERİLERİ
            * Günlük alışkanlıklar
            * Egzersiz önerileri
            * Beslenme tavsiyeleri
            
            # KORUYUCU ÖNLEMLER
            [Hastalıklardan korunma yöntemleri]
            
            # YAŞAM KALİTESİ
            [Yaşam kalitesini artırıcı öneriler]
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
                'response': str(response.content) if response.content else "Yanıt alınamadı."
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
        
        service_type = data.get('service_type')
        user_input = data.get('input')
        
        if not service_type or not user_input:
            return jsonify({'success': False, 'error': 'Eksik parametre'})
            
        assistant = AIAssistant()
        result = assistant.generate_response(service_type, user_input)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
