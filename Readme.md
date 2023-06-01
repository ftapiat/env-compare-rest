This project uses Python3.9

## Install

- Install venv (Use the "python" or "python3" command. If neither work, use "python3.9")
```bash
python3.9 -m venv ./venv
```

- Enter the virtual env
```bash
. venv/bin/activate
```

- Install python dependencies
```bash
pip install -r requirements.txt
```

- Install serverless globally using npm
```bash
npm install -g serverless
```

- Install project dependencies (serverless plugins)
```bash
npm install
```

- Create .env.local file with the environment variables
```bash
cp .env.example .env.local
```

## Run project

- Run the project locally
```bash
sls wsgi serve --stage local
# Add [-p NUMBER] to change the port
```

- Deploy to AWS (This will require a .env file with the stage [Example, .env.dev])
```bash
sls deploy

# Or specifying the stage: dev, prod, etc
sls deploy --stage dev --verbose 
```

## Other commands

- Update requirements.txt
```bash
pip freeze > requirements.txt
```

- Remove the project from AWS by stage
```bash
sls remove --stage dev
```