import json


def convertPythonDataIntoJsonData(serial, column):
    try:
        jsonData = []
        print("hi*****************************************************************************************************")
        for data in serial:
            pythonData = dict(zip(column, data))
            print(pythonData)
            jsonData.append(pythonData)
        # return json.dumps(jsonData, default=str), None
        return jsonData, None
    except Exception as error:
        return None, error
