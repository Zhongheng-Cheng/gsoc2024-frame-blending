import json
import os

file_path = "./data/evaluation.json"
dir_name = os.path.dirname(file_path)
if not os.path.exists(dir_name):
    os.makedirs(dir_name)
if not os.path.exists(file_path):
    with open(file_path, 'w') as file:
        file.write('[]')

class Evaluation():
    def __init__(self,
                 completeness: int = 0,
                 clarity: int = 0,
                 relevance: int = 0,
                 depth_of_understanding: int = 0,
                 coherence: int = 0,
                 execute_time:int = 0,
                 additional_notes: str = None,
                 ):
        self.matrix = {
            "completeness": completeness,
            "clarity": clarity,
            "relevance": relevance,
            "depth_of_understanding": depth_of_understanding,
            "coherence": coherence,
            "execute_time": execute_time,
            "additional_notes": additional_notes,
        }
    
    def to_dict(self):
        return self.matrix


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
            self.users = json.load(in_file)

    def _save(self):
        fn = self._get_data_file_name()
        with open(fn, "w") as out_file:
            json.dump(self.users, out_file)

    def get_result(self,
                   id: str = None,
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
                      id: str = None,
                      frames: list = None,
                      settings: list = None,
                      blending_result: str = None,
                      evaluations: Evaluation = None,
                      ):
        if id in [result["id"] for result in self.blending_results]:
            print(f"result id: {id} already exists")
            return
        self.blending_results.append({
            "id": id,
            "frames": frames,
            "settings": settings,
            "blending_result": blending_result,
            "evaluations": [evaluations.to_dict()],
        })
        self._save()
        return
    
    def insert_evaluation(self,
                          evaluation: Evaluation,
                          id: str = None,
                          frames: list = None,
                          settings: list = None,
                          ):
        target_results = self.get_result(id, frames, settings)
        for result in target_results:
            result["evaluations"].append(evaluation)
        self._save()
