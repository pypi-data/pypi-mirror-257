import json
import os
import pathlib
import requests
import sys

from typing import Callable, Optional
from merrymake.streamhelper import read_to_end
from merrymake.nullmerrymake import NullMerrymake
from merrymake.imerrymake import IMerrymake
from merrymake.merrymimetypes import MerryMimetypes, MerryMimetype
from merrymake.envelope import Envelope

class Merrymake(IMerrymake):
    """Merrymake is the main class of this library, as it exposes all other
     functionality, through a builder pattern.

     @author Merrymake.eu (Chirstian Clausen, Nicolaj Græsholt)
    """

    @staticmethod
    def service():
        """This is the root call for a Merrymake service.

        Returns
        -------
        A Merrymake builder to make further calls on
        """

        args = sys.argv[1:]
        return Merrymake(args)

    def __init__(self, args):

        try:
            self.action = args[-2]
            buf = json.loads(args[-1]);
            self.envelope = Envelope(buf.get("messageId"), buf.get("traceId"), buf.get("sessionId"))
            self.payloadBytes = read_to_end(sys.stdin.buffer)
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print('Decoding JSON has failed')
            raise Exception("Decoding JSON has failed")
        except:
            print("Could not read from stdin")
            raise Exception("Could not read from stdin")

    def handle(self, action: str, handler: Callable[[bytearray, Envelope], None]):
        if self.action == action:
            handler(self.payloadBytes, self.envelope)
            return NullMerrymake()
        else:
            return self

    def initialize(self, f: Callable[[], None]):
        f()

    @staticmethod
    def post_event_to_rapids(pEvent: str):
        """Post an event to the central message queue (Rapids), without a payload.

        Parameters
        ----------
        event : string
            The event to post
        """

        uri = f"{os.getenv('RAPIDS')}/{pEvent}"
        requests.post(uri)

    @staticmethod
    def post_to_rapids(pEvent: str, body: str, content_type: MerryMimetype):
        """Post an event to the central message queue (Rapids), with a payload and its
         content type.

        Parameters
        ----------
        event : string
            The event to post
        body : string
            The payload
        contentType : MimeType
            The content type of the payload
        """

        headers = {'Content-Type': content_type.__str__()}
        uri = f"{os.getenv('RAPIDS')}/{pEvent}"

        requests.post(uri, data=body, headers=headers)

    @staticmethod
    def reply_to_origin(body: str, content_type: MerryMimetype):
        """Post a reply back to the originator of the trace, with a payload and its
         content type.

        Parameters
        ----------
        body : string
            The payload
        contentType : MimeType
            The content type of the payload
        """

        Merrymake.post_to_rapids("$reply", body, content_type)

    @staticmethod
    def reply_file_to_origin(path: str):
        """Send a file back to the originator of the trace.

        Parameters
        ----------
        path : string
            The path to the file
        """

        # get the extension, skip the dot
        extension = pathlib.Path(path).suffix[1:]

        mime = MerryMimetypes.get_mime_type(extension)

        Merrymake.reply_file_to_origin_with_content_type(path, mime)

    @staticmethod
    def reply_file_to_origin_with_content_type(path: str, content_type: MerryMimetype):
        """Send a file back to the originator of the trace.

        Parameters
        ----------
        path : string
            The path to the file starting from main/resources
        contentType : MimeType
            The content type of the file
        """
        with open(path, 'r') as file:
            body = file.read()
            Merrymake.post_to_rapids("$reply", body, content_type)

    @staticmethod
    def join_channel(channel: str):
        """Subscribe to a channel
        Events will stream back messages broadcast to that channel. You can join multiple channels. You stay in the channel until the
        request is terminated.

        Note: The origin-event has to be set as "streaming: true" in the
        event-catalogue.

        Parameters
        ----------
        channel : string
            The channel to join
        """

        Merrymake.post_to_rapids("$join", channel, MerryMimetypes.get_mime_type("txt"))

    @staticmethod
    def broadcast_to_channel(to: str, event: str, payload: str):
        """Broadcast a message (event and payload) to all listeners in a channel.

        Parameters
        ----------
        to : string
            The channel to broadcast to
        event : string
            The event-type of the message
        payload : string
            The payload of the message
        """

        Merrymake.post_to_rapids("$broadcast", json.dumps({"to": to, "event": event, "payload": payload}), MerryMimetypes.get_mime_type("json"))
