
from ollama import chat, ResponseError
from pydantic import BaseModel, ValidationError
from pydantic import BaseModel

MODEL = "qwen3:4b-instruct"


class JobAnalysis(BaseModel):
    required_technologies: list[str]
    preferred_technologies: list[str]
    min_experience_years: int | None


SYSTEM_PROMPT = """
Sen bir teknik iş ilanı analiz asistanısın.

İş ilanındaki teknolojileri iki kategoriye ayır:

required_technologies:
- Zorunlu teknolojiler
- "bilmeli", "şarttır", "gereklidir"

preferred_technologies:
- Tercih edilen teknolojiler
- "tercihen", "avantajdır", "artı puandır"

ÖNEMLİ:
"X bilmek avantajdır" ifadesindeki X teknolojisi
KESİNLİKLE preferred_technologies listesine
eklenmelidir.

ÖRNEK 1:
İlan: Python zorunlu, Redis tercih sebebidir.

Çıktı:
{
  "required_technologies": ["Python"],
  "preferred_technologies": ["Redis"],
  "min_experience_years": null
}

ÖRNEK 2:
İlan: Django bilen geliştirici aranıyor.
React bilmek avantajdır.

Çıktı:
{
  "required_technologies": ["Django"],
  "preferred_technologies": ["React"],
  "min_experience_years": null
}

Kurallar:
- Aynı teknolojiyi iki listeye ekleme.
- Deneyim yılı yoksa null döndür.
- İlanda olmayan teknolojileri ekleme.
- Yalnızca istenen JSON yapısını üret.
"""

def analyze_job(job: str) -> JobAnalysis:
    response = chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": job,
            },
        ],
        format=JobAnalysis.model_json_schema(),
        options={"temperature": 0},
    )

    return JobAnalysis.model_validate_json(
        response.message.content
    )


jobs = [
    "Python ve Django bilen, tercihen Redis tecrübesi olan bir geliştirici arıyoruz. En az 3 yıl backend geliştirme deneyimi gereklidir. React bilmek avantajdır."    
]

for job in jobs:
    try:
        result = analyze_job(job)

        print("İlan:", job)
        print(result.model_dump_json(indent=2))
        print("-" * 40)

    except (ValidationError, ResponseError) as exc:
        print("Hata:", exc)
