from django.shortcuts import render
from .services import extrair_dados_nota_fiscal
import json 

def upload_file(request):
    context = {}

    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')

        if not pdf_file or not pdf_file.name.endswith('.pdf'):
            context['error_message'] = "Erro: Por favor, envie um arquivo no formato PDF."
            return render(request, 'extrator/upload.html', context)
        
        try:
            dados_extraidos_dict = extrair_dados_nota_fiscal(pdf_file.read())
            
            context['extracted_data_json'] = json.dumps(
                dados_extraidos_dict, indent=4, ensure_ascii=False
            )
            
        except Exception as e:
            context['error_message'] = str(e)

    return render(request, 'extrator/upload.html', context)