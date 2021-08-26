from app import app, db
from models import *


# @app.route('/')
# def index():
#      return 'hello'


class Conn():

    def toCheck(a):
        username = db.session.query(User).filter(User.username == a).first()
        return username

    def toLogin(a, b):
        username = db.session.query(User).filter(
            and_(User.username == a, User.password == b)).first()
        return username

    def toRegister(a, b, c, d, e):
        user = User(username=a, password=b, fullname=c, email=d, role=e)
        db.session.add(user)
        db.session.commit()

    def toProfile(a):
        profile = db.session.query(User).filter(User.id == a).first()
        return profile

    def toUpdate(a, b, c, d, e, f, g, h):
        updated = db.session.query(User).filter(User.id == a).first()
        updated.fullname = b
        updated.desc = c
        updated.email = d
        updated.password = e
        updated.pay_rate = f
        updated.id_channel = g
        updated.pic = h
        db.session.commit()

    def uploadImg(a, b,): 
        user = db.session.query(User).filter(User.id == a).first() 
        user.pic = b
        db.session.commit()

        return user
 

    # # PROFILE
    # def getImg(me):
    #     owner = str(me)
    #     img = db.session.query(User).filter(User.id == me).first()

    #     return [owner, img]


  
 

class Style():
    # selectTag = ['Entertainment', 'History']
    def setTag(ID, selectTag):

        for count in range(27):
            stmt1 = (delete(style).where(style.c.user_id == ID, style.c.tag_id == count+1))
            db.session.execute(stmt1)
            db.session.commit()

        for tag in selectTag:
            keyid = name2id(tag)
            stmt2 = style.insert().values(user_id=ID, tag_id=keyid)
            db.session.execute(stmt2)
            db.session.commit()

    # SHOW CHECKBOX

    def showPos(a):
        stmt = db.session.query(style).filter(style.c.user_id == a).all()
        data = []
        for tag in stmt:
            add = tag[0]
            data.append(add)
        Tags = posTag(data)
        return Tags

    # find User by tag_id

    def byTag(a):
        data = db.session.query(User).join(style).filter(style.c.tag_id == a).all()
        return data


# TAG position
# input =  [1,2,3,4]
def posTag(input):
    position = [0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0, 0, 0, 0,
                0, 0, 0]
    for x in input:
        position[x] = 1
    return position


# convert tag_name to tag_id
def name2id(style):   
    for k, v in datas.items():  
        if style == k:
            return v  # [1 ,6] 

# convert tag_id to tag_name 
def id2name(style):   
    for k, v in datas.items():  
        if style == v:
            return k  # ["Enteraintment" ,"Kids"]
      

def posToId(input):   # [1,0,1,0,1]
    c = 0
    data = []
    for i in input:
        if i == 1:
            data.append(c)
        c += 1 

    return data       # [1,3,5]
            



# TAG
global datas
datas = {
    "Entertainment": 1,
    "Health": 2,
    "Education": 3,
    "Lifestyle": 4,
    "Travel": 5,

    "Kids": 6,
    "Review": 7,
    "Tech": 8,
    "Movie": 9,
    "Animation": 10,

    "Music": 11,
    "ASMR": 12,
    "Food": 13,
    "Sport": 14,
    "Game": 15,

    "Beauty": 16,
    "Gossip": 17,
    "DIY": 18,
    "Art": 19,
    "Podcast": 20,

    "Motivation": 21,
    "History": 22,
    "Science": 23,
    "NEWS": 24,
    "Product": 25,

    "Service": 26
}
