# Oasis

Northeastern Oasis is a university-endorsed web platform that provides students the opportunity to share, collaborate, and deploy real solutions that can further improve the Northeastern experience.

### Setup

1. Clone the repository
```shell
git clone https://github.com/northeastern-oasis/oasis.git
cd oasis
```

2. Create and activate a virtual environment
```shell
  python3 -m venv venv
  source venv/bin/activate
  ```

3. Create two terminal windows. One for the frontend and one for the backend

  **Backend Window**

  a. Move into the backend directory
  
  ```shell
  cd backend
  ```
  
  b. Install the requirements
  
  ```shell
  pip3 install -r requirements.txt
  ```
  
  c. Make the Django migrations
  
  ```shell
  python3 manage.py makemigrations
  ```
  
  d. Run the migrations
  
  ```shell
  python3 manage.py migrate
  ```
  
  e. Start the server
  
  ```shell
  python3 manage.py runserver
  ```

  **Frontend Window**

  a. Move into the frontend directory
  
  ```shell
  cd frontend
  ```
  
  b. Install node modules
  
  ```shell
  npm install
  ```
  
  c. Start the server
  
  ```shell
  npm start
  ```

The project should now be running on localhost:3000
