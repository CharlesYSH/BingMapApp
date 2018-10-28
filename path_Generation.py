'''
parameter : 
    train 
    length
    prime
    top_n
return :
    array of the positions
'''
import numpy as np
import pandas as pd
from math import *
import keras
from keras import backend as K
from keras.utils import to_categorical
from keras.models import Sequential,load_model
from keras.layers import LSTM,Embedding,Dense,Dropout
from keras.optimizers import RMSprop


def load_place():
    fd = open('data/all_place_dataset.txt')
    all_place = fd.read()
    places = all_place.split('\n')[:-1]
    #places_num = len(places)
    for i in range(len(places)):
        places[i] = places[i].split(',')

    places = np.asarray(places)
    
    points = []
    for item in places[...,2:]:
        points.append([float(item[0]),float(item[1])])
    points = np.asarray(points)
    
    fd.close()
    return places,points

def load_data():
    #fd = open('all_place_dataset.txt')
    fn = open('data/nearby_place_2500m.txt')
    #all_place = fd.read()
    nearby_place = fn.read()
    pairs = nearby_place.split('\n')[:-1]
    for i in range(len(pairs)):
        pairs[i] = list(map(eval,pairs[i].split(',')))
    
    places,points=load_place()
    #places = all_place.split('\n')[:-1]
    places_num = len(places)
    #for i in range(len(places)):
    #    places[i] = places[i].split(',')

    #places = np.asarray(places)
    place_label = places[...,0]
    place_label = to_categorical(place_label,num_classes=len(places))
    #points = []
    #for item in places[...,2:]:
    #    points.append([float(item[0]),float(item[1])])
    #points = np.asarray(points)
    
    #dataset = sorted(temp, key=lambda item: item[1])
    dataset = []
    for pair in pairs:
        repeat = (2599-pair[2]) // 100
        for i in range(int(repeat)):
            dataset.append(pair[:2])
    
    dataset = np.asarray(dataset)
    np.random.shuffle(dataset)
    #roll_dataset = np.roll(dataset,shift=-1,axis=1)
    y = []
    for data in dataset:
        y.append(place_label[data[1]])
    y = np.asarray(y)
    #int(0.9*len(dataset))
    x_train = dataset[...,0].reshape(-1,1)
    y_train = y.reshape(-1,1,places_num)
    #x_test = dataset[int(0.9*len(dataset)):,0].reshape(-1,1)
    #y_test = y[int(0.9*len(dataset)):].reshape(-1,1,places_num)
    
    fn.close()
    return x_train,y_train,places_num,points,places

def getDistance(latA, lonA, latB, lonB):
    if latA == latB and lonA == lonB:
        return 0
    ra = 6378140  # radius of equator: meter  
    rb = 6356755  # radius of polar: meter  
    flatten = (ra - rb) / ra  # Partial rate of the earth  
    # change angle to radians  
    radLatA = radians(latA)  
    radLonA = radians(lonA)  
    radLatB = radians(latB)  
    radLonB = radians(lonB)  

    pA = atan(rb / ra * tan(radLatA))  
    pB = atan(rb / ra * tan(radLatB))  
    x = acos(sin(pA) * sin(pB) + cos(pA) * cos(pB) * cos(radLonA - radLonB))
    if sin(x / 2) == 0:
        return 0
    c1 = (sin(x) - x) * (sin(pA) + sin(pB))**2 / cos(x / 2)**2  
    c2 = (sin(x) + x) * (sin(pA) - sin(pB))**2 / sin(x / 2)**2  
    dr = flatten / 8 * (c1 - c2)  
    distance = ra * (x + dr)  
    return distance

