import pandas as pd
from scipy.sparse import data
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
question=   {
                'que1':'How happy do you feel today1-100)', 
                'que2':'How many people you met today ? (1-100)',
                'que3':'How productive do you feel today?(1-100)',
                'que4':'Has any thing good happened today? (If not yet don’t worry you can come and edit here whenever any good happens today) (yes/ no)',
                'que5':'How fast do you fall sleep at night  (for an average person it is 7-10 minutes)? (easily, it takes some time like more  than avg time, needs a pill to sleep, )',
                'que6':'Do you go out often and like to socialize ? (1-100)'
            }
"""
    eaisily | takes some time usually more than average time |, needs a pill
    1       |    2                                           |   3

    level1  level2     level3   level4      level5 
    happy   low mood    upset   disturbed   high stress
""" 
def predict_stress_level(answers):
    dataset=pd.read_csv("temp.csv")
    print(dataset.head())
    X=dataset[['que1', 'que2', 'que3', 'que4', 'que5', 'que6']]
    y=dataset['class']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    knn=KNeighborsClassifier(n_neighbors=5)
    knn.fit(X_train,y_train)
    # x_new=[30,20,7,20,0, 2,30]
    y_new=knn.predict(answers)
    return y_new[0]

    # print(dataset)
    # print("Model created")
    # count=0
    # while True:
    #     if(count == 3 ):
    #         break

    #     x_new=[[]]


    #     print("How happy do you feel today ? (1-100) ")
    #     a=input()
    #     x_new[0].append(a)
        
    #     print("How many people you met today ? (1-100) ")
    #     a=input()
    #     x_new[0].append(a)
        
    #     print("How productive do you feel today? (1-100) ")
    #     a=input()
    #     x_new[0].append(a)
        
    #     print("Has any thing good happened today? (If not yet don’t worry you can come and edit here whenever any good happens today) (yes/ no) ")
    #     a=input()
    #     x_new[0].append(a)
        
    #     print("How fast do you fall sleep at night  (for an average person it is 7-10 minutes)? (easily, it takes some time like more  than avg time, needs a pill to sleep, ) ")
    #     a=input()
    #     x_new[0].append(a)

    #     print("Do you go out often and like to socialize ? (1-100)")
    #     a=input()
    #     x_new[0].append(a)


    #     X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42)
    #     knn=KNeighborsClassifier(n_neighbors=5)
    #     knn.fit(X,y)
    #     y_new=knn.predict(x_new)
    
        
    #     t=input(f"Is leve {y_new[0]} type predection correct ? (y/n) ")
    #     if(t=="y" or t=="Y"):
    #         x_new[0].append(y_new[0])
    #     else:
    #         r=input("enter correct level of stress ")
    #         x_new[0].append(r)
    #     dataset.loc[len(dataset.index)]=x_new[0]   

    #     yesno=input("do you want to exit and save changes ? ")
    #     if(yesno=="y"):
    #         dataset.to_csv("temp1.csv", index=False)
    #         break
# if __name__=="__main__":
#     print(predict_stress_level([[30,20,7,0, 2,30]]))