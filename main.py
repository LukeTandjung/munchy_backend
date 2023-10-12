""" # SERVER-SIDE CODE TO OPTIMISE DIET

import os
from flask import Flask, request
from bot import MunchyBot
import session

app = Flask(__name__)

bot = MunchyBot()
        
@app.route('/', methods = ['POST'])
def webhook():
    input = request.get_json()
    return bot.handle_updates(input)
    
if __name__ == '__main__':
   app.run(threaded = True) 


@app.route("/<string:email>/diet", methods = ["POST"])
def create_user_diet(email):
    request_data = request.get_json()
    user = {
        "Email": request_data["Email"],
        "Password": request_data["Password"],
        "Promotional": request_data["Promotional"],
        "Name": request_data["Name"],
        "Age": request_data["Age"],
        "Sex": request_data["Sex"],
        "Height": request_data["Height"],
        "Weight": request_data["Weight"],
        "Body Fat": request_data["Body Fat"],
        "Diet": request_data["Diet"]
    }
    ...
    return jsonify(user_diet_dict)
 """