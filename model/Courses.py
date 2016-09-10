import pymongo

client = pymongo.MongoClient()
db = client['courses']
# courses_collection = db['courses']
# Dev Collection
courses_collection = db['test']

class Courses:

    def __init__(self):
        self.env = 'dev'

        if self.env == 'dev':
            self.collection = db['test']
        else:
            self.collection = db['courses']


    def init_bot(self, raw_data):
        data = dict()

        data['token'] = raw_data.token
        data['messages'] = list( raw_data.messages )
        data['connections'] = dict()


        self.collection.insert_one(data)


    def get_description(self):
        pass

    def new_user(self, bot_token, chat_id):

        bot_record = self.collection.find({ 'token': bot_token })

        connections = bot_record['connections']

        new_user = connections[chat_id] = dict()
        new_user['last_read'] = False
        new_user['messages_number'] = 0

        self.collection.update(
            { 'token': bot_token },
            { '$set': {'connections': connections } },
            upsert=False
        )

        updated_bot_record = self.collection.find({ 'token': bot_token })
        return updated_bot_record['messages'][0]


        # bot_record = self.collection.find_one_and_update(
        #     { "token": bot_token  },
        #     { "connections":  new_user }
        # )



    def get_info(self):
        pass

    def set_read(self):
        pass