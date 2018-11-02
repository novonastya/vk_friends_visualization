#Подключение к апи
import vk

my_access_token = ''
session = vk.Session(access_token=my_access_token)
vk_api = vk.API(session)

#Получение списка моих друзей
#id, first_name, last_name, sex, photo
my_friends_full = vk_api.friends.get(user_id='25670710', v='5.89', fields=['sex', 'photo_50'], lang=0)

#Количество моих друзей
my_friends_count = my_friends_full['count']
#Список id моих друзей
my_friends_ids = []
for i in range(my_friends_count):
    #Если аккаунт открыт, добавляем id
    try:
        if not my_friends_full['items'][i]['is_closed']:
            my_friends_ids.append(my_friends_full['items'][i]['id'])
    except KeyError:
        pass

#Получение друзей друзей
#Словарь {id_friend: [friend_friends_ids]}
my_friends_friends = {}

for current_id in my_friends_ids:
    current_id_friend_list = vk_api.friends.get(user_id=current_id, v='5.87')['items']
    my_friends_friends[current_id] = current_id_friend_list

#Словарь для визуализации
SEX_TO_STR = {1:'Женский', 2:'Мужской'}

#Словарь {friend_id: {first_name, last_name, sex, photo}}
my_friends_names = {}
my_friends_sex = {}
my_friends_photo_links = {}
for i in range(my_friends_count):
    current_id = my_friends_full['items'][i]['id']
    current_first_name = my_friends_full['items'][i]['first_name']
    current_last_name = my_friends_full['items'][i]['last_name']
    current_sex = my_friends_full['items'][i]['sex']
    current_photo_link = my_friends_full['items'][i]['photo_50']
    my_friends_names[current_id] = current_first_name + ' ' + current_last_name
    my_friends_sex[current_id] = SEX_TO_STR[current_sex]
    my_friends_photo_links[current_id] = current_photo_link

#Список ребер будущего графа
friends_graph_edges = []
#Для всех пар друзей смотрим являются ли они друзьями 
#И если да, добавляем соотв. ребро
for my_friend_id in my_friends_ids:
    for mutual_friend_id in my_friends_ids:
        if mutual_friend_id in my_friends_friends[my_friend_id]:
            friends_graph_edges.append((my_friend_id, mutual_friend_id))

import networkx as nx

#Создание графа
my_friends_graph=nx.Graph()
for my_friend_id in my_friends_ids:
    my_friends_graph.add_node(my_friend_id, 
                             name=my_friends_names[my_friend_id], 
                             sex=my_friends_sex[my_friend_id],
                             image=my_friends_photo_links[my_friend_id])
my_friends_graph.add_edges_from(friends_graph_edges)

#Экспорт графа для визуализации
nx.write_gexf(my_friends_graph, "my_friends_graph.gexf")

