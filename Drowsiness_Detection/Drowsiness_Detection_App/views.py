from datetime import datetime
import sys

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render, redirect
from Drowsiness_Detection_App.models import *

from django.core import serializers
import json
from django.http import JsonResponse

from Drowsiness_Detection_App.serilaizer import Userregserializer

# Create your views here.


def login(request):
    return render(request, "login.html")


def logout(request):
    auth.logout(request)
    return render(request, "login.html")


def register(request):
    return render(request, "register.html")


def registered(request):
    firstname = request.POST["Firstname"]
    lastname = request.POST["Lastname"]
    gender = request.POST["Gender"]
    place = request.POST["Place"]
    post = request.POST["Post"]
    pin = request.POST["Pin"]
    email = request.POST["Email"]
    phone = request.POST["Phone"]
    vehicle_no = request.POST["VehicleNo"]
    username = request.POST["Username"]
    password = request.POST["Password"]
    login_obj = Login()
    login_obj.Username = username
    login_obj.Password = password
    login_obj.Type = 'user'
    login_obj.save()
    user_obj = User()
    user_obj.Firstname = firstname
    user_obj.Lastname = lastname
    user_obj.Gender = gender
    user_obj.Place = place
    user_obj.Post = post
    user_obj.Pin = pin
    user_obj.Email = email
    user_obj.Phone = phone
    user_obj.Vehicle = vehicle_no
    user_obj.LID = login_obj
    user_obj.save()
    return HttpResponse('''<script>alert ("registration successful");window.location="/"</script>''')


def login_fun(request):
    try:
        username = request.POST["Username"]
        password = request.POST["Password"]
        login_obj = Login.objects.get(Username=username, Password=password)
        if login_obj.Type == "admin":
            ob = auth.authenticate(username='admin', password='admin')
            if ob is not None:
                auth.login(request, ob)
            return redirect("admin_home")
        if login_obj.Type == "user":
            request.session['user_id'] = login_obj.id
            ob = auth.authenticate(username='admin', password='admin')
            if ob is not None:
                auth.login(request, ob)
            return redirect("user_home")
        if login_obj.Type == "block":
            return HttpResponse('''<script>alert ("sorry you are blocked!");window.location="/"</script>''')
    except:
        return HttpResponse('''<script>alert ("incorrect username or password");window.location="/"</script>''')


@login_required(login_url='/')
def admin_home(request):
    return render(request, "admin home.html")


@login_required(login_url='/')
def user_home(request):
    return render(request, "user home.html")


@login_required(login_url='/')
def block_unblock(request):
    user_obj = User.objects.all()
    return render(request, "block and unblock user.html", {'user_obj': user_obj})


@login_required(login_url='/')
def block(request, block_id):
    user_obj = User.objects.get(id=block_id)
    login_obj = Login.objects.get(id=user_obj.LID.id)
    login_obj.Type = "block"
    login_obj.save()
    return HttpResponse('''<script>alert ("blocked");window.location="/block_unblock"</script>''')


@login_required(login_url='/')
def unblock(request, unblock_id):
    user_obj = User.objects.get(id=unblock_id)
    login_obj = Login.objects.get(id=user_obj.LID.id)
    login_obj.Type = "user"
    login_obj.save()
    return HttpResponse('''<script>alert ("unblocked");window.location="/block_unblock"</script>''')


@login_required(login_url='/')
def add_manage_music(request):
    music_obj = Music.objects.all()
    return render(request, "add and manage music.html", {'music_obj': music_obj})


@login_required(login_url='/')
def add_music(request):
    return render(request, "add new.html")


@login_required(login_url='/')
def adding_musics(request):
    music = request.FILES["Music_files"]
    details = request.POST["Details"]
    emotions = request.POST["select_emotions"]
    music_obj = Music()
    music_obj.Musics = music
    music_obj.Details = details
    music_obj.Emotions = emotions
    music_obj.Date = datetime.now()
    music_obj.save()
    return HttpResponse('''<script>alert ("music added successfully");window.location="/add_manage_music"</script>''')


@login_required(login_url='/')
def delete(request, delete_id):
    music_obj = Music.objects.get(id=delete_id)
    music_obj.delete()
    return HttpResponse('''<script>alert ("music deleted");window.location="/add_manage_music"</script>''')


@login_required(login_url='/')
def complaints_reply_admin(request):
    complain_obj = Complaints.objects.all()
    return render(request, "view complaint and send reply.html", {'complaint_obj': complain_obj})


@login_required(login_url='/')
def reply_form(request, reply_id):
    request.session['reply_id'] = reply_id
    return render(request, "send reply.html")


