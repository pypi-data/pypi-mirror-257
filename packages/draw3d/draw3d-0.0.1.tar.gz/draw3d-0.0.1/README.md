### draw3d工具包

#### 本项目旨在使用不同的Python绘图后端绘制三维规则图形

#### 1. 安装

```shell
pip install draw3d
```



#### 2. 使用示例

##### 2.1 Matplotlib后端

```python
import matplotlib.pyplot as plt

axGlob = plt.axes(projection='3d')
MatplotPainter.drawCube(axGlob, 0, 0, 0, 0.5, 0.5, 0.5)	# 绘制cube
MatplotPainter.drawCylinder(axGlob, 0.5, 0, 0, 1, 0.5, 0.5, alpha=0.8, main_axis='x')	# 绘制圆柱体

MatplotPainter.setAxisLimits(axGlob, 2, 2, 2)	# 设置各坐标轴范围
MatplotPainter.setInitView(axGlob, 50, 50)	# 设置初始视角
plt.show()	# 显示图形
```

<img src="https://cdn.thirdbody.cn/1.png" style="zoom:67%;" />