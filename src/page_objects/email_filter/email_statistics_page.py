from playwright.sync_api import Page, expect

from src.page_objects.base_page import BasePage


class EmailStatisticsPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.analysis_graph_title = self.page.get_by_text('ANALYSIS GRAPH', exact=True)
        self.risk_assesssment_title = self.page.get_by_text(
            'RISK ASSESSMENT', exact=True
        )
        self.email_statistics_title = self.page.get_by_text(
            'EMAIL STATISTICS', exact=True
        )

    def verify_sections_display(self):
        expect(self.analysis_graph_title).to_be_visible()
        expect(self.risk_assesssment_title).to_be_visible()
        expect(self.email_statistics_title).to_be_visible()
