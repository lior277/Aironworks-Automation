import random
import string

import faker

fake = faker.Faker()


def generate_faker_multiline_text(lines=5, empty_line_prob=0.3):
    special_chars = string.punctuation + '©®™✓€£¥•→←↑↓§±'
    result = []

    for _ in range(lines):
        if random.random() < empty_line_prob:
            result.append('')  # empty line
            continue

        indent = ' ' * random.randint(0, 8)
        base = fake.sentence(nb_words=random.randint(5, 10))
        sprinkled = ''.join(
            char if random.random() > 0.1 else random.choice(special_chars)
            for char in base
        )
        result.append(indent + sprinkled)

    return '\n'.join(result)
