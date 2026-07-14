"""
题目：
给定一个整数列表 nums 和目标值 target，找出列表中两个数，
使它们之和等于 target，返回这两个数的下标。

示例：
nums = [2, 7, 11, 15]
target = 9

预期结果：
[0, 1]
"""


def two_sum(nums, target):
    n = len(nums)

    for num1 in range(0, n - 1):
        for num2 in range(num1 + 1, n):
            if nums[num1] + nums[num2] == target:
                return [num1, num2]

    return []


# 时间复杂度：O(n²)
# 空间复杂度：O(1)


"""
哈希表法：

遍历当前数字
→ 计算还缺少的数字 target - 当前数字
→ 检查需要的数字是否已经出现在字典中
→ 存在则返回两个下标
→ 不存在则记录当前数字和下标
"""


def two_sum_hash(nums, target):
    # 字典底层使用哈希表，键查找平均时间复杂度为 O(1)
    seen = {}

    # enumerate() 在遍历列表时，同时获得下标和元素值
    for index, number in enumerate(nums):
        needed = target - number

        if needed in seen:
            return [seen[needed], index]

        # 键保存数字，值保存该数字对应的下标
        seen[number] = index

    # 所有元素检查完仍然没有找到
    return []


# 平均时间复杂度：O(n)
# 空间复杂度：O(n)


if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9

    result_brute_force = two_sum(nums, target)
    result_hash = two_sum_hash(nums, target)

    print("双层循环：", result_brute_force)
    print("哈希表法：", result_hash)