#!/bin/sh

# 清理旧的构建文件
rm -rf build dist rustsrc/target

# 重新构建
# python setup.py bdist_wheel
python setup.py bdist_wheel sdist

# 检查构建结果
ls -la dist/

# pip uninstall symbolic -y

# # 安装新的 wheel 包
# pip install dist/symbolic-*.whl


# echo "测试导入:"
# python -c "import symbolic; print('Version:', symbolic.__version__ if hasattr(symbolic, '__version__') else 'Not found')"

# echo "测试基本功能:"
# python -c "import symbolic; print('Import successful!'); print('Available modules:', dir(symbolic))"

# echo "测试 demangle 功能:"
# python -c "from symbolic import demangle; result = demangle('_ZN4base8internal12CheckedCastINS_6subtle11PrecheckedEdEEEPNS0_13CheckedNumericEdE'); print('Demangle result:', result)"

# echo "测试 arch_is_known 功能:"
# python -c "from symbolic import arch_is_known; print('x86_64 known:', arch_is_known('x86_64'))"

