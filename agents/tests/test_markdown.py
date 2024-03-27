import asyncio

from metagpt.logs import logger
from metagpt.roles.role import Role, RoleReactMode
from metagpt.schema import Message

from agents.actions.write_markdown import WriteMarkdown


class Test(Role):
    name: str = "Test"
    profile: str = "TestMarkdown"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._init_actions([WriteMarkdown])
        self._set_react_mode(react_mode=RoleReactMode.BY_ORDER.value)
    
    async def _act(self) -> Message:
        logger.info(f"{self._setting}: to do {self.rc.todo}({self.rc.todo.name})")
        todo = self.rc.todo

        msg = self.get_memories(k=1)[0]  # find the most k recent messages
        result = await todo.run(msg.content)

        msg = Message(content=result, role=self.profile, cause_by=type(todo))
        self.rc.memory.add(msg)
        return msg


text: str = """
DS-SLAM

- paper：:book: DS-SLAM: A Semantic Visual SLAM towards Dynamic Environments
- code：:material-github: DS-SLAM

Introduction

使用语义分割网络和光流相结合的方法减少视觉 SLAM 中动态物体造成的影响。

基于ORB-SLAM2提出了动态环境中的完整语义SLAM系统（DS-SLAM），可以减少动态对象对姿态估计的影响。 该系统的有效性在 TUM RGB-D 数据集 上进行评估。 结果表明，DS-SLAM 在动态环境中的准确性和鲁棒性方面明显优于 ORB-SLAM2。 该系统还与机器人操作系统（ROS）集成，并通过在真实环境中对机器人进行 DS-SLAM 测试来验证其性能。
2.将语义分割网络单独的放在一个线程当中，将语义分割和运动一致性检查的方法（光流法（通过计算光流的不一致性来区分静态背景和运动目标））相结合，过滤掉场景中的动态物体。从而提高了定位模块和建图模块在动态场景下的鲁棒性和准确性。

DS-SLAM 创建一个单独的线程来构建一个密集的语义 3D 八叉树图 。密集语义 3D 八叉树图采用 log-odds score（对数优势记分法） 方法过滤掉不稳定的体素并更新这些体素的语义。

RELATED WORK

在以前的工作中，语义图通常由两部分组成：几何部分和语义部分。语义方法预先训练了对象识别子系统，并将语义信息附加到识别的对象模型上。他们的工作仅集中在语义映射和对象识别上，而语义信息在其他部分的信息却没有很好地使用。近期工作利用场景中的几何属性和语义属性共同估计相机的姿势，点和对象，从而显著提高了对象识别的准确性。

在本文中，语义信息不仅用于生成基于八叉树的环境表示，而且还用于在动态环境中跟踪过程中过滤异常值。

SYSTEM INTRUDUCTION

Framework of DS-SLAM

Kinect2捕获的原始RGB图像在跟踪线程和语义分割线程中同时进行处理。跟踪线程首先提取ORB特征点，然后粗略检查特征点的移动一致性并保存潜在的异常值。然后跟踪线程等待具有由语义分割线程预测的像素级语义标签的图像。分割结果到达后，将根据分割结果和之前检测到的潜在异常值，丢弃位于运动物体中的ORB特征点异常值。然后，通过匹配其余的稳定特征点来计算变换矩阵。

Semantic Segmentation

DS-SLAM采用SegNet提供基于caffe的像素级实时语义分割。在PASCAL VOC数据集上训练的SegNet总共可以分割20个类。在实际应用中，人最有可能是动态对象，因此我们假设位于人身上的特征点最有可能是异常值。

Moving Consistency Check

经过语义分割的模块后，可以得到一个分割的Mask的，所以现在的任务就是去确定，某个关键点是否是移动的，如果有一定数量的移动点落在了某一个分割出来的物体轮廓内部，那这个物体就被视为动态，上面所有的特征点都会被剔除。

判断动态点步骤：

计算光流金字塔得到当前帧中已经匹配的特征点
如果匹配点对离图像的边缘太近，或者各自以两个相匹配的点为中心，其 3x3 区域范围内像素值差异太大，这个匹配点就会被丢弃
使用 RANSAC 的方法（使用最多内点）找到基础矩阵 F
使用基础矩阵计算当前帧的极线，已知上一帧中的特征点像素位置为 ，这个点在当前帧中对应的位置为 ，然后就可以求出点  投影到当前帧中的极线 
 
 
计算匹配的特征点到它对应极线的距离，如果这个距离超过阈值则被视为移动点，反之为静态点。距离的计算方法为：
 
Outlier Rejection

由于人体等运动物体的柔性变形和复杂运动，移动一致性检查方法很难提取完整动态区域的轮廓，更何况提取整个轮廓的时间开销非常大。在DS-SLAM中，由于采用了语义分割网络，可以很容易地获得物体的完整轮廓。我们的想法是将语义信息和移动一致性检查结果结合起来，完成两级语义知识库的建立：

对象是否移动。如果在分割对象的轮廓中存在通过移动一致性检查而产生的一定数量的动态点，则确定该对象正在移动。
如果确定分割对象正在移动，则删除位于对象轮廓中的所有特征点。通过这种方式，可以精确地消除异常值。此外，错误分割的影响也可以在一定程度上降低。
"""

def main(msg=""):
    role = Test()
    logger.info(msg)
    result = asyncio.run(role.run(msg))
    logger.info(result)


if __name__ == "__main__":
    main(text)