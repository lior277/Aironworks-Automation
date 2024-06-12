from playwright.sync_api import Page


class EducationLandingPage:
    def __init__(self, page: Page, link_url: str):
        self.page = page
        self.email_input = self.page.get_by_role("textbox", name="email")
        self.submit_button = self.page.get_by_role("button", name="Submit")
        self.complete_button = self.page.get_by_role("button", name="Complete")
        self.embedded_content = self.page.frame_locator("iframe")
        self.link_url = link_url

    @property
    def iframe(self):
        return self.page.main_frame.child_frames[0]

    def open(self):
        self.page.goto(self.link_url)
        self.page.wait_for_load_state("load")
