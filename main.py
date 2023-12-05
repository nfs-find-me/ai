import cv2

# Charger le modèle de détection de visages Haar Cascade
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')


def detect_and_draw_selfie(image_path, output_image_path):
    # Charger l'image
    img = cv2.imread(image_path)

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
            if percentFace > 20:
                print("C'est un selfie !")
            else:
                print("Ce n'est pas un selfie !")
                print('result : ' + str(percentFace) + '%' + ' of the image')



# Exemple d'utilisation
input_image_path = "images/selfie.jpg"
output_image_path = "image_avec_rectangles.jpg"
detect_and_draw_selfie(input_image_path, output_image_path)
