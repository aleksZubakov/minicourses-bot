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
        data = {}

        bot_record = self.collection.find_one( { 'token': raw_data['token'] } )
        if bot_record is None:
            # From User Data
            data['token'] = raw_data['token']
            data['bot_name'] = raw_data['name']
            data['screen_name'] = raw_data['screen_name']
            data['tags'] = raw_data['tags']
            data['author'] = raw_data['author']
            data['description'] = raw_data['description']
            data['messages'] = list( raw_data['messages'] )

            # Init with default
            data['connections_count'] = 0
            data['connections'] = dict()

            self.collection.insert_one(data)
            return True
        else:
            raise IndexError('Bot with token "{0}" already exists'.format(raw_data['token']))

    def get_description(self):
        pass

    def new_user(self, bot_token, chat_id):

        bot_record = self.collection.find_one({ 'token': bot_token })
        # print(bot_record)
        if bot_record is None:
            raise ValueError('Not bot present with token "{0}"'.format(bot_token))
        print('>',bot_record)

        connections = bot_record['connections']

        new_user = connections[str(chat_id)] = dict()
        new_user['last_read'] = False
        new_user['messages_number'] = 0

        try:
            new_connections_count = bot_record['connections_count'] + 1
        except KeyError:
            c = 0
            for i in bot_record['connections']:
                c += 1
            new_connections_count = c


        self.collection.update(
            { 'token': bot_token },
            { '$set': {'connections': connections, 'connections_count': new_connections_count } },
            upsert=False
        )

        updated_bot_record = self.collection.find_one({ 'token': bot_token })
        return updated_bot_record['messages'][0]

    def get_info(self, bot_token, chat_id):

        chat_id = str(chat_id)

        bot_record = self.collection.find_one({ 'token': bot_token })
        connections = bot_record['connections']
        cur_connection = connections[chat_id]
        is_read = cur_connection['last_read']
        # cur_msg_number = cur_connection['messages_number']

        if is_read:
            msg_number = cur_connection['messages_number'] =  cur_connection['messages_number'] +  1
            cur_connection['last_read'] = False
        else:
            msg_number = cur_connection['messages_number']

        self.collection.update(
            { 'token': bot_token },
            { '$set': { 'connections': connections } }
        )

        updated_bot_record = self.collection.find_one( { 'token': bot_token } )
        print(updated_bot_record)


        return 10, updated_bot_record['messages'][msg_number]





    def set_read(self, bot_token, chat_id):
        bot_record = self.collection.find_one({ 'token': bot_token })

        connections = bot_record['connections']
        connections[chat_id]['last_read'] = True

        self.collection.update(
            { 'token': bot_token },
            { '$set': { 'connections': connections } }
        )

        return True


    def get_all_courses(self):
        pass
