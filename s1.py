import cv2
import math
import numpy as np
import time

class player:
    def __init__(self):
        self.x=100
        self.y=100
        self.forward=0

    def move(self,vec):
        self.x+=vec[0]
        self.y+=vec[1]

    def rot(self,dir,ang):
        if dir==0:
            self.forward+=ang
        else:
            if dir==1:
                self.forward-=ang
# 定义观察者类，主要成员变量有：x,y当前位置坐标，forward为目光方向，用极坐标角度表示

class mapNode:
    def __init__(self):
        self.x=0
        self.y=0
        self.next=None
# 定义地图的节点，整个地图由节点组成，节点连接形成墙壁
map_list = [mapNode() for i in range(12)]
# 节点数组构成完整地图，下文会设置节点的内容

def isCol(pos1,pos2):
    # pos1 and pos2 are 2d vector,hs is Threshold
    tmp1=pos1[0]-pos2[0]
    tmp2=pos1[1]-pos2[1]
    tmp3=math.sqrt(tmp1*tmp1+tmp2*tmp2)
    if tmp3<2:
        return True
    else:
        return False
# 此函数用于测量两个点是否重合，传递两个坐标，如果坐标距离小于阈值则判断重合

def shotLight(sor,tar,bis):
    # tar is 2d vec(possition),sor is player obj
    for i in range(1000):
        tmp0 = sor.x+i*math.cos(sor.forward+bis)
        tmp1 = sor.y+i*math.sin(sor.forward+bis)
        # print([tmp0,tmp1])
        if isCol([tmp0,tmp1],tar):
            # print("Light_point,distance:",i)
            return i
    return -1
# 此函数用于从一个点发射光线并检测是否碰撞到物体，用一个循环来每次小距离延长光线，并调用上文的isCol来检测碰撞
# sor为观察者对象，tar为物体的坐标，bis观察者目光角度偏置

def shotWall(sor,wallNode,bis):
    # sor is play obj,wallNode is map Node obj
    if wallNode.next!=None:
        vec=[wallNode.next.x-wallNode.x,wallNode.next.y-wallNode.y]
        cds=100
        for i in range(cds):
            tar=[wallNode.x+1/cds*i*vec[0],wallNode.y+1/cds*i*vec[1]]
            ans=shotLight(sor,tar,bis)
            if ans!=-1:
                return ans
        return -1
    else:
        return -1
# 此函数用于检测观察者能否看见节点，通过前文的光线函数和初中数学知识实现

def shotMap(sor,maplist,bis):
    # sor is play obj
    index=-1
    for i in range(len(maplist)):
        ans=shotWall(sor,maplist[i],bis)
        index=i
        if ans!=-1:
            return ans, index
    return ans,index
# 合并前文的函数，调用时候直接传入地图list，循环检测list中的所有节点

Zoom=10
# 地图缩放

# 此处开始设置墙壁节点的位置并连接相应的节点
index=0
map_list[index].x=5
map_list[index].y=10
map_list[index].next=map_list[index+1]

index=1
map_list[index].x=5
map_list[index].y=5
map_list[index].next=map_list[index+1]

index=2
map_list[index].x=10
map_list[index].y=5
map_list[index].next=None

index=3
map_list[index].x=15
map_list[index].y=5
map_list[index].next=map_list[index+1]

index=4
map_list[index].x=20
map_list[index].y=5
map_list[index].next=map_list[index+1]

index=5
map_list[index].x=20
map_list[index].y=10
map_list[index].next=None

index=6
map_list[index].x=20
map_list[index].y=15
map_list[index].next=map_list[index+1]

index=7
map_list[index].x=20
map_list[index].y=20
map_list[index].next=map_list[index+1]

index=8
map_list[index].x=15
map_list[index].y=20
map_list[index].next=None

index=9
map_list[index].x=10
map_list[index].y=20
map_list[index].next=map_list[index+1]

index=10
map_list[index].x=5
map_list[index].y=20
map_list[index].next=map_list[index+1]

