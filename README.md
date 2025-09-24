# Extrator de Dados de Notas Fiscais com IA

Este projeto é uma aplicação web desenvolvida em Django que utiliza a Inteligência Artificial do Google Gemini para extrair informações de Notas Fiscais Eletrônicas (NF-e) em formato PDF. O sistema foi criado como parte de um projeto acadêmico de Gestão Financeira, com foco em automatizar a entrada de dados de contas a pagar.

## Funcionalidades

- **Upload de PDF:** Interface web simples para o usuário carregar um arquivo PDF de uma nota fiscal.
- **Extração com IA:** Utiliza a API do Google Gemini para ler o conteúdo do PDF e extrair os dados essenciais do documento.
- **Interpretação de Dados:** Além de extrair, a IA é instruída a interpretar os produtos da nota para classificar a despesa em categorias predefinidas (ex: MANUTENÇÃO E OPERAÇÃO, ADMINISTRATIVAS, etc.).
- **Visualização em JSON:** Exibe os dados extraídos em um formato JSON estruturado e de fácil leitura na própria tela.
- **Copiar JSON:** Funcionalidade para copiar os dados extraídos com um único clique, facilitando a integração com outros sistemas.

## Tecnologias Utilizadas

- **Backend:** Python 3, Django
- **Inteligência Artificial:** Google Gemini API (gemini-1.5-flash-latest)
- **Manipulação de PDF:** PyMuPDF (`fitz`)
- **Frontend:** HTML5, CSS3 (estilo contido no template)
- **Gerenciamento de Segredos:** `python-dotenv`

## Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto em um ambiente local.

### Pré-requisitos

- Python 3.10 ou superior
- `pip` (gerenciador de pacotes do Python)

### Passos para Instalação

1.  **Clone o repositório:**
    ```bash
    git clone [https://github.com/seu-usuario/seu-repositorio.git](https://github.com/seu-usuario/seu-repositorio.git)
    cd seu-repositorio
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    # Cria o ambiente virtual
    python -m venv venv

    # Ativa no Windows
    .\venv\Scripts\activate

    # Ativa no macOS/Linux
    source venv/bin/activate
    ```

3.  **Instale as dependências:**
    (Crie um arquivo `requirements.txt` na raiz do projeto com o conteúdo abaixo e execute o comando `pip install -r requirements.txt`)
    ```txt
    Django
    google-generativeai
    python-dotenv
    PyMuPDF
    ```
    Comando para instalar:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure as variáveis de ambiente:**
    - Copie o arquivo de exemplo `.env.example` para um novo arquivo chamado `.env`:
      ```bash
      # No Windows
      copy .env.example .env

      # No macOS/Linux
      cp .env.example .env
      ```
    - Abra o arquivo `.env` e insira sua chave da API do Google Gemini:
      ```
      GEMINI_API_KEY=SUA_CHAVE_API_AQUI
      ```

5.  **Execute as migrações do Django (opcional para este projeto, mas é uma boa prática):**
    ```bash
    python manage.py migrate
    ```

6.  **Inicie o servidor de desenvolvimento:**
    ```bash
    python manage.py runserver
    ```

A aplicação estará disponível em `http://127.0.0.1:8000/`.

## Como Usar

1.  Acesse `http://127.0.0.1:8000/` no seu navegador.
2.  Clique em "Escolher arquivo" e selecione um documento PDF de uma NF-e.
3.  Clique no botão "EXTRAIR DADOS".
4.  A página será recarregada e, se a extração for bem-sucedida, os dados aparecerão formatados em uma caixa de JSON.
5.  Caso ocorra algum erro durante o processo, uma mensagem de erro será exibida.

---