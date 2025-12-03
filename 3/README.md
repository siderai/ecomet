# Task 3: GitHub to ClickHouse ETL

## Setup

```bash
cp example.env .env
# Edit .env with your GitHub token

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run ch
docker-compose up -d

python run.py
```