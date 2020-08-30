from flask import Flask,jsonify,request,Response
from bson.json_util import dumps
import json
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/akshara"
app.config["DEBUG"] = True
mongo = PyMongo(app)
ticket = mongo.db.tickets

@app.route('/',methods=['GET'])
def home():
    return jsonify({'msg' : 'Welcome to Ticket Booking System'}),200

@app.route('/book',methods=['POST'])
def book():
    data = json.loads(request.get_data())
    # print(type(data))
    try :
        count = 0
        ticket_data = ticket.find({})
        for i in ticket_data:
                count = i['ticketID']

        data['ticketID'] = count+1
        ticket.insert(data)
        return jsonify({'msg' : 'booked successfully'}),200

    except Exception as e :
        return jsonify({'msg' : str(e)}),500

@app.route('/update',methods=['POST'])
def update_time():
    data = json.loads(request.get_data())
    try :
        name = data['name']
        new_time = data['time']

        ticket.find_one_and_update({'name':name },{'$set' : {'time' : new_time}})
        return jsonify({'msg':'updated successfully'}),200

    except Exception as e:
        return jsonify({'msg' : str(e)}),500

@app.route('/delete/name',methods=['POST'])
def delete(name):
    try :
        ticket.delete_one({'name':name})
        return jsonify({'msg':'deleted successfully'}),200

    except Exception as e:
        return  jsonify({'msg' : str(e)}),500

@app.route('/user/<name>',methods=['GET'])
def viewUserTicket(name):
    try :
        ticketInfo = ticket.find_one({"name" : name},{'_id' : 0,'ticketID':0})
        return ticketInfo

    except Exception as e:
        return jsonify({'msg' : str(e)}),500

@app.route('/viewAll',methods=['GET'])
def viewAllTickets():
    try :
        data = []
        tickets = ticket.find({},{'_id':0,'ticketID':0})
        for t in tickets :
            data.append(t)
        return jsonify({'AllTickets' : data}),200

    except Exception as e :
        return jsonify({'msg':str(e)}),500

@app.route('/expired',methods=['GET'])
def removeExpired():
    pass

if __name__ == "__main__":
    app.run() 