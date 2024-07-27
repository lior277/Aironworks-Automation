from playwright.sync_api import expect


def is_selected(element):
    expect(element).to_have_attribute('aria-selected', 'true')
