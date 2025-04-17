import pandas as pd
import string as s
import random as r
from cryptography.fernet import Fernet as F
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

if __name__ == '__main__':
    #verifying master key
    m_password = input("Master Key - ")

    #platform
    def platform_function():
        platform = input("Platform: ")
        #to ensure its not blank
        while not platform.strip():
            print("Enter the platform name!")
            platform = input("Platform: ")
        return platform

    #username
    def username_function():
        username = input("UserName: ")
        #to ensure username is not blank
        while not username.strip():
            print("Username cannot be blank!")
            username=input("UserName: ")
        return username

    #password
    def password_function():
        while True:
            y_n = input("Do you want to generate a password? Y/N: ").strip().lower()
            if y_n == 'y':
                try:
                    n = int(input("Length: "))
                    punctuation="#$%!@*&"
                    pass_elements = s.ascii_letters+ punctuation +s.digits
                    pass_generated = ''.join(r.choices(pass_elements,k=n))
                    password = pass_generated
                    break
                except ValueError:
                    print("Please enter a valid password length!")
            elif y_n=='n':
                password = input("Password: ")
                #to ensure password is not blank
                while not password.strip():
                    print("Password cannot be empty!")
                    password = input("Password: ")
                break
            else:
                print("Enter a valid input!")
        return password
    
    #encryption_decryption
    def encrypt_function(password,m_password):
        salt = os.urandom(16)
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=1_200_000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(m_password.encode()))
        f_obj = F(key)
        encrypted_pass = f_obj.encrypt(password.encode())
        #b64encode and decode this below converts raw bytes into plain text which makes it portable,easy to store and read from csv
        encrypted_pass_b64 = base64.b64encode(encrypted_pass).decode()  
        salt_b64 = base64.b64encode(salt).decode()
        return encrypted_pass_b64,salt_b64
    
    #storing username and password
    def store_function(platform,username,password,salt):

        #reading csv
        try:
            df = pd.read_csv('u_p.csv')
        
        except FileNotFoundError:
            df = pd.DataFrame(columns=["Platform","Username","Password","Salt"])

        new = pd.DataFrame(
            [
                {
                    "Platform":platform,
                    "Username":username,
                    "Password":password,
                    "Salt":salt
                }
            ]
        )
        df = pd.concat([df,new],ignore_index=True)
        df.to_csv('u_p.csv',index=False)
        print("TADA!! Done")
                          

    #calling for all functions
    platform = platform_function()
    username = username_function()
    password = password_function()
    password,salt = encrypt_function(password,m_password)
    store_function(platform,username,password,salt)

    
     





    

 