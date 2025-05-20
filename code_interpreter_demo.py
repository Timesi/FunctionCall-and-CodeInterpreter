from transformers import AutoTokenizer, AutoModel
import re


def model_chat(query):
    system_prompt = """你是一个智能的编程助手，你需要使用python完成用户的代码需求。"""
    system_info = {
        "role": "system",
        "content": system_prompt
    }

    response, history = model.chat(tokenizer, query, history=[system_info])

    # 生成代码
    try:
        code = re.findall(r'```python\n(.*?)```', response, re.DOTALL)[0]
    except:
        return "生成的回答中不包含Python代码"

    # 编译代码
    try:
        compile(code, "<string>", "exec")
    except:
        return "生成代码有误"

    # 执行代码
    try:
        out_dict = {}
        exec(code, {}, out_dict)
        print("执行成功")

        result = f"排序前：{out_dict.get('arr1', '')}\n排序后：{out_dict.get('arr2', '')}"
        return result
    except:
        return "生成代码执行出错"


if __name__ == "__main__":
    model_path = "D:\\models\\chatglm3-6b"
    tokenizer = AutoTokenizer.from_pretrained(model_path, trust_remote_code=True)
    model = AutoModel.from_pretrained(model_path, trust_remote_code=True).half().cuda().eval()
    ans = model_chat("帮我写一个冒泡排序的代码,排序前的变量为：arr1，排序后的变量为：arr2，不要改变arr1中的值")
    print(ans)