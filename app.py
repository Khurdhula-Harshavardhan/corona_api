import flask 
from flask import request
from corona import Corona_data
key='H@r$ha'

#object for communicating with class..
Obj = Corona_data()


app = flask.Flask(__name__)

@app.route("/", methods=['GET'])

def extract() :
    try :
        apikey = request.args.get('key')
        place=request.args.get('place')
        if apikey == key :
                response = Obj.search(place)
                return (response)
        elif len(apikey)==0 or apikey!=key :
                return ({"Status":"failed",
                        "Error" : "Invalid API KEY"})
        elif len(place)==0 :
                return ({"Status":"Failed",
                        "Error" : "No arguement given for place."})
        else :
                return ({"Status":"Failed",
                        "Error" : "403 Invalid Request!"})

    except :
            return ({"Status":"failed",
                "Error" : "403 Forbidden request. Please contact host."})

if __name__ == '__main__' : 
        app.run(debug=True)


