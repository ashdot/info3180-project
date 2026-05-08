# INFO3180 Group Project

DriftDater is a Dating Web application that allows users to create detailed profiles, discover compatible matches and initiate connections with other users. This application uses the Vue 3 frontend framework as well as the Flask backend API, along with a database to store relevant user information.

## Team Members & Roles

Members | Roles
--- | ---
Rochele Webster | Backend Lead
Jada-Marie Dotting | Frontend Lead
Amoye Walters | QA/Testing Lead
Ashle Johnson | Deployment Lead
Alexia Barrows | Project Manager


## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.volar) (and disable Vetur) + [TypeScript Vue Plugin (Volar)](https://marketplace.visualstudio.com/items?itemName=johnsoncodehk.vscode-typescript-vue-plugin).


## Setup Instructions

### Prerequisites

Ensure you have the following installed before running 

Python 3.10+
Node.js 18+
PostgreSQL (or SQLite for local development)
Git

### 1. Clone the Repository

```bash
$ git clone https://github.com/ashdot/info3180-project.git
$ cd info3180-project
```

### 2. Backend Setup (Flask)

**Create and activate a virtual environment:**
```bash
# Create the environment
$ python -m venv venv

# Activate (Windows)
$ .\venv\Scripts\activate

# Activate (macOS/Linux)
$ source venv/bin/activate
```

**Install Python dependencies:**
```bash
$ pip install -r requirements.txt
```

**Configure environment variables — create a .env file in the project root:**

SECRET_KEY=your-secret-key-here  
DATABASE_URL=postgresql://user:password@localhost/driftdater  
UPLOAD_FOLDER=./uploads


```bash
$ python3 -c "import secrets; print(secrets.token_hex(32))"
#N.B - A Secret Key can be Created using -> Secret library in python 
```





**Run database migrations:**

```bash
$ flask db init 
$ flask db migrate 
$ flask db upgrade
```

**Start the Flask development server:**

```bash
$ flask --app app --debug run
# Runs at http://localhost:5000
```


### 3. FrontEnd Setup (Vue/Vite)

Open a new terminal and navigate to the frontend directory:

```bash
$ cd frontend

#Install Node.js dependencies:

$ npm install

#Start the Vite development server:

$ npm run dev
# Runs at http://localhost:5173

```

## API Documentation 

Endpoint | Method | Description | Auth Required | Response | 
--- | --- | --- | --- | ---
/api/v1/signup | POST | Register a new user and auto-create profile | No | 201 Created
/api/v1/auth/login | POST | Login and create session | No | 200 + user data
/api/v1/auth/logout | POST | Logout and clear session | Yes | 200 OK
/api/v1/profile/all | GET | List all public profiles | Yes | 200 + profiles[]
/api/v1/profile/<user_id> | GET | Get a specific user's profile | Yes | 200 + profile
/api/v1/profile | GET | Display current user's own profile | Yes | 200 + profile
/api/v1/profile/edit | PUT | Update own profile (with photo upload) | Yes | 200 OK
/api/v1/profiles/<id>/save | POST | Toggle save/unsave a profile | Yes | 201 Created / 200 OK
/api/v1/matches | GET | Get scored matches for current user | Yes | 200 + matches[]
/api/v1/profiles/<id>/like | POST | Like a profile (handles mutual matches) | Yes | 201 + match status
/api/v1/profiles/<id>/dislike | POST | Dislike a profile | Yes | 201 OK
/api/v1/profiles/<id>/pass | POST | Pass on a profile (hide from future results) | Yes | 201 OK
/api/v1/contacts/<user_id> | GET | List of mutual match contacts | Yes | 200 + contacts[]
/api/v1/messages/<match_id> | GET | Get conversation history for a match | Yes | 200 + messages[]
/api/v1/messages/<match_id> | POST | Send a message to a match | Yes | 201 + message
/api/v1/notifications | GET | Get user notifications | Yes | 200 + notifications[]
/api/search | GET | Search/filter profiles with sorting | Yes | 200 + results[]





## Deployed Application Link 






## Known Issues and Limitations 
