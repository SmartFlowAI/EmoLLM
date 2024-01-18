#!/bin/bash

# 定义生活领域的列表
areas_of_life=(
    "工作"
    "学业"
    "生活"
    "身体"
    "家人"
    "朋友"
    "社交"
    "恋爱"
    "就业"
    "责任"
    "爱好"
    "环境"
    "隐私"
    "安全"
    "梦想"
    "自由"
)

# 使用for循环遍历数组
for area in "${areas_of_life[@]}"; do
    echo "当前生活领域: $area"
    python qwen_gen_data.py --data $area
done
