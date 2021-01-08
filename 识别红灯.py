# IR灰度跟踪示例

#

# 这个例子展示了使用OpenMV Cam进行红外信标灰度跟踪。



import sensor, image, time



from pyb import UART



import json


#uart = UART(3, 115200)

#实例化一个19200波特率的串口3



thresholds = (22, 100, 20, 127, -128, 127) # 识别绿光的阈值



sensor.reset()

#初始化摄像头，reset()是sensor模块里面的函数



sensor.set_pixformat(sensor.RGB565)

#设置图像色彩格式，有RGB565色彩图和GRAYSCALE灰度图两种



sensor.set_framesize(sensor.QVGA)

#设置图像像素大小


sensor.set_windowing((240, 240)) # VGA中心240x240像素
sensor.set_auto_exposure(False, exposure_us=2000)
sensor.set_auto_gain(False) # 颜色跟踪必须关闭自动增益
sensor.set_auto_whitebal(False, rgb_gain_db = (1,-1,1))
sensor.skip_frames(time = 2000)
clock1 = time.clock()
clock2 = time.clock()
while(True)
    x=0
    y=0
    w=0
    h=0
    while(1):    #1循环——不断找色块的循环
        clock1.tick()
        img = sensor.snapshot()
        blobs = img.find_blobs([thresholds],False,x_stride=2,y_stride=1,area_threshold=10,merge=True)
        print(clock1.fps())
        if blobs:
            print("wdnmd终于找到了")
            for b in blobs :
                x1 = b[0]   #x
                y1 = b[1]   #y
                w1 = b[2]   #w
                h1 = b[3]   #h
                if w*h==0:  #第一个色块判断
                    x=x1
                    y=y1
                    w=w1
                    h=h1
                if x>x1:    #找到的x还比原来的小
                    w=x-x1;
                    x=x1
                if y<y1:
                    h=y-y1
                    y=y1
            print(clock1.fps())
            break
        else
            print(clock2.fps())
            continue
    while(2):    #2循环——roi区域内找

        clock2.tick()
        img = sensor.snapshot()
        roi=[x-10,y-10,w+20,h+20]
        draw_rectangle(x-10,y-10,w+20,h+20,color=blue)
        blobs = img.find_blobs([thresholds],roi=roi,False,merge=True)
        if blobs:
            for b in blobs:
                x1 = b[0]   #x
                y1 = b[1]   #y
                w1 = b[2]   #w
                h1 = b[3]   #h
                if w*h==0:  #第一个色块判断
                    x=x1
                    y=y1
                    w=w1
                    h=h1
                if x>x1:    #找到的x还比原来的小
                    w=x-x1;
                    x=x1
                if y<y1:
                    h=y-y1
                    y=y1
            cw=w/2
            ch=h/2
            cx=cw+x
            cy=ch+y
            draw_rectangle(x,y,w,h,color=red)
            print(clock2.fps())
        else
            print(clock2.fps())
            break


