import sys
import os
sys.path.append(os.getcwd())
from scene.dataset_readers import readColmapSceneInfo

DATA_PATH = "/home/crgj/wdd/data/new/flame_steak/"

def test_time_normalization():
    print(f" Loading dataset from {DATA_PATH}...")
    
    if not os.path.exists(DATA_PATH):
        print(f" Path {DATA_PATH} not found.")
        return

    
    # WDD: 2024-05-21 [修复测试脚本] 补充缺失的参数以匹配新的函数签名
    # 调用改造后的加载器，提供默认值
    # depths="" 表示不加载深度图
    # train_test_exp=False 表示不启用训练/测试分离的特殊曝光处理
    scene_info = readColmapSceneInfo(path=DATA_PATH, images="images", depths="", eval=False, train_test_exp=False)
    cameras = scene_info.train_cameras + scene_info.test_cameras
    
    # 验证时间属性
    times = [cam.time for cam in cameras]
    sorted_times = sorted(list(set(times))) # 去重后排序

    # WDD: 2024-05-22 [修改测试脚本] 增加视角和帧数的中文说明
    print(f"\n[测试结果]")
    print(f"  -> 总共加载的视角（相机）数量: {len(cameras)}")
    print(f"  -> 识别出的总帧数: {len(sorted_times)}")
    
    # WDD: 2024-05-22 补充显示每个子目录下的摄像机数量
    # WDD: 2024-05-22 [修复逻辑错误] 使用总视角数除以总帧数来计算每帧的相机数
    if sorted_times: # 确保帧数不为零，避免除零错误
        num_cameras_per_frame = len(cameras) // len(sorted_times)
        print(f"  -> 每个子目录（帧）下的摄像机数量: {num_cameras_per_frame}  (总视角数 / 总帧数)")

    min_t, max_t = (min(times), max(times)) if times else (0, 0)
    print(f"\n[INFO] 时间戳范围: [{min_t:.4f}, {max_t:.4f}]")
    print(f"[INFO] 前5个唯一时间戳: {sorted_times[:5]}")
    
    if min_t < 0.0 or max_t > 1.0:
        print("[FAIL] Time is not normalized between 0 and 1.")
    else:
        print("[SUCCESS] 时间戳归一化正确。")
            
    

if __name__ == "__main__":
    test_time_normalization()