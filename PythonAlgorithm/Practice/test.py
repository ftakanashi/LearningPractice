# -*- coding:utf-8 -*-
def findleft(nums,target):
    left,right = 0, len(nums) - 1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    if nums[right] != target:
        leftIdx = -1
    else:
        leftIdx = right

    return leftIdx

def findright(nums,target):
    left,right = 0,len(nums)-1
    while left < right:
        mid = (left + right) // 2
        if nums[mid] > target:
            right = mid - 1
        else:
            left = mid

    if nums[left] != target:
        return -1
    else:
        return left

if __name__ == '__main__':
    print findleft([5,7,7,8,8,10],8)