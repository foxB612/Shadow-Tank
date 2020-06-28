# Shadow-Tank
A simple python tool to make shadow tank images. Currently only support B&W image.

一款基于Python的制作幻影坦克图的简易工具。目前只支持输出黑白图像。

##### What is Shadow Tank? 什么是幻影坦克？

A Shadow Tank image is an image file with a smartly arranged alpha channel, so that it shows different pictures with different backgrounds. Normally a shadow tank image contains two pictures corresponding to black (or dark grey) background and white (or light grey) background.
一种 ~~开车专用图~~ 神奇的图片，在不同的背景下会显示出不同的图片。由于百度贴吧和QQ等平台的图片查看机制是预览时白底、点开黑底，完美地为幻影坦克提供了工作环境，因此这类图片一度流传甚广。

##### Working Principle 工作机制

The key of a Shadow Tank image is its alpha channel. It enables a pixel to show different colour with different background. According to alpha compositing, a pixel with $RGB(r_1, g_1, b_1)$ and alpha $\alpha$ as foreground and a pixel with solid $RGB(r_0, g_0, b_0)$ as background will result in $RGB(r_2, g_2, b_2)$, where

$$
\begin{cases}
r_2 = r_1 \alpha + r_0 (1 - \alpha)\\
g_2 = g_1 \alpha + g_0 (1 - \alpha)\\
b_2 = b_1 \alpha + b_0 (1 - \alpha)
\end{cases}
$$

Therefore, for the same pixel $RGBA(r_1, g_1, b_1, \alpha)$, different background $RGB(r_0, g_0, b_0)$ will give different result $RGB(r_2, g_2, b_2)$.

##### How to generate a Shadow Tank 如何制作幻影坦克图

Knowing the working principle, all we need to do is reverse-engineering. What we want is such a pixel $RGBA(r, g, b, \alpha)$ that displays $RGB(r_1, g_1, b_1)$ with white background $RGB(255, 255, 255)$ and $RGB(r_2, g_2, b_2)$ with black background $RGB(0,0,0)$. So we can get the following equations:
$$
\begin{cases}
r_1 = r \alpha + 255 \cdot (1 - \alpha)\\
g_1 = g \alpha + 255 \cdot (1 - \alpha)\\
b_1 = b \alpha + 255 \cdot (1 - \alpha)
\end{cases}
\begin{cases}
r_2 = r \alpha + 0 \cdot (1 - \alpha)\\
g_2 = g \alpha + 0 \cdot (1 - \alpha)\\
b_2 = b \alpha + 0 \cdot (1 - \alpha)
\end{cases}
$$

It's clear that we can't always get a solution from the above equations. But with a compromisation, things get easier: let's convert the two pictures into grey-scale ones, i.e. $\begin{cases} r_1 = g_1 = b_1\\ r_2 = g_2 = b_2 \end{cases}$. Then the equations become
$$
\begin{cases}
c_1 = c \alpha + 255 \cdot (1 - \alpha)\\
c_2 = c \alpha + 0 \cdot (1 - \alpha)
\end{cases}
$$

Then we can always get a solution
$$
\begin{cases}
\alpha = 1 -{{c_1 - c_2} \over 255}\\
 c = {c_2 \over \alpha}
\end{cases}
$$
But we need to note that there is a limitation: $c_1>c_2$ must holds, otherwise we will get an $\alpha$ out of $[0, 1]$. It's easy to understand, since a pixel always looks brighter with a white background than with a black background. So we need to brighten the white-based image and darken the black-based image in advance.

To conclude, the process of merging two images into a Shadow Tank image is the following:

1. Convert the two images to grey-scale ones and scale them to be of the same size.
2. Check if the value of pixels in white-based image are all bigger than those in the same positions in the black-based image. If not, brighten the white-based image and darken the black-based image and check again.
3. For every pixel, calculate the new alpha $\alpha$ and color $c$ with the equation $\begin{cases} \alpha = 1 - { {c_1 - c_2} \over 255}\\ c = {c_2 \over \alpha} \end{cases}$.
4. Export the generated image.

##### Usage 使用方法

`python ShadowTank.py <inputfile1> <inputfile2> <outputfile>`

##### Dependencies 依赖项

numpy (for easy operation of array)