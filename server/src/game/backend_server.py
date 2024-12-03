from flask import Flask, jsonify
import src.game.betting_round as betround

app = Flask(__name__)


@app.route('/getRoundData', methods=['GET'])
def getRoundData():
    data = {
        'message': 'Hello from Flask!',
        'items': [1, 2, 3, 4, 5]
    }
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True)