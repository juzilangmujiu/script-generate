#streamlit run main.py
import streamlit as st
from backend import generate_script

#标题
st.title("🎞视频脚本生成器")

#侧边栏
with st.sidebar:
    #用户文本输入
    openai_api_key=st.text_input("请输入OpenAI API密钥：",type="password")
    #页面文字，这里是链接，注意链接写法。[文字](链接)
    st.markdown("[获取OpenAI API密钥](https://platform.openai.com/account/api-keys)")
    model_name = st.text_input("请输入您要用的模型名称（默认为gpt-5.2）：")
    # if model_name is not None:
    #     model_name=model_name
    # else:
    #     model_name="gpt-5.2"
    #与上面代码意思一样，只不过这边还考虑到model_name为空字符串、0、False、空列表的情况
    model_name = model_name if model_name else "gpt-5.2"




subject=st.text_input("🎥请输入视频的主题")
#输入数字
video_length=st.number_input("⏰请输入视频的大致时常（单位：分钟）",min_value=0.1,step=0.1)
#数字拖动框
creativity=st.slider("✨请输入视频脚本的创造力（数字越大创造力越大）",min_value=0.0,max_value=1.5,
                     value=1.0,step=0.1)
#按钮，返回布尔值：点了就是1，不点就是0
submit=st.button("生成脚本")

#发送前的校验
if submit and not openai_api_key:
    st.info("请输入您的OpenAI API密钥") #提示信息
    st.stop() #执行到这里之后就不往下执行
if submit and not subject:
    st.info("请输入视频的主题")
    st.stop()
if submit and not video_length>=0.1:
    st.info("视频时常要大于0.1分钟")
    st.stop()
if submit:    #排除上述情况后，只要用户点击提交，就能直接执行了
    #代码等待时间太长了，弄一个加载提示
    with (st.spinner("AI正在思考中，请稍等...")): # type: ignore
        title_response,script_response,search_result=generate_script(subject,video_length,creativity,openai_api_key,model_name)
    st.success("视频脚本已经生成！🎉🎉🎉")
    st.subheader("🔥标题：")  #副标题
    st.write(title_response)
    st.subheader("📝视频脚本：")  # 副标题
    st.write(script_response)
    #折叠展开组件
    with st.expander("👀维基百科搜索结果："):
        st.info(search_result)
