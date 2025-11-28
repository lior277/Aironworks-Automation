from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage


class AIAgentPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.ask_box = self.page.get_by_role('textbox', name='Ask me anything')
        self.send_button = self.page.get_by_role('button', name='Send')
        self.user_message_boxes = self.page.locator(
            '//div[contains(@class, "css-s4hhx1")]'
        )
        self.ai_message_boxes = self.page.locator(
            '//div[contains(@class, "css-12ia9as")]'
        )
        self.scenario_blocks = self.ai_message_boxes.nth(-1).locator(
            '//div[contains(@class, "css-1resfla")]'
        )
        self.education_blocks = self.ai_message_boxes.nth(-1).locator(
            '//div[contains(@class, "css-2cfzeo")]'
        )
        self.campaign_blocks = self.ai_message_boxes.nth(-1).locator(
            '//div[contains(@class, "css-14zyegh")]'
        )
        self.education_campaign_blocks = self.ai_message_boxes.nth(-1).locator(
            '//div[contains(@class, "css-14zyegh")]'
        )
        self.split_panel = self.page.locator('//div[contains(@class, "css-c60s8t")]')

    def ask_ai_agent(
        self, question: str, question_type: str, keyword: str, number_blocks=3
    ):
        self.ask_box.fill(question)
        self.send_button.click()
        expect(self.user_message_boxes.nth(-1)).to_contain_text(
            question, ignore_case=True
        )
        match question_type:
            case 'search preview scenario':
                self.search_preview_scenario_check(number_blocks, keyword)
            case 'search preview education content':
                self.search_preview_education_content_check(number_blocks, keyword)
            case 'search preview campaign':
                self.search_preview_campaign_check(number_blocks)
            case 'search preview education campaign':
                self.search_preview_education_campaign_check(number_blocks)
            case _:
                raise ValueError(f'Invalid question type: {question_type}')

    def search_preview_scenario_check(self, number_blocks: int, keyword: str):
        expect(self.scenario_blocks).to_have_count(number_blocks, timeout=180_000)
        count = self.scenario_blocks.count()
        for i in range(count):
            expect(self.scenario_blocks.nth(i).locator('//h6')).to_contain_text(
                keyword, ignore_case=True
            )
            expect(
                self.scenario_blocks.nth(i).get_by_role(
                    'button', name='Preview Scenario'
                )
            ).to_be_visible()
            self.scenario_blocks.nth(i).get_by_role(
                'button', name='Preview Scenario'
            ).click()
            expect(self.split_panel).to_be_visible()
            expect(
                self.split_panel.get_by_role('heading', name='Scenarios Preview')
            ).to_be_visible()
            self.split_panel.get_by_role('button', name='Close').click()
            expect(self.split_panel).to_be_hidden()

    def search_preview_education_content_check(self, number_blocks: int, keyword: str):
        expect(self.education_blocks).to_have_count(number_blocks, timeout=180_000)
        count = self.education_blocks.count()
        for i in range(count):
            expect(
                self.education_blocks.nth(i).get_by_role('heading', level=3)
            ).to_contain_text(keyword, ignore_case=True)
            expect(
                self.education_blocks.nth(i).get_by_role(
                    'button', name='Preview Content'
                )
            ).to_be_visible()
            self.education_blocks.nth(i).get_by_role(
                'button', name='Preview Content'
            ).click()
            expect(self.split_panel).to_be_visible()
            expect(
                self.split_panel.get_by_role('heading', name='Content Preview')
            ).to_be_visible()
            self.split_panel.get_by_role('button', name='Close').click()
            expect(self.split_panel).to_be_hidden()

    def search_preview_campaign_check(self, number_blocks: int):
        expect(self.campaign_blocks).to_have_count(number_blocks, timeout=180_000)
        count = self.campaign_blocks.count()
        for i in range(count):
            expect(
                self.campaign_blocks.nth(i).get_by_role(
                    'button', name='Preview Campaign'
                )
            ).to_be_visible()
            self.campaign_blocks.nth(i).get_by_role(
                'button', name='Preview Campaign'
            ).click()
            expect(self.split_panel).to_be_visible()
            expect(
                self.split_panel.get_by_role('heading', name='Campaign Preview')
            ).to_be_visible()
            self.split_panel.get_by_role('button', name='Close').click()
            expect(self.split_panel).to_be_hidden()

    def search_preview_education_campaign_check(self, number_blocks: int):
        expect(self.education_campaign_blocks).to_have_count(
            number_blocks, timeout=180_000
        )
        count = self.education_campaign_blocks.count()
        for i in range(count):
            expect(
                self.education_campaign_blocks.nth(i).get_by_role(
                    'button', name='Preview Campaign'
                )
            ).to_be_visible()
            self.education_campaign_blocks.nth(i).get_by_role(
                'button', name='Preview Campaign'
            ).click()
            expect(self.split_panel).to_be_visible()
            expect(
                self.split_panel.get_by_role('heading', name='Campaign Preview')
            ).to_be_visible()
            self.split_panel.get_by_role('button', name='Close').click()
            expect(self.split_panel).to_be_hidden()
