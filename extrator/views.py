from django.shortcuts import render
import json
from agents.agent_extrator.processador_pdf import AgentExtrator

def upload_file(request):
    context = {}

    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')

        if not pdf_file or not pdf_file.name.endswith('.pdf'):
            context['error_message'] = "Erro: Por favor, envie um arquivo no formato PDF."
            return render(request, 'extrator/upload.html', context)
        
        try:
            # 1. Instancia o agente
            agente_extrator = AgentExtrator()
            
            # 2. Executa a ação do agente
            dados_extraidos_dict = agente_extrator.executar(pdf_file.read())
            
            # Formata o JSON para exibição
            context['extracted_data_json'] = json.dumps(
                dados_extraidos_dict, indent=4, ensure_ascii=False
            )
            
        except Exception as e:
            context['error_message'] = str(e)

    return render(request, 'extrator/upload.html', context)