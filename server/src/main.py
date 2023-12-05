from flask import Flask, render_template, request, redirect, url_for, flash, abort
from werkzeug.utils import secure_filename
import cv2
import os

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static/images')
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


app = Flask(__name__)
app.secret_key = 'votre_clé_secrète'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
selfie = False


# Fonction pour vérifier si l'extension du fichier est autorisée
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/upload', methods=['POST'])
def upload_file():
    # Vérifie si un fichier a été inclus dans la demande
    if 'file' not in request.files:
        flash('Aucun fichier sélectionné')
        return redirect(request.url)
    file = request.files['file']

    # Si l'utilisateur n'a pas sélectionné de fichier, le champ de fichier sera vide
    if file.filename == '':
        flash('Aucun fichier sélectionné')
        return redirect(request.url)

    # Si le fichier est autorisé et a une extension valide
    if file and allowed_file(file.filename):
        # Sécurisez le nom du fichier pour éviter les attaques
        filename = secure_filename(file.filename)
        # Enregistrez le fichier dans le dossier d'uploads
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        return index(os.path.join(app.config['UPLOAD_FOLDER'], filename))

    # Si le fichier n'est pas autorisé
    flash('Extension de fichier non autorisée')
    return redirect(request.url)

def index(input_image_path):
    print('Hello world !')
    # Launch model.py
    # Charger le modèle de détection de visages Haar Cascade
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    def detect_and_draw_selfie(image_path, output_image_path):
        # Charger l'image
        print("Chemin du fichier image :", image_path)
        img = cv2.imread(image_path)
        print(img)
        if img is None:
            # Gestion de l'erreur ici
            return

        # Convertir l'image en niveaux de gris
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Détecter les visages dans l'image
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        # Height de l'image d'origine
        heightImg = str(img.shape[0])
        widthImg = str(img.shape[1])
        print("Height image: " + heightImg)
        print("Width image: " + widthImg)

        # Dessiner des rectangles autour des visages détectés
        print("Faces found: " + str(len(faces)))
        if len(faces) > 0:
            for (x, y, w, h) in faces:
                print("Height face: " + str(h))
                cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)

                # Enregistrer l'image résultante avec les rectangles dessinés
                cv2.imwrite(output_image_path, img)
                # Supprimer le fichier image d'origine
                if os.path.exists(os.path.join(os.path.dirname(__file__), image_path)):
                    os.remove(os.path.join(os.path.dirname(__file__), image_path))

                print('Faces found: ', len(faces))

                surfaceImg = int(heightImg) * int(widthImg)
                surfaceFace = h * w
                print('h : ' + str(h))
                print('w : ' + str(w))
                print('heightImg : ' + str(heightImg))
                print('widthImg : ' + str(widthImg))
                print('surfaceFace : ' + str(surfaceFace))
                print('surfaceImg : ' + str(surfaceImg))
                percentFace = surfaceFace / surfaceImg * 100

                print("percent " + str(percentFace) + "%" + " of the image")
                # Si la taille de la face est supérieure à 1/3 de la taille de l'image, alors c'est un selfie
                global selfie
                if percentFace > 10:
                    selfie = True
                    print("C'est un selfie !")
                else:
                    selfie = False
                    print("Ce n'est pas un selfie !")
                    print('result : ' + str(percentFace) + '%' + ' of the image')
                print("selfie " + str(selfie))
                if (selfie):
                    # Return 400 bad request
                    abort(400, "Selfie is not authorized")

    # Exemple d'utilisation
    #input_image_path = os.path.join(os.path.dirname(__file__), 'static/images/selfie.jpg')
    # Supprimer le fichier result.jpg s'il existe

    output_image_path = os.path.join(os.path.dirname(__file__), 'static/images/result.jpg')
    detect_and_draw_selfie(input_image_path, output_image_path)
    # Render index.html
    print('selfie : ' + str(selfie))
    return render_template('index.html', is_selfie=selfie)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)), debug=True)

