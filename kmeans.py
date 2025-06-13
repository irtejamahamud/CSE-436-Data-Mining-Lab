import sys
from person import Person
from math import fabs

def convert_array_to_int(array):
    converted = []
    for item in array:
        converted.append(int(item))
    return converted

def read_entry_file(entry_file_path):
    splitted_lines = []
    with open(entry_file_path) as file:
        for line in file:
            splitted_lines.append(line.split('::'))
    return splitted_lines

def load_read_lines(constructor, lines):
    loaded_objects = []
    for line in lines:
        loaded_objects.append(constructor(line[0], line[1], line[2], line[3], line[4]))
    return loaded_objects

def index_nearest_mean(observation, means):
    nearest_index = 0
    less_distance = (observation - means[0])
    for index, mean in enumerate(means):
        if (fabs(observation - mean)) < less_distance:
            less_distance = fabs(observation - mean)
            nearest_index = index
    return nearest_index

def are_clusters_equal(curr_clusters, next_clusters):
    for index, curr_cluster in enumerate(curr_clusters):
        next_cluster = next_clusters[index]
        if len(curr_cluster) != len(next_cluster):
            return False
        for index, person in enumerate(curr_cluster):
            if (person.age != next_cluster[index].age):
                return False
    return True

def cluster_average(cluster):
    if len(cluster) == 0:
        return 0

    avg_sum = 0
    for person in cluster:
        avg_sum += person.age
    return (avg_sum / len(cluster))

def kmeans(clusters, means):
    next_clusters = [[] for i in range(len(means))]
    for cluster in clusters:
        for person in cluster:
            nearest_index = index_nearest_mean(person.age, means)
            next_clusters[nearest_index].append(person)

    final_clusters = next_clusters
    if not are_clusters_equal(clusters, next_clusters):
        next_means = []
        for cluster in next_clusters:
            next_means.append(cluster_average(cluster))
        final_clusters = kmeans(next_clusters, next_means)

    return final_clusters

def create_people_file(file_path, people):
    file = open(file_path, 'w+')
    for person in people:
        file.write(person.id + '::')
        file.write(person.gender + '::')
        file.write(str(person.age) + '::')
        file.write(person.occupation + '::')
        file.write(person.zip_code + '\n')
    file.close()

entry_file_path = sys.argv[1]
ages = convert_array_to_int(sys.argv[2:])
read_lines = read_entry_file(entry_file_path)
list_people = load_read_lines(Person, read_lines)
clustered_people = kmeans([list_people], ages)

for index, people in enumerate(clustered_people):
    file_dir = './export/'
    file_name = str(index) + '_' + str(len(people)) + '_' + str(index)
    file_path = file_dir + file_name + '.txt'
    create_people_file(file_path, people)