def pick_rest(path, rest_type=0):
    insert_index = path[-1]
    #print('pick',insert_index)
    df = pd.read_csv('data/Restaurant.csv')
    rest_list = df.values[...]
    place,points = load_place()    
    #pick restaurant
    dist_to_r = []
    for i in range(len(rest_list)):
        if rest_list[i][rest_type+4]==1:
            dist = getDistance(rest_list[i][2],rest_list[i][3],points[insert_index][0],points[insert_index][1])
            dist_to_r.append([rest_list[i][0],dist])
    dist_to_r.sort(key=lambda item: item[1])
    # too far
    if dist_to_r[0][1]>=2500.0 :
        dist_to_r = []
        for i in range(len(rest_list)):
            dist = getDistance(rest_list[i][2],rest_list[i][3],points[insert_index][0],points[insert_index][1])
            dist_to_r.append([rest_list[i][0],dist])
        dist_to_r.sort(key=lambda item: item[1])

    restaurant = rest_list[dist_to_r[0][0]]
    
    #pick place
    dist_to_p = []
    for i in range(len(points)):
        dist = getDistance(restaurant[2],restaurant[3],points[i][0],points[i][1])
        dist_to_p.append([i,dist])
    dist_to_p.sort(key=lambda item:item[1])
    
    target_index=-1
    for tar in dist_to_p:
        if tar[0] not in path:
            target_index = tar[0]
            break
    return restaurant,target_index

def build_model(places_num,embed_size):
    model = Sequential()
    model.add(Embedding(places_num, embed_size))

    # bulid your RNN model here,recurrent_regularizer=regularizers.l2(0.01)
    model.add(LSTM(512,return_sequences=True))
    model.add(Dropout(0.2))
    #model.add(LSTM(512, return_sequences=True))
    #model.add(Dropout(0.2))

    model.add(Dense(places_num, activation='softmax')) 
    print(model.summary()) 
    return model

def generate(model,prime,places_num,length=10,top_n=10,rest_type_flag=[0],insert_flag=[2]):
    point = prime[0]
    x_pred = prime
    count = 100
    rest_type_index = 0
    insert_index = 0
    restaurant = []
    rest_list = []
    #for i in range(length):
    while len(point)<length and count>0:
        count -= 1

        if insert_index<len(insert_flag) :
            if insert_flag[insert_index] == len(point):
                restaurant,target_index = pick_rest(point,rest_type_flag[rest_type_index])
                rest_list.append(restaurant)
                insert_index += 1
                rest_type_index += 1
                if target_index != -1 :
                    x_pred = [[target_index]]

        pred = model.predict(x_pred)
        index = pick_top_n(pred, places_num, top_n=top_n)
        if index in point :
            continue
        point.append(index)
        x_pred = [[index]]

    return point,rest_list

def pick_top_n(preds, places_num, top_n=10):
    prob = np.squeeze(preds)
    prob[np.argsort(prob)[:-top_n]] = 0
    # normalize
    prob = prob / np.sum(prob)
    # randomly sample
    index = np.random.choice(places_num, 1, p=prob)[0]
    return index

def path_Generation(train=False,length=5,position=[24.8002,120.9795],top_n=10,epochs=10,batch_size=128,rest_type_flag=[0],insert_flag=[1]):
    #if __name__ == '__main__'(train=False,length=10,prime=[0],top_n=5):
    #length=10
    #prime=[0] 24.80982,120.975139
    #top_n=5
    x_train,y_train,places_num,points,places = load_data()
    if train:
        embed_size = 512 
        #x_train,y_train,x_test,y_test,places_num = load_data(length=5)
        model = build_model(places_num,embed_size)
        optimizer = RMSprop() # choose your optimizer
        model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=['accuracy'])
        model.fit(x_train, y_train, epochs=epochs, batch_size=batch_size, shuffle=True, validation_split=0.1) 
        model.save('model/save.hdf5')
    else :
        model = load_model('model/save.hdf5')
        

        dist_to_p = []
        for i in range(len(points)):
            dist = getDistance(position[0],position[1],points[i][0],points[i][1])
            dist_to_p.append([i,dist])
        dist_to_p.sort(key=lambda item:item[1])
        prime = dist_to_p[0][0]

        path,rest_list = generate(model=model,prime=[[prime]], places_num=places_num, length=length, top_n=top_n, rest_type_flag=rest_type_flag, insert_flag=insert_flag)
        ans = []
        add = []
        for index in path:
            ans.append(points[index].tolist())
            add.append(places[index][1])
        for i in range(len(insert_flag)):
            insert_index = insert_flag[i]
            ans.insert(insert_index+i,rest_list[i][2:4].tolist())
            add.insert(insert_index+i,rest_list[i][1])

        K.clear_session()
        print(rest_list)
        return ans,add