@login_required(login_url='/')
def send_reply(request):
    reply = request.POST["Reply"]
    # obj_id = request.session['reply_id']
    reply_obj = Complaints.objects.get(id=request.session['reply_id'])
    reply_obj.Reply = reply
    reply_obj.save()
    return HttpResponse('''<script>alert ("Reply sent successfully");
                        window.location="/complaints_reply_admin"</script>''')


@login_required(login_url='/')
def view_feedback(request):
    feedback_obj = Feedback.objects.all()
    return render(request, "view feedback.html", {'feedback_obj': feedback_obj})

# ///////////////////////////////////////////////////////////////webservice/////////////////////////////////////////

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class login_code(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        try:
            users = Login.objects.get(Username=username, Password=password)
            print("------------>", users)
            if users is None:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                data = {
                    'lid': users.id,
                    'task':'success'

                }
                return Response(data, status=status.HTTP_200_OK)
        except:
                return Response(status=status.HTTP_204_NO_CONTENT)

class registration(APIView):
    def post(self, request):
        print('------------->', request.data)
        firstname = request.data.get('Firstname')
        lastname = request.data.get('Lastname')
        place = request.data.get('Place')
        post_office =request.data.get('Post')
        pin_code = request.data.get('Pin')
        phone = request.data.get('Phone')
        gender = request.data.get('Gender')
        vehicle = request.data.get('Vehicle')
        email_id = request.data.get('Email')
        username = request.data.get('Username')
        password = request.data.get('Pass')
        lob = Login()
        lob.Username = username
        lob.Password = password
        lob.Type = 'user'
        lob.save()

        user_obj = User()
        user_obj.Firstname = firstname
        user_obj.Lastname = lastname
        user_obj.Place = place
        user_obj.Post = post_office
        user_obj.Pin = pin_code
        user_obj.Phone = phone
        user_obj.Gender = gender
        user_obj.Vehicle = vehicle
        user_obj.Email = email_id
        user_obj.LID = lob
        user_obj.save()
        return Response(status=status.HTTP_200_OK)

def add_music_app(request):
    music = request.FILES["file"]
    fs = FileSystemStorage()
    fn = fs.save(music.name, music)
    details = request.POST["Details"]
    emotions = request.POST["Emotions"]
    music_obj = Music()
    music_obj.Musics = fn
    music_obj.Details = details
    music_obj.Emotions = emotions
    music_obj.Date = datetime.now()
    music_obj.save()
    data = {"task": "success"}
    r = json.dumps(data)
    return HttpResponse(r)


def feedback_app(request):
    feedback = request.POST["Feedback"]
    feedback_id = request.POST["lid"]
    feedback_obj = Feedback()
    feedback_obj.Feedbacks = feedback
    feedback_obj.Date = datetime.now()
    feedback_obj.UID = User.objects.get(LID__id=feedback_id)
    feedback_obj.save()
    data = {'task': "success"}
    r = json.dumps(data)
    return HttpResponse(r)


class send_complaint_app(APIView):
    def get(self, request, lid):
        user_id = lid
        complaint_obj = Complaints.objects.filter(UID__LID__id=user_id)
        data = []
        for i in complaint_obj:
            row = {'Complaint': i.Complaint, 'Reply': i.Reply, 'Date': str(i.Date)}
            data.append(row)
        return Response(data, status=status.HTTP_200_OK)
    def post(self, request, lid):
        complaints = request.data.get("Complaint")
        u_id = lid
        date = datetime.now()
        reply = "waiting"
        complaint_obj = Complaints()
        complaint_obj.Complaint = complaints
        complaint_obj.Date = date
        complaint_obj.Reply = reply
        complaint_obj.UID = User.objects.get(LID__id=u_id)
        complaint_obj.save()
        return Response(status=status.HTTP_200_OK)
def reply_app(request):
    user_id = request.POST['lid']
    complaint_obj = Complaints.objects.filter(UID__LID__id=user_id)
    data = []
    for i in complaint_obj:
        row = {'Complaint': i.Complaint, 'Reply': i.Reply, 'Date': str(i.Date)}
        data.append(row)
    r = json.dumps(data)
    return HttpResponse(r)


def music_app(request):
    music_obj = Music.objects.all()
    music_datas = []

    for i in music_obj:
        data = {'Musics': str(i.Musics.url), 'Details': i.Details, 'Emotions': i.Emotions, 'mid': i.id}
        music_datas.append(data)

    r = json.dumps(music_datas)
    return HttpResponse(r)


def e_view_music(request):
    mid = request.POST['mid']
    music_obj = Music.objects.filter(id=mid)
    music_datas = []

    for i in music_obj:
        data = {'Musics': str(i.Musics), 'Details': i.Details, 'Emotions': i.Emotions, 'mid': i.id}
        music_datas.append(data)

    r = json.dumps(music_datas)
    return HttpResponse(r)


def edit_music(request):
    music = request.FILES["file"]
    fs = FileSystemStorage()
    fn = fs.save(music.name, music)
    details = request.POST["Details"]
    emotions = request.POST["Emotions"]
    music_obj = Music()
    music_obj.Musics = fn
    music_obj.Details = details
    music_obj.Emotions = emotions
    music_obj.Date = datetime.now()
    music_obj.save()
    data = {"task": "success"}
    r = json.dumps(data)
    return HttpResponse(r)


def delete_app(request):
    music_id = request.POST["m_id"]
    music_obj = Music.objects.get(id=music_id)
    music_obj.delete()
    data = {"task": "success"}
    r = json.dumps(data)
    return HttpResponse(r)


from django.http import HttpResponse
from rest_framework.views import APIView
import cv2
import numpy as np
import dlib
import json
from imutils import face_utils
from playsound import playsound

class detect(APIView):
    cap = None  # Class-level attribute to store the camera instance

    def get(self, request):
        """Function to start drowsiness detection."""
        self.cap = cv2.VideoCapture(0)  # Assign camera to class attribute
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

        sleep = 0
        drowsy = 0
        active = 0
        status = ""
        color = (0, 0, 0)

        def compute(pta, ptb):
            return np.linalg.norm(pta - ptb)

        def blinked(a, b, c, d, e, f):
            up = compute(b, d) + compute(c, e)
            down = compute(a, f)
            ratio = up / (2.0 * down)

            if ratio > 0.25:
                return 2
            elif 0.21 < ratio <= 0.25:
                return 1
            else:
                return 0

        while True:
            status1 = request.data.get('status')  # Fetch status dynamically
            
            if status1 != "activate":
                print("Deactivating...")
                self.close_video()
                sys.exit("Server shutting down as status is not 'activate'")
                break  # Exit the loop if status1 is not "activate"

            ret, frame = self.cap.read()
            if not ret:
                break
            


            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = detector(gray)

            for face in faces:
                x1, y1, x2, y2 = face.left(), face.top(), face.right(), face.bottom()
                face_frame = frame.copy()
                cv2.rectangle(face_frame, (x1, y1), (x2, y2), (0, 255, 0), 1)
                landmarks = predictor(gray, face)
                landmarks = face_utils.shape_to_np(landmarks)

                left_blink = blinked(landmarks[36], landmarks[37], landmarks[38],
                                    landmarks[41], landmarks[40], landmarks[39])
                right_blink = blinked(landmarks[42], landmarks[43], landmarks[44],
                                    landmarks[47], landmarks[46], landmarks[45])

                if left_blink == 0 or right_blink == 0:
                    sleep += 1
                    drowsy = 0
                    active = 0
                    if sleep > 6:
                        status = "SLEEPING!!!"
                        playsound("alarm.wav")
                        color = (255, 0, 0)

                elif left_blink == 1 or right_blink == 1:
                    drowsy += 1
                    sleep = 0
                    active = 0
                    if drowsy > 6:
                        status = "DROWSY !"
                        playsound("alarm.wav")
                        color = (255, 0, 0)

                else:
                    active += 1
                    drowsy = 0
                    sleep = 0
                    if active > 6:
                        status = "ACTIVE"
                        color = (0, 255, 0)

                cv2.putText(frame, status, (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)

                for (x, y) in landmarks:
                    cv2.circle(face_frame, (x, y), 1, (0, 0, 255), -1)

            if cv2.waitKey(5) & 0xFF == 27:
                break  # Break on ESC key press

        self.close_video()  # Ensure camera is closed after loop

        data = {"task": "Deactivated"}
        return HttpResponse(json.dumps(data), content_type="application/json")

    @classmethod
    def close_video(cls):
        """Class method to release the camera and close OpenCV windows."""
        if cls.cap is not None:
            cls.cap.release()
            cv2.destroyAllWindows()
            cls.cap = None  # Reset to None
  

from django.shortcuts import get_object_or_404
class ViewProfileApi(APIView):
    def get(self, request, lid):
        obj = User.objects.filter(LID_id=lid)
        serializer = Userregserializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, lid):
        obj = get_object_or_404(User, LID=lid)
        user_serial = Userregserializer(obj, data=request.data, partial=True)  # Enable partial updates

        if user_serial.is_valid():
            user_serial.save()
            return Response(user_serial.data, status=status.HTTP_200_OK)
        
        return Response(user_serial.errors, status=status.HTTP_400_BAD_REQUEST)


