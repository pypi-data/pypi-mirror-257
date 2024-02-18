import io
import re
from PIL import Image
from fastapi import HTTPException, Response

# determined by server
class Option:
    maxwidth: int
    maxheight: int

class imageAPI:

    version: int
    pathPrefix: str
    opt: Option

    def __init__(self, version: int, pathPrefix: str, *opt: Option) -> None:
        self.version = version
        self.pathPrefix = pathPrefix
        self.opt = opt 

    #return readablestreaming of image and its format
    def returnImage(self, imagePath: str, reqPath: str) -> Response:
        paths = self.__reqPathParser(reqPath)
        img = Image.open(imagePath)
        if (not img): raise HTTPException(status_code=400, detail='Not Found')

        reg = self.__regionSelector(paths["region"], img.size)
        print(reg)
        siz = self.__sizeSelector(reg[2], reg[3], paths["size"])
        rot = self.__angleSelector(paths["rotation"])
        qua = self.__qualitySelector(paths["quality"])
        fom = self.__fromatSelector(paths["format"])
        
        cropped = img.crop((reg[0], reg[1], reg[0]+reg[2], reg[1]+reg[3]))
        sized = cropped.resize(siz)
        if rot["isFlip"] == True:
            sized = sized.transpose(Image.FLIP_LEFT_RIGHT)
        rotated = sized.rotate(rot["angle"], expand=True)
        if qua:
            qualitated = rotated.convert(qua)
        else:   
            qualitated = rotated

        vf = io.BytesIO()
        qualitated.save(vf, format=fom)
        return Response(vf.getvalue(), status_code=200, media_type=f'image/{fom}')
    
    #return technicalPropaties
    def returnInfo(self, imagePath: str, identifier: str) -> dict[str, any]:
        img = Image.open(imagePath)
        if (not img): raise HTTPException(status_code=400, detail='Not Found')
        metaData = img.size

        sizes: list[dict[str, int]] = []

        size: tuple[int, int] = (img.size[0], img.size[1])

        while (size[0] >100 and size[1] > 100) :
            sizes.append({
                "width": size[0],
                "height": size[1],
            })
            size = (int(size[0]/2), int(size[1]/2))

        json = {
            "@context": f"http://iiif.io/api/image/{self.version}/context.json",
            "@id": f"{self.pathPrefix}/{identifier}/info.json",
            "protocol": "http://iiif.io/api/image",
            "width": metaData[0],
            "height": metaData[1],
            "sizes": sizes,
            "tiles": [
                {"width": 512, "scaleFactors":[1, 2, 4, 8, 16]}
            ],
            "extraFormats": ["jpg", "jpeg", "tif", "tiff", "png"],
            "extraQualities": ["color", "gray", "bitonal"],
            "extraFeatures": [
                "baseUriRedirect",
                "mirroring",
                "regionByPct",
                "regionByPx",
                "regionSquare",
                "rotationArbitrary",
                "rotationBy90s",
                "sizeByConfinedWh",
                "sizeByH",
                "sizeByPct",
                "sizeByW",
                "sizeByWh",
                "sizeUpscaling",
            ],
        }
        if self.opt:
            json["maxWidth"] = self.opt.maxwidth
            json["maxHeight"] = self.opt.maxheight
        return json

    #utilities
    #return (x, y, width, height)
    def __regionSelector(self, region: str, metaData: tuple[int, int]) -> tuple[int, int, int, int]:

        if region == "full":
            return (0, 0, metaData[0], metaData[1])
        elif region == "square":
            if metaData[0] > metaData[1]:
                margin: int = (metaData[0] - metaData[1]) / 2
                return (margin, 0, metaData[1], metaData[1])
            else:
                margin: int = (metaData[1] - metaData[0]) /2
                return (0, margin, metaData[0], metaData[0])
        elif re.match(r'^pct:\d{1,},\d{1,},\d{1,},\d{1,}$', region):
            xywh = region[4:].split(',')
            x = round(int(xywh[0]) * 0.01 * metaData[0])
            y = round(int(xywh[1]) * 0.01 * metaData[1])
            w = round(int(xywh[2]) * 0.01 * metaData[0])
            h = round(int(xywh[3]) * 0.01 * metaData[1])
            return (x, y, w, h)
        elif re.match(r'^\d{1,},\d{1,},\d{1,},\d{1,}$', region):
            xywh = region.split(',')
            x = int(xywh[0])
            y = int(xywh[1])
            w = int(xywh[2])
            h = int(xywh[3])
            if (x > metaData[0]) or (y > metaData[1]) or (w > metaData[1]) or (h > metaData[1]):
                raise HTTPException(status_code=400, detail="Bad Request")
            return (x, y, w, h)
        else:
            raise HTTPException(status_code=400, detail="Bad Request")
    
    #return (width, height)
    def __sizeSelector(self, width: int, height: int, size: str) -> tuple[int, int]:
        if size == "max":
            if self.opt:
                if width > self.opt.maxwidth or height > self.opt.maxheight:
                    raise HTTPException(status_code=400, detail="Bad Request")
            return (width, height)
        elif size == "^max":
            return (width, height)
        elif re.match(r'^pct:\d{1,}$', size):
            n: int = int(size[4:])
            if (n > 100):
                raise HTTPException(status_code=400, detail="Bad Request")
            return (int(width*0.01*n), int(height*0.01*n))
        elif re.match(r'^\^pct:\d{1,}$', size):
            n: int = int(size[5:])
            return (int(width*0.01*n), int(height*0.01*n))
        #w,h
        elif re.match(r'^\d{1,},\d{1,}$', size):
            w: int = int(size.split(',')[0])
            h: int = int(size.split(',')[1])
            if (w > width) or (h > height):
                raise HTTPException(status_code=400, detail="Bad Request")
            return (w, h)
        #^w,h
        elif re.match(r'^\^\d{1,},\d{1,}$', size):
            w: int = int(size[1:].split(',')[0])
            h: int = int(size[1:].split(',')[1])
            return (w, h)
        #!w,h
        elif re.match(r'^\!\d{1,},\d{1,}$', size):
            w: int = int(size[1:].split(',')[0])
            h: int = int(size[1:].split(',')[1])
            if (w > width) or (h > height):
                raise HTTPException(status_code=400, detail="Bad Request")
            if w/width > h/height:
                return (int(w*h/height), h)
            else:
                return (w, int(h*w/width))
        #^!w,h
        elif re.match(r'^\^\!\d{1,},\d{1,}$', size):
            w: int = int(size[2:].split(',')[0])
            h: int = int(size[2:].split(',')[1])
            if w/width > h/height:
                return (int(w*h/height), h)
            else:
                return (w, int(h*w/width))
        #w,
        elif re.match(r'^\d{1,},$', size):
            w: int = int(size[0])
            if w > width:
                raise HTTPException(status_code=400, detail="Bad Request")
            return (w, height)
        #^w
        elif re.match(r'^\^\d{1,},$', size):
            w: int = int(size[0])
            return (w, height)
        #,h
        elif re.match(r'^,\d{1,}$', size):
            h: int = int(size[1])
            if h > height:
                raise HTTPException(status_code=400, detail="Bad Request")
            return (width, h)
        #^,h
        elif re.match(r'^\^,\d{1,}$', size):
            h: int = int(size[1])
            return (width, h)
        else:
            raise HTTPException(status_code=400, detail="Bad Request")
    
    #return {"angle": int, "isFlip": boolean}
    def __angleSelector(self, rotation: str) -> dict[str, any]:
        if re.match(r'^\!\d{1,}$', rotation):
            angle: float = float(rotation[1:])
            if angle > 360 or angle < 0:
                raise HTTPException(status_code=400, detail="Bad Request")
            return {"angle": angle, "isFlip": True}
        elif re.match(r'^\d{1,}$', rotation):
            angle: float = float(rotation)
            if angle > 360 or angle <0:
                raise HTTPException(status_code=400, detail="Bad Request")
            return {"angle": angle, "isFlip": False}
        else:
            raise HTTPException(status_code=400, detail="Bad Request")
    
    def __qualitySelector(self, quality: str) -> str | None:
        if quality == 'default':
            return None
        elif quality == 'color':
            return None
        elif quality == 'gray':
            return 'L'
        elif quality == 'bitonal':
            return '1'
        else:
            raise HTTPException(status_code=400, detail="Bad Request")
        
    def __reqPathParser(self, reqPath: str) -> dict[str, str]:
        splited = reqPath.split('/')
        region = splited[0]
        size = splited[1]
        rotation = splited[2]
        quality = splited[3].split('.')[0]
        format = splited[3].split('.')[1]   
        return {
            "region": region,
            "size": size,
            "rotation": rotation,
            "quality": quality,
            "format": format,
        }
    
    def __fromatSelector(self, format: str) -> str:
        allowed_formats = ["jpg", "jpeg", "tif", "tiff", "png"]
        if not format in allowed_formats:
            raise HTTPException(status_code=400, detail="Bad Request")
        if format == 'jpg':
            return 'jpeg'
        if format == 'tif':
            return 'tiff'
        return format