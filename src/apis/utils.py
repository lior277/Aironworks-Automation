def get_request_context_for_page(playwright, page, base_url):
    return playwright.request.new_context(
        base_url=base_url,
        storage_state=page.request.storage_state(),
    )
