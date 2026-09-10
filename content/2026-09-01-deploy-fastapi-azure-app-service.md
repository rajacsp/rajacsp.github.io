Title: Deploying a Local FastAPI App to Azure App Service
Date: 2026-09-01
Category: Cloud Deployment
Tags: azure, fastapi, app-service, python, devops
Slug: deploy-fastapi-azure-app-service
Status: Published
Cover: image/2026-09-01-deploy-fastapi-azure-app-service/1789004104021-opt.jpg

![1789004104021](image/2026-09-01-deploy-fastapi-azure-app-service/1789004104021.png)

Deploying a FastAPI application from your local machine to Azure App Service is a straightforward process once you know the sequence. This guide walks through authenticating, provisioning the infrastructure, configuring the runtime, and shipping your code. Replace the placeholder names below with your own resource group and app names.

## Authenticate and Select Subscription

**Log in to Azure**
Start by authenticating your CLI session and pointing it at the correct subscription.

```bash
az login
az account set --subscription "00000000-1111-2222-3333-444444444444"
```

## Clean Up and Verify Existing Resources

**Delete the old app**
Remove the previous web app if you're starting fresh.

```bash
az webapp delete \
  --resource-group myapp-rg \
  --name myapp-sample-test1
```

**Verify existing plans**
List the App Service plans in your resource group to confirm what's already there.

```bash
az appservice plan list --resource-group myapp-rg -o table
```

## Provision the Infrastructure

**Create an App Service plan**
Create a Linux-based plan on the B1 SKU to host the new app.

```bash
az appservice plan create \
  --resource-group myapp-rg \
  --name myapp-testing-plan \
  --sku B1 \
  --is-linux
```

**Create the web app**
Provision the web app on the Python 3.12 runtime, attached to the plan you just created.

```bash
az webapp create \
  --resource-group myapp-rg \
  --plan myapp-testing-plan \
  --name myapp-fastapi-13 \
  --runtime "PYTHON:3.12"
```

## Configure Build and Startup

**Enable build during deployment**
Turn on Oryx build automation so dependencies are installed during deployment.

```bash
az webapp config appsettings set \
  --resource-group myapp-rg \
  --name myapp-fastapi-13 \
  --settings SCM_DO_BUILD_DURING_DEPLOYMENT=true
```

**Clone your app locally**
Pull your source code down to your machine.

```bash
git clone https://github.com/myorg/fastapi-sample
cd fastapi-sample
```

**Confirm the port binding**
Make sure your `app.py` reads the port from the environment so Azure can route traffic correctly.

```python
port = int(os.environ.get("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

**Set the startup command**
Tell App Service how to launch your application.

```bash
az webapp config set \
  --resource-group myapp-rg \
  --name myapp-fastapi-13 \
  --startup-file "python app.py"
```

## Zip and Deploy

**Package the app**
Create a deployment archive, excluding version control and virtual environment artifacts.

```bash
zip -r deploy.zip . -x '*.git*' -x '*__pycache__*' -x '*.venv*' -x '*venv*'
```

**Deploy the archive**
Push the zip to Azure App Service.

```bash
az webapp deploy \
  --resource-group myapp-rg \
  --name myapp-fastapi-13 \
  --src-path deploy.zip \
  --type zip
```

**Stream the logs**
Watch the live deployment and startup logs to confirm a clean boot.

```bash
az webapp log tail \
  --resource-group myapp-rg \
  --name myapp-fastapi-13
```

## Retrieve the Live URL

**Get the default hostname**
Fetch the public URL of your deployed app.

```bash
az webapp show \
  --resource-group myapp-rg \
  --name myapp-fastapi-13 \
  --query defaultHostName -o tsv
```

Your app is now live at `myapp-fastapi-13.azurewebsites.net`.
