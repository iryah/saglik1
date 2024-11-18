class AIAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
class AIAssistant:
    def __init__(self):
        self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
    
    def format_response(self, response):
        # Content Block ve diğer gereksiz metinleri temizle
        text = response
        if "ContentBlock(text=" in text:
            text = text.split("ContentBlock(text=")[1]
            text = text.rsplit(", type='text')", 1)[0]
            text = text.strip('"')
            text = text.strip("'")
        
        # Escape karakterlerini düzgün boşluklara çevir
        text = text.replace("\\n", "\n")
        text = text.replace("\\t", "    ")
        
        # Başlıkları düzenle
        lines = text.split("\n")
        formatted_lines = []
        
        for line in lines:
            # Başlıkları vurgula
            if line.isupper() or (line.strip() and line.strip()[0] == '#'):
                formatted_lines.extend(["", "### " + line.strip('# '), ""])
            # Liste öğelerini düzenle
            elif line.strip().startswith('*'):
                formatted_lines.append(line)
            # Normal metni ekle
            elif line.strip():
                formatted_lines.append(line)
        
        # Fazla boş satırları temizle ve metni birleştir
        final_text = "\n".join(formatted_lines)
        final_text = "\n".join(line for line, _ in itertools.groupby(final_text.splitlines()))
        
        return final_text
        
        return cleaned_text

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
