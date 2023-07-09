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

## Usage
1. Sign up for a new account or log in if you already have one.
2. Browse messages from other users on the home page.
3. Follow other users to see their messages in your timeline.
4. Post new messages by clicking on the "New Message" button.
5. Edit or delete your own messages using the appropriate buttons.
6. Explore the follower and following pages of other users.
7. Log out when you're done using the platform.

## Testing

To run the unittests, select a test suite from the tests folder and run the following command, replacing file_name.py with the correct file name:
```bash
python -m unittest file_name.py
