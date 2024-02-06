import hashlib
import random, string
from limits import *

class AgoraInterpreterFilter:
    def __init__(self, nextFilter):
        self.next = nextFilter

    def setDBManager(self, db):
        self.db = db

    def setEmailer(self, eml):
        self.eml = eml

    def setHost(self, host):
        self.host = host

    def setFileManager(self, fm):
        self.fm = fm

    def generateToken(self, ttype):
        return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(TOKEN_LENGTHS[ttype]))

    def createAccount(self, emailAddress, username, hpassword, acceptable):
        old_uid = self.db.emailExists(emailAddress)
        if not old_uid is None:
            self.db.deleteUser(old_uid)     # Delete any unconfirmed accounts with this address
        if acceptable:
            recovery = self.generateToken("recovery")
            hrecovery = hashlib.sha256(recovery.encode()).hexdigest()
            uid = self.db.createUser(emailAddress, username, hpassword, hrecovery)
            confirm = self.generateToken("creation")
            confirm_url = f'{self.host}/confirm/{confirm}'
            self.eml.confirmAccountEmail(emailAddress, confirm_url)
            self.db.createToken(uid, confirm, "creation")
    
    def confirmCreate(self, uid, creationToken):
        self.db.expireToken(creationToken)
        self.db.verifyUser(uid)

    def login(self, uid):
        session = self.generateToken("session")
        self.db.createToken(uid, session, "session")
        return session

    def logout(self, sessionToken):
        self.db.expireToken(sessionToken)

    def deleteAccount(self, uid, email):
        raise NotImplementedError
    def confirmDelete(self, uid):
        raise NotImplementedError

    def recoverAccount(self, emailAddress, acceptable):
        raise NotImplementedError
    def backupRecover(self, uid, emailAddress):
        raise NotImplementedError
    def confirmRecover(self, uid, hpassword):
        raise NotImplementedError



    def changeStatus(self, uid, newStatus):
        self.db.setStatus(uid, newStatus)

    def changePicture(self, uid, imageId):
        self.db.setPicture(uid, imageId)
    
    def changeEmail(self, uid, emailAddress, acceptable):
        raise NotImplementedError
    
    def changeUsername(self, uid, username):
        self.db.setUsername(uid, username)



    def writePost(self, uid, title, content):
        filename = f"post{self.generateToken('postid')}.md"
        self.db.insertPost(uid, title, filename)
        self.fm.writePost(filename, content)

    def deletePost(self, pid):
        self.db.deletePost(pid)
    
    def uploadImage(self, uid, title, extension, imgData):
        accessid = self.generateToken('imgid')
        filename = f"img{accessid}.{extension}"
        self.db.insertImage(uid, title, filename, accessid)
        self.fm.saveImage(filename, imgData)
        return accessid

    def deleteImage(self, imageId):
        filename = self.db.imgExists(imageId)
        self.db.deleteImage(imageId)
        self.fm.deleteImage(filename) 



    def friendRequest(self, uid1, uid2):
        raise NotImplementedError

    def comment(self, uid, pid, content):
        self.db.insertComment(uid, pid, content)

    def bugReport(self, uid, content):
        raise NotImplementedError



    def adminSuspend(self, uid):
        raise NotImplementedError
    def adminUnsuspend(self, uid):
        raise NotImplementedError
    def adminDelete(self, uid):
        raise NotImplementedError
