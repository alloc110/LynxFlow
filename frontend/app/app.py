import streamlit as st
from streamlit_agraph import agraph, Node, Edge, Config

st.set_page_config(layout="wide")
st.title("Mô phỏng Data Pipeline (Có điều khiển)")

# 1. Khởi tạo trạng thái Bật/Tắt cho các container trong session_state
# Mặc định tất cả đều đang chạy (True = UP)
if "status" not in st.session_state:
    st.session_state.status = {
        "frontend": True,
        "backend": True,
        "kafka": True,
        "flink": True,
        "db": True
    }

# 2. Bảng điều khiển (Control Panel) với các nút Toggle
st.markdown("### 🎛️ Bảng điều khiển Container")
cols = st.columns(5)

# Cập nhật trạng thái thông qua các nút gạt (Toggle)
st.session_state.status["frontend"] = cols[0].toggle("Frontend UI", value=st.session_state.status["frontend"])
st.session_state.status["backend"] = cols[1].toggle("Backend API", value=st.session_state.status["backend"])
st.session_state.status["kafka"] = cols[2].toggle("Kafka Broker", value=st.session_state.status["kafka"])
st.session_state.status["flink"] = cols[3].toggle("Flink Job", value=st.session_state.status["flink"])
st.session_state.status["db"] = cols[4].toggle("PostgreSQL", value=st.session_state.status["db"])

st.divider()

# 3. Hàm hỗ trợ vẽ Node tùy theo trạng thái
def create_node(node_id, label, default_border):
    is_up = st.session_state.status[node_id]
    return Node(
        id=node_id,
        label=f"{label}\n{'🟢 UP' if is_up else '🔴 DOWN'}",
        shape="box",
        # Đổi màu thành xám/đỏ nếu bị tắt
        color={
            "background": "#1e1e2e" if is_up else "#181825", 
            "border": default_border if is_up else "#f38ba8" # Đỏ khi Down
        },
        font={"color": "#cdd6f4" if is_up else "#585b70", "size": 16}
    )

nodes = [
    create_node("frontend", "Frontend UI", "#89b4fa"),
    create_node("backend", "Backend API", "#a6e3a1"),
    create_node("kafka", "Apache Kafka", "#f9e2af"),
    create_node("flink", "Apache Flink", "#fab387"),
    create_node("db", "PostgreSQL", "#cba6f7")
]

# 4. Hàm hỗ trợ vẽ Luồng (Edge)
# Luồng chỉ "chạy" khi CẢ HAI container ở 2 đầu đều đang UP
def create_edge(source, target, label):
    source_up = st.session_state.status[source]
    target_up = st.session_state.status[target]
    both_up = source_up and target_up
    
    return Edge(
        source=source, 
        target=target, 
        label=label,
        # animated=True tạo cảm giác luồng dữ liệu đang chạy qua
        animated=both_up, 
        color="#89b4fa" if both_up else "#45475a", # Màu sáng khi chạy, xám khi dừng
        width=3 if both_up else 1
    )

edges = [
    create_edge("frontend", "backend", "REST API"),
    create_edge("backend", "kafka", "Produce"),
    create_edge("kafka", "flink", "Consume Stream"),
    create_edge("db", "kafka", "CDC (Debezium)")
]

# 5. Cấu hình tắt vật lý (Để các khối đứng yên khi kéo 1 khối)
config = Config(
    width="100%", 
    height=500,
    directed=True,
    # QUAN TRỌNG: Tắt physics để các node không bị lực hút/đẩy như lò xo
    physics=False,
    hierarchical=False,
    nodeHighlightBehavior=True
)

# Render biểu đồ
agraph(nodes=nodes, edges=edges, config=config)