![Publish](https://github.com/osboo/sharegood/actions/workflows/publish.yaml/badge.svg)
# Sharegood
Telegram bot for tracking car expences and notifications of regular service

## Run in VS Code
- Install dev environment (Docker env for VS Code) [link](https://code.visualstudio.com/docs/remote/containers#_getting-started)

- Re-open folder in container
- `ngrok http 7071`
- put https temprary URL to `.env` file as `NGROK_URL`. Env file should be in form of KEY=VALUE
- define `SharegoodToken` variable in .env file. Check Botfather to get token for corresponding bot.
- run `bash utils/set-webhook.sh`
- define `botUsersIDs` as `xxxxxxxxx;` allowed telegram ids
- run func in VS Code - press F5

## Run locally
- install [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
- install [Azure Func core tools](docs.microsoft.com/en-us/azure/azure-functions/functions-run-local)
- install [ngrok](https://dashboard.ngrok.com/get-started/setup)
- run `ngrok http 7071`
- put https temprary URL to `.env` file as `NGROK_URL`
- run `bash utils/set-webhook.sh`
- run `func host start`

## Run tests
 - Define local Azurite as temp database `StorageAccountConnectionString` equal to 
 ```
 DefaultEndpointsProtocol=http;AccountName=devstoreaccount1;AccountKey=Eby8vdM02xNOcqFlqUwJPLlmEtlCDXJ1OUzFT50uSRZ6IFsuFq2UVErCz4I6tq/K1SZFPTOtr/KBHBeksoGMGw==;TableEndpoint=http://127.0.0.1:10002/devstoreaccount1;
 ```
 - Run Azurite: see [doc](https://docs.microsoft.com/en-us/azure/storage/common/storage-use-azurite?tabs=visual-studio-code)
 - run `pytests mybot/tests` or use VSCode Test Explorer

## Useful links
### Preparation
 - Install dev environment (Docker env for VS Code) [link] (https://code.visualstudio.com/docs/remote/containers#_getting-started)
 - Try asyncio

### Aiogram
 -[x] Bulid echo bot local [link](https://surik00.gitbooks.io/aiogram-lessons/content/chapter1.html)
 -[x] Migrate to webhook - see set-webhook.sh

### Azure Function
[Manual](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python#create-and-test-the-local-functions-project)

- [x] Sample test local echo function
- [x] Switch to Docker
- [-] [Deploy to Azure](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python#enable-continuous-deployment-to-azure)

### Integrate Aiogram bot with Azure Fuction
Helping links:
- [Bot on telebot lib in Azure Function](https://masyan.ru/2019/10/serverless-azure-functions-telegram-python-bots/)
- [AIOGram bot in AWS Lambda](https://github.com/DavisDmitry/aiogram-aws-serverless-example/blob/master/bot.py) 

### Use Azure Key Vault to get sensitive data
[Tutorial](https://www.c-sharpcorner.com/article/how-to-access-azure-key-vault-secrets-through-rest-api-using-postman/)
