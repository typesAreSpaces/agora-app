import email
import hashlib
import os
from AgoraFilter import *
from limits import *
from agora_errors import *

class AgoraSyntacticFilter(AgoraFilter):

    def validateEmail(self, emailAddress):
        if email.utils.parseaddr(emailAddress) == ('', ''):
            raise AgoraEInvalidEmail
    
    def isLengthBetween(self, str, lower, upper):
        length = len(str)
        return not ((length > upper) or (length < lower))

    def validateUsername(self, username):
        if not self.isLengthBetween(username, USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH):
            raise AgoraEInvalidUsername

    def validatePassword(self, password):
        if not self.isLengthBetween(password, PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH):
            raise AgoraEInvalidPassword
        return hashlib.sha256(password.encode()).hexdigest()

    def validateToken(self, token, tokenType):
        expectLength = TOKEN_LENGTHS[tokenType]
        if token is None or len(token) != expectLength:
            raise AgoraEInvalidToken
        if not token.isalnum():
            raise AgoraEInvalidToken
        if tokenType == "backup":
            return hashlib.sha256(token.encode()).hexdigest()

    def validateStatus(self, status):
        if not self.isLengthBetween(status, STATUS_MIN_LENGTH, STATUS_MAX_LENGTH):
            raise AgoraEInvalidStatus

    def validatePost(self, content):
        if not self.isLengthBetween(content, 0, POST_MAX_LENGTH):
            raise AgoraEInvalidPost

    def validatePostTitle(self, title):
        if not self.isLengthBetween(title, POST_TITLE_MIN_LENGTH, POST_TITLE_MAX_LENGTH):
            raise AgoraEInvalidTitle

    def validateImageTitle(self, title):
        if not self.isLengthBetween(title, IMG_TITLE_MIN_LENGTH, IMG_TITLE_MAX_LENGTH):
            raise AgoraEInvalidTitle
        if '.' not in title:
            raise AgoraEInvalidTitle
        extension = title.rsplit('.', 1)[1].lower()
        if extension not in USER_IMAGE_EXTENSIONS:
            raise AgoraEInvalidTitle
        return extension

    def validateImage(self, imgData):
        imgSize = imgData.seek(0, os.SEEK_END)
        if imgSize > IMG_MAX_SIZE_BYTES:
            raise AgoraEBadImage
        imgData.seek(0, 0)

    def validateComment(self, comment):
        if not self.isLengthBetween(comment, COMMENT_MIN_LENGTH, COMMENT_MAX_LENGTH):
            raise AgoraEInvalidComment

    def validateReport(self, content):
        if not self.isLengthBetween(content, BUG_REPORT_MIN_LENGTH, BUG_REPORT_MAX_LENGTH):
            raise AgoraEInvalidReport

    def validateQuery(self, content):
        if not self.isLengthBetween(content, 0, QUERY_MAX_LENGTH):
            raise AgoraEInvalidQuery

    def isValidId(self, strid):
        return strid.isdigit()

    def isValidImgId(self, strid):
        return strid.isalnum()


    def createAccount(self, emailAddress, username, password, captcha):
        self.validateEmail(emailAddress)
        self.validateUsername(username)
        hpassword = self.validatePassword(password)
        return self.next.createAccount(emailAddress, username, hpassword, captcha)

    def confirmCreate(self, creationToken):
        self.validateToken(creationToken, "creation")
        return self.next.confirmCreate(creationToken)



    def login(self, username, password, captcha):
        self.validateUsername(username)
        hpassword = self.validatePassword(password)
        return self.next.login(username, hpassword, captcha)

    def logout(self, sessionToken):
        self.validateToken(sessionToken, "session")
        return self.next.logout(sessionToken)



    def deleteAccount(self, sessionToken, password):
        self.validateToken(sessionToken, "session")
        hpassword = self.validatePassword(password)
        return self.next.deleteAccount(sessionToken, hpassword)

    def confirmDelete(self, deletionToken):
        self.validateToken(deletionToken, "deletion")
        return self.next.confirmDelete(deletionToken)



    def recoverAccount(self, emailAddress):
        self.validateEmail(emailAddress)
        return self.next.recoverAccount(emailAddress)

    def backupRecover(self, backupCode, emailAddress):
        hbackupCode = self.validateToken(backupCode, "backup") 
        self.validateEmail(emailAddress)
        return self.next.backupRecover(hbackupCode, emailAddress)

    def confirmRecover(self, recoveryToken, password):
        self.validateToken(recoveryToken, "recovery")
        hpassword = self.validatePassword(password)
        return self.next.confirmRecover(recoveryToken, hpassword)



    def getUser(self, uid):
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.getUser(int(uid))
    
    def getPost(self, pid):
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        return self.next.getPost(int(pid))
    
    def getImage(self, imageId):
        if not self.isValidImgId(imageId):
            raise AgoraENoSuchImage
        return self.next.getImage(imageId)
    
    def searchUsers(self, query):
        self.validateQuery(query)
        return self.next.searchUsers(query)
    
    def searchPosts(self, query):
        self.validateQuery(query)
        return self.next.searchPosts(query)



    def getMyUser(self, sessionToken, concise=False):
        self.validateToken(sessionToken, "session")
        return self.next.getMyUser(sessionToken, concise=concise)



    def changeStatus(self, sessionToken, newStatus):
        self.validateToken(sessionToken, "session")
        self.validateStatus(newStatus)
        return self.next.changeStatus(sessionToken, newStatus)
    
    def changePicture(self, sessionToken, imageId):
        self.validateToken(sessionToken, "session")
        if not self.isValidImgId(imageId):
            raise AgoraENoSuchImage
        return self.next.changePicture(sessionToken, imageId)
    
    def changeEmail(self, sessionToken, emailAddress):
        self.validateToken(sessionToken, "session")
        self.validateEmail(emailAddress)
        return self.next.changeEmail(sessionToken, emailAddress)

    def confirmEmail(self, emailToken):
        self.validateToken(emailToken, "email")
        return self.next.confirmEmail(emailToken)

    def changeUsername(self, sessionToken, username):
        self.validateToken(sessionToken, "session")
        self.validateUsername(username)
        return self.next.changeUsername(sessionToken, username)

    def writePost(self, sessionToken, title, content, captcha):
        self.validateToken(sessionToken, "session")
        self.validatePostTitle(title)
        self.validatePost(content)
        return self.next.writePost(sessionToken, title, content, captcha)

    def editPost(self, sessionToken, pid, title, content):
        self.validateToken(sessionToken, "session")
        self.validatePostTitle(title)
        self.validatePost(content)
        return self.next.editPost(sessionToken, pid, title, content)   
 
    def deletePost(self, sessionToken, pid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        return self.next.deletePost(sessionToken, int(pid))
    
    def uploadImage(self, sessionToken, title, imgData):
        self.validateToken(sessionToken, "session")
        extension = self.validateImageTitle(title)
        self.validateImage(imgData)
        return self.next.uploadImage(sessionToken, title, extension, imgData)
    
    def deleteImage(self, sessionToken, imageId):
        self.validateToken(sessionToken, "session")
        if not self.isValidImgId(imageId):
            raise AgoraENoSuchImage
        return self.next.deleteImage(sessionToken, imageId)

    def listImages(self, sessionToken):
        self.validateToken(sessionToken, "session")
        return self.next.listImages(sessionToken)



    def friendRequest(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.friendRequest(sessionToken, int(uid))

    def unfriend(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.unfriend(sessionToken, int(uid))

    def viewFriendReqs(self, sessionToken):
        self.validateToken(sessionToken, "session")
        return self.next.viewFriendReqs(sessionToken)
    
    def acceptFriendReq(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.acceptFriendReq(sessionToken, int(uid))



    def comment(self, sessionToken, pid, content, captcha):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        self.validateComment(content)
        return self.next.comment(sessionToken, int(pid), content, captcha)

    def deleteComment(self, sessionToken, cid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(cid):
            raise AgoraEInvalidComment
        return self.next.deleteComment(sessionToken, int(cid))
    
    def like(self, sessionToken, pid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        return self.next.like(sessionToken, int(pid))

    def unlike(self, sessionToken, pid): 
        self.validateToken(sessionToken, "session")
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        return self.next.unlike(sessionToken, int(pid))

    def dislike(self, sessionToken, pid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(pid):
            raise AgoraENoSuchPost
        return self.next.dislike(sessionToken, int(pid))

    def bugReport(self, sessionToken, content):
        self.validateToken(sessionToken, "session")
        self.validateReport(content)
        return self.next.bugReport(sessionToken, content)



    def adminGetUser(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.adminGetUser(sessionToken, int(uid))

    def adminSuspend(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.adminSuspend(sessionToken, int(uid))

    def adminUnsuspend(self, sessionToken, uid):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        return self.next.adminUnsuspend(sessionToken, int(uid))
    
    def adminDelete(self, sessionToken, uid, password):
        self.validateToken(sessionToken, "session")
        if not self.isValidId(uid):
            raise AgoraENoSuchUser
        hpassword = self.validatePassword(password)
        return self.next.adminDelete(sessionToken, int(uid), hpassword)
