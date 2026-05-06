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

### Clone the Repository

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

N.B - A Secret Key can be Created using -> Secret library in python 



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







## Deployed Application Link 






## Known Issues and Limitations 