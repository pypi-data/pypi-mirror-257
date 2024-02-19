from math import radians, sin, cos, sqrt, atan2
import pandas as pd
from datetime import datetime
from prettytable import PrettyTable
import csv
from operator import itemgetter
from scipy.spatial import cKDTree
from operator import itemgetter
import timeit
import statistics
import matplotlib.pyplot as plt

def calculate_distance_haversine(coord1, coord2):
    # Calcola la distanza tra due coordinate (x, y) utilizzando la formula della distanza tra due punti di Haversine
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))
    earth_radius = 6371  # in km
    distance = earth_radius * c
    return distance

def calculate_distance(coord1, coord2):
    # Calcola la distanza euclidea tra due punti su un piano cartesiano 
    (x1, y1) = coord1
    (x2, y2) = coord2
    distance = sqrt((x2 - x1)**2 + (y2 - y1)**2)
    return distance    

def calculate_avg_coordinates(cluster_stay_points):
    if not cluster_stay_points:
        return None

    points = cluster_stay_points["points"]

    # Inizializza le variabili per la somma delle coordinate
    sum_x = 0.0
    sum_y = 0.0

    # Calcola la somma delle coordinate dei punti all'interno del cluster
    for point in points:
        coordinates = point["coordinates"]
        sum_x += coordinates[0]
        sum_y += coordinates[1]

    # Calcola la media delle coordinate
    avg_x = sum_x / len(points)
    avg_y = sum_y / len(points)

    return (avg_x, avg_y)

def stay_point_detection(points, distance_threshold, time_threshold):
    p = 0
    i = 0
    stay_points = []

    while p < len(points):
        cluster_stay_points = {"points": []}
        i = p+1
        s_found = 0
        cluster_stay_points["points"].append(points[p])

        while i < len(points):
            distance = calculate_distance(points[p]["coordinates"], points[i]["coordinates"])
            time_difference = (points[i-1]["timestamp"].timestamp() - points[p]["timestamp"].timestamp())

            if points[p]["person_id"] == points[i]["person_id"]:
                if distance >= distance_threshold:    
                    if time_difference >= time_threshold:
                        current_stay_point = {
                                    "person_id": points[p]["person_id"],
                                    "id": len(stay_points) + 1,
                                    "coordinates": calculate_avg_coordinates(cluster_stay_points),
                                    "time_range": (points[i-1]["timestamp"], points[p]["timestamp"])
                                }
                        stay_points.append(current_stay_point)  
                        p = i
                        s_found = 1
                        break
                    else: 
                        break    
                elif i == len(points) - 1 and time_difference >= time_threshold:
                        current_stay_point = {
                                    "person_id": points[p]["person_id"],
                                    "id": len(stay_points) + 1,
                                    "coordinates": calculate_avg_coordinates(cluster_stay_points),
                                    "time_range": (points[i-1]["timestamp"], points[p]["timestamp"])
                                }
                        stay_points.append(current_stay_point)
                        s_found = 1
                        break
                elif i == len(points):
                    break
                
                cluster_stay_points["points"].append(points[i])
                i = i+1
            else: 
                p += 1

        if s_found == 0:
            p += 1

    return stay_points

def stay_point_detection_trace(points, distance_threshold, time_threshold):
    p = 0
    i = 0
    stay_points = []
    print(len(points))

    while p < len(points):
        cluster_stay_points = {"points": []}
        i = p+1
        s_found = 0
        cluster_stay_points["points"].append(points[p])

        while i < len(points):
            distance = calculate_distance(points[p]["coordinates"], points[i]["coordinates"])
            time_difference = (points[i-1]["timestamp"].timestamp() - points[p]["timestamp"].timestamp())

            if points[p]["person_id"] == points[i]["person_id"] and points[p]["trace_id"] == points[i]["trace_id"]:
                if distance >= distance_threshold:   
                    if time_difference >= time_threshold:
                        current_stay_point = {
                                    "person_id": points[p]["person_id"],
                                    "trace_id": points[p]["trace_id"],
                                    "id": len(stay_points) + 1,
                                    "coordinates": calculate_avg_coordinates(cluster_stay_points),
                                    "time_range": (points[i-1]["timestamp"], points[p]["timestamp"])
                                }
                        stay_points.append(current_stay_point)  
                        p = i
                        s_found = 1
                        break
                    else: 
                        break    
                elif i == len(points) - 1 and time_difference >= time_threshold:
                        current_stay_point = {
                                    "person_id": points[p]["person_id"],
                                    "trace_id": points[p]["trace_id"],
                                    "id": len(stay_points) + 1,
                                    "coordinates": calculate_avg_coordinates(cluster_stay_points),
                                    "time_range": (points[i-1]["timestamp"], points[p]["timestamp"])
                                }
                        stay_points.append(current_stay_point)
                        s_found = 1
                        break
                elif i == len(points):
                    break
                
                cluster_stay_points["points"].append(points[i])
                i = i+1
            else: 
                p += 1

        if s_found == 0:
            p += 1

    return stay_points


