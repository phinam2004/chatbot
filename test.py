from PIL import Image
import streamlit as st
import google.generativeai as genai
import requests

# Configure the API key
genai.configure(api_key="AIzaSyCFraGC90mqhajxQwd1na44f9dPvSoQmFQ")  # Replace with your API key

# Tải ảnh từ file cục bộ
image_path = 'anh.jpg'  # Thay bằng đường dẫn đến ảnh của bạn
image = Image.open(image_path)

# Hiển thị ảnh
st.image(image, use_container_width=True)

# # Đường dẫn đến ảnh nền từ internet
# background_image_url = 'https://img.lovepik.com/photo/50062/4783.jpg_wh860.jpg'  # Sử dụng đường dẫn URL đầy đủ

# Set up the model
generation_config = {
    "temperature": 0.9,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_MEDIUM_AND_ABOVE"},
]

model = genai.GenerativeModel(model_name="gemini-1.5-flash-002",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Initialize chat session
if "chat" not in st.session_state:
    st.session_state.chat = model.start_chat(history=[])

# Function to generate specific responses for PUBG, including images
def respond_to_question(question):
    question_lower = question.lower()  # Normalize the input
    response = ""

    if "cách chơi" in question_lower:
        response = "Cách chơi PUBG rất đơn giản. Bạn bắt đầu bằng việc nhảy dù từ máy bay và hạ cánh xuống mặt đất." \
                   " Tìm kiếm trang bị và vũ khí để sinh tồn. Luôn chú ý đến vòng bo và di chuyển để tránh bị loại."
    
    elif "vũ khí" in question_lower:
        if "groza" in question_lower:
            response = "Groza là khẩu súng rất quen thuộc với mọi người sức mạnh của nó thì không còn gì để bàn cãi nó là thực sự là khẩu súng trường mạnh nhất hiện nay. Tuy nhiên khẩu súng này khá khó kiếm nó chỉ xuất hiện trong hòm tiếp tế và người chơi chỉ sử dụng 4x Scope vì súng không hỗ trợ 8x Scope nhưng nếu bạn đã có nó trong tay thì thật sự bạn đang nắm giữ một vũ khí cực kì lợi hại đó.\n"\
                        "Thông số súng Groza: \n"\
                        "Sát thương cơ bản: 49 \n"\
                        "Tốc độ ra đạn: 715m/s\n"\
                        "Zero Distance: 100-300m\n"\
                        "Băng đạn cơ bản: 30 viên\n"\
                        "Chế độ bắn: Đơn và Tự động"
            display_image("https://cdn.tgdd.vn/2020/09/content/5-800x550.jpg")
        
        elif "M16A4" in question_lower:
            response = "M16A4 đây là khẩu súng phổ biến chỉ xếp sau AKM trong loại súng trường này."\
                       "Thông số súng M16A4:"\
                       "Sát thương cơ bản: 43"\
                       "Tốc độ ra đạn: 900m/s"\
                       "Băng đạn cơ bản: 30 viên"\
                       "Chế độ bắn:  Đơn - Burst"
            display_image("https://cdn.tgdd.vn/2020/09/content/2-800x550.jpg")
        
        elif "akm" in question_lower:
            response = "AKM là một trong những loại súng AR mạnh nhất, với sát thương cao nhưng độ giật lớn."\
                       "Thông số súng AKM:"\
                       "Sát thương cơ bản: 49"\
                       "Tốc độ ra đạn: 715 m/s"\
                       "Băng đạn cơ bản: 30 viên"\
                       "Chế độ bắn: Đơn và Tự động"
            display_image("https://cdn.tgdd.vn/2020/09/content/1-800x550-7.jpg")
        
    elif "chiến thuật" in question_lower:
        response = "Một chiến thuật phổ biến là hãy ẩn nấp trong bụi cây hoặc các công trình. " \
                   "Thời điểm tốt nhất tấn công là khi kẻ thù không để ý đến bạn."
    
    elif "bản đồ" in question_lower:
        response = "Hiện tại có ba bản đồ chính trong PUBG: Erangel, Miramar và Sanhok." \
                   " Mỗi bản đồ đều có đặc điểm riêng mà bạn cần nắm rõ để chiến thắng."

    # Fallback response for unrelated queries
    if not response:
        response = "Tôi chỉ biết về game PUBG chứ không biết về các vấn đề khác ngoài game."

    return response

# Helper function to display an image
def display_image(image_url):
    """Displays an image from a given URL."""
    st.image(image_url, caption="Hình ảnh vũ khí", use_container_width=True)

# Streamlit app
st.title("Gemini Chatbot - PUBG Support")
st.write("Chào mừng bạn đến với chatbot hỗ trợ PUBG! Hãy hỏi tôi về cách chơi, trang bị, chiến thuật, hoặc bản đồ.")


# HTML content example with CSS and background image
html_content = """
<style>
body {
    background-image: url('https://img.lovepik.com/photo/50062/4783.jpg_wh860.jpg'); /* Thay đổi đường dẫn ảnh nền tại đây */
    background-size: cover;
    background-position: center;
    font-family: Arial, sans-serif;
}

.container {
    background-color: rgba(241, 241, 241, 0.8);  /* Sử dụng màu nền với độ trong suốt */
    padding: 20px; 
    border-radius: 10px; 
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); 
    max-width: 600px; 
    margin: auto; 
}

h3 {
    color: #0073e6;
    text-align: center;
}

ul {
    list-style-type: none; 
    padding: 0; 
}

ul li {
    font-size: 18px; 
    margin-bottom: 10px; 
    padding: 8px; 
    background-color: #e0e0e0; 
    border-radius: 5px; 
    transition: background-color 0.3s;
}

ul li:hover {
    background-color: #d0d0d0; /* Hiệu ứng hover */
}

footer {
    text-align: center; 
    margin-top: 20px; 
    color: #555; 
}
</style>

<div class="container">
    <h3>Chuyên mục hỗ trợ PUBG:</h3>
    <ul>
        <li>Cách chơi</li>
        <li>Vũ khí</li>
        <li>Chiến thuật</li>
        <li>Bản đồ</li>
    </ul>
    <footer>
        <p>Hãy hỏi tôi bất cứ điều gì bạn cần biết!</p>
    </footer>
</div>
"""

# Tạo thanh công cụ
with st.sidebar:
    st.title("Công cụ hỗ trợ")
    
    # Tạo các lựa chọn trong thanh công cụ
    selected_option = st.radio(
        "Chọn chức năng:",
        ["Cách chơi", "Vũ khí", "Chiến thuật", "Bản đồ"]
    )

    if selected_option == "Cách chơi":
        st.header("Cách chơi PUBG")
        st.write("Hướng dẫn cơ bản về cách chơi game PUBG.")
    elif selected_option == "Vũ khí":
        st.header("Các loại vũ khí trong PUBG")
        st.write("Thông tin chi tiết về các loại vũ khí trong game PUBG.")
    elif selected_option == "Chiến thuật":
        st.header("Chiến thuật chơi PUBG")
        st.write("Các chiến thuật và mẹo chơi game PUBG.")
    elif selected_option == "Bản đồ":
        st.header("Bản đồ PUBG")
        st.write("Hướng dẫn về các bản đồ chơi trong PUBG.")

# Hiển thị nội dung dựa trên lựa chọn trong thanh công cụ
if selected_option == "Cách chơi":
    st.subheader("Hướng dẫn cơ bản")
    st.write("Trong PUBG, mục tiêu là trở thành người chơi cuối cùng sống sót. Bạn cần tìm vũ khí, trang bị và hạ gục các đối thủ khác.")
    st.write("Để di chuyển, sử dụng các phím mũi tên hoặc WASD. Nhấn phím Ctrl để nằm, phím Shift để chạy và phím Space để nhảy.")
    st.write("Khi gặp đối thủ, hãy ngắm bằng chuột trái và bắn bằng chuột phải.")
elif selected_option == "Vũ khí":
    st.subheader("Các loại vũ khí")
    st.write("PUBG có nhiều loại vũ khí khác nhau, bao gồm súng trường, súng ngắn, súng tiểu liên và súng bắn tỉa.")
    st.write("Mỗi loại vũ khí đều có ưu và nhược điểm riêng. Hãy thử nghiệm các loại vũ khí và tìm ra những gì phù hợp với phong cách chơi của bạn.")
elif selected_option == "Chiến thuật":
    st.subheader("Chiến thuật chơi")
    st.write("Một số mẹo và chiến thuật chơi PUBG bao gồm:")
    st.write("- Di chuyển cẩn thận và tránh những khu vực nguy hiểm")
    st.write("- Tìm vị trí cao để quan sát và bắn trước")
    st.write("- Sử dụng trang bị và cấp độ vũ khí phù hợp")
    st.write("- Phối hợp với đội ngũ để tăng cơ hội chiến thắng")
elif selected_option == "Bản đồ":
    st.subheader("Các bản đồ PUBG")
    st.write("PUBG có nhiều bản đồ khác nhau, mỗi bản đồ đều có địa hình, đặc điểm và thách thức riêng.")
    st.write("Một số bản đồ phổ biến bao gồm Erangel, Miramar, Sanhok và Vikendi.")
    st.write("Hãy khám phá các bản đồ và tìm hiểu cách di chuyển và ẩn náu tốt nhất trên từng bản đồ.")

st.markdown(html_content, unsafe_allow_html=True)

st.markdown(html_content, unsafe_allow_html=True)

# Display chat history
for message in st.session_state.chat.history:
    role = message['role']
    content = message['parts'][0]['text']
    with st.chat_message(role):
        st.markdown(content)

# User input
user_input = st.chat_input("Type your message here...")

if user_input:
    # Add user message to chat
    st.chat_message("user").markdown(user_input)

    # Generate response using the respond_to_question function
    response_text = respond_to_question(user_input)

    # Display assistant response
    with st.chat_message("assistant"):
        st.markdown(response_text)

    # Update chat history (ensure the structure is consistent)
    st.session_state.chat.history.append({
        "role": "assistant",
        "parts": [{"text": response_text}]
    })