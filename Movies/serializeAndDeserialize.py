import json


def convertPythonDataIntoJsonData(serial, column):
    """
       this is used for key value pair so that further it will  convert into json data:
    :param serial:this columns data comes from db for
    :param column: this is used for making column name
    :return:it will return column value pair ;
    """
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
