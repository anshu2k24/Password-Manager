import pandas as pd
import string as s
import random as r
from cryptography.fernet import Fernet as F
import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from google import genai
from dotenv import load_dotenv

if __name__ == '__main__':
    
    #taking master key
    m_password = input("Master Key - ")

    #platform
    def platform_function():
        platform = input("Platform: ")
        #to ensure its not blank
        while not platform.strip():
            print("Enter the platform name!")
            platform = input("Platform: ")
        return platform
    
    # saving user details for generating username
    def user_details():
        # name function
        def name_input():
            name = input("Enter your name: ")
            while not name.strip():
                print("Please enter a valid name!")
                name = input("Name: ")
            return name
        
        # dob function
        def dob_input():
            dob = input("Enter your Date of Birth (ddmmyy) :")
            while not dob.strip():
                print("Please enter a valid DOB!")
                dob = input("DOB: ")
            return dob

        # favword function
        def favword_input():
            favword = input("Enter your favorite word: ")
            while not favword.strip():
                print("Please enter a valid favorite word!")
                favword = input("favword: ")
            return favword

        # fanumb function
        def favnumb_input():
            favnumb = input("Enter your favorite number: ")
            while not favnumb.strip():
                print("Please enter a valid number!")
                favnumb = input("Enter your favorite number: ")
            return favnumb
        
        name = name_input()
        dob = dob_input()
        favword = favword_input()
        favnumb = favnumb_input()

        # storing details
        df = pd.DataFrame(columns=["name","dob","favword","favnumb"])
        
        new = pd.DataFrame(
            [
            {
                "name" : name,
                "dob" : dob,
                "favword" : favword,
                "favnumb" : favnumb
            }
        ])

        df = pd.concat([df,new],ignore_index=True)
        df.to_csv('u_details.csv',index=False)
        print("Saved user details!")

    # gemini
    load_dotenv()
    client = genai.Client(api_key=os.getenv("gemini_api"))
    def gemini_gen(name,dob,favword,favnumb,platform):
        prompt = (
            f"Generate five unique, one-word usernames specifically for the platform {platform}. "
            f"Create them by creatively combining or transforming the following personal details:\n"
            f"- Name: {name}\n"
            f"- Date of birth (DDMMYY): {dob}\n"
            f"- Favorite number: {favnumb}\n"
            f"- Favorite word: {favword}\n\n"
            f"The usernames should be:\n"
            f"- One word only (no spaces or underscores)\n"
            f"- Creative, fancy, exciting, and memorable\n"
            f"- Suitable for a fun, modern online identity\n"
            f"- Ideally a mix of real and invented words\n"
            f"- also keep in mind if its a professional platform then suggest professional usernames accordingly\n"
            f"Format your response as:\n"
            f'"Username1","Username2","Username3","Username4","Username5"'
            f"Do not include any explanations, greetings, or extra text — only the list of usernames, "
            f"comma-separated, and each wrapped in double quotes."
        )
        response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=[prompt]
        )
        print(response.text.strip())
        return response.text.strip()

    #username
    def username_function():
        while True:
            y_n = input("Do you want to generate a username? Y/N: ").strip().lower()
            if y_n == 'y':
                try:
                    udf = pd.read_csv('u_details.csv')
                except FileNotFoundError:
                    user_details()
                    udf = pd.read_csv('u_details.csv')
                u_det = udf.iloc[0]
                name = u_det['name']
                dob = u_det['dob']
                favword = u_det['favword']
                favnumb = u_det['favnumb']
                # calling gemini function
                username_list =gemini_gen(name,dob,favword,favnumb,platform).split(",")
                for u in username_list:
                    u.strip('"')
                # username_series = pd.Series(username_list)
                for i,u in enumerate(username_list):
                    print(f"{i}: {u}")
                n = int(input("Enter the no. beside the username you want to use: "))
                # checking if n is valid or not
                while n<0 or n>=len(username_list):
                    print("Enter a valid input")
                    n = int(input("Enter the no. beside the username you want to use: "))
                username = username_list[n].strip('"')
                
            elif y_n == 'n':
                username = input("UserName: ")
                #to ensure username is not blank
                while not username.strip():
                    print("Username cannot be blank!")
                    username=input("UserName: ")
            else:
                print("Enter a valid input!")
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

    
     





    

 