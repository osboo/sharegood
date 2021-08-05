# sharegood
Telegram bot for sharing good

# Plan
## Preparation
 - Install dev environment (Docker env for VS Code) [link] (https://code.visualstudio.com/docs/remote/containers#_getting-started)
 - Try asyncio

## Aiogram
 -[x] Bulid echo bot local [link](https://surik00.gitbooks.io/aiogram-lessons/content/chapter1.html)
 -[x] Migrate to webhook - see set-webhook.sh

## Azure Function
[Manual](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python#create-and-test-the-local-functions-project)

- [x] Sample test local echo function
- [x] Switch to Docker
- [-] [Deploy to Azure](https://docs.microsoft.com/en-us/azure/azure-functions/functions-create-function-linux-custom-image?tabs=bash%2Cportal&pivots=programming-language-python#enable-continuous-deployment-to-azure)

## Integrate Aiogram bot with Azure Fuction
Helping links:
- [Bot on telebot lib in Azure Function](https://masyan.ru/2019/10/serverless-azure-functions-telegram-python-bots/)
- [AIOGram bot in AWS Lambda](https://github.com/DavisDmitry/aiogram-aws-serverless-example/blob/master/bot.py) 