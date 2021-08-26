import os
from flask import render_template, request, flash, session, url_for, redirect
from views import *
from flask.views import View
from werkzeug.utils import secure_filename
from googleapiclient.discovery import build
import random


class MyProfile(View):
    def dispatch_request(self):
        if 'loggedin' in session:
            me = session['id']
            profile = Conn.toProfile(me)
            tags = Style.showPos(me)
            api = ''

            if session['role'] == 'youtuber':
                try:
                    api = APIs.ID(profile.id_channel)
                except:
                    api = ''

            return render_template('/profile.html', data=profile, tag=tags, api=api)

        return render_template('/login.html')


class UpdateProfile(View):
    def dispatch_request(self):
        if request.method == "POST":
            a = request.form['id']
            b = request.form['fullname']
            c = request.form['desc']
            d = request.form['email']
            e = request.form['password']
            f = request.form['payrate']
            g = request.form['id_channel']
            h = request.form['pic']

            updated = Conn.toUpdate(a, b, c, d, e, f, g, h)
            flash('Updated')
        return redirect(url_for('profile', data=updated))

    def uploadIMG():
        if request.method == "POST":
            FilePath = request.files['file']
            if not FilePath:
                return 'No pic uploaded!', 400

            filename = secure_filename(FilePath.filename)
            if not filename:
                return 'Bad upload!', 400

        last_upload = ''
        maindir = 'static/uploads/'
        me = str(session['id'])
        user = Conn.toProfile(me)

        if user:
            last_upload = user.pic

        if last_upload:
            os.remove(maindir + me + '/' + last_upload)

        path = os.path.join(maindir, me + '/')

        if not os.path.exists(path):
            os.makedirs(path)

        FilePath.save(os.path.join(maindir + me + '/', filename))
        updated = Conn.uploadImg(me, filename)

        flash('Updated')
        return redirect(url_for('profile', img=updated))


# UPDATE USER TAG

class SaveTag(View):
    def dispatch_request(self):
        if request.method == "POST":
            id = request.form['id']
            select = request.form.getlist('checkbox')
            # Save
            Style.setTag(id, select)

            return redirect(url_for('profile'))


# Search By Tag
class SearchByTag(View):
    def dispatch_request(self):
        return render_template('tag.html')

    def getTag(tag):

        tagID = name2id(tag)
        users = Style.byTag(tagID)

        # # if no data
        # if users == []:
        #     users = "nothing"

        return render_template('tagresult.html', datas=users)


# HOME PAGE
class Recommended(View):
    def dispatch_request(self):

        if session['role'] == "youtuber":
            # code 
            users = db.session.query(User).filter(User.role == "sponsor").all()
            random.shuffle(users)         
        else:
            # code
            users = db.session.query(User).filter(User.role == "youtuber").all() 
            random.shuffle(users)

        indx = []
        for i in range(9):
            indx.append(users[i]) 

        return render_template('recommended.html', datas= indx)


# USER PROFILE
class Visit(View):

    # /visit/<id>
    def VisitTo(id):
        user = Conn.toProfile(id)
        tags =[]
        pos = Style.showPos(id) # [1,0,1,0,0]
        style = posToId(pos)

        for i in style:
            x = id2name(i)
            tags.append(x)    

        if session['role'] == "youtuber":
            return render_template('visit.html', data=user, tags=tags)
        else: 
            fetch = APIs.ID(user.id_channel)  
            return render_template('visit2.html', data=user, tags=tags, api=fetch)


# SEARCH
class SearchProfile(View):
    def dispatch_request(self):

        return render_template('search.html')

    def searchName(name):

        # name = request.form["search"]
        # search = "%{}%".format(name)
        # record = db.session.query.filter(User.fullname.like(search)).all()

        return render_template('tagresult.html', )


class APIs(View):
    # API
    def ID(channelID):
        api_key = "AIzaSyAae50fLK2RJv8DDJg93SX08H0uEPCiuuU"
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.channels().list(
            part="statistics,snippet",
            id=channelID
        )
        response = request.execute()

        # FETCH API
        titleChannel = response["items"][0]["snippet"]["localized"]["title"]
        subscriberCount = format(
            int(response["items"][0]["statistics"]["subscriberCount"]), ",")

        viewCount = format(
            int(response["items"][0]["statistics"]["viewCount"]), ",")
        videoCount = format(
            int(response["items"][0]["statistics"]["videoCount"]), ",")

        publishedAt = response["items"][0]["snippet"]["publishedAt"]
        pic = response["items"][0]["snippet"]["thumbnails"]["high"]["url"]

        return [titleChannel, subscriberCount, viewCount, videoCount, publishedAt, pic]

    # API VIDEO

    def vdo(channelID):
        api_key = "AIzaSyAbk_yiUDw86r6AALwJYsLvBJB5BXT31aQ"
        youtube = build("youtube", "v3", developerKey=api_key)
        request = youtube.search().list(
            part="snippet",
            channelId=channelID,
            maxResults=10
        )
        response = request.execute()
        vidId = response["items"][0]["id"]["videoId"]

        return vidId
