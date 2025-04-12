import pandas as pd
import string as str
import random as r

if __name__ == '__main__':
    df = pd.read_csv('u_p.csv')

    # punctuation="#$%!@*&"
    pass_elements = str.ascii_letters+str.punctuation+str.digits
    n = int(input("Length: "))
    pass_generated = ''.join(r.choices(pass_elements,k=n))
    # print(pass_generated)

    username = input("UserName: ")
    password = pass_generated
    # password = input("Password: ")

    new = pd.DataFrame([{"UserName":username,"Password":password}])
    df = pd.concat([df,new],ignore_index=True)
    df.to_csv('u_p.csv',index=False)

    