def nearest_neighbor_search(stay_points, interest_points, distance_threshold):
    stay_points_coords = [point['avg_coordinates'] for point in stay_points]
    interest_points_coords = [point['coordinates'] for point in interest_points]

    stay_tree = cKDTree(stay_points_coords)
    interest_tree = cKDTree(interest_points_coords)

    result = []

    for stay_point in stay_points:
        # Cerca il punto di interesse più vicino al punto di stop
        nearest_indices = interest_tree.query_ball_point(stay_point['avg_coordinates'], r=distance_threshold)

        if nearest_indices:
            min_distance = float('inf')
            closest_interest = None

            for idx in nearest_indices:
                distance = calculate_distance(stay_point['avg_coordinates'], interest_points[idx]['coordinates'])
                if distance < min_distance:
                    closest_interest = interest_points[idx]
                    min_distance = distance

            if closest_interest:
                result.append({
                    "person_id": stay_point['person_id'],
                    "label": closest_interest["label"],
                    "distance": min_distance,
                    "start_time": stay_point['start_time'],
                    "end_time": stay_point['end_time']
                })

    for stay_point in stay_points:
        found = False
        for point in result:
            if point['person_id'] == stay_point['person_id'] and point['start_time'] == stay_point['start_time']:
                found = True
                break
        if not found:
            result.append({
                "person_id": stay_point['person_id'],
                "label": "*",
                "distance": None,
                "start_time": stay_point['start_time'],
                "end_time": stay_point['end_time']
            })

    filtered_result = [point if point['distance'] is not None and point['distance'] < distance_threshold
                      else {**point, "label": "*"}
                      for point in result]

    filtered_result.sort(key=itemgetter('person_id', 'start_time'))

    return filtered_result


def nearest_neighbor_search_old(stay_points, interests_points, distance_threshold):
    result = []
    filtered_result = []

    for stay_point in stay_points:
        closest_interest = None
        min_distance = float('inf')  # Inizializza con una distanza infinita

        for interest_point in interests_points:
            distance = calculate_distance(stay_point['avg_coordinates'], interest_point['coordinates'])

            if distance < min_distance:
                closest_interest = interest_point
                min_distance = distance
        
        if closest_interest:
            result.append({
                "person_id": stay_point['person_id'],
                "label": closest_interest["label"],
                "distance": min_distance,
                "start_time": stay_point['start_time'],
                "end_time": stay_point['end_time']
            })
    # Filtra i punti con distanza minore di distance_thrashold
    for point in result:
        if point['distance'] < distance_threshold:
            filtered_result.append(point)
        else:
            point["label"] = "*"  # Imposta il campo label a "*"
            point["distance"] = None
            filtered_result.append(point)
    # Ordina per label
    #filtered_result.sort(key=lambda x: x['person_id'], x['start_time'])
    filtered_result.sort(key=itemgetter('person_id', 'start_time'))
    return filtered_result