index=11
map_list[index].x=5
map_list[index].y=15
map_list[index].next=None

# 地图缩放
for item in map_list:
    item.x*=Zoom
    item.y*=Zoom


img_size = (1024, 1024)  # 图像尺寸
bg_color = (255, 255, 255)  # 背景色为白色
radius = 10  # 原点半径
color = (0, 0, 255)  # 原点颜色为蓝色
thickness = -1  # 填充圆形
delay = 1  # 帧率


def drawMap(map_list,img):
    for item in map_list:
        if item.next!=None:
            st=[int(item.x),int(item.y)]
            ed=[int(item.next.x),int(item.next.y)]
            cv2.line(img, st, ed, (100, 0, 0), 1, 4)
# 绘制地图，在img对象中循环画墙（墙壁就是line线段）


def drawPlayer(player,img):
    c = (10, 10, 10)
    pos=[int(player.x),int(player.y)]
    cv2.circle(img, pos, 1, c, -1)

    st = [int(player.x),int(player.y)]
    le=200
    ed = [int(player.x+le*math.cos(player.forward)),int(player.y+le*math.sin(player.forward))]
    # print(st,ed)
    cv2.line(img, st, ed, (200, 200, 200), 1, 4)
# 绘制观察者及其目光


# main
img = np.zeros((img_size[1], img_size[0], 3), dtype=np.uint8)
img[:, :] = bg_color

myplay=player()
myplay.x=90
myplay.y=20
myplay.forward=45/57
# 初始化观察者位置和目光角度

st=[myplay.x,myplay.y]
# print(shotWall(myplay,map_list[7]))
# print((shotMap(myplay,map_list,0)))
img=drawMap(map_list,img)
drawPlayer(myplay,img)
ang=50
tplay=player()
tplay.x=myplay.x
tplay.y=myplay.y
# tplay.forward=(45+(ang/2))/57
# drawPlayer(tplay,img)
# tplay.forward=(45-(ang/2))/57
# drawPlayer(tplay,img)
# cv2.imshow("text", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

img2 = np.zeros((1024, 1024, 3), dtype=np.uint8)
img2[:, :] = bg_color
#
st=[0,512]
ed=[1024,512]
cv2.line(img2, st, ed, (0, 0, 0), 1, 4)
cv2.namedWindow("rend")
# cv2.imshow("text", img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# 颜色库list
colorlist=[
(50,200,40),
(10,200,20),
(100,50,100),
(100,30,200),
(100,200,200),
(20,10,100),
(50,50,75),
(50,50,255),
(50,10,75),
(125,50,50),
(225,150,30),
(255,20,10),
]


# 这里开始是主函数，上面一部分代码大部分没啥用，调试时候没删完的
drawMap(map_list,img2)
drawPlayer(myplay,img2)

# ang为目光范围角度，将其细分成100份作为目光中线偏置值
cds=200
for i in range(cds):
    scan=(-ang+ang*2*(i/cds))/57
    tplay.forward = 45/57+scan
    drawPlayer(tplay, img2)
    dis=shotMap(myplay,map_list,scan)
    # 如果目前偏置打中墙壁则会返回最近的墙壁距离和墙体节点的编号，光线延长走完都打不着返回-1
    # print(i, dis)
    if dis[0]!=-1:
        lo=int(0+dis[0])
        hi=int(1024-dis[0])
        # hi和lo为绘制竖线的上下坐标，而水平方向坐标则用大循环的i来均分水平线
        st = [int(0+i*1024/cds), lo]
        ed = [int(0+i*1024/cds), hi]
        c=colorlist[dis[1]%12]
        # 用墙体节点编号作为颜色库的下标来绘制异色墙体
        cv2.line(img2, st, ed, c, 1, 4)
    #     绘图并刷新
    cv2.imshow("rend", img2)
    if cv2.waitKey(delay) == 1:
        break

# cv2.imshow("rend", img2)
cv2.waitKey(0)
cv2.destroyAllWindows()