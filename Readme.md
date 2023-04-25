Este proyecto usa Python3.9

## Instalación

- Instalar venv (Usar "python" o "python3" si no funciona "python3.9")
```bash
python3.9 -m venv ./venv
```

- Entrar al entorno virtual (En Ubuntu)
```bash
. venv/bin/activate
```

- Instalar dependencias python
```bash
pip install -r requirements.txt
```

- Instalar serverless de forma global
```bash
npm install -g serverless
```

- Instalar dependencias serverless
```bash
npm install
```

## Ejecución

- Ejecutar localmente
```bash
sls wsgi serve
```

- Desplegar a AWS
```bash
sls deploy

# O espeficicando el stage: dev, prod, etc
sls deploy --stage dev
```


## Otros comandos

- Guardar dependencias en un archivo requirements.txt
```bash
pip freeze > requirements.txt
```