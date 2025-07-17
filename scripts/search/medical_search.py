import os
import requests
import json

class MedicalSearch:
    """
    用于调用您的医疗检索 API 的封装类。
    """
    def __init__(self, api_key):
        """
        初始化 MedicalSearch 类。

        Args:
            api_key (str): 您的医疗检索 API 的授权 token。
        """
        self.api_key = api_key
        # self.base_url = "https://cloud.infini-ai.com/AIStudio/inference/api/if-dbjcvomldl2t6avm/process-batch-query/"
        self.base_url = "http://if-dbjcvomldl2t6avm-service:8888/process-batch-query/"
        self.headers = {
            # "Authorization": f"Bearer {self.api_key}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def search(self, query, topk=10):
        """
        执行医疗检索。

        Args:
            query (str): 要检索的查询内容。
            topk (int): 需要返回的文本块数量。

        Returns:
            list: 包含检索结果的列表，每个结果是一个字典。
        """
        payload = {
            "question": [query],
            "topk": topk
        }

        try:
            response = requests.post(self.base_url, headers=self.headers, data=json.dumps(payload))
            response.raise_for_status()  # 如果请求失败 (状态码非 2xx)，则抛出异常
            results = response.json()
            results = results['results'][0]['retrieved_documents'][0]['docs']
            snippets = results.split('(Title:')[1:]
            snippets = [{"snippet": '(Title: '+item.strip()} for item in snippets]

            # 在这里，我们假设 API 返回的格式是一个包含文本块列表的 JSON。
            # 您可能需要根据实际返回的格式调整以下的数据处理部分。
            # 我们将每个文本块构造成一个包含 'snippet' 键的字典，以兼容 WebThinker 的数据格式。
            return snippets

        except requests.exceptions.RequestException as e:
            print(f"调用医疗检索 API 时发生错误: {e}")
            return []

if __name__ == '__main__':
    # 从环境变量中获取 API Key，请确保在运行前已设置该环境变量
    api_key = os.environ.get("MEDICAL_API_KEY")
    if not api_key:
        raise ValueError("请设置环境变量 'MEDICAL_API_KEY' 为您的 API token")

    medical_search_engine = MedicalSearch(api_key=api_key)
    search_query = "treatment for headache"
    search_results = medical_search_engine.search(search_query, topk=5)

    print(f"查询 '{search_query}' 的医疗检索结果:")
    for i, result in enumerate(search_results, 1):
        print(f"{i}. {result.get('snippet')}")