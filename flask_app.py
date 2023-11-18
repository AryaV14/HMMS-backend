from CRUD import fetcher,insertor,user_search
from connect import connector
from flask_cors import CORS
import json 
from flask import Flask , request, jsonify ,session
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'super secret key'
CORS(app)
# conn=None

# global conn 
# just checking

conn,_=connector()

@app.route('/',methods=['POST','GET'])
def home():
    
    return "flask home"

# @app.route('/list',methods=['POST','GET'])
# def list():
#     global conn
#     id=request.json['hostelid']
#     print(type(id))
#     query = f"SELECT * FROM inmate where inmate_id = '{id}';"
#     print(query)
#     data=fetcher(conn,query)
    
    return data

@app.route('/userreg' ,methods=['POST','GET'])
def reg_user():
    global conn
    conn,_=connector()
    # from post data
    data =request.json
    # print(data)
    
    # print(data['hostelid'],data['password'])
    hostelid =data['hostelid'].upper()
    password =data['password'].upper()
    if hostelid !='' and password !='':
        query1 = f"SELECT * FROM user_det where inmate_id = '{hostelid}';"
        data1 =fetcher(conn,query1)
        print(data1)
        if data1 ==[]:
            query = f"INSERT INTO User_det (inmate_id, password) VALUES ('{hostelid}', '{password}');"
            query_mess = f"INSERT INTO mess_out (hostel_id) VALUES ('{hostelid}');"
            query_dash = f"INSERT INTO inmate (hostel_id) VALUES ('{hostelid}');"
            insertor(conn,query)
            insertor(conn,query_mess)
            response_data = {'message': 'Data received successfully', 'status': 200}
            return jsonify(response_data)
        else:
            response_data = {'message': 'User already exits', 'status': 404}
            return jsonify(response_data)
    else:
        response_data = {'message': 'Data not received', 'status': 405  }
        return jsonify(response_data)


@app.route('/userlog' ,methods=['POST','GET'])
def log_user():
    conn,_=connector()
    data =request.json
    
    hostelid =data['hostelid'].upper()
    password =data['password'].upper()
    if hostelid =='' or password =='':
        response_data = {'message': 'Data not received', 'status': 405  }
        return jsonify(response_data)
    query = f"SELECT * FROM user_det where inmate_id ='{hostelid}';"

    
    # print(query)
    data =user_search(conn,query)
    print(data)
    
    if data is not None  and hostelid == data[0] and password == data[1]:
        response_data = {'key':hostelid,'message': 'User logged in successfully', 'status': 200}
        return jsonify(response_data)
        
    else:
        response_data = {'message': 'Login Unsuccessfull', 'status': 404}
        return jsonify(response_data)

@app.route('/userlogout' )
def logout_user():
    uid=session.get('userid', None)
    session.pop('userid', None)
    response_data = {'message': "log out successfull", 'status': 200}
    return jsonify(response_data)

@app.route('/dash' ,methods=['GET','POST'])
def dash():
    conn,_=connector()
    key =request.json
    id=key['hostelid']
    id=id.upper()
    query = f"SELECT * FROM inmate where hostel_id = '{id}';"
    data =fetcher(conn,query)
    
    return data


@app.route('/messreq' ,methods=['GET','POST'])
def messreq():

    # conn,_=connector()
    data =request.json
    print(data['messmode'])
    if data['messmode'] == 'MESSOUT':
        query = f"UPDATE mess_out SET mess_mode = 'true', date = '{data['date']}' WHERE hostel_id = '{data['hostel_id']}';"

        print("query",query)
        insertor(conn,query)
        response_data = {'message': 'Mess request sent successfully', 'status': 200}
        return jsonify(response_data)
    elif data['messmode'] == 'MESSIN':
        query = f"SELECT date FROM mess_out where hostel_id = '{data['hostel_id']}';"
        fetch_date =fetcher(conn,query)
        date_object = fetch_date[0][0]
        # #########################################
        mess_out_date = date_object.strftime('%m/%d/%Y')
        mess_in_date=data['date']
        # ##########################################
        mess_out_date_1 = datetime.strptime(mess_out_date, '%m/%d/%Y').date()
        mess_in_date_2 = datetime.strptime(mess_in_date, '%m/%d/%Y').date()
        # #############################################
        diff=mess_in_date_2-mess_out_date_1
        print(diff.days)
        number_of_days=diff.days
        # #############################################
        query = f"UPDATE mess_out SET mess_mode = 'false' WHERE hostel_id = '{data['hostel_id']}';"
        insertor(conn,query)

        
        response_data = {'message': 'Mess request sent successfully', 'status': 200}
        return jsonify(response_data)
    data=jsonify("data","data")
    return data



if __name__ == '__main__':
    app.run(debug=True)