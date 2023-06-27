# Warbler

Warbler is a social media platform where users can post short messages, follow other users, and interact with their messages.

## Installation

1. Clone the repository:

```bash
git clone https://github.com/cneumann01/warbler.git
```

2. Navigate to the project directory:

```bash
cd warbler
```

3. Create a virtual environment:

```bash
python -m venv .venv
```

4. Activate the virtual environment:

```bash
source .venv/bin/activate
```

5. Install the required dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

6. Set up the database:

```bash
createdb warbler
python seed.py
```

7. Start the server:

```bash
flask run
```
Open your web browser and visit http://localhost:5000 to access Warbler.
