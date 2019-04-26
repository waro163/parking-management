# -*- coding: utf-8 -*-
import requests,json

# local_base_url = "http://localhost:8000/api/v1.0"
local_base_url="http://39.104.81.6:8000/api/v1.0"
account=""
token=""
password=""
session_id=""
parking_id=""
parking_id=""
order_id=""


def gettoken():
    global account,token
    account=input("input your account to get the token:")
    url = local_base_url+"/user/gettoken"
    payload = '{"head":{},"body":{"account":"%s"}}'% account
    headers = {
    'Content-Type': "application/json"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    token = json.loads(response.text).get("body").get("token")
    print(response.text,token)

def register():
    global password,session_id
    url = local_base_url+"/user/register"
    password=input("input your password to register")
    print("your account:",account)
    print("your token:",token)
    payload = '{"head":{},"body":{"account":"%s","token": "%s","password":"%s"}}'%(account,token,password)
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "d1d507d3-ac86-4a7d-8df0-d3f4634f25ea"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    session_id = json.loads(response.text).get("body").get("session_id")
    print(response.text,session_id)

def login():
    global session_id
    account = input("input your email account:")
    password = input("input your password:")
    url = local_base_url+"/user/login"
    payload = '{"head":{},"body":{"account":"%s","password":"%s"}}'%(account,password)
    headers = {
    'Content-Type': "application/json"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    session_id = json.loads(response.text).get('body').get("session_id")
    print(response.text,session_id)

def parkings():
    latitude = input("input your latitude:")
    longitude = input("input your longitude:")
    distance = input("input your distance:")
    url = local_base_url+"/parkings"
    payload = '{"head":{},"body":{"session_id": "%s","latitude":"%s","longitude":"%s","distance":"%s"}}'%(session_id,latitude,longitude,distance)
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "ad9295b9-3082-4ddb-9d25-b226e2434acb"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    all_parking_zone = json.loads(response.text).get("body").get("parkings")
    print(response.text,all_parking_zone)

def unlock():
    global order_id,parking_id
    parking_id=input("input you will park the parking zone NO.:")
    url = local_base_url+"/parkings/unlock"
    payload = '{"head":{},"body":{"session_id": "%s","parking_id":"%s"}}'%(session_id,parking_id)
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "32b05a4b-4ef6-4c50-bfe9-9d9ce6c38471"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    order_id = json.loads(response.text).get("body").get("order_id")
    print(response.text,order_id)

def lock():
    global parking_id
    url = local_base_url+"/parkings/lock"
    print("latest you use parking zone id is:",parking_id)
    _parking_id = input("input you want to lock the parking zone NO.")
    if _parking_id:
        parking_id = _parking_id
    # _order_id = input("input the order id the you lock:")
    # if _order_id:
    #     order_id = _order_id
    print("you will lock the NO.%s parking zone" % parking_id)
    payload = '{"head":{},"body":{"session_id": "%s","parking_id":"%s"}}'%(session_id,parking_id)
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "cd640ea4-1ec9-4228-815b-7489e74acce4"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def rating():
    _order_id = input("input you want to rate the order is:")
    _score=input("input your score to the parking zone:")
    _comment = input("input your comment to the parking zone:")
    url = local_base_url+"/parkings/rating"
    payload = '{"head":{},"body":{"session_id": "%s","order_id": "%s","score":"%s","comment":"%s"}}'%(session_id,_order_id,_score,_comment)
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "bcc429d2-e12d-4240-bc14-02ee5f40bead"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def orders():
    url = local_base_url+"/orders"
    payload = '{"head":{},"body":{"session_id": "%s"}}'%session_id
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "40ff53b3-7404-4efd-b04a-2f0f6708c3cd"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    all_orders=json.loads(response.text).get("body").get("orders")
    for each_order in all_orders:
        print(each_order)


def order_pay():
    order_id = input("input you want to pay order id:")
    url = local_base_url+"/order/pay"
    payload = '{"head":{},"body":{"order_id": "%s","session_id":"%s"}}'%(order_id,session_id)
    headers = {
    'Content-Type': "application/json",
    'cache-control': "no-cache",
    'Postman-Token': "53d25703-1012-4c62-a8d0-559906f247f9"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

def parkings_status():
    url = local_base_url + "/parkings/status"
    payload = '{"head":{},"body":{"session_id":"%s"}}' %  session_id
    headers = {
        'Content-Type': "application/json",
        'cache-control': "no-cache",
        'Postman-Token': "53d25703-1012-4c62-a8d0-559906f247f9"
    }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)

if __name__ == "__main__":
    Usage = """
    input number to entry the progress:
    1->get the token before register
    2->register the account
    3->login the app(you must register the app)
    4->get the parking zone around your position
    5->unlock the parking zone by scanning QR code
    6->lock the parking zone
    7->rate your parking
    8->check your history orders
    9->pay your order
    10->manager to check all parking zone status
    input "q" to exit the app
    """
    while True:
        choice = input(Usage)
        if choice == "q":
            break
        elif choice == "1":
            gettoken()
        elif choice == "2":
            register()
        elif choice == "3":
            login()
        elif choice == "4":
            parkings()
        elif choice == "5":
            unlock()
        elif choice == '6':
            lock()
        elif choice == '7':
            rating()
        elif choice == "8":
            orders()
        elif choice == "9":
            order_pay()
        elif choice == "10":
            parkings_status()
        else:
            print("invalid choice, pleace choose again")
