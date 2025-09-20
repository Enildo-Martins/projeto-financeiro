# extrator/services.py

import os
import fitz  # PyMuPDF
import google.generativeai as genai
import json
from dotenv import load_dotenv

load_dotenv()

def extrair_dados_nota_fiscal(pdf_stream):
    try:
        pdf_document = fitz.open(stream=pdf_stream, filetype="pdf")
        pdf_text = ""
        for page in pdf_document:
            pdf_text += page.get_text()
        
        if not pdf_text.strip():
            raise Exception("Não foi possível extrair texto do PDF. O arquivo pode estar vazio ou ser uma imagem.")

        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("A chave da API do Gemini não foi encontrada.")
        
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-1.5-flash-latest')

        # --- PROMPT DE MÁXIMA PRECISÃO ---
        prompt = f"""
            Sua tarefa é atuar como um sistema de OCR e extração de dados de alta precisão, especializado em DANFEs (Documento Auxiliar da Nota Fiscal Eletrônica) do Brasil. Você deve analisar o texto fornecido e preencher a estrutura JSON abaixo com exatidão absoluta, sem erros, omissões ou trocas de informação.

            A ESTRUTURA FINAL DEVE SER EXATAMENTE ESTA:
            {{
              "identificacao": {{"numero": "string", "serie": "string", "data_emissao": "string (YYYY-MM-DD)", "data_saida_entrada": "string (YYYY-MM-DD)", "natureza_operacao": "string"}},
              "emitente": {{"nome_razao_social": "string", "cnpj": "string", "inscricao_estadual": "string", "endereco_completo": "string"}},
              "destinatario": {{"nome_razao_social": "string", "cpf_cnpj": "string", "inscricao_estadual": "string", "endereco_completo": "string"}},
              "produtos": [{{"codigo": "string", "descricao": "string", "ncm": "string", "cfop": "string", "unidade": "string", "quantidade": "float", "valor_unitario": "float", "valor_total": "float"}}],
              "totais": {{"base_calculo_icms": "float", "valor_icms": "float", "valor_frete": "float", "valor_seguro": "float", "desconto": "float", "outras_despesas": "float", "valor_total_produtos": "float", "valor_total_nota": "float"}},
              "fatura_duplicatas": [{{"numero_fatura": "string", "data_vencimento": "string (YYYY-MM-DD)", "valor": "float"}}],
              "transporte": {{"modalidade_frete": "string", "transportadora_nome": "string", "transportadora_cnpj_cpf": "string", "placa_veiculo": "string"}},
              "classificacao_despesa": "string"
            }}

            GUIA DE EXTRAÇÃO DETALHADO POR SEÇÃO:

            1.  **Seção 'emitente'**:
                -   Localize a caixa no topo do documento com o título "IDENTIFICAÇÃO DO EMITENTE".
                -   TODOS os dados desta seção JSON (`nome_razao_social`, `cnpj`, `inscricao_estadual`, `endereco_completo`) devem ser extraídos EXCLUSIVAMENTE de dentro desta caixa.
                -   O CNPJ do emitente está nesta caixa.
                -   A Inscrição Estadual do emitente está nesta caixa.

            2.  **Seção 'destinatario'**:
                -   Localize a caixa com o título "DESTINATARIO/REMETENTE".
                -   TODOS os dados desta seção JSON (`nome_razao_social`, `cpf_cnpj`, `endereco_completo`) devem ser extraídos EXCLUSIVAMENTE de dentro desta caixa.
                -   O `nome_razao_social` do destinatário geralmente está em uma linha própria, abaixo do rótulo.
                -   O CPF ou CNPJ do destinatário está nesta caixa.

            3.  **Seção 'produtos'**:
                -   Localize a tabela com o título "DADOS DOS PRODUTOS/SERVIÇOS".
                -   Para cada linha da tabela, crie um objeto JSON.
                -   O campo `codigo` deve ser extraído da coluna "CÓDIGO". Transcreva-o com precisão absoluta. A letra 'O' é diferente do número '0'. Exemplo: 'BODKG5CTR9' é o correto.
                -   Extraia as outras colunas (`NCM/SH`, `CFOP`, `UNID`, `QUANT`, `VALOR UNITÁRIO`, `VALOR TOTAL`) para os campos correspondentes.

            4.  **Seção 'fatura_duplicatas'**:
                -   Localize a caixa "FATURA/DUPLICATA". Se estiver vazia, retorne uma lista vazia `[]`.

            5.  **Regra de Verificação Final (MUITO IMPORTANTE)**:
                -   Antes de finalizar, verifique: O CNPJ em `emitente.cnpj` pertence ao EMITENTE? O CPF/CNPJ em `destinatario.cpf_cnpj` pertence ao DESTINATÁRIO? A Inscrição Estadual em `emitente.inscricao_estadual` pertence ao EMITENTE? É CRÍTICO que esses valores não estejam trocados entre as seções.

            6.  **Regra de Classificação de Despesa**:
                -   Classifique a despesa com base nos produtos em uma das categorias: INSUMOS AGRÍCOLAS, MANUTENÇÃO E OPERAÇÃO, INFRAESTRUTURA E UTILIDADES, DESPESAS GERAIS E ADMINISTRATIVAS, INVESTIMENTOS (apenas máquinas, veículos, imóveis).

            Analise o texto a seguir com o máximo de atenção e detalhe, seguindo o guia acima, e retorne APENAS o JSON perfeito e validado.

            --- TEXTO DA NOTA FISCAL ---
            {pdf_text}
            --- FIM DO TEXTO ---
        """

        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '').strip()
        
        return json.loads(cleaned_response)

    except Exception as e:
        raise Exception(f"Erro no serviço de extração: {e}")