def nearest_neighbor_search_with_trace(stay_points, interest_points, distance_threshold):
    stay_points_coords = [(point['avg_coordinates']) for point in stay_points]
    interest_points_coords = [(point['coordinates']) for point in interest_points]

    stay_tree = cKDTree(stay_points_coords, compact_nodes=False)
    interest_tree = cKDTree(interest_points_coords, compact_nodes=False)

    result = []

    for stay_point in stay_points:
        # Cerca il punto di interesse più vicino al punto di stop
        nearest_indices = interest_tree.query_ball_point((stay_point['avg_coordinates']), r=distance_threshold)

        if nearest_indices:
            min_distance = float('inf')
            closest_interest = None

            for idx in nearest_indices:
                distance = calculate_distance(stay_point['avg_coordinates'], interest_points[idx]['coordinates'])
                if distance < min_distance:
                    closest_interest = interest_points[idx]
                    min_distance = distance

            if closest_interest:
                result.append({
                    "person_id": stay_point['person_id'],
                    "trace_id": stay_point['trace_id'],
                    "label": closest_interest["label"],
                    "distance": min_distance,
                    "start_time": stay_point['start_time'],
                    "end_time": stay_point['end_time']
                })

    for stay_point in stay_points:
        found = False
        for point in result:
            if point['person_id'] == stay_point['person_id'] and point['trace_id'] == stay_point['trace_id'] and point['start_time'] == stay_point['start_time']:
                found = True
                break
        if not found:
            result.append({
                "person_id": stay_point['person_id'],
                "trace_id": stay_point['trace_id'],
                "label": "*",
                "distance": None,
                "start_time": stay_point['start_time'],
                "end_time": stay_point['end_time']
            })

    filtered_result = [point if point['distance'] is not None and point['distance'] < distance_threshold
                      else {**point, "label": "*"}
                      for point in result]

    filtered_result.sort(key=itemgetter('person_id', 'trace_id', 'start_time'))

    return filtered_result


def nearest_neighbor_search_with_trace_old(stay_points, interests_points, distance_threshold):
    result = []
    filtered_result = []

    for stay_point in stay_points:
        closest_interest = None
        min_distance = float('inf')  # Inizializza con una distanza infinita

        for interest_point in interests_points:
            distance = calculate_distance(stay_point['avg_coordinates'], interest_point['coordinates'])

            if distance < min_distance:
                closest_interest = interest_point
                min_distance = distance
        
        if closest_interest:
            result.append({
                "person_id": stay_point['person_id'],
                "trace_id" : stay_point['trace_id'],
                "label": closest_interest["label"],
                "distance": min_distance,
                "start_time": stay_point['start_time'],
                "end_time": stay_point['end_time']
            })
    for point in result:
        if point['distance'] < distance_threshold:
            filtered_result.append(point)
        else:
            point["label"] = "*"  # Imposta il campo label a "*"
            point["distance"] = None
            filtered_result.append(point)
    # Ordina per label
    #filtered_result.sort(key=lambda x: x["person_id"], x["trace_id"], x["start_time"], x["label"])
    filtered_result.sort(key=itemgetter('person_id', 'trace_id', 'start_time'))             
    return filtered_result

def visit_detection(matching_poi, t_difference_thrashold=None):
    visits = []

    if t_difference_thrashold is None:
        current_visit = None  # Inizializza la visita corrente a None
        for point in matching_poi:
            if point['label'] != "*":
                if current_visit is None:
                    # Se è la prima visita, inizializza la visita corrente
                    current_visit = {
                        'person_id': point['person_id'],
                        'label': point['label'],
                        'start_time': point['start_time'],
                        'end_time': point['end_time']
                    }
                elif point['person_id'] == current_visit['person_id'] and point['label'] == current_visit['label']:
                    # Se il punto ha lo stesso person_id e label della visita corrente, aggiorna l'end_time
                    current_visit['end_time'] = point['end_time']
                else:
                    # Altrimenti, la visita è finita, aggiungila alla lista delle visite e inizializza una nuova visita
                    visits.append(current_visit)
                    current_visit = {
                        'person_id': point['person_id'],
                        'label': point['label'],
                        'start_time': point['start_time'],
                        'end_time': point['end_time']
                    }
            else:
                visits.append(current_visit)
                current_visit = {
                        'person_id': point['person_id'],
                        'label': point['label'],
                        'start_time': point['start_time'],
                        'end_time': point['end_time']
                    }
            # Aggiungi l'ultima visita (se esiste)
        if current_visit is not None:
            visits.append(current_visit)
        
        return visits
    else:
        current_visit = None
        for i in range(len(matching_poi)):
            current_point = matching_poi[i]
            #print(current_point)
            if matching_poi[i]['label'] != "*":
                
                if current_visit is None:
                    current_visit = {
                        'person_id': current_point['person_id'],
                        'label': current_point['label'],
                        'start_time': current_point['start_time'],
                        'end_time': current_point['end_time']
                    }
                elif current_point['person_id'] == current_visit['person_id'] and current_point['label'] == current_visit['label']:
                    previous_point = matching_poi[i - 1]

                    # Converti le stringhe di timestamp in oggetti datetime
                    start_time = datetime.strptime(previous_point['end_time'], '%Y-%m-%d %H:%M:%S.%f')
                    end_time = datetime.strptime(current_point['start_time'], '%Y-%m-%d %H:%M:%S.%f')
                    time_difference = (end_time.timestamp() - start_time.timestamp())

                    if time_difference <= t_difference_thrashold:
                        current_visit['end_time'] = current_point['end_time']
                    else: 
                        visits.append(current_visit)
                        current_visit = {
                        'person_id': current_point['person_id'],
                        'label': current_point['label'],
                        'start_time': current_point['start_time'],
                        'end_time': current_point['end_time']
                    }    
                else:
                    visits.append(current_visit)
                    current_visit = {
                        'person_id': current_point['person_id'],
                        'label': current_point['label'],
                        'start_time': current_point['start_time'],
                        'end_time': current_point['end_time']
                    }
            else:
                visits.append(current_visit)
                current_visit = {
                        'person_id': current_point['person_id'],
                        'label': current_point['label'],
                        'start_time': current_point['start_time'],
                        'end_time': current_point['end_time']
                }
        if current_visit is not None:
            visits.append(current_visit)

        return visits

