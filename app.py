import json
from flask import Flask, request, abort
from rainbond_python.parameter import Parameter
from rainbond_python.db_connect import DBConnect
from rainbond_python.error_handler import error_handler

app = Flask(__name__)
error_handler(app)
db = DBConnect(db='dragonli', collection='scripts')


@app.route('/api/1.0/script', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_script():
    parameter = Parameter(request)

    if parameter.method == 'GET':
        param = parameter.verification(
            checking=parameter.param_url, verify={'search': str}, null_value=True)
        find_dict = {'title': {'$regex': param['search']}}
        find_data_list = db.find_docu(find_dict=find_dict)
        return json.dumps(find_data_list)

    elif parameter.method == 'POST':
        param = parameter.verification(checking=parameter.param_json,
                                       verify={'title': str, 'script': str, 'language': str}, optional={'language': 'auto'})
        new_data = db.write_one_docu(docu=param)
        return new_data, 201, []

    elif parameter.method == 'PUT':
        param = parameter.verification(checking=parameter.param_json,
                                       verify={'id': str, 'title': str, 'script': str, 'language': str}, optional={'language': 'auto'})
        find_dict = {'id': param['id']}
        modify_dict = {'title': param['title'], 'script': param['script'], 'language': param['language']}
        update_count = db.update_docu(
            find_docu=find_dict, modify_docu=modify_dict)
        return update_count

    elif parameter.method == 'DELETE':
        param = parameter.verification(
            checking=parameter.param_json, verify={'id': str})
        delete_result = db.delete_docu(
            find_docu={'id': param['id']}, false_delete=True)
        return delete_result


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
