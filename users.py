from database import CursorFromConnectionFromPool


class Users():

    def __init__(self, id, screen_name, oauth_token, oauth_token_secret):
        self.id = id
        self.screen_name = screen_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    def __repr__(self):
        return "{a}".format(a=self.screen_name)

    def save_to_db(self):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('insert into users (screen_name, oauth_token, oauth_token_secret) values (%s,%s,%s)',
                           (self.screen_name, self.oauth_token, self.oauth_token_secret))

    @ classmethod
    def read_from_db(cls, screen_name):
        with CursorFromConnectionFromPool() as cursor:
            cursor.execute('select * from users where screen_name = %s',
                           (screen_name,))  # tuple
            user_data = cursor.fetchone()  # return list

        if user_data is not None:
            return cls(id = user_data[0], screen_name=user_data[1], oauth_token=user_data[2], oauth_token_secret=user_data[3])  # class constructor returns class object