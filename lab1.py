OPEN_list=[]
CLOSE_list=[]
success_shape=[1,2,3,8,0,4,7,6,5]
Main_deep=50
code_format=int(len(success_shape)**0.5)
print(code_format)
class tree_Node(object):
    def __init__(self, initlist, node=None, x_move=0, y_move=0, x_init=0, y_init=0):

        self.child_list = []
        self.child_num = []  # 里面是child的移动方向list
        self.success_child=None

        if node is None:
            '''是根节点'''
            self.parent_node = None
            self.shape = initlist
            self.pos = [x_init, y_init]
            self.deep=0
            print("root node generating...")
            for le in  range(code_format):
                print(self.shape[le*code_format:le*code_format+code_format])

        else:
            self.parent_node = node
            self.deep = node.deep +1   # 节点深度
            pos_ini = node.pos[:]  # 继承父节点空格位置
            self.shape = initlist[:]
            self.pos = [pos_ini[0] + x_move, pos_ini[1] + y_move]
            print(pos_ini,"-->",self.pos," 方向：",[x_move,y_move])


        self.parent_move = [x_move, y_move]  # 父节点的移动方向，用于搜索时排除父节点
        self.cate = OPEN_list
        self.status = False  # 有无被搜索过
        '''child数量等于3则表示添加了所有子节点，标true'''
        self.diff=0
        self.huff_n = 0
        sh = len(success_shape)
        for i in range(sh):
            if self.shape[i]!=success_shape[i]:
                self.diff+=1
            huf1 = success_shape.index(self.shape[i])
            self.huff_n += (abs(huf1 // code_format - i // code_format) + abs(huf1 % code_format - i % code_format))
        if self.diff == 0:
            self.success = True
        else:self.success = False
        self.f_value=self.deep+self.huff_n
        # self.step=0单开一个计算

    def show_node(self):
        print("F value:",self.f_value," |deep:",self.deep," huff:",self.huff_n)
        for le in range(code_format):
            print(self.shape[le * code_format:le * code_format + code_format])

    def move_node(self, x_move, y_move):
        '''
        根据移动方向改变交换空格0和目标的值
        :param x_move: -1,0,1
        :param y_move: -1,0,1
        :return: 改变后的shape
        '''
        shape0 = self.shape[:]
        pos1 = [self.pos[0] + x_move, self.pos[1] + y_move]  # 目标位置
        shape0[self.pos[1] * code_format + self.pos[0]] = shape0[pos1[1] * code_format + pos1[0]]
        shape0[pos1[1] * code_format + pos1[0]] = 0
        return shape0

    def add_child(self):  #
        '''
        搜索方向：上下左右，排除一个减一
        保证唯一性：不和父节点相同
        搜索close表查看是否有相同
        :param num:一次添加几个
        :return:
        '''
        print("---------------------------------------\nparent node:")
        self.show_node()
        num=3
        for move_x in range(-1, 2):
            for move_y in range(-1, 2):
                '''
                是否移动1位
                是否和父节点不相反
                子节点没加过
                没移动出九宫格
                '''
                if abs(move_x + move_y) == 1 \
                        and abs(move_x + self.parent_move[0]) + abs(move_y + self.parent_move[1]) \
                        and [move_x, move_y] not in self.child_num \
                        and code_format>move_x + self.pos[0] >= 0 and code_format>move_y + self.pos[1] >= 0:
                    shape_child = self.move_node(move_x, move_y)
                    print("child:",shape_child)
                    self.child_num.append([move_x, move_y])
                    newchild = tree_Node(shape_child, self, move_x, move_y)
                    self.child_list.append(newchild)
                    num -= 1
                    if newchild.success == True:
                        self.success_child = newchild
                        return True

                if num <= 0: break
            if num <= 0: break
            '''
                    新建node
                    TODO 判断是否success
                    
            '''
        return False

    def is_success(self):
        if self.shape==success_shape:
            self.success=True
            return True
        else:return False

    def huff(self):
        self.huff_n=0
        sh=len(success_shape)
        for i in range(sh):
            huf1=success_shape.index(self.shape[i])
            self.huff_n+=(abs(huf1//code_format - i//code_format)+abs(huf1%code_format - i%code_format))
        return self.huff_n



class BinaryIndexTree(object):
    '''
    TODO 判断是否出现在close表，如果是A*需要评估F值
    TODO 子节点加到open的前面还是后面还是排序在加
    TODO show函数：清屏，显示九宫格数字，每添加一个节点show一次，下方提示深度等和是否成功
    '''
    linklist=[]
    def __init__(self, initlist,x,y):
        '''初始化树'''
        self.success_path = []
        self.init_map = initlist
        OPEN_list=[]
        CLOSE_list=[]
        self.root_node=tree_Node(self.init_map)
        self.root_node.pos=[x,y]

    def main_search(self,search_type):
        node=self.root_node
        OPEN_list.append(node)
        if search_type=="link":
            self.link_search()
        else:

            while len(OPEN_list):
                #print("open:",OPEN_list)
                #print(node.shape)
                if node.success:
                    self.sucess_build(node)
                    break
                if search_type == "broad":
                    if self.broad_search(node):
                        self.sucess_build(node)
                        break
                    else:
                        node = OPEN_list[0]
                        #node.show_node()
                        print("open 长度",len(OPEN_list),"close 长度：",len(CLOSE_list))
                        continue
                if search_type == "deep":
                    if self.deep_search(node):
                        self.sucess_build(node)
                        print("open 长度", len(OPEN_list), "close 长度：", len(CLOSE_list))
                        break
                    else:
                        node = OPEN_list[0]
                        continue
                if search_type == "A":
                    if self.A_star(node):
                        self.sucess_build(node)
                        break
                    else:
                        node = OPEN_list[0]
                        print("open 长度", len(OPEN_list), "close 长度：", len(CLOSE_list))
                        continue
            print("open 长度", len(OPEN_list), "close 长度：", len(CLOSE_list))
            print("success path:")
            self.show_success()
            '''判断open不为空'''
            '''选第一个node进入特定搜索函数'''
            '''判断是否在close中，
            在：A*则比较F值，修改parent，其他直接return false，
            不在：产生子节点判断success，计算f值，根据顺序排序子节点'''
            '''父节点加入close，子节点按搜索type加入open'''
            '''返回主循环，如果子节点有success，把node加入path，返回自身'''
            ''''''

    def sucess_build(self,node:tree_Node):
        self.success_path.insert(0, node)
        while node.parent_node != None:
            self.success_path.insert(0,node.parent_node)
            node=node.parent_node

    def link_search(self):
        pass

    def broad_search(self,node:tree_Node):
        if node.success==True:
            #self.success_path.append(node)
            return True
        else:
            if self.inclose(node):
                print("in close")
                del OPEN_list[0]
                return False

            if node.add_child():
                self.success_path.append(node.success_child)
                #self.success_path.insert(0,node)
                return True
            else:
                CLOSE_list.append(node)
                del OPEN_list[0]
                for item in node.child_list:
                    if self.inopen(item):
                        print("in open")
                        continue
                    if self.inclose(item):
                        print("in close")
                        continue
                    OPEN_list.append(item)
        print("open长度",len(OPEN_list))
        self.show_open()
        return False


    def deep_search(self,node:tree_Node):
        if node.success == True:
            # self.success_path.append(node)
            return True
        else:
            if self.inclose(node):
                print("in close")
                del OPEN_list[0]
                return False

            if node.add_child():
                self.success_path.append(node.success_child)
                # self.success_path.insert(0,node)
                print("成功")
                return True
            else:
                CLOSE_list.append(node)
                del OPEN_list[0]
                i=0
                for item in node.child_list:
                    if self.inopen(item):
                        print("in open")
                        continue
                    if self.inclose(item):
                        print("in close")
                        continue
                    OPEN_list.insert(i,item)
                    node.show_node()
                    i+=1
        print("open长度", len(OPEN_list))
        self.show_open()
        return False

    def A_star(self,node:tree_Node):
        if node.success==True:
            #self.success_path.append(node)
            return True
        else:
            pos=self.inclose(node)
            if pos:
                '''计算f值比较大小，修改parent,i-1是close中的位置'''
                f_new=node.f_value
                f_old=CLOSE_list[pos-1].f_value
                print("in close")
                if f_new<=f_old:
                    CLOSE_list[pos - 1].parent_node=node.parent_node
                    print("change parent")
                del OPEN_list[0]
                return False

            if node.add_child():
                self.success_path.append(node.success_child)
                #self.success_path.insert(0,node)
                return True
            else:
                '''
                TODO child 计算f，排序
                '''
                CLOSE_list.append(node)
                del OPEN_list[0]
                childlist=[]
                for item in node.child_list:
                    if self.inopen(item):
                        print("in open")
                        continue
                    if self.inclose(item):
                        print("in close")
                        continue
                    ch_pos=0
                    for chs in OPEN_list:
                        if item.f_value>chs.f_value:
                            ch_pos+=1
                        else:break
                    OPEN_list.insert(ch_pos,item)


        print("open长度",len(OPEN_list),"子节点数量：",len(node.child_list))
        #self.show_open()
        return False

    def inclose(self,node:tree_Node):
        i=1
        for nodes in CLOSE_list:
            if nodes.shape == node.shape:
                return i
            i+=1
        return False
    def inopen(self,node:tree_Node):
        i=1
        for nodes in OPEN_list:
            if nodes.shape == node.shape:
                return i
            i+=1
        return False

    def can_solve(self):
        '''
        TODO 判断由初始矩阵转目标矩阵是否有解
        如何判断是否有解我在网上找了下，是判断初始矩阵的状态字符串的逆序数与目标矩阵的状态字符串的逆序数是否同奇或者同偶，如果同是奇数或同是偶数就有解。否者无解。
        :return:
        '''




    def show_close(self):
        for node in CLOSE_list:
            node.show_node()

    def show_open(self):
        for node in OPEN_list:
            node.show_node()

    def show_success(self):
        for node in self.success_path:
            node.show_node()
    '''
    
    '''

init_map1=[2,0,3,1,8,4,7,6,5]
init_map12=[2,3,0,1,8,4,7,6,5]
init_map2=[2,8,3,1,6,4,0,7,5]

init_map15=[1,2,3,0,5,6,7,4,9,10,11,8,13,14,15,12]
success_shape=[1,2,3,4,5,6,7,8,9,10,11,12,0,13,14,15]
code_format=int(len(success_shape)**0.5)
xp=3
yp=0
ss3=BinaryIndexTree(init_map15,xp,yp)
#ss33=BinaryIndexTree(init_map15,xp,yp)
ss3.main_search("A")
print("总长度：",len(ss3.success_path))

'''
ss1=BinaryIndexTree([2,0,3,1,8,4,7,6,5],1,0)
ss11=BinaryIndexTree([2,0,3,1,8,4,7,6,5],1,0)
ss1.main_search("broad")
ss11.main_search("deep")
'''

print("*****************deep*************************")
'''
ss2=BinaryIndexTree([2,8,3,1,6,4,0,7,5],0,2)
#ss22=BinaryIndexTree([2,8,3,1,6,4,0,7,5],0,2)
ss2.main_search("A")
print("总长度：",len(ss2.success_path))
#ss22.main_search("broad")'''
'''
init_map15=[11,9,4,15,1,3,0,12,7,5,8,6,13,2,10,14]
success_shape=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]
code_format=int(len(success_shape)**0.5)
xp=2
yp=1
ss3=BinaryIndexTree(init_map15,xp,yp)
#ss33=BinaryIndexTree(init_map15,xp,yp)
ss3.main_search("A")
print("总长度：",len(ss3.success_path))
#ss33.main_search("broad")
'''
print("*****************A_star*************************")

#

#print("总长度：",len(ss22.success_path))

