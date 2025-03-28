from mvmusic.api.tests import BaseClientTest


class TestGetLicense(BaseClientTest):
    def test_get_license(self):
        resp = self.make_request("getLicense")

        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.headers["Query-Count"], "1")

        self.assertDictEqual(resp.json, {
            "subsonic-response": {
                "status": "ok",
                "version": self.version,
                "license": {
                    "valid": True
                }
            }
        })
