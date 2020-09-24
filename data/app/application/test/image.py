from PIL import Image,ImageFont,ImageDraw,ImageEnhance
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
        ratio = im.size[0]/im.size[1]
        print(ratio)
        im.thumbnail((int(pix),int(pix/ratio)))
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

def resize_paste(file,new_size):
    with Image.open(file) as imageA:
        ratio_file = imageA.size[0]/imageA.size[1]
        ratio_new = new_size[0]/new_size[1]
        resultPicture = Image.new('RGBA', new_size, (0, 0, 0, 0))
        if ratio_file <= ratio_new:
            #取resize height
            nim = imageA.resize( (int(new_size[1]*ratio_file), new_size[1]), Image.BILINEAR )
            #fill width
            fill_pix = int((new_size[0] - nim.size[0])/2)
            resultPicture.paste(nim,(fill_pix,0))
        else:
            #取resize width
            nim = imageA.resize( (new_size[0] ,int(new_size[0]/ratio_file) ), Image.BILINEAR )
            #fill height
            fill_pix = int((new_size[1] - nim.size[1])/2)
            resultPicture.paste(nim,(0,fill_pix))
        print(f'new size:{nim.size}')
        resultPicture.save(f'new_{os.path.splitext(file)[0]}.png')
        print(f'result size:{resultPicture.size}')
    #resultPicture = Image.new('RGBA', new_size, (0, 0, 0, 0))
    #把照片貼到底圖
    #resultPicture.paste(imageA,(0,0))
    #resultPicture.save("已合成圖片.png")
    
def resize_crop(file,new_size):
     
    with Image.open(file) as imageA:
        ratio_file = imageA.size[0]/imageA.size[1]
        ratio_new = new_size[0]/new_size[1]
        if ratio_file >= ratio_new:
            #取resize height
            nim = imageA.resize( (int(new_size[1]*ratio_file), new_size[1]), Image.BILINEAR )
            #crop width
            crop_pix = int((nim.size[0]-new_size[0])/2)
            result = nim.crop((crop_pix,0,int(new_size[0]+crop_pix),new_size[1]))
        else:
            #取resize width
            nim = imageA.resize( (new_size[0] ,int(new_size[0]/ratio_file) ), Image.BILINEAR )
            #crop height
            crop_pix = int((nim.size[1]-new_size[1])/2)
            result = nim.crop((0,crop_pix,nim.size[0],int(new_size[1]+crop_pix)))
        #print(f'new size:{result.size}')
        result.save(f'new_{file}', quality=100)    
        
def logo_watermark(img, logo_path):
    '''
    新增一個圖片水印,原理就是合併圖層，用png比較好
    '''
    baseim = img
    logoim = Image.open(logo_path)
    bw, bh = baseim.size
    lw, lh = logoim.size
    baseim.paste(logoim, (bw-lw, bh-lh))
    baseim.save('test3.jpg', 'JPEG')
    

def text_watermark(img, text, out_file="test4.jpg", angle=0, opacity=0.25):
    '''
    新增一個文字水印，做成透明水印的模樣，應該是png圖層合併
    http://www.pythoncentral.io/watermark-images-python-2x/
    這裡會產生著名的 ImportError("The _imagingft C module is not installed") 錯誤
    Pillow通過安裝來解決 pip install Pillow
    '''
    with Image.open(file) as img:
        watermark = Image.new('RGBA', img.size, (255,255,255,0)) 
        #白色底, 透明度0

        FONT = "msjh.ttc"
        size = 12
        #得到字型
        n_font = ImageFont.truetype(FONT, size)
        n_width, n_height = n_font.getsize(text)
        text_box = min(watermark.size[0], watermark.size[1])
        #文字逐漸放大，但是要小於圖片的寬高最小值
        while (n_width+n_height <  text_box):
            size += 2
            n_font = ImageFont.truetype(FONT, size=size)
            n_width, n_height = n_font.getsize(text)

        text_width = (watermark.size[0] - n_width) / 2
        text_height = (watermark.size[1] - n_height) / 1.25
        #watermark = watermark.resize((text_width,text_height), Image.ANTIALIAS)
        #在水印層加畫筆
        draw = ImageDraw.Draw(watermark, 'RGBA')                                       
        draw.text((text_width,text_height),
                  text, font=n_font, fill="#FFFFFF")
        watermark = watermark.rotate(angle, Image.BICUBIC)
        alpha = watermark.split()[3]
        alpha = ImageEnhance.Brightness(alpha).enhance(opacity)
        watermark.putalpha(alpha)
        Image.composite(watermark, img, watermark).save(out_file, 'JPEG')
        
    
if __name__ == '__main__':
    file1 = "image1.jpg"
    file2 = "image2.png"
    file3 = "height1.jpg"
    #info(file)
    file = file3
    #resize(file,f'new_{file}',800)
    #thumbnail(file1,200)
    #crop(file1,300,300,800,800)
    #resize_crop(file,(800,1200))
    #resize_paste(file,(800,1200))
    text_watermark(file1,"fuck your mother")
