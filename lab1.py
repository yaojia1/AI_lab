OPEN_list=[]
CLOSE_list=[]
success_shape=[1,2,3,8,0,4,7,6,5]
main_map=[]
pos_x=0
pos_y=0
Main_deep=10
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


#fix_point=[]
#active_point_ini=[]
#map_new=[]


class BinaryIndexTree(object):
    '''
    TODO 判断是否出现在close表，如果是A*需要评估F值
    TODO 子节点加到open的前面还是后面还是排序在加
    TODO show函数：清屏，显示九宫格数字，每添加一个节点show一次，下方提示深度等和是否成功
    '''
    linklist=[]
    def __init__(self, initlist,x,y):
        '''初始化树'''
        self.map_new = []
        self.route = []
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
                        print("sucess!!!")
                        node.show_node()
                        break
                    else:
                        node = OPEN_list[0]
                        #node.show_node()
                        print("open 长度",len(OPEN_list),"close 长度：",len(CLOSE_list))
                        continue
                if search_type == "deep":
                    if self.deep_search(node):
                        self.sucess_build(node)
                        print("sucess!!!")
                        node.show_node()
                        print("open 长度", len(OPEN_list), "close 长度：", len(CLOSE_list))
                        break
                    else:
                        node = OPEN_list[0]
                        continue
                if search_type == "A":
                    if self.A_star(node):
                        self.sucess_build(node)
                        print("sucess!!!")
                        node.show_node()
                        break
                    else:
                        node = OPEN_list[0]
                        print("open 长度", len(OPEN_list), "close 长度：", len(CLOSE_list))
                        continue
            print("open 长度", len(OPEN_list), "close 长度：", len(CLOSE_list))
            #print("success path:")
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

    def search_point(self,pos,n):
        if n==0:
            return
        active_point=self.active_point_ini[:]
        fix_point=self.fix_point[:]

        pass
    def build_route(self):

        active_point=self.active_point_ini[:]
        po1 = self.root_node.pos[:]
        active_point.remove(po1)
        if len(active_point)==1:
            print(active_point[0],po1)
            if abs(po1[0]-active_point[0][0])+abs(po1[1]-active_point[0][1])==1:
                self.map_new[po1[0]+po1[1]*code_format]=self.map_new[active_point[0][0]+active_point[0][1]*code_format]
                self.map_new[active_point[0][0] + active_point[0][1] * code_format]=0
                #print(code_format,active_point[0],po1,self.map_new[po1[0]+po1[1]*code_format],self.map_new[active_point[0][0] + active_point[0][1] * 3])
                self.route.append([po1,active_point[0]])
                for i in range(code_format):
                    print(self.map_new[i * code_format:(i + 1) * code_format])
                print("success")
                # del self.active_point_ini[0]
                return False
            else:
                print("faild")
                return False

        #active_point.remove(po1)
        po2=active_point[0]
        del active_point[0]
        i=self.map_new.index(success_shape[po2[1]*code_format+po2[0]])
        po3 = [i % code_format, i // code_format]
        active_point.remove(po3)
        route_i=[po1, po2, po3]
        print("route point",route_i)
        cent=[(po1[0]+po2[0]+po3[0])/3,(po1[1]+po2[1]+po3[1])/3]
        route_2=[]
        num=0

        while num<3:

            print("**********************************************\nactive point:" , active_point)

            move_x=route_i[num%3][0]
            move_y = route_i[num % 3][1]
            route_2.append([move_x, move_y])
            print("selected point",route_i)
            print("route point:", route_2)

            toward_x = True
            x_length = route_i[(num + 1) % 3][0] - move_x
            y_length = route_i[(num + 1) % 3][1] - move_y
            if move_y < route_i[(num + 1) % 3][1]:
                if y_length * (cent[0] - move_x) < cent[1] * x_length:
                    toward_x = False
                else:
                    toward_x = True
            elif move_y > route_i[(num + 1) % 3][1]:
                if y_length * (cent[0] - move_x) < cent[1] * x_length:
                    toward_x = True
                else:
                    toward_x = False
            else: toward_x = False

            while  move_x!=route_i[(num+1)%3][0] and move_y!=route_i[(num+1)%3][1]:
                '''三角形中心点'''
                print("-------------------\nmoving point:", [move_x, move_y], "第", num % 3+1, "个route：", route_i[(num + 1) % 3],toward_x)
                if toward_x :
                    if move_x==route_i[(num+1)%3][0]:
                        toward_x=False
                        continue
                    po_new=[move_x+(route_i[(num+1)%3][0]>move_x),move_y]
                    if po_new in active_point:
                        route_2.append(po_new)
                        active_point.remove(po_new)
                        print("add x point" , po_new)
                        move_x+=(route_i[(num+1)%3][0]>move_x)
                        continue
                    if po_new in self.fix_point and po_new not in route_2:
                        route_2.append(po_new)
                        #self.fix_point.remove(po_new)
                        print("add x fix point", po_new)
                        move_x += (route_i[(num + 1) % 3][0] > move_x)
                        continue
                    if po_new==route_i[(num+1)%3]:
                        #route_2.append(po_new)
                        break
                if move_y!=route_i[(num+1)%3][1]:
                    po_new = [move_x , move_y + (route_i[(num + 1) % 3][1] > move_y)]
                    if po_new in active_point:
                        route_2.append(po_new)
                        active_point.remove(po_new)
                        move_y+=(route_i[(num + 1) % 3][1] > move_y)
                        print("add y point", po_new)
                        continue
                    if po_new in self.fix_point and po_new not in route_2:
                        route_2.append(po_new)
                        #self.fix_point.remove(po_new)
                        move_y+=(route_i[(num + 1) % 3][1] > move_y)
                        print("add y fix point", po_new)
                        continue
                    if po_new==route_i[(num+1)%3]:
                        #route_2.append(po_new)
                        break

                ppp=0
                for point in active_point:
                    if abs(point[0]-move_x)+abs(point[1]-move_y)==1:
                        print("add ex point",[move_x,move_y],point)
                        move_x,move_y=point[0],point[1]
                        route_2.append(point[:])
                        active_point.remove(point)
                        ppp=1
                        break

                if ppp==0:
                    for point in self.fix_point:
                        if point not in route_2 and abs(point[0] - move_x) + abs(point[1] - move_y) == 1:
                            print("add fix point", [move_x, move_y], point)
                            move_x, move_y = point[0], point[1]
                            route_2.append(point[:])
                            self.fix_point.remove(point)
                            ppp = 1
                            break
                    if ppp==0:
                        print("无法产生环路", move_x, move_y, route_i[(num + 1) % 3])
                        print("route ", route_2)
                        print("active", active_point)
                        return False



            num+=1
        '''数字换位置'''
        value_fix = route_2.index(po2)
        value_move = route_2.index(po3)
        pos_blank= route_2.index(po1)
        weiyi=value_fix-value_move
        map_new_2= self.map_new[:]
        print("最终route：",route_2,"位移：",weiyi)
        for pos in range(len(route_2)):
            po_fix=route_2[(pos+weiyi)%len(route_2)]
            po_move = route_2[pos]
            map_new_2[po_fix[0]+po_fix[1]*code_format]= self.map_new[po_move[0] + po_move[1] * code_format]
            if map_new_2[po_fix[0]+po_fix[1]*code_format]==0:
                self.root_node.pos =po_fix
        self.map_new=map_new_2[:]
        self.route.append(route_2)

        #del self.active_point_ini[0]
        return True


                #if move_y <  and
                #if (route_i[(num+1)%3][0]-move_x)*(route_i[(num+2)%3][0]-move_x)>=0:
                #if (route_i[(num+1)%3][1]-move_y)/(route_i[(num+1)%3][0]-move_x)>(route_i[(num+2)%3][1]-move_y)/(route_i[(num+2)%3][0]-move_x):
                    #



    def link_search(self):
        #[x,y]=self.root_node.pos
        #fix_point=[]
        #active_point=[]
        #map_new=[]
        #link_route=[]
        self.fix_point = []
        self.active_point_ini = []
        for i in range(len(success_shape)):
            self.map_new.append(self.init_map[i])
            if self.init_map[i]==success_shape[i]:
                self.fix_point.append([i%code_format,i//code_format])
            else:self.active_point_ini.append([i%code_format,i//code_format])
        while self.map_new!=success_shape and self.build_route():
            print("@@@@@@@@@next point@@@@@@@@@@@@@@@@\n")
            for i in range(code_format):
                print(self.map_new[i*code_format:(i+1)*code_format])
            self.fix_point=[]
            self.active_point_ini=[]
            for i in range(len(success_shape)):
                if self.map_new[i] == success_shape[i]:
                    self.fix_point.append([i % code_format, i // code_format])
                else:
                    self.active_point_ini.append([i % code_format, i // code_format])
        #print("success")
        for i in range(code_format):
            print(self.map_new[i * code_format:(i + 1) * code_format])
        print("总route")
        for ro in self.route:
            print(ro)


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
            #if node.deep>=Main_deep:
            #    return False
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
                    if node.deep>=Main_deep:
                        print("too deep")
                        continue
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
'''
init_map1=[2,0,3,1,8,4,7,6,5]
init_map12=[2,3,0,1,8,4,7,6,5]
init_map2=[2,8,3,1,6,4,7,0,5]
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

while True:
        x = int(input("请输入数码种类：（8 or 15）"))
        if x == 8:
            main_map = [2, 8, 3, 1, 6, 4, 7, 0, 5]
            success_shape = [1, 2, 3, 8, 0, 4, 7, 6, 5]
            pos_x = 1
            pos_y = 2
        else:
            main_map = [1, 2, 3, 0, 5, 6, 7, 4, 9, 10, 11, 8, 13, 14, 15, 12]
            success_shape = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,0]
            pos_x = 3
            pos_y = 0
        code_format = int(len(success_shape) ** 0.5)
        print(main_map,success_shape)
        tree = BinaryIndexTree(main_map, pos_x, pos_y)
        s = input("请输入搜索种类：（broad or deep or A or link）")
        print("*****************",s,"*************************")
        tree.main_search(s)

        del tree
        break


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


