import re
from django.utils.text import slugify as django_slugify


AR_TO_FA_CHARS = {
    "ك": "ک",
    "ي": "ی",
    "ى": "ی",
    "ؤ": "و",
    "إ": "ا",
    "أ": "ا",
    "آ": "ا",
    "ة": "ه",
}


FA_AR_NUMS_TO_EN = str.maketrans(
    "۰۱۲۳۴۵۶۷۸۹٠١٢٣٤٥٦٧٨٩",
    "01234567890123456789"
)

def slugify_fa(text: str) -> str:
   
    """
        Normalize Persian text and generate SEO-friendly slug.

        - Converts Arabic characters to Persian
        - Normalizes numbers
        - Handles ZWNJ

     """
   
    if not text:
        return ""

    text = str(text)

    for ar, fa in AR_TO_FA_CHARS.items():
        text = text.replace(ar, fa)

    text = text.translate(FA_AR_NUMS_TO_EN)
    text = text.replace("\u200c", " ")      # ZWNJ
    text = re.sub(r"\s+", " ", text).strip()
    slug = django_slugify(text, allow_unicode=True)
    slug = re.sub(r"-{2,}", "-", slug).strip("-")

    return slug
