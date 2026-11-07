
import tiktoken

encoding = tiktoken.get_encoding("cl100k_base")

job_description = """
En az 4 yıl Python tecrübesi,
Django, FastAPI ve PostgreSQL bilgisi
olan backend developer aranıyor.
"""


def build_prompt(job: str) -> str:
    return f"""
Sen bir teknik işe alım asistanısın.

Aşağıdaki iş ilanını analiz et.

Yalnızca JSON formatında cevap ver.

Alanlar:
- technologies: list[str] veya null
- min_experience_years: int veya null

İş ilanı:
{job}
"""


def count_tokens(text: str) -> int:
    return len(encoding.encode(text))


def check_context(text: str, limit: int = 500) -> bool:
    return count_tokens(text) <= limit


prompt = build_prompt(job_description)

print("Prompt:", prompt)
print("Token sayısı:", count_tokens(prompt))
print("Sınıra uygun:", check_context(prompt))
