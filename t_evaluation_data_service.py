import json
from evaluation_data_service import EvaluationMatrix, EvaluationDataService

def get_data_service():

    config = {
        "data_directory": "data",
        "data_file": "evaluation.json"
    }

    ds = EvaluationDataService(config)
    return ds

def t1():

    ds = get_data_service()
    results = ds.get_result()
    print("t1: results = ", json.dumps(results, indent=4))

    
    print("=================")

    ds.create_result(
        id = '4',
        frames = ["Travel", "Aging"],
        settings = ["zero-shot", "rhetorical"],
        blending_result = "test result",
        evaluations = EvaluationMatrix(
            completeness = 4,
            clarity = 4,
            relevance = 4,
            depth_of_understanding = 4,
            coherence = 4,
            execute_time = 4,
            additional_notes = "It is good, too"
        )
    )

    print('===================')
    ds = get_data_service()
    results = ds.get_result()
    print("t1: results = ", json.dumps(results, indent=4))

if __name__ == "__main__":
    t1()
