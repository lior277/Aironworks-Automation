def convert_language_code_to_text(language_code: str) -> str:
    match language_code:
        case 'en':
            return 'English'
        case 'jp':
            return 'Japanese'
        case _:
            return language_code
