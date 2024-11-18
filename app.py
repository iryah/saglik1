from flask import Flask, render_template, request, jsonify
from anthropic import Anthropic
import os

app = Flask(__name__)

class AIHealthAssistant:
   def __init__(self):
       self.client = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
       self.current_step = 'initial'
       self.answers = {}

   def get_next_question(self):
       questions = {
           'initial': {
               'message': "Şikayetinizi kısaca anlatır mısınız?",
               'next': 'duration'
           },
           'duration': {
               'message': "Bu şikayetler ne zamandır devam ediyor? (gün/hafta/ay)",
               'next': 'severity'
           },
           'severity': {
               'message': "Şikayetlerinizin şiddeti 1-10 arasında nedir?",
               'next': 'timing'
           },
           'timing': {
               'message': "Belirli bir zamanda/durumda artış/azalma oluyor mu?",
               'next': 'medical_history'
           },
           'medical_history': {
               'message': "Geçmiş hastalıklarınız veya sürekli kullandığınız ilaçlar var mı?",
               'next': 'lifestyle'
           },
           'lifestyle': {
               'message': "Sigara/alkol kullanımı, düzenli egzersiz yapıyor musunuz?",
               'next': 'analyze'
           }
       }
       return questions.get(self.current_step, {'message': 'Analiz tamamlandı'})

   def process_answer(self, answer):
       self.answers[self.current_step] = answer
       
       if self.current_step == 'lifestyle':
           return self.analyze_symptoms()
       
       question = self.get_next_question()
       self.current_step = question.get('next', 'analyze')
       return {
           'success': True,
           'question': question['message'],
           'is_final': self.current_step == 'analyze'
       }

   def analyze_symptoms(self):
       prompt = f"""
       Hastanın verdiği bilgiler:
       Şikayet: {self.answers.get('initial')}
       Süre: {self.answers.get('duration')}
       Şiddet: {self.answers.get('severity')}
       Zamanlama: {self.answers.get('timing')}
       Tıbbi Geçmiş: {self.answers.get('medical_history')}
       Yaşam Tarzı: {self.answers.get('lifestyle')}

       # DURUM DEĞERLENDİRMESİ
       [Semptomların detaylı analizi]

       # OLASI NEDENLER
       [Göz önünde bulundurulması gereken durumlar]

       # ÖNERİLER
       * Yapılması gerekenler
       * Dikkat edilmesi gerekenler

       # ACİLİYET DURUMU
       [Hastaneye gitme gerekliliği]
       """

       try:
           response = self.client.messages.create(
               model="claude-3-sonnet-20240229",
               messages=[{"role": "user", "content": prompt}],
               max_tokens=4000
           )
           return {
               'success': True,
               'response': self.format_response(str(response.content)),
               'is_final': True
           }
       except Exception as e:
           return {
               'success': False,
               'error': str(e)
           }

   def format_response(self, response):
       text = response
       if "ContentBlock(text=" in text:
           text = text.split("ContentBlock(text=")[1]
           text = text.rsplit(", type='text')", 1)[0]
           text = text.strip('"').strip("'")
       
       text = text.replace("\\n", "\n")
       
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
               current_section["title"] = line.lstrip("#").strip()
           else:
               if line.startswith('*'):
                   line = f"• {line.strip('* ')}"
               current_section["content"].append(line)
       
       if current_section["title"]:
           sections.append(current_section)
       
       html = '<div class="space-y-4">'
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

@app.route('/api/ask', methods=['POST'])
def ask():
   data = request.get_json()
   answer = data.get('answer')
   
   if not hasattr(app, 'health_assistant'):
       app.health_assistant = AIHealthAssistant()
   
   result = app.health_assistant.process_answer(answer)
   return jsonify(result)

@app.route('/')
def home():
   return render_template('index.html')

if __name__ == '__main__':
   app.run(debug=True)
