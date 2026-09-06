"""供 Text2SQL 编排器使用的 DashScope 客户端。"""

import re
from typing import Any

from dashscope import MultiModalConversation
from dotenv import load_dotenv


load_dotenv()

from config import LLM_CONFIG


class LLMClient:
    """使用 DashScope 根据系统消息和用户 Prompt 生成 SQL。"""

    def __init__(self) -> None:
        self.api_key = LLM_CONFIG["api_key"]
        self.model = LLM_CONFIG["model"]
        self.temperature = LLM_CONFIG["temperature"]
        self.max_tokens = LLM_CONFIG["max_tokens"]

        if not self.api_key:
            raise RuntimeError("未配置 DASHSCOPE_API_KEY")

    def generate_sql(self, system_msg: str, prompt: str) -> str:
        """调用 DashScope，并将响应转换为纯 SQL 字符串。"""
        response = MultiModalConversation.call(
            api_key=self.api_key,
            model=self.model,
            messages=[
                {"role": "system", "content": [{"text": system_msg}]},
                {"role": "user", "content": [{"text": prompt}]},
            ],
            temperature=self.temperature,
            max_tokens=self.max_tokens,
            enable_thinking=False,
        )

        if response.status_code != 200:
            raise RuntimeError(
                "DashScope 请求失败（DashScope request failed）："
                f"错误码={getattr(response, 'code', '')}，"
                f"错误信息={getattr(response, 'message', '')}，"
                f"请求 ID={getattr(response, 'request_id', '')}"
            )

        content = response.output.choices[0].message.content
        return self._strip_sql_fence(self._content_to_text(content))

    @staticmethod
    def _content_to_text(content: Any) -> str:
        if isinstance(content, str):
            return content.strip()

        if isinstance(content, list):
            return "".join(
                part.get("text", "") for part in content if isinstance(part, dict)
            ).strip()

        raise RuntimeError("DashScope 响应中未包含文本内容")

    @staticmethod
    def _strip_sql_fence(text: str) -> str:
        return re.sub(
            r"^```(?:sql)?\s*|\s*```$",
            "",
            text.strip(),
            flags=re.IGNORECASE,
        ).strip()
