# Star-Chart/星图

灵感来源：[战鹰看水友顶级P图以为是自己 结果放大全是俞俐均！](https://www.bilibili.com/video/BV1v14y1F7p1/?spm_id_from=333.337.search-card.all.click&vd_source=4b31b9003403d923eaff40ee4c18507f)

这个仓库包含一个小脚本，输入一个目的图像，输入一组被拼图像，就可以得到如上面视频所示的效果

> 为什么要叫星图呢，因为最终得到的效果就是无数张小图像拼接成了一张大图，就像星星组成了银河一样。

# 用法
将目的图像放入`./pic`中，将被拼图像放入`./inner_pic`中，适当修改`'./config/config.py`的参数，运行命令

```
python utils.py
```

即可得到结果

# 效果展示(迪丽热巴)
![](./res.jpg)