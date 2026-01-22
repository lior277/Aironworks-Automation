from playwright.sync_api import Page


def wait_for_loading(page: Page, timeout: int = 10_000) -> None:
    selectors = [
        '.loading-spinner',
        "[data-testid='loading']",
        '.MuiCircularProgress-root',
        '.MuiBackdrop-root',
    ]
    for sel in selectors:
        try:
            page.locator(sel).first.wait_for(state='hidden', timeout=timeout)
            return
        except Exception:
            continue