def visit_detection_with_trace(matching_poi, t_difference_thrashold=None):
    visits = []        
    
    if t_difference_thrashold is None:
        current_visit = None  # Inizializza la visita corrente a None
        for point in matching_poi:
            if point['label'] != "*":
                if current_visit is None:
                    # Se è la prima visita, inizializza la visita corrente
                    current_visit = {
                        'person_id': point['person_id'],
                        'trace_id': point['trace_id'],
                        'label': point['label'],
                        'start_time': point['start_time'],
                        'end_time': point['end_time']
                    }
                elif point['person_id'] == current_visit['person_id'] and point['label'] == current_visit['label'] and point['trace_id'] == current_visit['trace_id']:
                    # Se il punto ha lo stesso person_id e label della visita corrente, aggiorna l'end_time
                    current_visit['end_time'] = point['end_time']
                else:
                    # Altrimenti, la visita è finita, aggiungila alla lista delle visite e inizializza una nuova visita
                    visits.append(current_visit)
                    current_visit = {
                        'person_id': point['person_id'],
                        'trace_id': point['trace_id'],
                        'label': point['label'],
                        'start_time': point['start_time'],
                        'end_time': point['end_time']
                    }
            else:
                visits.append(current_visit)
                current_visit = {
                        'person_id': point['person_id'],
                        'trace_id': point['trace_id'],
                        'label': point['label'],
                        'start_time': point['start_time'],
                        'end_time': point['end_time']
                    }    
        # Aggiungi l'ultima visita (se esiste)
        if current_visit is not None:
            visits.append(current_visit)

        return visits
    else:
        current_visit = None
        for i in range(len(matching_poi)):
            current_point = matching_poi[i]
            if matching_poi[i]['label'] != "*": 
                if current_visit is None:
                    current_visit = {
                        'person_id': current_point['person_id'],
                        'trace_id': current_point['trace_id'],
                        'label': current_point['label'],
                        'start_time': current_point['start_time'],
                        'end_time': current_point['end_time']
                    }
                elif current_point['person_id'] == current_visit['person_id'] and current_point['label'] == current_visit['label'] and current_point['trace_id'] == current_visit['trace_id']:
                    previous_point = matching_poi[i - 1]

                    # Converti le stringhe di timestamp in oggetti datetime
                    start_time = datetime.strptime(previous_point['end_time'], '%Y-%m-%d %H:%M:%S.%f')
                    end_time = datetime.strptime(current_point['start_time'], '%Y-%m-%d %H:%M:%S.%f')
                    time_difference = (end_time.timestamp() - start_time.timestamp())

                    if time_difference <= t_difference_thrashold:
                        current_visit['end_time'] = current_point['end_time']
                    else: 
                        visits.append(current_visit)
                        current_visit = {
                        'person_id': current_point['person_id'],
                        'trace_id': current_point['trace_id'],
                        'label': current_point['label'],
                        'start_time': current_point['start_time'],
                        'end_time': current_point['end_time']
                    }    
                else:
                    visits.append(current_visit)
                    current_visit = {
                        'person_id': current_point['person_id'],
                        'trace_id': current_point['trace_id'],
                        'label': current_point['label'],
                        'start_time': current_point['start_time'],
                        'end_time': current_point['end_time']
                    }
            else:
                visits.append(current_visit)
                current_visit = {
                        'person_id': current_point['person_id'],
                        'trace_id': current_point['trace_id'],
                        'label': current_point['label'],
                        'start_time': current_point['start_time'],
                        'end_time': current_point['end_time']
                }
        if current_visit is not None:
            visits.append(current_visit)

        return visits

