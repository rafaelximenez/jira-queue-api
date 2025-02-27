import functions_framework
from google.cloud import storage
import json
import datetime
import requests

@functions_framework.http
def salvar_e_enviar(request):
    """Recebe um JSON via POST, salva no Cloud Storage e envia para uma API externa.

    Args:
        request (flask.Request): O objeto de requisição HTTP, contendo o JSON no corpo.

    Returns:
        tuple: Uma tupla contendo:
            - Uma mensagem de sucesso ou erro (str).
            - O código de status HTTP (int).
            - (Opcional) Um dicionário de cabeçalhos adicionais (ex: {'Allow': 'POST'}).
    """

    if request.method != 'POST':
        return ('Method Not Allowed', 405, {'Allow': 'POST'})

    if not request.is_json:
        return ('Bad Request: Expecting JSON data', 400)

    request_json = request.get_json(silent=True)

    if not request_json:
        return ('Bad Request: Invalid JSON data', 400)

    print(f"Dados recebidos: {request_json}")

    try:
        bucket_name = 'suri-storage-files'
        folder_name = 'jira/issues'
        timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
        file_name = f'planilha_linha_{timestamp}.json'
        file_path = f'{folder_name}/{file_name}' if folder_name else file_name

        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)
        blob.upload_from_string(data=json.dumps(request_json), content_type='application/json')
        print(f"Arquivo salvo: gs://{bucket_name}/{file_path}")

    except Exception as e:
        print(f"Erro ao salvar no Cloud Storage: {e}")
        return (f'Erro ao salvar no Cloud Storage: {e}', 500)

    try:
        api_url = "https://jira-management-task-api-87769041781.us-central1.run.app/criar_task/"
        headers = {
            "Content-Type": "application/json",
        }

        response = requests.post(api_url, headers=headers, json=request_json)
        response.raise_for_status()
        print(f"Resposta da API externa: {response.text}")
        return (f'Arquivo salvo e dados enviados para API! Caminho: gs://{bucket_name}/{file_path}', 200)

    except requests.exceptions.RequestException as e:
        print(f"Erro ao enviar para a API externa: {e}")
        return (f'Erro ao enviar para a API externa: {e}', 500)
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return (f'Erro inesperado: {e}', 500)