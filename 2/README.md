# Task 2 setup guide

```bash
# Setup environment
cp .env.example .env
# Edit .env (pass gh token)

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run tests
pytest tests/

# Run application
python run.py
```
