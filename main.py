import pandas as pd

if __name__ == '__main__':
    df = pd.read_csv('u_p.csv')

    username = input("UserName: ")
    password = input("Password: ")

    new = pd.DataFrame([{"UserName":username,"Password":password}])
    df = pd.concat([df,new],ignore_index=True)
    df.to_csv('u_p.csv',index=False)

    