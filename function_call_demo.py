import akshare as ak
from transformers import AutoTokenizer, AutoModel


# 空气质量排行榜查询
def air_quality_rank(date):
    data = ak.air_quality_rank(date=date)
    return data


# 函数映射字典
FUNCTION_MAP = {
    "air_quality_rank": air_quality_rank
}


def get_tools():
    tools = [
        {
            "name": "air_quality_rank",
            "description": "根据指定年份查询城市的空气质量排名数据",
            "parameters": {
                "type": "object",
                "properties": {
                    "date": {
                        "type": "string",
                        "description": "日期，格式为YYYY"
                    },
                },
                "required": ["date"]
            }
        },
    ]
    return tools


def model_chat(query):
    global model, tokenizer
    system_prompt = "你是一个人工智能助手，你需要根据用户提供的工具，回复用户的需求，工具如下："
    system_info = {
        "role": "system",
        "content": system_prompt,
        "tools": get_tools()
    }

    res, his = model.chat(tokenizer, query, history=[system_info])

    if isinstance(res, dict):
        func = res.get("name")
        params = res.get("parameters")

        # 验证函数名和参数
        if func in FUNCTION_MAP and "date" in params:
            func = FUNCTION_MAP[func]
            data = func(**params)

    return data


if __name__ == "__main__":
    model_path = "D:\\models\\chatglm3-6b"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda().eval()
    ans = model_chat("查询2024年的空气质量排名")
    print(ans)
