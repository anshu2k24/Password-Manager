import pandas as pd
import string as str
import random as r

if __name__ == '__main__':
    df = pd.read_csv('u_p.csv')

    punctuation="#$%!@*&"
    pass_elements = str.ascii_letters+ punctuation +str.digits

    #username
    username = input("UserName: ")

    #password
    y_n = input("Do you want to generate a password? Y/N: ")
    if y_n=='Y' or 'y':
        n = int(input("Length: "))
        pass_generated = ''.join(r.choices(pass_elements,k=n))
        password = pass_generated
    else:
        password = input("Password: ")

    #storing username and password
    new = pd.DataFrame([{"UserName":username,"Password":password}])
    df = pd.concat([df,new],ignore_index=True)
    df.to_csv('u_p.csv',index=False)
    print("TADA!! Done")

    