class AIAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
class AIAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
 def format_response(self, response):
    # Gereksiz metinleri temizle
    text = response
    if "ContentBlock(text=" in text:
        text = text.split("ContentBlock(text=")[1]
        text = text.rsplit(", type='text')", 1)[0]
        text = text.strip('"').strip("'")
    
    # HTML tablo formatına dönüştür
    html = """
    <div class="overflow-x-auto">
        <table class="min-w-full bg-white rounded-lg overflow-hidden">
            <thead class="bg-blue-600 text-white">
                <tr>
                    <th class="px-4 py-2 text-left">Başlık</th>
                    <th class="px-4 py-2 text-left">Detay</th>
                </tr>
            </thead>
            <tbody>
    """
    
    current_title = ""
    current_content = []
    
    lines = text.split("\\n")
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            # Önceki başlığı ekle
            if current_title and current_content:
                content_html = "<br>".join(current_content)
                html += f"""
                <tr class="border-b">
                    <td class="px-4 py-2 font-semibold bg-gray-50">{current_title}</td>
                    <td class="px-4 py-2">{content_html}</td>
                </tr>
                """
            current_title = line.strip('# ')
            current_content = []
        elif line.strip():
            if line.startswith('*'):
                current_content.append(f"• {line.strip('* ')}")
            else:
                current_content.append(line)
    
    # Son başlığı ekle
    if current_title and current_content:
        content_html = "<br>".join(current_content)
        html += f"""
        <tr class="border-b">
            <td class="px-4 py-2 font-semibold bg-gray-50">{current_title}</td>
            <td class="px-4 py-2">{content_html}</td>
        </tr>
        """
    
    html += """
            </tbody>
        </table>
    </div>
    """
    
    return html

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
            
            # Yanıtı formatla
            formatted_response = self.format_response(str(response.content))
            
            return {
                'success': True,
                'response': formatted_response
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
