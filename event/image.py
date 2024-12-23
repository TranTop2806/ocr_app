# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw

lines = [('古本=國演義悉一第四囘', [[517, 127], [530, 127], [530, 333], [517, 333]]), ('來呈董卓車曰怨望作詩殺之有名矣遂命李僞帶武士十人入宮弒帝帝與后妃正在模上宮女報李價至帝六', [[488, 761], [495, 61], [514, 62], [508, 762]]), ('蠻儒以動酒奉帝帝問何故儒曰春日融和董相國特上壽酒太后曰旣云壽酒汝可先飮個怒曰汝不飲耶呼左', [[468, 759], [475, 62], [493, 63], [486, 760]]), ('右持短刀白練於前曰發酒不飲可領此二物唐妃跪告曰妾身代帝飲酒願公存母子性命儒叱曰汝何人可代', [[447, 760], [454, 62], [472, 63], [466, 761]]), ('王死乃舉酒與何太后曰汝可先飲后大駡何進無謀引賊入京致有今日之福儒催逼帝帝曰容我輿太后作别', [[426, 760], [433, 62], [451, 63], [445, 761]]), ('乃大慟而作歌其歌曰一天地易令曰月翻棄萬乘兮退守藩爲臣遍令命不久大勢去兮空溪潜一唐妃亦作歌', [[406, 759], [411, 61], [429, 62], [425, 760]]), ('曰一皇天將崩兮后土類身爲帝姬兮恨不隨生死昊路令從此別奈何營速令心中悲一歌罷相抱而哭李儒此', [[386, 762], [389, 63], [408, 64], [404, 763]]), ('曰相國立等囘報汝等俄延望誰救耶太后大爲蓋賊福我母子皇天不估汝等助惡必當滅族儒大怒雙手扯住', [[364, 760], [370, 63], [388, 64], [383, 761]]), ('太后直按下樓叱武士絞死唐妃以酤漸灌殺少帝還報董卓章命葬於城外自此每夜入宮姦淫宮女夜宿龍狀', [[343, 759], [349, 62], [367, 63], [362, 760]]), ('當引軍出域行到陽城地方時當二月村民社赛男女皆集直命軍士圍住盡皆殺之掠婦之財物裝載章上期頭', [[323, 760], [329, 62], [346, 63], [341, 761]]), ('千餘顆於車下連輪還都拇言殺賊大勝而囘於城門下贊燒人頭以婦女財物分散衆軍越騎校尉伍孚字德瑜', [[302, 760], [308, 62], [326, 63], [321, 761]]), ('見車殘暴憤恨不平當於朝服內披小銷藏短刁欲伺便殺卓一日卓入朝学迎之閣下拔刀直刺卓車乞力大兩', [[282, 760], [287, 62], [305, 63], [300, 761]]), ('手揾住呂市便入揪倒伍孚單問曰誰敎汝反孚瞪目大喝曰汝非吾君吾非汝臣何反之有汝罪惡盈天人人可', [[261, 759], [267, 63], [284, 64], [279, 760]]), ('得而詠之吾恨不車裂汝以謝天下寧大怒命牽出剖翩之孚至死駡不絶口後人有詩讚之曰一漢末忠臣說在', [[240, 761], [244, 61], [263, 62], [259, 762]]), ('李冲天豪氣世間無朝堂殺賊名猶在萬古堪稱大文夫L董車自此川入常带甲士護衞時責紹迕渤海聞知董', [[220, 760], [225, 62], [243, 63], [238, 761]]), ('卓弄權乃差人齎密書來見王允書略曰[車賊歉天廢主人不忍言而公恣其跋扈如不聽聞豈報國效忠之臣', [[198, 759], [204, 62], [222, 63], [217, 760]]), ('哉經今集兵練卒欲掃淸王室未敢經動公若有心當乘間圖之若有驅使卽當本命4王允得書尋思無計一曰', [[178, 758], [183, 62], [201, 63], [196, 759]]), ('於侍班閣子內見舊臣俱在允曰今日老夫賤隆晚間敢屈衆位到舍 小酌衆官皆曰必來祝壽當晚王允設宴後', [[157, 760], [163, 62], [180, 63], [175, 761]]), ('堂公抑皆至酒行數巡王允忽然揸面大哭衆官驚問曰司徒崭誕何故發悲允曰今曰並非賤降因欲與衆位一一', [[136, 761], [141, 62], [160, 63], [154, 762]]), ('敍恐黄車見疑故託言耳董申欺主弄權社稷旦夕難保想高皇誅秦滅楚奄有天下誰想傳至今日乃喪於董事', [[115, 761], [120, 61], [139, 62], [133, 762]]), ('之手此吾所以哭也於是衆官皆哭坐中一人獨撫掌笑曰滿朝公卿夜哭到昍謂哭到夜谔能哭死卓董否允覩', [[95, 760], [100, 61], [118, 62], [113, 761]]), ('之乃 驍騎校尉曹操也允怒曰汝祖宗亦食祿谟朝今不思報國而反笑耶操曰操不笑別事笑衆位無一計殺舊', [[74, 758], [78, 61], [98, 62], [93, 759]])]
width=612
height=792

image_path = "data/TQDN_1/page_1.png"

def draw_bounding_boxes(image_path: str, lines: list,width, height, output_path: str = "output_bbox.png"):
    """
    Vẽ bounding boxes trên hình ảnh dựa trên tọa độ bbox.
    """
    # Mở hình ảnh
    image = Image.open(image_path)
    image = image.resize((width, height))
    draw = ImageDraw.Draw(image)



    # Vẽ mỗi bbox
    for line, bbox in lines:
        points = [(x, y) for x, y in bbox]
        points.append(points[0]) 
        draw.line(points, fill="blue", width=2)  

    # Lưu hình ảnh kết quả
    image.save(output_path)


# Gọi hàm
draw_bounding_boxes(image_path,  lines, width, height)