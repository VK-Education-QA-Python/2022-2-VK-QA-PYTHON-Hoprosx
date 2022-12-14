from mysql import MysqlClient
from flask import Flask, make_response, jsonify

app = Flask(__name__)


@app.route('/vk_id/<username>', methods=['GET'])
def get_user_vk_id(username):
    """Возвращает id пользователя"""
    with sql.connection.cursor() as cursor:
        cursor.execute(f'''SELECT id FROM test_users
                                where username = "{username}";''')
        vk_id = cursor.fetchone().get('id')

    if vk_id:
        response = make_response(jsonify({'vk_id': vk_id}), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(jsonify({}), 404)
        response.headers['Content-Type'] = 'application/json'
        return response


if __name__ == '__main__':
    sql = MysqlClient(db_name='vkeducation',
                      user='root',
                      password='password')
    sql.connect()
    app.run(host='0.0.0.0')
