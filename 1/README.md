# Task 1 setup guide

```bash
# Setup environment
cp .env.example .env
# Edit .env if needed (defaults work fine)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Start database
docker-compose up -d

# Run application
python main.py

# Test (in another terminal)
curl http://127.0.0.1:8000/api/db_version
```