def read_interests_points_from_csv(file_path):
    # Legge i dati dal file CSV ignorando la prima riga e restituisce una lista di punti con le coordinate e relativo label   
    data = pd.read_csv(file_path, header=None, skiprows=[0])
    interests_points = []

    for _, row in data.iterrows():
        point = {
            "label" : row[0],  # Indice numerico della colonna del label
            "coordinates": (row[1], row[2])  # Indici numerici delle colonne x e y
        }
        interests_points.append(point)
        
    return interests_points

def read_matching_points_from_csv(file_path, trace_id=False):
    data = pd.read_csv(file_path, header=None, skiprows=[0])
    matching_points = []   

    if not trace_id:
        for _, row in data.iterrows():
            point = {
                "person_id" : row[0], 
                "label": row[1], 
                "distance":(row[2]),
                "start_time": (row[3]),
                "end_time": (row[4]),
            }
            matching_points.append(point)
    else:    
        for _, row in data.iterrows():
            point = {
                "person_id" : row[0],
                "trace_id": row[1],
                "label": row[2],
                "distance":(row[3]),
                "start_time": (row[4]),
                "end_time": (row[5]),
            }
            matching_points.append(point)
        
    return matching_points

def read_stay_points_from_csv(file_path, trace_id=False):
    # Legge i dati dal file CSV ignorando la prima riga e restituisce una lista di punti con person_id, coordinates e start/end time e duration  
    data = pd.read_csv(file_path, header=None, skiprows=[0])
    stay_points = []

    if not trace_id:
        for _, row in data.iterrows():
            point = {
                "person_id" : row[0],  # Indice numerico della colonna del label
                "avg_coordinates": (row[1],row[2]),  # Indici numerici delle colonne x e y
                "start_time": (row[3]),
                "end_time": (row[4]),
                "duration":(row[5])
            }
            stay_points.append(point)
    else:
        for _, row in data.iterrows():
            point = {
                "person_id" : row[0],  # Indice numerico della colonna del label
                "trace_id": row[1],
                "avg_coordinates": (row[2],row[3]),  # Indici numerici delle colonne x e y
                "start_time": (row[4]),
                "end_time": (row[5]),
                "duration":(row[6])
            }
            stay_points.append(point) 

    return stay_points

def read_trajectory_from_csv(file_path):
    # Legge i dati dal file CSV ignorando la prima riga e restituisce una lista di punti con le coordinate e il timestamp
    data = pd.read_csv(file_path, header=None, skiprows=[0])
    trajectory = []
    #controlla il numero di colonne
    if data.shape[1] == 4:
        for _, row in data.iterrows():
            # Converti la parte temporale in un formato datetime
            timestamp_with_microseconds = datetime.strptime(row[1], "%Y-%m-%d %H:%M:%S.%f")
            timestamp = timestamp_with_microseconds

            point = {
                "person_id": row[0],  # Indice numerico della colonna del person_id
                "coordinates": (row[2], row[3]),  # Indici numerici delle colonne x e y
                "timestamp": timestamp  # Indice numerico della colonna timeStamp
            }
            trajectory.append(point)
    
            trajectory.sort(key=lambda x: (x['person_id'], x['timestamp']))

    elif data.shape[1] == 5:
        for _, row in data.iterrows():
            # Converti la parte temporale in un formato datetime
            timestamp_with_microseconds = datetime.strptime(row[4], "%Y-%m-%d %H:%M:%S.%f")
            timestamp = timestamp_with_microseconds

            point = {
                "person_id": row[0],  # Indice numerico della colonna del person_id
                "trace_id": row[1],
                "coordinates": (row[2], row[3]),  # Indici numerici delle colonne x e y
                "timestamp": timestamp  # Indice numerico della colonna timeStamp
            }
            trajectory.append(point)
    
            trajectory.sort(key=lambda x: (x['person_id'], x['trace_id'], x['timestamp'])) 

    return trajectory

