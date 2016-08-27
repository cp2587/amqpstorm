from amqpstorm.management.base import ManagementHandler

API_CHANNEL = 'channels/%s'
API_CHANNELS = 'channels'


class Channel(ManagementHandler):
    def get(self, channel):
        """Get Connection details.

        :param channel: Channel name

        :rtype: dict
        """
        return self.config.http_client.get(API_CHANNEL % channel)

    def list(self):
        """List all Channels.

        :rtype: list
        """
        return self.config.http_client.get(API_CHANNELS)
