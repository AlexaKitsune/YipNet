# YipNet

## Installation

Before starting the project, ensure you have MySQL (we are using XAMPP) installed and running. You will need these services to support the backend of the application.

To start the project, open two terminals in the repository folder.

Each terminal will serve both the **frontend**. and the **backend**.

### Frontend

The frontend is developed using Vue.js and Node.js.

To set up the frontend, follow these steps:

```bash
# 1. Open your terminal and navigate to the /frontend directory:
cd frontend

# 2. Install the necessary Node.js modules:
npm install
```

Run the frontend locally in development mode with:

```bash
npm run serve
```

### Backend

The backend is developed using Python and Flask.

To configure the backend, perform the following steps:

```bash
# 1. Navigate to the /backend directory:
cd backend

# 2. Create a Python virtual environment:
py -3 -m venv venv

# 3. Activate the virtual environment (on Windows):
venv\Scripts\activate

# 4. Install the required Python packages from the requirements.txt file:
pip install -r requirements.txt
```

Finally, run the development server with the following command:

```bash
python src/app.py
```