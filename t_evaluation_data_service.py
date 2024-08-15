import json
from evaluation_data_service import EvaluationDataService

def show_change(func):
    def wrapper(*args, **kwargs):
        ds = get_data_service()
        results = ds.get_result()
        print("Before = ", json.dumps(results, indent=4))
        print('===================')
        func(*args, **kwargs)
        print('===================')
        ds = get_data_service()
        results = ds.get_result()
        print("After = ", json.dumps(results, indent=4))
        return
    return wrapper
        

def get_data_service():

    config = {
        "data_directory": "data",
        "data_file": "evaluation.json"
    }

    ds = EvaluationDataService(config)
    return ds

def test_get_result():
    ds = get_data_service()
    result = ds.get_result(id=0)
    print(result)
    return

@show_change
def test_create_result():

    ds = get_data_service()

    ds.create_result(
        frames = ["Travel", "Aging"],
        settings = ["zero-shot", "rhetorical"],
        blending_result = "test result",
        evaluations = {
            "completeness": 4,
            "clarity": 4,
            "relevance": 4,
            "depth_of_understanding": 4,
            "coherence": 4,
            "execute_time": 4,
            "additional_notes": "It is good, too"
        }
    )

@show_change
def test_update():
    ds = get_data_service()
    ds.insert_evaluation(
        evaluation = {
            "completeness": 6,
            "clarity": 6,
            "relevance": 6,
            "depth_of_understanding": 6,
            "coherence": 6,
            "execute_time": 6,
            "additional_notes": "It is bad"
        },
        id = 0
    )

@show_change
def test_delete():
    ds = get_data_service()
    ds.delete_result(
        id = 0
    )

if __name__ == "__main__":
    
    test_create_result()
    # test_update()
    # test_get_result()
    # test_delete()