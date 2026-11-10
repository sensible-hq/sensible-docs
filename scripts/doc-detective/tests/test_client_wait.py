"""SensibleClient._wait: polls an extraction, and gives up at its deadline instead of hanging."""

import unittest
from unittest import mock

from codetests import sensible
from codetests.errors import CodeTestError


class Response:
    def __init__(self, body):
        self.body = body

    def raise_for_status(self):
        pass

    def json(self):
        return self.body


class WaitTest(unittest.TestCase):
    def client(self, *bodies):
        client = sensible.SensibleClient("key")
        polls = [Response(b) for b in bodies]
        client._api = mock.Mock(side_effect=lambda method, path: polls.pop(0) if len(polls) > 1 else polls[0])
        return client

    @mock.patch("time.sleep", lambda s: None)
    def test_returns_when_complete(self):
        client = self.client({"status": "PROCESSING"}, {"status": "COMPLETE", "parsed_document": {}})
        self.assertEqual(client._wait("e1")["status"], "COMPLETE")

    def test_gives_up_at_the_deadline(self):
        clock = iter(range(0, 10_000, 100))
        with mock.patch("time.time", lambda: next(clock)), mock.patch("time.sleep", lambda s: None):
            with self.assertRaises(CodeTestError) as caught:
                self.client({"status": "PROCESSING"})._wait("e1", timeout=240)
        self.assertIn("didn't finish within 240 seconds", str(caught.exception))


if __name__ == "__main__":
    unittest.main()
