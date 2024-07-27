from playwright.sync_api import Page, Playwright, APIRequestContext


def get_request_context_for_page(
    playwright: Playwright, page: Page, base_url
) -> APIRequestContext:
    return playwright.request.new_context(
        base_url=base_url, storage_state=page.request.storage_state()
    )
