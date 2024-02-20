"""

Simple library for creating message queue based on Redis and its channels


v1, 2024, https://github.com/AndrewLt
"""


import redis


class MessageQueue:
    def __init__(self, queue_name: str, queue_method: str = 'FIFO', **kwargs):
        """
        :param queue_name: name of message chanel
        :param queue_method: FIFO or LIFO
        :param kwargs: redis host, port and any parameters for obj redis.Redis()
        """
        self.queue_name = queue_name
        self.q_method = 1 if queue_method == 'FIFO' else 0
        self._redis_connector = redis.Redis(**kwargs)

    def send_message(self, message):
        """
        :param message: message body
        :return: the length of the list after the push operation
        """
        return self._redis_connector.rpush(self.queue_name, message)

    def get_message(self):
        """
        :return: message from the channel
        """
        if self.q_method:
            return self._redis_connector.lpop(self.queue_name)
        return self._redis_connector.rpop(self.queue_name)

