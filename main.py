from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/', methods=['GET'])
def index():
    return "Hello, world!"

@app.route('/calculate', methods=['POST'])
def calculate():
    # 클라이언트로부터 받은 JSON 데이터 처리
    received_data = request.json
    print("Received data:", received_data)

    # 결과를 담을 리스트 초기화
    result = []
    result1 = []

    # 각 세트별로 평균값과 Pass/Fail 계산
    for set_data in received_data:
        # '데이터' 값만 추출하여 숫자로 변환
        data_values = [float(row['data']) for row in set_data['rows'] if 'data' in row]

        # '기준값'과 '허용 공차' 추출
        standard_value = float(set_data['standardValue'])
        tolerance = float(set_data['tolerance'])

        # 평균값 계산
        if data_values:
            data_avg = sum(data_values) / len(data_values)
        else:
            data_avg = 0

        # 각 행의 Pass/Fail 결정
        pass_fail_list = []
        for data in data_values:
            lower_bound = standard_value - tolerance
            upper_bound = standard_value + tolerance
            if lower_bound <= data <= upper_bound:
                pass_fail_list.append('P')
            else:
                pass_fail_list.append('F')

        # 평균값과 Pass/Fail 결과를 세트에 추가
        set_result1 ={"pass_fail": pass_fail_list,
                      "data_avg": data_avg,}
        print(set_result1)
        result1.append(set_result1)

    # 결과를 JSON 형태로 반환
    return jsonify(result1)

if __name__ == "__main__":
    app.run(debug=True)