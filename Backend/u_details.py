import pandas as pd

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

    # favwords function
    def favword_input():
        favword = input("Enter your favorite words: ")
        while not favword.strip():
            print("Please enter a valid favorite words!")
            favword = input("favorite words: ")
        return favword

    # pob function
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
    df = pd.DataFrame(columns=["name","dob","pob","favnumb"])
    
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