def write_stay_points_to_csv(stay_points, output_file, trace_id=False):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        # Scrivi l'intestazione del file CSV
        if not trace_id:
            writer.writerow(["person_id", "avg_x", "avg_y", "start_time", "end_time", "duration"])

            for point in stay_points:
                start_time = point["time_range"][1].strftime("%Y-%m-%d %H:%M:%S.%f")
                end_time = point["time_range"][0].strftime("%Y-%m-%d %H:%M:%S.%f")
                duration = point["time_range"][0] - point["time_range"][1]
                duration_str = str(duration)
                avg_x, avg_y = point["coordinates"][0], point["coordinates"][1]

                writer.writerow([point["person_id"], avg_x, avg_y, start_time, end_time, duration_str])
        else:
            writer.writerow(["person_id", "trace_id", "avg_x", "avg_y", "start_time", "end_time", "duration"])

            for point in stay_points:
                start_time = point["time_range"][1].strftime("%Y-%m-%d %H:%M:%S.%f")
                end_time = point["time_range"][0].strftime("%Y-%m-%d %H:%M:%S.%f")
                duration = point["time_range"][0] - point["time_range"][1]
                duration_str = str(duration)
                avg_x, avg_y = point["coordinates"][0], point["coordinates"][1]

                writer.writerow([point["person_id"], point["trace_id"], avg_x, avg_y, start_time, end_time, duration_str])          

def write_matching_poi_to_csv(matching_poi, output_file, trace_id=False):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        # Scrivi l'intestazione del file CSV
        if not trace_id:
            writer.writerow(["person_id", "label", "distance", "start_time", "end_time"])

            for point in matching_poi:
                writer.writerow([point["person_id"], point["label"], point["distance"], point["start_time"], point["end_time"]])
        else:
            writer.writerow(["person_id", "trace_id", "label", "distance", "start_time", "end_time"])

            for point in matching_poi:
                writer.writerow([point["person_id"], point["trace_id"], point["label"], point["distance"], point["start_time"], point["end_time"]])

def write_visits_to_csv(visits, output_file, trace_id=False):
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file, delimiter=',')
        # Scrivi l'intestazione del file CSV
        if not trace_id:
            writer.writerow(["person_id", "label", "start_time", "end_time"])

            for point in visits:
                writer.writerow([point["person_id"], point["label"], point["start_time"], point["end_time"]])
        else:
            writer.writerow(["person_id", "trace_id", "label", "start_time", "end_time"])

            for point in visits:
                writer.writerow([point["person_id"], point["trace_id"], point["label"], point["start_time"], point["end_time"]])

def print_stay_points_table(stay_points, trace_id=False):
    # Mostra i risultati in una tabella
    table = PrettyTable()
    if not trace_id:
        table.field_names = ["person_ID", "Coordinates", "Start Time", "End Time", "Duration"]
        
        for point in stay_points:
            start_time = point["time_range"][1].strftime("%Y-%m-%d %H:%M:%S.%f")
            end_time = point["time_range"][0].strftime("%Y-%m-%d %H:%M:%S.%f")
            duration = point["time_range"][0] - point["time_range"][1]
            duration_str = str(duration)
            #duration_minutes = (point["time_range"][1] - point["time_range"][0]).seconds / 60
            avg_coordinates = (point["coordinates"][0], point["coordinates"][1])
            
            table.add_row([point["person_id"], avg_coordinates, start_time, end_time, duration_str])
        
        print(table)
    else:  
        table.field_names = ["person_ID", "trace_id", "Coordinates", "Start Time", "End Time", "Duration"]
        
        for point in stay_points:
            start_time = point["time_range"][1].strftime("%Y-%m-%d %H:%M:%S.%f")
            end_time = point["time_range"][0].strftime("%Y-%m-%d %H:%M:%S.%f")
            duration = point["time_range"][0] - point["time_range"][1]
            duration_str = str(duration)
            #duration_minutes = (point["time_range"][1] - point["time_range"][0]).seconds / 60
            avg_coordinates = (point["coordinates"][0], point["coordinates"][1])
            
            table.add_row([point["person_id"], point["trace_id"], avg_coordinates, start_time, end_time, duration_str])
        
        print(table)  

