## CoopManatí 
CoopManatí is a credit union and financial institution with more than 75 years of service in Puerto Rico. Its mission is to promote the socioeconomic development of its members by offering a wide range of financial products and services, including savings accounts, loans, and other financial solutions.

## Purpose 
The following code represents a small feature of the overall project developed for the CCOM4075 – Software Engineering course. The main goal of this project is to implement a Customer Service Analytics and Flow Management Tool for CoopManatí, which serves as an enhancement to their current queue management system.

Currently, CoopManatí’s system functions solely as a queue manager. However, the organization requires a more comprehensive and adaptable solution. Therefore, this project aims to design a custom, web-based application capable of integrating not only queue management but also analytics, user management, monitoring, and reporting functionalities that facilitate data-driven decision-making and operational efficiency.

## Scope of this code
The current scope of this code is the Login/Logout and Change Password features / functional requirements for the administrators and employees.

### Login/Logout
Administrators and employees can enter their CoopManatí credentials to log in to the system. If the login is successful, they are greeted with a temporary dashboard where they can click the “Settings” button located at the top-right corner of the screen to log out. However, if the credentials are incorrect, an error message will appear, and the user will be redirected back to the login page.

### Change password
Both administrators and employees can change their passwords by clicking the “¿Olvidaste tu contraseña?” link. This link redirects them to the Change Password page, where they are prompted to enter their company email, a new password, and a confirmation of the new password.

If an employee requests a password change and no errors are detected, an email notification is sent to their branch administrator for approval. On the other hand, if an administrator initiates a password change and no errors are found, a confirmation email is sent directly to their company email to approve the password reset.

## How to test this feature
Prerequisites:
  1. Download the MySQL Workbench and MySQL Server


#### Create local database instance
1. Open MySQL Workbench, click the (+) button in MySQL Connections
2. The "Set Up New Connection" window will pop-up, only change _Connection Name_ to "prototype_db" 
3. Click Ok
4. The new connection should be listed in the MySQL Connections section, double click to open
5. In the query tab, copy and paste the contents of _schema.sql_
6. Execute the queries one by one
   - If "prototype_db" does not exist, you can ignore the first SQL query
   - Remember to double click the database once created to select it for the next queries (click the refresh button in the __schemas_ section.
   - ****IMPORTANT****: In the first insert into the employee table (admin insertion), change the email from "your-email@gmail.com" to your actual email to properly test the change password feature.

#### Clone the repository 
  ```bash
  git clone https://github.com/joel-messiel/functional_prototype.git
  ```
#### Create and activate virtual environment
  ```bash
  python -m venv .venv
  
  source .venv/bin/activate  # On Linux/macOS
  .venv\Scripts\activate   # On Windows
  ```
#### Install dependencies
  ```bash
  pip install -r requirements.txt
  ```

#### Change connectDB.py database credentials
Change the credentials to your local database credentials
```
DB_URL = '127.0.0.1'
DB_NAME = 'prototype_db'
DB_PORT = 3306
DB_USER = 'root'
DB_PASSWORD = ''
```

#### Configure email for _Change password_ feature
****IMPORTANT: If you skip this step, the _Change password_ feature will not work. *****
Developers should consider creating a new email account for sending the password reset emails. This account should enable `Allow less secure apps to ON` if using a gmail account and generate an app password. For more information see: [How to Generate a Gmail App Password from Your Account](https://www.getmailbird.com/gmail-app-password/)

[Click here for more details on how the code works](https://realpython.com/python-send-email/ )


  1. Create a new file with the name ".env"
  2. Copy and paste the following to the file
     ```bash
       EMAIL_USER="your email"
       APP_PASSWORD="app token
     ```
#### Run the application
```bash
python -m flask --app main.py run
```

#### Open the app
Go to http://127.0.0.1:5000/ to view the app





