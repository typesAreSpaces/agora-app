# backend

ACCOUNT_CREATION_TOKEN_LENGTH = 30
ACCOUNT_DELETION_TOKEN_LENGTH = 30
ACCOUNT_RECOVERY_TOKEN_LENGTH = 30
ACCOUNT_BACKUP_KEY_LENGTH = 30
ACCOUNT_EMAIL_TOKEN_LENGTH = 30

SESSION_TOKEN_LENGTH = 30
SESSION_MAX_DURATION_MINS = 120

POST_RANDOM_ID_LENGTH = 10
IMG_RANDOM_ID_LENGTH = 10

TOKEN_LENGTHS = {
    "creation": ACCOUNT_CREATION_TOKEN_LENGTH,
    "deletion": ACCOUNT_DELETION_TOKEN_LENGTH,
    "recovery": ACCOUNT_RECOVERY_TOKEN_LENGTH,
    "backup": ACCOUNT_BACKUP_KEY_LENGTH,
    "session": SESSION_TOKEN_LENGTH,
    "postid": POST_RANDOM_ID_LENGTH,
    "imgid": IMG_RANDOM_ID_LENGTH,
    "email": ACCOUNT_EMAIL_TOKEN_LENGTH
}

QUERY_MAX_LENGTH = 100

USER_MAX_POSTS = 200
USER_MAX_POSTS_PER_DAY = 5

USER_MAX_IMAGES = 50
USER_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg']

USER_MAX_COMMENTS_PER_DAY = 50

FRIEND_REQUESTS_MAX_PER_DAY = 20

#frontend

USERNAME_MAX_LENGTH = 30
USERNAME_MIN_LENGTH = 1

PASSWORD_MAX_LENGTH = 50
PASSWORD_MIN_LENGTH = 15

STATUS_MAX_LENGTH = 200
STATUS_MIN_LENGTH = 0

POST_MAX_LENGTH = 10000

POST_TITLE_MAX_LENGTH = 100
POST_TITLE_MIN_LENGTH = 1

IMG_TITLE_MAX_LENGTH = 100
IMG_TITLE_MIN_LENGTH = 1
IMG_MAX_SIZE_BYTES = 1000000

COMMENT_MAX_LENGTH = 200
COMMENT_MIN_LENGTH = 1

BUG_REPORT_MAX_LENGTH = 5000
BUG_REPORT_MIN_LENGTH = 100

INPUT_LENGTH_LIMITS = {
    "username": (USERNAME_MIN_LENGTH, USERNAME_MAX_LENGTH),
    "password": (PASSWORD_MIN_LENGTH, PASSWORD_MAX_LENGTH),
    "status": (STATUS_MIN_LENGTH, STATUS_MAX_LENGTH),
    "post-body": (0, POST_MAX_LENGTH),
    "post-title": (POST_TITLE_MIN_LENGTH, POST_TITLE_MAX_LENGTH),
    "image-title": (IMG_TITLE_MIN_LENGTH, IMG_TITLE_MAX_LENGTH),
    "comment": (COMMENT_MIN_LENGTH, COMMENT_MAX_LENGTH),
    "bug-report": (BUG_REPORT_MIN_LENGTH, BUG_REPORT_MAX_LENGTH)
}

