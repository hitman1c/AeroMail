import unittest

from email_template import format_email


class EmailTemplateTests(unittest.TestCase):
    def test_format_email_includes_sender_details(self):
        email = format_email(
            "Welcome",
            "John",
            "Thanks for joining our platform.",
            sender_name="MailFlow Pro",
            sender_email="support@example.com",
        )

        self.assertIn("Subject: Welcome", email)
        self.assertIn("Dear John,", email)
        self.assertIn("MailFlow Pro", email)
        self.assertIn("support@example.com", email)


if __name__ == "__main__":
    unittest.main()
