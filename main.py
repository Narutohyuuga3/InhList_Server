import os
from flask import Flask, request, render_template, send_file, abort
import json


app = Flask(__name__)

app.config['UPLOAD_EXTENSIONS']=['.pcm', '.jpg','.txt']

app.config['PASSWORD']=['E-Inhalatorprototypenentwicklung-der-Stufe_2!ükx/%']
app.config['USER']=['E-Inhalator-Client_1']

#configure interface if it visible for internet browsers
humanmode = False

################ FUNCTIONS #############################

### HANDLE A UPLOAD ###
def upload(folderpath, filetype):

        #print(folderpath)
        #print(filetype)
        global filelist
        #print("Ich bin hier")

        #print(request.files)

        uploaded_file = request.files[filetype]


        #print("reqFiles.... ")
        filename=uploaded_file.filename
        #print("Filename: "+ filename+"!")
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            #print(file_ext)
            if file_ext not in app.config['UPLOAD_EXTENSIONS']:
                #print("400 Fehler du seggl")
                abort(400)

            uploaded_file.save(os.path.join('static/'+ folderpath, filename))
            if filetype =='audio':
                filelist.append(filename)
                with open("static/database/filelist.json","w", encoding="utf-8") as file:
                   json.dump(filelist, file, ensure_ascii=False, indent=2)
                   return
            return
        return

### HANDLE PATH TRAVERSAL ###
def no_pathtravel(thepath):
    countpoints=thepath.count(".")
    countslashes=thepath.count("/")
    countpercentages=thepath.count("%")

    if countpoints>5 or countslashes>5 or countpercentages>2:
        return False
    else:
        return True


############################################
##             KEY PROTOCOLLING           ##
############################################
with open("static/database/filelist.json", "r", encoding="utf-8") as file:
        filelist = json.load(file)

############ MAINPROGRAMM ##################
@app.route('/')
def index():
    checkpath=request.url
    if no_pathtravel(checkpath):
        global humanmode
        if humanmode:
            return render_template('index.html')
        else:
            return 'Machine-Mode'
    else:
        return 'Meeeep!'

############################################
##              FROM APP TO PC            ##
############################################
@app.route('/uploadPCM', methods=['GET','POST'])
def uploadPCM():
    checkpath=request.url
    if no_pathtravel(checkpath):
        print("##########HEADER#################")
        print(1+1)
        print(request.headers)
        print("################################")
        if request.method == "POST":
            upload('PCM', 'audio')
        global humanmode
        if humanmode:
            return render_template('uploadPCM.html')
        else:
            return 'Machine-Mode'
    else:
        return 'Meeeep!'


@app.route('/downloadPCM', methods=['GET'])
def downloadPCM():
    checkpath=request.url
    if no_pathtravel(checkpath):
        global humanmode
        if humanmode:
            return render_template('downloadPCM.html')
        else:
            return 'Machine-Mode'
    else:
        return 'Meeeep!'

@app.route('/return-filesPCM/')
def return_files_PCM():
    checkpath=request.url
    if no_pathtravel(checkpath):
        if 'PCMkey' in request.args:
            PCMkey = request.args['PCMkey']
            try:
                return send_file('static/PCM/' + PCMkey, attachment_filename = PCMkey, as_attachment=True)
            except Exception as e:
                return str(e)
        else:
            return downloadPCM()
    else:
        return 'Meeeep!'

@app.route('/downloadFILES', methods=['GET','POST'])
def downloadFILES():
    checkpath=request.url
    if no_pathtravel(checkpath):
        print('patchtraversal passed')
        if request.method == "POST":
            print('POST passed')
            if 'fckwq' in request.form and 'kdwedu' in request.form:
                user=request.form['fckwq']
                pswd=request.form['kdwedu']
                #print('u: '+ user)
                #print('k:'+ pswd)
                if user in app.config['USER'] and pswd in app.config['PASSWORD']:
                    print('login succeed')
                    try:
                        return send_file('static/database/filelist.json', attachment_filename = 'filelist.json', as_attachment=True)
                    except Exception as e:
                        return str(e)
            else:
                print('error!')
                return 'no access!'
        else:
            return 'missing informations!'
    else:
        return 'Meeeep!'

############################################
##              FROM PC TO APP            ##
############################################
@app.route('/uploadTXT', methods=['GET','POST'])
def uploadTXT():
    checkpath=request.url
    if no_pathtravel(checkpath):
        if request.method == "POST":
            upload('TXT', 'text')
        global humanmode
        if humanmode:
            return render_template('uploadTXT.html')
        else:
            return 'Machine-Mode'
    else:
        return 'Meeeep!'

@app.route('/downloadTXT/', methods=['GET'])
def downloadTXT():
    checkpath=request.url
    if no_pathtravel(checkpath):
        global humanmode
        if humanmode:
            return render_template('downloadTXT.html')
        else:
            return 'Machine-Mode'
    else:
        return 'Meeeep!'

@app.route('/return-filesTXT/')
def return_files_TXT():
    checkpath=request.url
    if no_pathtravel(checkpath):
        print("Schoiße, der han a file gfordert! Tu watt!")
        if 'TXTkey' in request.args:
            filekey = request.args['TXTkey']
            print(filekey)
            try:
                print("seems like, it was gültich!")
                return send_file('static/TXT/' + filekey, attachment_filename = filekey, as_attachment=True)
            except Exception as e:
                print("schoiße wars")
                return str(e)
        else:
            print("Wia sanns hier")
            return downloadTXT()
    else:
        return 'Meeeep!'



########################################################
### For Visual Studio Code Live Server use 127.0.0.1
### else for onlineserver from Pythonanywhere and co
### use 0.0.0.0
if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
############### MAINPROGRAMM END #######################