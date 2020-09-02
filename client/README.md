# Client

This is a web version of text alignment application. It consists of backend and frontend paths.

## Backend

- /be

Flask/uwsgi backend REST API service. It's pretty simple and contains all the alignment logic.

### Run

```
cd ./be
python main.py
```

## Frontend

- /fe

SPA. Vue + vuex + vuetify. UI for managing alignment process using BE and a tool for translators to edit processing documents.

### Run

```
cd ./fe
npm install
npm run serve
```
