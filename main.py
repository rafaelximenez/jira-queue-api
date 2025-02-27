import functions_framework
from google.cloud import storage
import json
import datetime

@functions_framework.http
def salvar_json_storage(request):
    """HTTP Cloud Function.
    Recebe um JSON via POST e salva em um arquivo no Google Cloud Storage.

    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>

    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """

    # --- 1. Validação da Requisição ---

    if request.method != 'POST':
        return ('Method Not Allowed', 405, {'Allow': 'POST'})

    if not request.is_json:
        return ('Bad Request: Expecting JSON data', 400)

    request_json = request.get_json(silent=True)

    if not request_json:
        return ('Bad Request: Invalid JSON data', 400)


    # --- 2. Configuração do Cloud Storage ---
    bucket_name = 'suri-storage-files'  # SUBSTITUA PELO NOME DO SEU BUCKET
    folder_name = 'jira/issues'       # SUBSTITUA PELA SUA PASTA (opcional)

    # --- 3. Criação do Nome do Arquivo (Único) ---
    timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')  # Formato: AnoMesDia-HoraMinutoSegundo-Microsegundo
    file_name = f'planilha_linha_{timestamp}.json'

    # --- 4. Caminho Completo do Arquivo no Storage ---
    file_path = f'{folder_name}/{file_name}' if folder_name else file_name  # Adiciona a pasta, se existir.

    # --- 5. Upload do JSON para o Cloud Storage ---

    try:
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(file_path)

        blob.upload_from_string(
            data=json.dumps(request_json),  # Converte o JSON para string
            content_type='application/json'
        )

        # --- 6. Resposta de Sucesso ---
        return (f'Arquivo salvo com sucesso: gs://{bucket_name}/{file_path}', 200) # Retorna o caminho do arquivo.

    except Exception as e:
        # --- 7. Tratamento de Erros ---
        print(f"Erro ao salvar no Cloud Storage: {e}")  # Log do erro.  Importante para debugging.
        return (f'Erro ao salvar no Cloud Storage: {e}', 500)