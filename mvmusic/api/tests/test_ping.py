from mvmusic.api.tests import BaseClientTest


class TestPing(BaseClientTest):
    def test_unauthorized_ping(self):
        resp = self.client.get("/rest/ping.view?f=json")

        self.assertEqual(resp.headers["Query-Count"], "0")
        self.assertEqual(resp.status_code, 401)

        self.assertDictEqual(resp.json, {
            "subsonic-response": {
                "status": "failed",
                "version": self.version,
                "error": {
                    "code": 40,
                    "message": "Unauthorized"
                }
            }
        })

    def test_ping(self):
        resp = self.make_request("ping")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["Query-Count"], "1")

        self.assertDictEqual(resp.json, {
            "subsonic-response": {
                "status": "ok",
                "version": self.version
            }
        })
