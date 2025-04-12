import pandas as pd
import string as s
import random as r

if __name__ == '__main__':
    
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
    
    #calling for all functions
    username = username_function()
    password =password_function()

    #reading csv
    try:
        df = pd.read_csv('u_p.csv')
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Username","Password"])

    #storing username and password
    new = pd.DataFrame([{"Username":username,"Password":password}])
    df = pd.concat([df,new],ignore_index=True)
    df.to_csv('u_p.csv',index=False)
    print("TADA!! Done")

 