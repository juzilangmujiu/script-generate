from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI
from langchain_community.utilities import WikipediaAPIWrapper
import os

#①生成视频标题 ②按照标题进行维基百科搜索 ③生成视频脚本
#提示词模板（实例）——模型实例——链——拼接、申请
def generate_script(subject,video_length,creativity,api_key,model_name="gpt-5.2"):

    title_template = ChatPromptTemplate.from_messages(
        [("human","请为这个以‘{Sub}’为主题的视频想一个爆款标题。")]
    )
    script_template = ChatPromptTemplate.from_messages(
        [("human","""你是一位短视频频道的博主。根据以下标题和相关信息，为短视频频道写一个视频脚本。
        视频标题：{title}，视频时长：{duration}分钟，生成的脚本的长度尽量遵循视频时长的要求。
        要求开头抓住眼球，中间提供干货内容, 结尾有惊喜,脚本格式也请按照【开头、中间,结尾】分隔。
        整体内容的表达方式要尽量轻松有趣，吸引年轻人。脚本内容可以结合以下维基百科搜索出的信息，
        但仅作为参考，只结合相关的即可, 对不相关的进行忽略：'{wiki_search}' """)]
    )

    model_case = ChatOpenAI(model=model_name ,openai_api_key=api_key ,
                            openai_api_base="https://api.aigc369.com/v1",
                            temperature=creativity)

    title_chain = title_template | model_case
    title_response = title_chain.invoke({"Sub":subject}).content

    def search_wikipedia(subject):
        try:
            # 尝试执行维基百科搜索
            search_result = WikipediaAPIWrapper(lang="zh").run(subject)
            # 如果搜索结果为空，也视为失败
            if not search_result.strip():
                return "没能找到结果，请自行回答"
            return search_result
        except Exception as e:
            # 捕获所有可能的异常
            return "没能找到结果，请自行回答"
    search_result = search_wikipedia(subject)
    script_chain = script_template | model_case
    script_response = script_chain.invoke({"title":title_response,
                                         "duration":video_length,
                                         "wiki_search":search_result}).content


    return title_response,script_response,search_result



#print(generate_script("数据分析",1,1.2,os.getenv("OPENAI_API_KEY")))