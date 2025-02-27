import functions_framework
from google.cloud import storage
import json
import datetime

@functions_framework.http
def salvar_json_storage(request):
    """Recebe um JSON via POST e salva em um arquivo no Google Cloud Storage.

    Args:
        request (flask.Request): O objeto de requisição HTTP.

    Returns:
        str: Uma mensagem de sucesso com o caminho do arquivo, ou uma mensagem de erro com código 500.
    """

    if request.method != 'POST':
        return ('Method Not Allowed', 405, {'Allow': 'POST'})

    if not request.is_json:
        return ('Bad Request: Expecting JSON data', 400)

    request_json = request.get_json(silent=True)

    if not request_json:
        return ('Bad Request: Invalid JSON data', 400)

    bucket_name = 'suri-storage-files'
    folder_name = 'jira/issues'

    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    file_name = f'planilha_linha_{timestamp}.json'
    file_path = f'{folder_name}/{file_name}' if folder_name else file_name

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)

        blob.upload_from_string(
            data=json.dumps(request_json),
            content_type='application/json'
        )

        return (f'Arquivo salvo com sucesso: gs://{bucket_name}/{file_path}', 200)

    except Exception as e:
        print(f"Erro ao salvar no Cloud Storage: {e}")
        return (f'Erro ao salvar no Cloud Storage: {e}', 500)