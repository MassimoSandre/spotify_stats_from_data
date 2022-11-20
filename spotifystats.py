import json
import datetime
import os.path


class SpotifyStats:
    def __init__(self, source_file_name_root="endsong_") -> None:
        self.__source_file_name_root = source_file_name_root
        self.__data = None


    # ======================= FILE AND DATA HANDLING =======================
    def load_data(self):
        self.__data = self.join_files()

    ##### file joining
    def join_files(self):
        index = 0
        full_data = []
        while os.path.isfile(self.__source_file_name_root+str(index)+".json"):
            data = self.get_data_from_file(self.__source_file_name_root+str(index)+".json")
            full_data = [*full_data,*data]
            index+=1
        return full_data

    ##### file joining and saving to file
    def join_files_and_save_to_file(self, to_file='streaming_history.json'):
        self.__data = self.join_files()
        self.save_data_in_file(to_file)
        

    ##### get json data from file
    def get_data_from_file(self,from_file):
        f = open(from_file,"r", encoding="utf8")
        self.__data = json.load(f)
        f.close()

    ##### put json data in file
    def save_data_in_file(self,to_file):
        f = open(to_file,"w",encoding="utf8")
        json.dump(self.__data,f,indent=4)
        f.close()

    # ======================= SORTING BY TIMESTAMP =======================
    ##### json file sorting by timestamp
    def sort_file_by_timestamp(self, from_file="streaming_history.json", to_file=''):
        if to_file == '':
            to_file = from_file
        self.__data = self.get_data_from_file(from_file)
        self.sort_data_by_timestamp()
        self.save_data_in_file(self.__data,to_file)

    ##### json data sorting by timestamp
    def sort_data_by_timestamp(self):
        def fkey(e):
            return datetime.datetime.strptime(e["ts"],"%Y-%m-%dT%H:%M:%SZ")
        self.__data.sort(key=fkey)


    # ======================= STREAMING TIME BY INTERVAL =======================
    ##### streaming time calculator
    def streaming_time_by_interval(self,from_date='', to_date=''):
        if from_date == '':
            from_date = datetime.datetime.strptime("1999", "%Y")
        else:
            from_date = datetime.datetime.strptime(from_date,"%Y-%m-%d")
        if to_date == '':
            to_date = datetime.datetime.now()
        else:
            to_date = datetime.datetime.strptime(to_date,"%Y-%m-%d")
        
        self.sort_data_by_timestamp(self.__data)

        i = 0
        total_time = 0
        while i < len(self.__data) and datetime.datetime.strptime(self.__data[i]["ts"],"%Y-%m-%dT%H:%M:%SZ") <= to_date:
            if datetime.datetime.strptime(self.__data[i]["ts"],"%Y-%m-%dT%H:%M:%SZ") >= from_date:
                total_time+=self.__data[i]["ms_played"]

            i+=1

        return total_time

    ##### streaming time calculator from file
    def streaming_time_by_interval_and_file(self,from_date='', to_date='', file='streaming_history.json'):
        self.__data = self.get_data_from_file(file)
        return self.streaming_time_by_interval(from_date, to_date)

    # ======================= NUMBER OF TRACKS BY INTERVAL =======================
    ##### number of tracks streamed by interval
    def no_tracks_by_interval(self, from_date='', to_date=''):
        if from_date == '':
            from_date = datetime.datetime.strptime("1999", "%Y")
        else:
            from_date = datetime.datetime.strptime(from_date,"%Y-%m-%d")
        if to_date == '':
            to_date = datetime.datetime.now()
        else:
            to_date = datetime.datetime.strptime(to_date,"%Y-%m-%d")
        
        self.sort_data_by_timestamp()

        i = 0
        count = 0
        while i < len(self.__data) and datetime.datetime.strptime(self.__data[i]["ts"],"%Y-%m-%dT%H:%M:%SZ") <= to_date:
            if datetime.datetime.strptime(self.__data[i]["ts"],"%Y-%m-%dT%H:%M:%SZ") >= from_date:
                count+=1

            i+=1
        return count

    ##### number of tracks streamed by interval and file
    def no_tracks_by_interval_and_file(self,from_date='', to_date='', file='streaming_history.json'):
        data = self.__get_data_from_file(file)
        return self.__no_tracks_by_interval(from_date, to_date)

    # ======================= NUMBER OF TRACKS BY INTERVAL =======================
    ##### get track information
    def get_tracks_data(self):
        def f(e):
            return e["times_played"]
        tracks = []
        for r in self.__data:
            found = False
            for t in tracks:
                if t["track_name"] == r["master_metadata_track_name"]:
                    found = True
                    t["ms_played"]+=r["ms_played"]
                    t["times_played"]+=1
                    if datetime.datetime.strptime(t["first_ts"],"%Y-%m-%dT%H:%M:%SZ") > datetime.datetime.strptime(r["ts"],"%Y-%m-%dT%H:%M:%SZ"):
                        t["first_ts"] = r["ts"]
            
            if not found:
                tracks.append({})
                tracks[-1]["track_name"] = r["master_metadata_track_name"]
                tracks[-1]["artist_name"] = r["master_metadata_album_artist_name"]
                tracks[-1]["album_name"] = r["master_metadata_album_album_name"]
                tracks[-1]["first_ts"] = r["ts"]
                tracks[-1]["ms_played"] = r["ms_played"]
                tracks[-1]["times_played"] = 1

        tracks.sort(key=f,reverse=True)
        return tracks
                
    #### save track information to file
    def save_tracks_data_to_file(self,to_file="tracks_information.json"):
        tracks_data = self.get_tracks_data()
        self.__save_data_in_file(tracks_data,to_file)
