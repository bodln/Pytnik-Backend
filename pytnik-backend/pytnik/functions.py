from django.http import HttpResponse
import os
import itertools

def OK(request):
    return HttpResponse("OK")

def get_map_by_name(name):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'maps/' + name + '.txt')

    if os.path.isfile(file_path):
        return file_path
    else:
        raise Exception('Map not found')

def load_map(map_name):
    try:
        with open(map_name, 'r') as f:
            f.readline()

            coin_distance = [[0]]
            ident = 1

            while True:
                line = f.readline().strip()
                if not len(line):
                    break

                values = [int(val) for val in line.split(',')]
                for iteration, coin_sublist in enumerate(coin_distance):
                    coin_sublist.append(values[2 + iteration])
                    
                coin_distance.append(values[2:2 + len(coin_distance)] + [0])

            return coin_distance

    except Exception as e:
        raise e

def permutations(list_perm):
    return list(itertools.permutations(list_perm))