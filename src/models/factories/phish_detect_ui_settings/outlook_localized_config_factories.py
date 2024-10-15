from src.models.phish_detect_ui_settings.outlook_localized_config import (
    OutlookConfigData,
)


class OutlookLocalizedConfigFactory:
    @staticmethod
    def get_default_en_config() -> OutlookConfigData:
        return OutlookConfigData(
            assessment_button=True,
            assessment_button_description="Click the above button to evaluate the email's security level and get risk assessment result",
            assessment_button_text='Perform AI Risk Assessment',
            incident_button=True,
            incident_button_description="Click the above button in case you entered a suspicious link or downloaded a suspicious file and forward the email to your organization's security center and allow them to conduct further investigation to assess the situation's risk level",
            incident_button_text='Report an Incident',
            language='en',
            subtext='',
        )

    @staticmethod
    def get_default_zh_config() -> OutlookConfigData:
        return OutlookConfigData(
            assessment_button=True,
            assessment_button_description='点击上面的按钮以评估电子邮件的安全级别并获取风险评估结果',
            assessment_button_text='执行人工智能风险评估',
            incident_button=True,
            incident_button_description='如果您输入了可疑链接或下载了可疑文件，请点击上面的按钮，并将电子邮件转发给您组织的安全中心，允许他们进行进一步调查以评估情况的风险级别',
            incident_button_text='报告事件',
            language='zh',
            subtext='',
        )

    @staticmethod
    def get_default_jp_config() -> OutlookConfigData:
        return OutlookConfigData(
            assessment_button=True,
            assessment_button_description='このボタンでメールの危険度をチェックしましょう。',
            assessment_button_text='AIでリスクを判定する',
            incident_button=True,
            incident_button_description='怪しいURLや添付ファイルを開いてしまった場合、このボタンですぐにセキュリティ担当者へ報告しましょう。',
            incident_button_text='報告する',
            language='jp',
            subtext='',
        )

    @staticmethod
    def get_outlook_config(
        assessment_button: bool, incident_button: bool
    ) -> OutlookConfigData:
        return OutlookConfigData(
            assessment_button=assessment_button,
            assessment_button_description="Click the above button to evaluate the email's security level and get risk assessment result",
            assessment_button_text='Perform AI Risk Assessment',
            incident_button=incident_button,
            incident_button_description="Click the above button in case you entered a suspicious link or downloaded a suspicious file and forward the email to your organization's security center and allow them to conduct further investigation to assess the situation's risk level",
            incident_button_text='Report an Incident',
            language='en',
            subtext='',
        )
