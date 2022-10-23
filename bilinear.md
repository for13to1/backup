[Bilinear interpolation](https://en.wikipedia.org/wiki/Bilinear_interpolation)

# 一维线性插值

1. 考虑一元函数 $y=f(x) = kx+b$，对应二维平面上的一条直线（这也是为啥叫**线性**插值的原因）
2. 曲线上有 2 个点 A 和 B，点 A 的坐标为 $(x_1, y_1)$，点 B 的坐标为 $(x_2, y_2)$，满足 $x_1\lt x_2$
3. 已知点 A 和 B 之间的点 C 的横坐标为 $x$，求其纵坐标 $y$

在二维平面直角坐标系中，根据相似三角形关系，易得：
$$\frac{y-y_1}{x-x_1}=\frac{y_2-y_1}{x_2-x_1}$$

由上式可推导：
$$\begin{aligned} y &= \frac{y_2-y_1}{x_2-x_1} (x-x_1) + y_1 \\ &= \frac{x_2-x}{x_2-x_1}y_1 + \frac{x-x_1}{x_2-x_1}y_2 \end{aligned}$$

分析上式：
- $x_2-x_1$ 为固定值
- $x\in[x_1,x_2]$，点 C 越靠近点 B（即 $x_2-x$ 越小），最终 $y_1$ 在最终得到的 $y$ 值中占的比例越小；反之亦然

# 二维线性插值

推广到二元函数 $z=f(x,y)=mx+ny+b$，对应三维空间的一个平面
![Bilinear interpolation.png](https://upload.wikimedia.org/wikipedia/commons/e/e7/Bilinear_interpolation.png)

已知 4 个点的坐标 $Q_{11}=(x_1,y_1)$、$Q_{21}=(x_2,y_1)$、$Q_{12}=(x_1,y_2)$、$Q_{22}=(x_2,y_2)$ 和对应函数值，求 4 点之间点 $P$ 的像素值 $f(P)=f(x,y)$

沿 x 轴方向，易得：
$$f(x,y_1)=\frac{x_2-x}{x_2-x_1}f(x_1,y_1)+\frac{x-x_1}{x_2-x_1}f(x_2,y_1)$$
$$f(x,y_2)=\frac{x_2-x}{x_2-x_1}f(x_1,y_2)+\frac{x-x_1}{x_2-x_1}f(x_2,y_2)$$

沿 y 轴方向，易得：
$$f(x,y) = \frac{y_2-y}{y_2-y_1}f(x,y_1)+\frac{y-y_1}{y_2-y_1}f(x,y_2)$$

展开可得：

$$\begin{aligned} f(x,y)
&= \frac{1}{(x_2-x_1)(y_2-y_1)} [
f(Q_{11})(x_2-x)(y_2-y) +
f(Q_{21})(x-x_1)(y_2-y) +
f(Q_{12})(x_2-x)(y-y_1) +
f(Q_{22})(x-x_1)(y-y_1)] \\
&= \frac{1}{(x_2-x_1)(y_2-y_1)}
\begin{bmatrix} x_2-x, x-x_1 \end{bmatrix} 
\begin{bmatrix} f(Q_{11}), f(Q_{12}) \\ f(Q_{21}), f(Q_{22}) \end{bmatrix} 
\begin{bmatrix} y_2-y\\ y-y_1 \end{bmatrix}
\end{aligned}$$

因为在数字图像中 $x_2-x_1=1, y_2-y_1=1$，所以：
$$f(x,y) = f(Q_{11})(x_2-x)(y_2-y) +
f(Q_{21})(x-x_1)(y_2-y) +
f(Q_{12})(x_2-x)(y-y_1) +
f(Q_{22})(x-x_1)(y-y_1)$$

设：
$$\begin{aligned}
w_{11} &= (x_2-x)(y_2-y) \\
w_{21} &= (x-x_1)(y_2-y) \\
w_{12} &= (x_2-x)(y-y_1) \\
w_{22} &= (x-x_1)(y-y_1)
\end{aligned}$$

则：
$$f(x,y) = w_{11}f(Q_{11}) + w_{21}f(Q_{21}) + w_{12}f(Q_{12}) + w_{22}f(Q_{22})$$

水平缩放比率为 $\text{ratio}_h=\frac{W_{dst}}{W_{src}}$
垂直缩放比率为 $\text{ratio}_v=\frac{H_{dst}}{H_{src}}$

如何根据原图计算目标图的像素点分别对应原图的坐标

$(x_{src},y_{src})$ 为输入图像中的坐标， $(x_{dst},y_{dst})$ 为输出图像中的坐标
$(W_{src},H_{src})$ 为输入图像的宽高， $(W_{dst},H_{dst})$ 为输出图像的宽高

其中的对应关系为：
$$x_{src}=\frac{W_{src}}{W_{dst}}x_{dst}$$
$$y_{src}=\frac{H_{src}}{H_{dst}}y_{dst}$$

**几何中心对齐**后的对应关系为：
$$x_{src}=\frac{W_{src}}{W_{dst}}(x_{dst}+0.5)-0.5$$
$$y_{src}=\frac{H_{src}}{H_{dst}}(y_{dst}+0.5)-0.5$$