def print_matching_poi_table(matching_poi, trace_id=False):
    # Mostra i risultati in una tabella
    table = PrettyTable()
    if not trace_id:
        table.field_names = ["Person_ID", "Label", "Distance", "Start Time", "End Time"]
        
        for point in matching_poi:
            table.add_row([point["person_id"], point["label"], point["distance"], point["start_time"], point["end_time"]])
        
        print(table)
    else:  
        table.field_names = ["Person_ID","Trace_id", "Label", "Distance", "Start Time", "End Time"]
        
        for point in matching_poi:
            table.add_row([point["person_id"], point["trace_id"], point["label"], point["distance"], point["start_time"], point["end_time"]])
        
        print(table)

def print_visits_table(visits, trace_id=False):
    # Mostra i risultati in una tabella
    table = PrettyTable()
    if not trace_id:
        table.field_names = ["Person_ID", "Label", "Start Time", "End Time"]
        
        for point in visits:
            table.add_row([point["person_id"], point["label"], point["start_time"], point["end_time"]])
            
        print(table)
    else:  
        table.field_names = ["Person_ID","Trace_id", "Label", "Start Time", "End Time"]
        
        for point in visits:
            table.add_row([point["person_id"], point["trace_id"], point["label"], point["start_time"], point["end_time"]])
        
        print(table)

def run_spd(input_file, distance_threshold, temporal_threshold, output_file, trace_id=False):
    trajectory = read_trajectory_from_csv(input_file)

    if not trace_id:
        # Esegui stay_point_detection senza trace_id
        stay_points = stay_point_detection(trajectory, distance_threshold, temporal_threshold)
        write_stay_points_to_csv(stay_points, output_file)
        print_stay_points_table(stay_points)
        
    else:
        # Esegui stay_point_detection_trace con trace_id
        stay_points = stay_point_detection_trace(trajectory, distance_threshold, temporal_threshold)
        write_stay_points_to_csv(stay_points, output_file, trace_id=True)
        print_stay_points_table(stay_points, trace_id=True)

def run_nns(poi_file, stops_file, distance_threshold, output_file, trace_id=False):
    if not trace_id: 
        interests_points = read_interests_points_from_csv(poi_file)
        stay_points = read_stay_points_from_csv(stops_file)
        
        matching_poi = nearest_neighbor_search(stay_points, interests_points, distance_threshold)
        print_matching_poi_table(matching_poi)
        write_matching_poi_to_csv(matching_poi, output_file)

    else:
        interests_points = read_interests_points_from_csv(poi_file)
        stay_points = read_stay_points_from_csv(stops_file, trace_id=True)

        matching_poi = nearest_neighbor_search_with_trace(stay_points, interests_points, distance_threshold)
        print_matching_poi_table(matching_poi, trace_id=True)
        write_matching_poi_to_csv(matching_poi, output_file, trace_id=True)
        

def run_vd(matching_poi, output_file, t_difference_thrashold=None, trace_id=False):
    if not trace_id:
        if t_difference_thrashold is None:
            matching_poi = read_matching_points_from_csv(matching_poi) 
            visits = visit_detection(matching_poi)
            print_visits_table(visits)
            write_visits_to_csv(visits, output_file)
        else:
            matching_poi = read_matching_points_from_csv(matching_poi) 
            visits = visit_detection(matching_poi, t_difference_thrashold)
            print_visits_table(visits)
            write_visits_to_csv(visits, output_file)
    else:
        if t_difference_thrashold is None:
            matching_poi = read_matching_points_from_csv(matching_poi, trace_id=True)
            visits = visit_detection_with_trace(matching_poi)
            #print(visits)
            print_visits_table(visits, trace_id=True)
            write_visits_to_csv(visits, output_file, trace_id=True)
        else:
            matching_poi = read_matching_points_from_csv(matching_poi, trace_id=True)
            visits = visit_detection_with_trace(matching_poi, t_difference_thrashold)
            print_visits_table(visits, trace_id=True) 
            write_visits_to_csv(visits, output_file, trace_id=True) 


def immpy():
    print("""
    ██╗  ██╗███╗   ██╗██╗███████╗██╗  ██╗
    ██║  ██║████╗  ██║██║██╔════╝██║ ██╔╝
    ███████║██╔██╗ ██║██║███████╗█████╔╝ 
    ██╔══██║██║╚██╗██║██║╚════██║██╔═██╗ 
    ██║  ██║██║ ╚████║██║███████║██║  ██╗
    ╚═╝  ╚═╝╚═╝  ╚═══╝╚═╝╚══════╝╚═╝  ╚═╝
    """)