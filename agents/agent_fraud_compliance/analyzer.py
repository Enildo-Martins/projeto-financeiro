import os
import json
import google.generativeai as genai
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

class AgentFraudCompliance:

    def __init__(self, extracted_data, api_key=None):
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")
        
        if not self.api_key:
            print("Aviso: API Key do Gemini não fornecida para o Analista de Risco.")

        self.data = extracted_data

    def analisar(self):
        if not self.api_key:
            raise ValueError("Chave da API do Gemini não configurada. Por favor, insira sua chave nas configurações.")

        genai.configure(api_key=self.api_key)
        
        model = genai.GenerativeModel(
            'gemini-2.5-flash', 
            generation_config={"response_mime_type": "application/json"}
        )

        hoje = datetime.now().strftime("%Y-%m-%d")

        system_prompt = f"""
            Você é um analista de risco financeiro sênior, especializado em detectar fraudes em notas fiscais.
            
            CONTEXTO TEMPORAL (CRÍTICO):
            - A data de hoje é: {hoje}
            - Use esta data como referência ABSOLUTA para verificar se a nota é futura ou passada.
            - Uma nota emitida em 2025-09-19 NÃO É FUTURA se hoje for {hoje} (novembro/2025).
            
            TAREFA:
            Analise os dados extraídos da nota fiscal abaixo e gere um parecer técnico em formato JSON.
            
            DADOS DA NOTA:
            {json.dumps(self.data, indent=2, ensure_ascii=False)}

            CRITÉRIOS DE ANÁLISE:
            1. Validade Temporal: Compare a 'data_emissao' da nota com a data de hoje ({hoje}). Só considere 'data futura' se a emissão for MAIOR que hoje.
            2. Inconsistência de Categorias: Verifique se os produtos condizem com a categoria da despesa.
            3. Análise de Preços: Compare mentalmente com valores de mercado.
            4. Padrões Suspeitos: Valores redondos excessivos, fornecedor incompatível.

            FORMATO DE SAÍDA OBRIGATÓRIO (JSON):
            {{
              "risk_score": <int, 0 a 10, onde 10 é risco altíssimo>,
              "summary": "<string, resumo curto e direto da análise>",
              "red_flags": [
                {{
                  "type": "<string, ex: 'SOBREPREÇO', 'INCONSISTÊNCIA', 'DATA FUTURA', 'FORNECEDOR SUSPEITO'>",
                  "description": "<string, explicação do alerta>"
                }}
              ]
            }}
        """

        try:
            response = model.generate_content(system_prompt)
            return json.loads(response.text)
        except Exception as e:
            return {
                "risk_score": 0,
                "summary": f"Erro na análise automática: {str(e)}",
                "red_flags": []
            }