import asyncio
import json
import os
import httpx
from contextlib import AsyncExitStack
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from openai import OpenAI
from utils import settings, base_prompt
from openai.types.chat import ChatCompletionMessageParam

DEEPSEEK_API_KEY = settings.DEEPSEEK_KEY

# Конфигурация серверов
SERVERS_CONF = {
    "heroui": ["-y", "@heroui/react-mcp@latest"],
    "shadcn": ["-y", "shadcn@latest", "mcp"]
}

unsafe_client = httpx.Client(verify=False)
client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url="https://api.deepseek.com", http_client=unsafe_client)

class MultiMCPAgent:
    def __init__(self, sessions: dict[str, ClientSession]):
        self.sessions = sessions
        self.tool_mapping = {} 
        self.history: list[ChatCompletionMessageParam] = [
            {"role": "system", "content": (
                "Ты — ведущий UI-инженер. Твоя задача: писать .tsx код.\n"
                "ПРАВИЛА:\n"
                "1. Сначала ОБЯЗАТЕЛЬНО вызови list_components для ВСЕХ доступных серверов (heroui и shadcn).\n"
                "2. Если нужного компонента (например, Table) нет в heroui, ищи его в shadcn.\n"
                "3. ЕСЛИ КОМПОНЕНТА(ИЛИ ПОХОЖЕГО) НЕТ НИ В ОДНОМ MCP СЕРВЕРЕ, ЗАПРЕЩЕНО ЕГО ВЫДУМЫВАТЬ ИЛИ ПИСАТЬ СВОЙ. "
                "В этом случае используй базовые HTML теги (div, span) с Tailwind или упрости UI.\n"
                "4. Используй только актуальный синтаксис из get_component_info.\n"
                "5. Код должен быть в блоке ```tsx.\n"
                "6. Проверь что код не содержит стандартных html тегов(кроме div), если они есть в heroui или shadcn. ЗАПРЕЩЕНО УКАЗЫВАТЬ АБСОЛЮТНЫЕ ЗНАЧЕНИЯ ШИРИНЫ И ВЫСОТЫ width и height в стилях\n"
            )}
        ]

    async def get_combined_tools(self):
        combined_tools = []
        for server_name, session in self.sessions.items():
            response = await session.list_tools()
            for t in response.tools:
                unique_name = f"{server_name}__{t.name}"
                self.tool_mapping[unique_name] = {"session": session, "original_name": t.name}
                
                combined_tools.append({
                    "type": "function",
                    "function": {
                        "name": unique_name,
                        "description": f"[{server_name.upper()}] {t.description}",
                        "parameters": t.inputSchema,
                    },
                })
        return combined_tools

    async def run(self, prompt: str):
        self.history.append({"role": "user", "content": prompt})
        tools = await self.get_combined_tools()

        while True:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=self.history,
                tools=tools,
                tool_choice="auto"
            )

            message = response.choices[0].message
            self.history.append(message)

            if message.content:
                print(f"\n[DeepSeek]: {message.content}")

            if not message.tool_calls:
                return message.content

            for tool_call in message.tool_calls:
                t_name = tool_call.function.name
                t_args = json.loads(tool_call.function.arguments)
                
                mapping = self.tool_mapping.get(t_name)
                if not mapping: continue

                print(f"[*] Executing {t_name}...")
                
                result = await mapping["session"].call_tool(mapping["original_name"], arguments=t_args)
                readable_result = "\n".join([str(c.text) if hasattr(c, 'text') else str(c) for c in result.content])
                
                if "list_components" in t_name:
                    print(f"[Data from {t_name}]:\n{readable_result}\n")

                self.history.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": readable_result
                })

async def main():
    async with AsyncExitStack() as stack:
        sessions = {}
        for name, args in SERVERS_CONF.items():
            params = StdioServerParameters(command="npx", args=args, env={**os.environ, "NODE_TLS_REJECT_UNAUTHORIZED": "0"})
            transport = await stack.enter_async_context(stdio_client(params))
            session = await stack.enter_async_context(ClientSession(transport[0], transport[1]))
            await session.initialize()
            sessions[name] = session

        agent = MultiMCPAgent(sessions)
        print("[System] Agent started. Checking for components...")
        await agent.run(base_prompt)


if __name__ == "__main__":
    asyncio.run(main())