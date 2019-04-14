class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        arr=[]
        brr=[]
        if len(nums)==0:
            return arr 
        
        for k in range(len(nums)):
            target=nums[k]
            for i in range(len(nums)):
                for j in range(i+1, len(nums)):
                    if (j==k) or (i==k):
                        continue
                        
                    if (nums[i]+nums[j] == -target):
                            arr.append([nums[i], nums[j], nums[k]])
        
        for a in range(len(arr)):
            arr[a].sort()
        arr.sort()
        
        for a in range(len(arr)):
            if arr[a] not in brr:
                brr.append(arr[a])
            else:
                continue 
                
                        
        return brr
