#!/bin/bash

# 构建包
echo "Building package..."
python setup.py bdist_wheel sdist

# 检查包
echo "Checking package..."
twine check dist/*

# 询问是否发布到 TestPyPI
read -p "Publish to TestPyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Publishing to TestPyPI..."
    twine upload --repository testpypi dist/*
fi

# 询问是否发布到正式 PyPI
read -p "Publish to PyPI? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Publishing to PyPI..."
    twine upload dist/*
fi

echo "Done!"
