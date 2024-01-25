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

#funcion que lee el archivo csv con el hsitorial de predicciones y lo devuelve en un arreglo
def show_entry():
    day_entry_list = pd.read_csv("/content/Class139B/static/assets/data_files/data_entry.csv")
    day_entry_list = day_entry_list.iloc[::-1]

    date1 = (day_entry_list['date'].values[0])
    date2 = (day_entry_list['date'].values[1])
    date3 = (day_entry_list['date'].values[2])

    entry1 = (day_entry_list['text'].values[0])
    entry2 = (day_entry_list['text'].values[1])
    entry3 = (day_entry_list['text'].values[2])

    emotion1 = (day_entry_list['emotion'].values[0])
    emotion2 = (day_entry_list['emotion'].values[1])
    emotion3 = (day_entry_list['emotion'].values[2])

    emotion_url_1 = ""
    emotion_url_2 = ""
    emotion_url_3 = ""

    for key, value in emo_code_url.items():
        if key==emotion1:
            emotion_url_1 = value[1]
        if key==emotion2:
            emotion_url_2 = value[1]
        if key==emotion3:
            emotion_url_3 = value[1]
    return [
        {
            "date": date1,
            "entry": entry1,
            "emotion": emotion1,
            "emotion_url": emotion_url_1
        },
        {
            "date": date2,
            "entry": entry2,
            "emotion": emotion2,
            "emotion_url": emotion_url_2
        },
        {
            "date": date3,
            "entry": entry3,
            "emotion": emotion3,
            "emotion_url": emotion_url_3
        }
    ]
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
