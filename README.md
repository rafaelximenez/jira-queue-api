# Cloud Function: Salvar JSON no Cloud Storage a partir de Planilha Google

Este projeto contém uma Cloud Function em Python que recebe dados em formato JSON via requisição HTTP POST e os salva em um arquivo no Google Cloud Storage.  A função é projetada para ser integrada com um script do Google Apps Script em uma Planilha Google, que envia os dados da planilha para a Cloud Function.

## Funcionalidades

*   **Recebimento de Dados:** Recebe dados em formato JSON via requisição HTTP POST.
*   **Validação da Requisição:** Verifica se o método da requisição é POST e se o conteúdo é JSON válido.
*   **Configuração Flexível:** Permite configurar o nome do bucket e da pasta (opcional) no Cloud Storage.
*   **Nomes de Arquivo Únicos:** Gera nomes de arquivo únicos usando timestamps, evitando sobrescritas.
*   **Upload para o Cloud Storage:** Salva os dados JSON em um arquivo no Cloud Storage.
*   **Tratamento de Erros:** Captura e registra erros, retornando uma resposta de erro apropriada.
*   **Resposta Detalhada:** Retorna uma mensagem de sucesso com o caminho completo do arquivo salvo ou uma mensagem de erro detalhada.

## Pré-requisitos

*   **Conta do Google Cloud:** Você precisa de uma conta do Google Cloud com um projeto ativo.
*   **Bucket do Cloud Storage:** Crie um bucket no Cloud Storage onde os arquivos serão salvos.  Anote o nome do bucket.
*   **API do Cloud Storage:** Certifique-se de que a API do Cloud Storage esteja habilitada no seu projeto do Google Cloud.
*   **SDK do Google Cloud (gcloud CLI):**  É recomendado instalar e configurar o SDK do Google Cloud (gcloud CLI) para facilitar a implantação da Cloud Function.  [https://cloud.google.com/sdk/docs/install](https://cloud.google.com/sdk/docs/install)
* **Conta de serviço:** Uma conta de serviço com as permissões adequadas.

## Estrutura do Projeto

```
cloud-function-salvar-json/
├── main.py       # Código principal da Cloud Function (Python)
└── requirements.txt  # Dependências da Cloud Function
```