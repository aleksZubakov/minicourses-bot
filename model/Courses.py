import pymongo
from random import randint

client = pymongo.MongoClient()
db = client['courses']
# courses_collection = db['courses']
# Dev Collection
courses_collection = db['test']


class Courses:

    def __init__(self):
        self.env = 'prod'

        if self.env == 'dev':
            self.collection = db['test']
        else:
            self.collection = db['courses']

    def init_bot(self, raw_data):
        data = {}

        bot_record = self.collection.find_one( { 'token': raw_data['token'] } )
        if bot_record is None:
            # From User Data
            data['token'] = str(raw_data['token'])
            # data['bot_name'] = raw_data['name']
            # data['screen_name'] = raw_data['screen_name']
            data['tags'] = raw_data['tags']
            data['author'] = raw_data['author']
            data['description'] = raw_data['description']
            data['created_at'] = raw_data['timestamp']
            data['messages'] = list( raw_data['messages'] )
            data['last_message'] = raw_data['last_message']

            # Init with default
            data['connections_count'] = 0
            data['connections'] = dict()

            self.collection.insert_one(data)
            return True
        else:
            # print('Bot with token "{0}" already exists'.format(raw_data['token']))
            pass

    def set_bot_name(self, bot_token, name, screen_name):
        self.collection.update_one(
            {'token': bot_token},
            { '$set': {
                'bot_name': name,
                'screen_name': screen_name
            }}
        )



    def get_description_name(self, bot_token):
        bot_record = self.collection.find_one( {'token': bot_token } )
        try:
            return bot_record['screen_name']
        except (IndexError, KeyError):
            return ""

    def new_user(self, bot_token, chat_id):
        chat_id = str(chat_id)
        # print(self.collection, bot_token, chat_id)
        bot_record = self.collection.find_one({ 'token': bot_token })
        # print(bot_record)
        if bot_record is None:
            # print('Not bot present with token "{0}"'.format(bot_token))
            pass
        # print('>',bot_record)

        connections = bot_record['connections']

        new_user = connections[str(chat_id)] = dict()
        new_user['last_read'] = False
        new_user['messages_number'] = 1
        new_user['delays'] = [ 10, 10, 10, 10, 10 ]
        new_user['missed'] = 0

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
        return 10, updated_bot_record['messages'][0]

    def get_info(self, bot_token, chat_id):

        chat_id = str(chat_id)

        bot_record = self.collection.find_one({ 'token': bot_token })
        connections = bot_record['connections']
        cur_connection = connections[chat_id]
        is_read = cur_connection['last_read']
        # cur_msg_number = cur_connection['messages_number']

        if is_read:
            msg_number = cur_connection['messages_number'] = cur_connection['messages_number'] +  1
            cur_connection['last_read'] = False
        else:
            msg_number = cur_connection['messages_number']

        try:
            delay = cur_connection['next_delay'] + randint(-5, 5)
        except KeyError:
            delay = 10 + randint(-5, 5)

        self.collection.update(
            { 'token': bot_token },
            { '$set': { 'connections': connections } }
        )

        updated_bot_record = self.collection.find_one( { 'token': bot_token } )
        # print(updated_bot_record)

        try:
            message_to_send = updated_bot_record['messages'][msg_number]
        except IndexError:
            message_to_send = updated_bot_record['last_message']
            delay = -1

        return delay, message_to_send






    def set_read(self, bot_token, chat_id, passed):
        # print("!!!!!",bot_token, chat_id, passed)
        bot_record = self.collection.find_one({ 'token': bot_token })
        chat_id = str(chat_id)
        # print(1, bot_record)
        connections = bot_record['connections']
        # print(2, connections)
        # print('!!!!',chat_id, connections[chat_id])
        connection = connections[chat_id]
        # print(3, connection)

        # connections[chat_id]['last_read'] = True
        connection['last_read'] = True
        # print(connection)
        delays = connection['delays']
        msg_count = connection['messages_number'] + 1
        missed = connection['missed']

        i = msg_count + missed + 1

        if passed > delays[ i % 5 ]:
            delays[(i - 1) % 5] = delays[(i - 1) % 5] + delays[ i % 5 ]
            delays[ i % 5 ] = passed - delays[ i % 5 ]
            delays[ (i + 1) % 5 ] = delays[ (i + 1) % 5 ] - delays[ i % 5 ]
            missed += 1
            delay = delays[ (i + 1) % 5 ]
        else:
            delays[ i % 5 ] -= passed
            delays[ (i - 1) % 5 ] += passed
            delay = delays[ i % 5 ]


        # print("!!!!", delay)
        connection['next_delay'] = delay



        self.collection.update(
            { 'token': bot_token },
            { '$set': { 'connections': connections } }
        )

        return True


    def get_all_courses(self):
        pass
