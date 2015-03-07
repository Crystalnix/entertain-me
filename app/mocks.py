__author__ = 'anmekin'

def get_fake_photos():
    return {"photos":{"page": 1, "pages": 1, "perpage": 100, "total": 5,
            "photo": [{"id": "14950215319", "owner": "92921037@N00", "secret": "677fd43117",
                       "server": "3892", "farm": 4, "title": "Virginia Beach Pier", "ispublic": 1,
                       "isfriend": 0, "isfamily": 0, "date_faved": "1425558480"},
            ]}, "stat": "ok"}

def bad_request_photos():
    return { "stat": "fail", "code": 1, "message": "User not found" }


def get_fake_users():
    return { "photo": { "person": [
      { "nsid": "131063911@N08", "username": "zeadramadan2000", "realname": "", "favedate": "1425717228", "iconserver": 0, "iconfarm": 0, "contact": 0, "friend": 0, "family": 0 },
    ], "id": "14950215319", "secret": "677fd43117", "server": "3892", "farm": 4, "page": 1, "pages": 72, "perpage": 10, "total": "717" }, "stat": "ok" }

def bad_request_users():
    return { "stat": "fail", "code": 1, "message": "Photo not found" }