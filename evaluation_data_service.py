import json
import os

file_path = "./data/evaluation.json"
dir_name = os.path.dirname(file_path)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        file.write('[]')
        

class EvaluationDataService():

    def __init__(self, config: dict):
        """
        :param config: A dictionary of configuration parameters.
        """

        self.data_dir = config['data_directory']
        self.data_file = config["data_file"]
        self.blending_results = []

        self._load()

    def _get_data_file_name(self):
        # TODO Using os.path is better than string concat
        result = self.data_dir + "/" + self.data_file
        return result

    def _load(self):
        fn = self._get_data_file_name()
        with open(fn, "r") as in_file:
            self.blending_results = json.load(in_file)

    def _save(self):
        fn = self._get_data_file_name()
        with open(fn, "w") as out_file:
            json.dump(self.blending_results, out_file, indent=4)

    def get_result(self,
                   id: int = None,
                   frames: list = None,
                   settings: list = None,
                   ) -> list:
        result = []
        for s in self.blending_results:
            if ((id is None or (s.get("id", None) == id)) and \
                    (frames is None or (s.get("frames", None) == frames)) and \
                    (settings is None or (s.get("settings", None) == settings))):
                result.append(s)
        return result
    
    def create_result(self,
                      frames: list = None,
                      settings: list = None,
                      blending_result: str = None,
                      evaluations: dict = None,
                      ):
        id_list = [result["id"] for result in self.blending_results]
        if id_list:
            id = max(id_list) + 1
        else:
            id = 0
        self.blending_results.append({
            "id": id,
            "frames": frames,
            "settings": settings,
            "blending_result": blending_result,
            "evaluations": [evaluations],
        })
        self._save()
        return
    
    def insert_evaluation(self,
                          evaluation: dict,
                          id: int = None,
                          frames: list = None,
                          settings: list = None,
                          ):
        for result in self.blending_results:
            if ((id is None or id == result.get("id", None)) and \
                    (frames is None or frames == result.get("frames", None)) and \
                    (settings is None or settings == result.get("settings", None))):
                result["evaluations"].append(evaluation)
        self._save()
        return

    def delete_result(self,
                      id: int
                      ):
        for i, result in enumerate(self.blending_results):
            if ((id == result.get("id", None))):
                del self.blending_results[i]
        self._save()
        return