from PIL import Image
import os

def resize(image,newimage,width):
    """
    resize() 這個方法會傳回一個新的 Image 物件，所以舊的 Image 不會被更動。resize() 接受兩個參數，
    第一個用來指定變更後的大小，是一個雙元素 tuple，分別用以指定影像的寬與高；第二個參數可以省略，
    是用來指定變更時使用的內插法，預設是 Image.NEAREST (取最近點)，這裡我們指定為品質比較好的 Image.BILINEAR。
    """
    with Image.open(image) as im:
        ratio = float(width)/im.size[0]
        height = int(im.size[1]*ratio)
        nim = im.resize( (width, height), Image.BILINEAR )
        print(f'new size:{nim.size}')
        nim.save(newimage, quality=100)

def info(file):
    with Image.open(file) as im:
        # format: jpeg/png/gif
        # size: 長,寛
        # mode:調色盤是 RGB/RGBA/P 全彩模式
        print(im.format, im.size, im.mode)
        #Image.save() 方法會根據欲存檔的副檔名，自動判斷要存圖檔的格式。
        im.save(f"quality100.{im.format.lower()}", quality=100 )
        
def thumbnail(file,pix):
    """
    縮圖的製作可能是特別常用的；PIL 對縮圖提供了一個方便的 thumbnail() 方法。
    thumbnail() 會直接修改 Image 物件本身，所以速度能比 resize() 更快，也消耗更少的記憶體。
    它不接受指定內插法的參數，而且只能縮小影像，不能放大影像；用法是：

    >>> im = Image.open( "sample01.jpg" )
    >>> im.thumbnail( (400,100) )
    >>> im.save( "thumbnail.jpg" )
    >>> print im.size
    (133, 100)
    
    thumbnail() 在接受尺寸參數的時候，行為與 resize() 不同；
    resize() 允許我們不等比例進行縮放，
    但 thumbnail() 只能進行等比例縮小，並且是以長、寬中比較小的那一個值為基準。
    因此，上面的程式所作出的 thumbnail.jpg 變成了 133*100 的小圖片：
    """
    with Image.open(file) as im:
        im.thumbnail((int(pix),int(pix)))
        im.save( f"{os.path.splitext(file)[0]}_thumbnail.{im.format.lower()}" )
        print(im.format, im.size, im.mode)
    
def crop(file,left,top,right,buttom):
    """
    對影像的內容進行裁切：
    >>> im = Image.open( "sample01.jpg" )
    >>> nim = im.crop( (700, 300, 1500, 1300) )
    >>> nim.save( "croped.jpg" )
    crop() 接受的 box 參數指定要裁切的左、上、右、下四個邊界值，形成一個矩形。
    +++
    如果要針對尺寸太大, 又要規範一定的長寛?
    1.resize到長邊大小一致 (正方形到長方形, 長方形到正方形, 需不同)
    2.再crop掉多的那邊長度
    """
    with Image.open(file) as im:
        nim = im.crop( (left,top,right,buttom) )
        nim.save( f"{os.path.splitext(file)[0]}_crop.{im.format.lower()}" )
        print(nim.format, nim.size, nim.mode)
        
    
if __name__ == '__main__':
    file1 = "image1.jpg"
    file2 = "image2.png"
    file3 = "image3.gif"
    #info(file)
    #resize(file,f'new_{file}',100)
    #thumbnail(file1,200)
    crop(file1,300,300,800,800)


