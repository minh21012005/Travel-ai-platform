from google import genai
from google.genai import types

from app.core.config import Settings
from app.infrastructure.llm.models import LLMRequest, LLMResponse

from .base import LLMClient


class GeminiClient(LLMClient):
    def __init__(self, settings: Settings):
        # Khởi tạo client đồng bộ
        self.client = genai.Client(api_key=settings.google_api_key)

    async def generate(
        self,
        request: LLMRequest,
    ) -> LLMResponse:

        # Lưu ý: generate_content ở đây là hàm đồng bộ (blocking).
        # Nếu muốn dùng async chuẩn, bạn nên cân nhắc đổi sang client async.
        response = self.client.models.generate_content(
            model="gemini-2.5-flash",
            contents=request.user_prompt,
            config=types.GenerateContentConfig(
                system_instruction=request.system_prompt,
            ),
        )

        return LLMResponse(
            text=response.text or "",
        )
