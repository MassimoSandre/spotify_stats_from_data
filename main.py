import json
import datetime
import os.path

##### file joining
def join_files(to_file='streaming_history.json'):
    index = 0
    full_data = []
    while os.path.isfile("endsong_"+str(index)+".json"):
        data = get_data_from_file("endsong_"+str(index)+".json")
        full_data = [*full_data,*data]
        index+=1
    save_data_in_file(full_data,to_file)
    
##### get json data from file
def get_data_from_file(from_file="streaming_history.json"):
    f = open(from_file,"r", encoding="utf8")
    data = json.load(f)
    f.close()
    return data

##### put json data in file
def save_data_in_file(data,to_file="streaming_history.json"):
    f = open(to_file,"w",encoding="utf8")
    json.dump(data,f,indent=4)
    f.close()

##### json file sorting by timestamp
def sort_file_by_timestamp(from_file="streaming_history.json", to_file=''):
    if to_file == '':
        to_file = from_file
    data = get_data_from_file(from_file)
    data = sort_data_by_timestamp(data)
    save_data_in_file(data,to_file)

##### json data sorting by timestamp
def sort_data_by_timestamp(data):
    def fkey(e):
        return datetime.datetime.strptime(e["ts"],"%Y-%m-%dT%H:%M:%SZ")
    data.sort(key=fkey)
    return data
    
##### streaming time calculator
def streaming_time_by_interval(data ,from_date='', to_date=''):
    if from_date == '':
        from_date = datetime.datetime.strptime("1999", "%Y")
    else:
        from_date = datetime.datetime.strptime(from_date,"%Y-%m-%d")
    if to_date == '':
        to_date = datetime.datetime.now()
    else:
        to_date = datetime.datetime.strptime(to_date,"%Y-%m-%d")
    
    data = sort_data_by_timestamp(data)

    i = 0
    total_time = 0
    while i < len(data) and datetime.datetime.strptime(data[i]["ts"],"%Y-%m-%dT%H:%M:%SZ") <= to_date:
        if datetime.datetime.strptime(data[i]["ts"],"%Y-%m-%dT%H:%M:%SZ") >= from_date:
            total_time+=data[i]["ms_played"]

        i+=1

    return total_time

##### streaming time calculator from file
def streaming_time_by_interval_and_file(from_date='', to_date='', file='streaming_history.json'):
    data = get_data_from_file(file)
    return streaming_time_by_interval(data)

##### number of tracks streamed by interval
def no_tracks_by_interval(data, from_date='', to_date=''):
    if from_date == '':
        from_date = datetime.datetime.strptime("1999", "%Y")
    else:
        from_date = datetime.datetime.strptime(from_date,"%Y-%m-%d")
    if to_date == '':
        to_date = datetime.datetime.now()
    else:
        to_date = datetime.datetime.strptime(to_date,"%Y-%m-%d")
    
    data = sort_data_by_timestamp(data)

    i = 0
    count = 0
    while i < len(data) and datetime.datetime.strptime(data[i]["ts"],"%Y-%m-%dT%H:%M:%SZ") <= to_date:
        if datetime.datetime.strptime(data[i]["ts"],"%Y-%m-%dT%H:%M:%SZ") >= from_date:
            count+=1

        i+=1
    return count

##### number of tracks streamed by interval and file
def no_tracks_by_interval_and_file(from_date='', to_date='', file='streaming_history.json'):
    data = get_data_from_file(file)
    return no_tracks_by_interval(data, from_date, to_date)


if not os.path.isfile("streaming_history.json"):
    join_files()

#print(streaming_time_by_interval_and_file("2022-09-01", "2022-12-01"))
print(no_tracks_by_interval_and_file())