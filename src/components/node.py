from src.components.client import Sender, Receiver, Client


class Node(object):
    """
    Represents virtual destination/service aka node.
    In a case of interconnect vm with qdrouterd is represented as a Router node.
    When there is a sender present on such node, it is a Sender node.
    All future representations should inherit from this class.
    """

    # TODO: restart method
    def __init__(self, hostname="localhost"):
        self.hostname = hostname


class ClientNode(Node):
    """
    Contains common API for sender/receiver, aka client, nodes
    Wraps actions from the perspective of the physical node over
    clients. This means that ClientNode contain client and wraps its interface to
    bridge the communication for the user
    """

    def __init__(self, hostname, client=None):
        """
        :param hostname: hostname or ip address of the physical node
        :type hostname: str
        :param client: client is an entity which is used for sending and receiving messages. Be sure that you are referencing class not instance.
        :type client: Client
        """
        super(ClientNode, self).__init__(hostname)
        self.client_class = client  # client as instance capable of send/receive - e.g. MessagingHandler implementation
        self.client = None

    @property
    def last_message(self):
        """
        :return: last message from the pool
        :rtype: proton.Message
        """
        return self.client.message_pool[-1]


class BasicSenderNode(ClientNode):
    """
    Basic representation of Sender Node
    """

    def __init__(self, hostname, sender=Sender):
        """
        :param hostname: hostname or ip address of the physical node
        :type hostname: str
        :param sender: client capable of sending messages
        :type sender: Client
        """
        super(BasicSenderNode, self).__init__(hostname, sender)

    def send(self, node, address=None, count=1, messages=[]):
        """
        :param node: target node where to send messages
        :type node: Node
        :param address: address where to send (queue name, topic name)
        :type address: str
        :param count: count of messages to send
        :type count: int
        :param messages: pool of messages to send - proton.Message
        :type messages: list
        :return: None
        """
        self.client = self.client_class(hostname=node.hostname, address=address, count=count, messages=messages)
        self.client.run()


class BasicReceiverNode(ClientNode):
    """
    Basic representation of Receiver Node
    """

    def __init__(self, hostname, receiver=Receiver):
        """
        :param hostname: hostname or ip address of the physical node
        :type hostname: str
        :param receiver: client capable of receiving messages
        :type receiver: Client
        """
        super(BasicReceiverNode, self).__init__(hostname, receiver)

    def receive(self, node, address=None, expected=1):
        """
        :param node: target node where to send messages
        :type node: Node
        :param address: address where to send (queue name, topic name)
        :type address: str
        :param expected: count of messages to be expected
        :type expected: int
        :return:
        """
        self.client = self.client_class(hostname=node.hostname, address=address, expected=expected)
        self.client.run()
