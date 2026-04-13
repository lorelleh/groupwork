import os
import subprocess
import sys
import torch

# --- 1. 自动检测 PyTorch 的 ABI 版本 (这是破局关键) ---
torch_abi = 1 if torch._C._GLIBCXX_USE_CXX11_ABI else 0
print(f"📊 检测到 PyTorch 使用的 ABI 版本为: {torch_abi}")

# --- 2. 配置路径 ---
BASE_DIR = "/root/autodl-tmp/opensplat"
BUILD_DIR = os.path.join(BASE_DIR, "build")
TORCH_CMAKE = torch.utils.cmake_prefix_path

def run_cmd(cmd, cwd=None):
    print(f"🚀 执行: {cmd}")
    res = subprocess.run(cmd, shell=True, cwd=cwd)
    if res.returncode != 0:
        print(f"❌ 失败，退出码: {res.returncode}")
        sys.exit(1)

def main():
    # A. 清理环境，卸载冲突的 Conda OpenCV
    print("🧹 正在清理环境冲突...")
    subprocess.run("conda remove -y opencv", shell=True) # 踢掉 Conda 的 OpenCV
    subprocess.run("apt-get update && apt-get install -y libopencv-dev", shell=True) # 换成稳健的系统版
    
    if os.path.exists(BUILD_DIR):
        import shutil
        shutil.rmtree(BUILD_DIR)
    os.makedirs(BUILD_DIR)

    # B. 构造 CMake 指令 (强制 ABI 对齐)
    # 我们不再手动注入 -lopencv，让 CMake 自己找系统库
    cmake_cmd = (
        f"cmake .. "
        f"-DCMAKE_CUDA_ARCHITECTURES=90 " # 5090 兼容模式
        f"-DCMAKE_CXX_FLAGS='-D_GLIBCXX_USE_CXX11_ABI={torch_abi}' "
        f"-DCMAKE_PREFIX_PATH='{TORCH_CMAKE}'"
    )

    print("⚙️ 配置 CMake...")
    run_cmd(cmake_cmd, cwd=BUILD_DIR)

    print("🔨 开始最终编译...")
    run_cmd("make -j", cwd=BUILD_DIR)

    print("✅ 恭喜！编译终于通过了！")
    
    # C. 启动训练
    print("🎬 启动 30,000 步高清训练...")
    train_cmd = "./opensplat /root/autodl-tmp/gs_project/opensplat_ready/ -o /root/autodl-tmp/gs_project/output_model/splat.ply -n 30000 -d 2"
    run_cmd(train_cmd, cwd=BUILD_DIR)

if __name__ == "__main__":
    main()