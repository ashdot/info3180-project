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

## Customize configuration

See [Vite Configuration Reference](https://vitejs.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

## Start Flask API

Remember to always create a virtual environment and install the packages in your requirements file

```bash
$ python -m venv venv (you may need to use python3 instead)
$ source venv/bin/activate (or .\venv\Scripts\activate on Windows)
$ pip install -r requirements.txt
$ flask --app app --debug run
```
