from flask import Flask, render_template, url_for, request, jsonify
from model_prediction import * 
from predict_response import *

#libreria para exponer la api a una url publica
from flask_ngrok import run_with_ngrok

 
app = Flask(__name__)

predicted_emotion=""
predicted_emotion_img_url=""

# correr la api en url publica
run_with_ngrok(app)


@app.route('/')
def index():
    entries = show_entry()
    return render_template("index.html", entries=entries)
 
@app.route('/predict-emotion', methods=["POST"])
def predict_emotion():
    
    # Obtener el texto de entrada del requerimiento POST.
    input_text = request.json.get("text")  
    
    if not input_text:
        # Respuesta a enviar si input_text no está definido.
        response = {
                    "status": "error",
                    "message": "¡Por favor, ingresa algún texto para predecir la emoción!"
                  }
        return jsonify(response)
    else:  
        predicted_emotion, predicted_emotion_img_url = predict(input_text)
        
        # Respuesta a enviar si input_text no esta indefinido.
        response = {
                    "status": "success",
                    "data": {
                            "predicted_emotion": predicted_emotion,
                            "predicted_emotion_img_url": predicted_emotion_img_url
                            }  
                   }

        # Enviar respuesta.         
        return jsonify(response)


@app.route("/save-entry", methods=["POST"])
def save_entry():

    # Obtener datos, predecir emoción y el texto ingresado por el usuario para guardar una entrada.
    date = request.json.get("date")           
    emotion = request.json.get("emotion")
    save_text = request.json.get("text")

    save_text = save_text.replace("\n", " ")

    # Entrada CSV. 
    entry = f'"{date}","{save_text}","{emotion}"\n'  

    with open("/content/Class139B/static/assets/data_files/data_entry.csv", "a") as f:
        f.write(entry)
    return jsonify("Success")


@app.route("/bot-response", methods=["POST"])
def bot():
    # Obtener la entrada del usuario.
    input_text = request.json.get("user_bot_input_text")
   
    # Llamar al método para obtener la respuesta del bot.
    bot_res = bot_response(input_text)

    response = {
            "bot_response": bot_res
        }

    return jsonify(response)     
     
app.run()
