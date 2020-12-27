遗留问题  
1.上传文件到url/dblog  
上传文件时提示：Forbidden (CSRF token missing or incorrect.): 这是由于跨域请求问题，可以通过在up-load组件中的header 中天机csrf属性进行验证  
现在的解决方案是在后台直接取消跨域验证 @csrf_exempt
