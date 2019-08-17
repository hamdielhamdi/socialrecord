import multiprocessing
import threading

from scroll_get_freinds import standalone_friends_getter
from get_user_post import get_posts_per_user_name
import pandas as pd
import os


def files(path):
    for file in os.listdir(path):
        if os.path.isfile(os.path.join(path, file)):
            yield file


def run(store=True):
    if not store:
        response = standalone_friends_getter()
    else:
        response = 'ok'
    if response == 'ok':
        name = list()
        for file in files("users_id_url_profile_db"):
            name.append({file.replace('_', '').replace('.csv', ''): file})
        select = max([int(list(i.keys())[0]) for i in name])
        for k in name:
            if list(k.keys())[0] == str(select):
                start_point = k[str(select)]
                id_url = pd.read_csv('users_id_url_profile_db/' + start_point, index_col=False)
                threads = []
                lendf = list(range(id_url.shape[0]))
                chunks = [lendf[x:x + 100] for x in range(0, len(lendf), 100)]
                print(chunks)
                # for index in lendf:
                    # get_posts_per_user_name(id_url.at[index, 'profile_name'], id_url.at[index, 'url_profile'])


run()