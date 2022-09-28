import pandas as pd
min_lenght = 3
max_lenght = 12

def generate():
    with open("english2.txt") as file:
        with open("dictionart.txt",'w') as result:
            for i in file.readlines():
                if min_lenght<=len(i)<=max_lenght:
                    result.write(i)
                    #print(i)

    pass

def generate_number():
    data = pd.read_csv('dictionary1.txt', sep=" ", header=None)
    data.columns = ["a"]
    for i in range(min_lenght,max_lenght+1):
        data_filtered = data[data['a'].str.len() == i]
        data_filtered = data_filtered['a']
        data_filtered.to_csv('player1data/data' + str(i)+'.csv', index=False)
        print(i," : ", data_filtered.size)
    pass
letters = "abcdefghijklmnopqrstuvwxyz"
def count_num_of_letter():
    dict = {}
    for i in range(min_lenght,max_lenght):
        dict[i] = []
        data = pd.read_csv('player1data/data'+str(i)+".csv", sep=",")
        for j in letters:
            dict[i].append([j,len(data[data['a'].str.contains(j,regex=False)])])
            pass
    for i in range(min_lenght,max_lenght):
        dict[i].sort(key=lambda x: x[1], reverse=True)
        t = []
        for i in dict[i][1:10]:
            t.append(i[0])
        print(t)
        

"""generate()
res = open("dictionary.txt",'r')
print(len(res.readlines()))"""
#generate_number()
count_num_of_letter()