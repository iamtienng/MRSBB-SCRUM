# MRSBB

Movie Recommendation System By Bot

## Setup Instructions

### Creating virtual environments

```bash
python3 -m venv MRSBBvenv
source MRSBBvenv/bin/activate
```

### Install Required Python Modules

```bash
pip install -r requirements.txt
```

### Start Web Server (BackEnd)

First cd into MRSBB folder

```bash
cd MRSBB
```

Next run the Django web server

```bash
python3 manage.py runserver
```

### [Install Node.js](https://nodejs.org/en/)

### Install Node Modules

First cd into the `FrontEnd` folder.

```bash
cd FrontEnd
```

Next install all dependicies.

```bash
npm install
```

### Compile the Front-End

Run the production compile script

```bash
npm run build
```

or for development:

```bash
npm run dev
```
