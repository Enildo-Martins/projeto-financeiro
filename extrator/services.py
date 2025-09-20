import os
import fitz  
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

        prompt = f"""
            Você é um assistente de IA especialista em extrair e interpretar dados de notas fiscais brasileiras. Sua tarefa mais importante é extrair os campos solicitados e, crucialmente, classificar a despesa.

            A ESTRUTURA FINAL DO JSON DEVE SER EXATAMENTE ESTA:
            {{
              "fornecedor": {{ "razao_social": "string", "fantasia": "string", "cnpj": "string" }},
              "faturado": {{ "nome_completo": "string", "cpf": "string" }},
              "numero_nota_fiscal": "string",
              "data_emissao": "string (no formato YYYY-MM-DD)",
              "descricao_produtos": ["string"],
              "parcelas": [{{ "data_vencimento": "string (no formato YYYY-MM-DD)", "valor_total": "float" }}],
              "classificacao_despesa": "string"
            }}

            REGRAS CRÍTICAS DE EXECUÇÃO:

            1.  **CLASSIFICAÇÃO DE DESPESA (TAREFA PRIORITÁRIA)**:
                -   Esta é a tarefa mais importante. O campo 'classificacao_despesa' NÃO PODE ser nulo.
                -   Analise a 'descricao_produtos' e escolha UMA das categorias da lista abaixo.
                -   Se um item não se encaixar perfeitamente em categorias industriais ou agrícolas (como uma raquete, material de escritório, etc.), classifique-o como 'ADMINISTRATIVAS'.

            2.  **NOME DO FATURADO (EXTRAÇÃO OBRIGATÓRIA)**:
                -   O campo 'faturado.nome_completo' é obrigatório.
                -   Em muitos DANFEs, o nome do destinatário aparece em uma linha sozinho, logo abaixo do rótulo "NOME RAZÃO SOCIAL". Procure atentamente por este padrão.

            3.  **DEMAIS REGRAS**:
                -   Preencha todos os outros campos da estrutura. Se 'fantasia' ou 'cpf' não existirem, use `null`.
                -   'parcelas' deve ser uma lista de objetos. Use o VALOR TOTAL DA NOTA para o campo 'valor_total'.

            LISTA DE CATEGORIAS DE DESPESAS PARA CLASSIFICAÇÃO:
            - **INSUMOS AGRÍCOLAS**: Sementes, Fertilizantes, Defensivos Agrícolas.
            - **MANUTENÇÃO E OPERAÇÃO**: Combustíveis, Lubrificantes, Peças, Ferramentas.
            - **RECURSOS HUMANOS**: Mão de Obra Temporária, Salários.
            - **SERVIÇOS OPERACIONAIS**: Frete, Transporte, Colheita Terceirizada.
            - **INFRAESTRUTURA E UTILIDADES**: Energia Elétrica, Materiais de Construção.
            - **ADMINISTRATIVAS**: Honorários, Despesas Bancárias, e outros itens de consumo ou escritório.
            - **SEGUROS E PROTEÇÃO**: Seguro Agrícola, Seguro de Ativos.
            - **IMPOSTOS E TAXAS**: ITR, IPTU, IPVA.
            - **INVESTIMENTOS**: Aquisição de Máquinas, Veículos, Imóveis.

            Analise o texto a seguir, siga as regras CRÍTICAS e retorne APENAS o JSON completo e correto.

            --- TEXTO DA NOTA FISCAL ---
            {pdf_text}
            --- FIM DO TEXTO ---
        """

        response = model.generate_content(prompt)
        cleaned_response = response.text.strip().replace('```json', '').replace('```', '').strip()
        
        return json.loads(cleaned_response)

    except Exception as e:
        raise Exception(f"Erro no serviço de extração: {e}")