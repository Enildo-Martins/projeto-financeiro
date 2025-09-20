# extrator/views.py

from django.shortcuts import render
from .services import extrair_dados_nota_fiscal
import json # Importe a biblioteca JSON

def upload_file(request):
    context = {}

    if request.method == 'POST':
        pdf_file = request.FILES.get('pdf_file')

        if not pdf_file or not pdf_file.name.endswith('.pdf'):
            context['error_message'] = "Erro: Por favor, envie um arquivo no formato PDF."
            return render(request, 'extrator/upload.html', context)
        
        try:
            dados_extraidos_dict = extrair_dados_nota_fiscal(pdf_file.read())
            
            # --- AJUSTE AQUI ---
            # Converte o dicionário para uma string JSON formatada para exibição
            # indent=4 cria a indentação bonita
            # ensure_ascii=False garante que caracteres como 'ç' e acentos apareçam corretamente
            context['extracted_data_json'] = json.dumps(
                dados_extraidos_dict, indent=4, ensure_ascii=False
            )
            
        except Exception as e:
            context['error_message'] = str(e)

    return render(request, 'extrator/upload.html', context)