from PIL import Image, ImageDraw
import numpy as np

# 创建画布
def create_canvas(width=400, height=400):
    return Image.new("RGB", (width, height), "white")

# 模拟毛笔笔画
def draw_stroke(draw, points, thickness=10):
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        # 添加随机偏移，模拟毛笔抖动
        x1 += np.random.uniform(-2, 2)
        y1 += np.random.uniform(-2, 2)
        x2 += np.random.uniform(-2, 2)
        y2 += np.random.uniform(-2, 2)
        draw.line([(x1, y1), (x2, y2)], fill="black", width=thickness)

# 定义“永”字的笔画（简化为关键点坐标）
def get_yong_strokes():
    strokes = [
        # 点
        [(200, 50), (200, 70)],
        # 横
        [(180, 100), (220, 100)],
        # 竖
        [(200, 100), (200, 200)],
        # 撇
        [(200, 150), (170, 200)],
        # 捺
        [(200, 150), (230, 200)],
        # 横折
        [(180, 250), (200, 250), (200, 300)],
        # 竖钩
        [(200, 300), (200, 350), (190, 340)]
    ]
    return strokes

# 主函数
def generate_calligraphy():
    # 初始化画布和绘图对象
    canvas = create_canvas()
    draw = ImageDraw.Draw(canvas)
    
    # 获取笔画并绘制
    strokes = get_yong_strokes()
    for stroke in strokes:
        thickness = np.random.randint(5, 15)  # 随机笔画粗细
        draw_stroke(draw, stroke, thickness)
    
    # 保存结果
    canvas.save("yong_calligraphy.png")
    print("书法字形已生成并保存为 'yong_calligraphy.png'")

if __name__ == "__main__":
    generate_calligraphy()