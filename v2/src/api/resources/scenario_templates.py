# v2/src/api/resources/scenario_templates.py
"""HTML email templates for scenarios"""


class ScenarioTemplates:
    """Collection of HTML email templates"""

    DEFAULT_TEMPLATE = """<!doctype html>
<html style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5;">
\t<body style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5; direction: ltr;" class="ck-content">
\t\t<p>Dear {{employee.full_name}},</p>
\t\t<p>{message_body}</p>
\t\t<p><a href="{{attack_url}}">Click here</a></p>
\t\t<p>{closing_message}</p>
\t\t<p>Sincerely,<br>{sender_name}</p>
\t</body>
</html>"""

    VOICEMAIL_TEMPLATE = """<!doctype html>
<html style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5;">
\t<body style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5; direction: ltr;" class="ck-content">
\t\t<p>Dear {{employee.full_name}},</p>
\t\t<p>You have received a new voicemail message.</p>
\t\t<p>Voicemail Details: - Sender: External Caller - Duration: 0:45 seconds</p>
\t\t<p>Please click on the link below to listen to your message:</p>
\t\t<p><a href="{{attack_url}}">ACCESS VOICEMAIL</a></p>
\t\t<p>This notification is sent from Google Cloud Application Integration. Please do not reply to this email.</p>
\t\t<p>Thank you, Google Cloud Support</p>
\t\t<p>© 2026 Google LLC. All rights reserved.</p>
\t</body>
</html>"""

    POLICY_UPDATE_TEMPLATE = """<!doctype html>
<html style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5;">
\t<body style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5; direction: ltr;" class="ck-content">
\t\t<p>Dear {{employee.full_name}},</p>
\t\t<p>This email is to inform you of a critical update to university policy that requires your immediate attention and acknowledgement. This is a mandatory update applicable to all students and staff.</p>
\t\t<p>To review and acknowledge the updated policy, please click on the secure link below to access the official university policy form. Failure to acknowledge this policy within 48 hours may result in temporary service interruptions.</p>
\t\t<p><a href="{{attack_url}}">Click here</a></p>
\t\t<p>Please ensure you complete this form at your earliest convenience.</p>
\t\t<p>Thank you for your cooperation.</p>
\t\t<p>Sincerely,<br>University Administration</p>
\t</body>
</html>"""

    PASSWORD_RESET_TEMPLATE = """<!doctype html>
<html style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5;">
\t<body style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5; direction: ltr;" class="ck-content">
\t\t<p>Dear {{employee.full_name}},</p>
\t\t<p>We received a request to reset your password. If you did not make this request, please ignore this email.</p>
\t\t<p>To reset your password, click the link below:</p>
\t\t<p><a href="{{attack_url}}">Reset Password</a></p>
\t\t<p>This link will expire in 24 hours for security reasons.</p>
\t\t<p>Best regards,<br>IT Security Team</p>
\t</body>
</html>"""

    INVOICE_TEMPLATE = """<!doctype html>
<html style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5;">
\t<body style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5; direction: ltr;" class="ck-content">
\t\t<p>Dear {{employee.full_name}},</p>
\t\t<p>Your invoice is ready for review. Please find the details below:</p>
\t\t<p>Invoice Number: INV-{invoice_number}<br>Amount Due: ${amount}<br>Due Date: {due_date}</p>
\t\t<p><a href="{{attack_url}}">View Invoice</a></p>
\t\t<p>Thank you for your business.</p>
\t\t<p>Regards,<br>Accounting Department</p>
\t</body>
</html>"""

    PACKAGE_DELIVERY_TEMPLATE = """<!doctype html>
<html style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5;">
\t<body style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5; direction: ltr;" class="ck-content">
\t\t<p>Dear {{employee.full_name}},</p>
\t\t<p>We attempted to deliver your package but you were not available.</p>
\t\t<p>Tracking Number: {tracking_number}<br>Delivery Attempt: {attempt_date}</p>
\t\t<p>To reschedule your delivery, please click below:</p>
\t\t<p><a href="{{attack_url}}">Reschedule Delivery</a></p>
\t\t<p>Thank you,<br>Delivery Services</p>
\t</body>
</html>"""

    HR_ANNOUNCEMENT_TEMPLATE = """<!doctype html>
<html style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5;">
\t<body style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5; direction: ltr;" class="ck-content">
\t\t<p>Dear {{employee.full_name}},</p>
\t\t<p>This is an important announcement from the Human Resources department.</p>
\t\t<p>{announcement_text}</p>
\t\t<p>Please review the full details by clicking the link below:</p>
\t\t<p><a href="{{attack_url}}">View Full Announcement</a></p>
\t\t<p>If you have any questions, please contact HR.</p>
\t\t<p>Best regards,<br>Human Resources</p>
\t</body>
</html>"""

    SECURITY_ALERT_TEMPLATE = """<!doctype html>
<html style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5;">
\t<body style="padding: 0; font-family: 'Public Sans', sans-serif; line-height: 1.5; direction: ltr;" class="ck-content">
\t\t<p>Dear {{employee.full_name}},</p>
\t\t<p><strong>SECURITY ALERT:</strong> Unusual activity detected on your account.</p>
\t\t<p>Location: {location}<br>Time: {timestamp}<br>Device: {device}</p>
\t\t<p>If this was not you, please verify your account immediately:</p>
\t\t<p><a href="{{attack_url}}">Verify Account</a></p>
\t\t<p>Stay secure,<br>Security Team</p>
\t</body>
</html>"""

    @staticmethod
    def get_template(template_name: str) -> str:
        """
        Get template by name

        Args:
            template_name: Name of the template (e.g., 'VOICEMAIL', 'POLICY_UPDATE')

        Returns:
            HTML template string
        """
        template_map = {
            'DEFAULT': ScenarioTemplates.DEFAULT_TEMPLATE,
            'VOICEMAIL': ScenarioTemplates.VOICEMAIL_TEMPLATE,
            'POLICY_UPDATE': ScenarioTemplates.POLICY_UPDATE_TEMPLATE,
            'PASSWORD_RESET': ScenarioTemplates.PASSWORD_RESET_TEMPLATE,
            'INVOICE': ScenarioTemplates.INVOICE_TEMPLATE,
            'PACKAGE_DELIVERY': ScenarioTemplates.PACKAGE_DELIVERY_TEMPLATE,
            'HR_ANNOUNCEMENT': ScenarioTemplates.HR_ANNOUNCEMENT_TEMPLATE,
            'SECURITY_ALERT': ScenarioTemplates.SECURITY_ALERT_TEMPLATE,
        }
        return template_map.get(
            template_name.upper(), ScenarioTemplates.DEFAULT_TEMPLATE
        )
