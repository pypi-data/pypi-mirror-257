## IIIF imageAPI for FastAPI
・Install
```python
pip install FastIIIFimageAPI
```
・Instantiation
```python
from iafa import imageapi
processor = imageapi.imageAPI(
    version=2,
    pathPrefix='https://example.com/api/v1/image',
    opt = {
        "maxwidth"=10000
        "maxheight"=10000
    }
)
```
version(int): The version of imageAPI (2 or 3)
pathPrefix(str): The prefix of your API's URI
opt(Option?): 
    maxwidth(int): Maximum image width your API can provide
    maxheight(int): Maximum image height your API can provide
    
・Image Requests
```python
from fastapi import FastAPI

app = FastAPI()

@app.get('/api/v1/image/{imageIdentifier}/{req_path:path}')
async def returnImage(imageIdentifier: str, req_path: str):
    imagePath = IDtoPath(imageIdentifier) #arbitary function to find imagepath by imageIdentifier
    return processor.returnImage(imagePath, req_path)
```
・Infomation Requests
```python
@app.get('/api/v1/image/{imageIdentifier}/info.json')
async def returnInfo(imageIdentifier: str):
    imagePath = IDtoPath(imageIdentifier) #arbitary function to find imagepath by imageIdentifier
    return processor.returnInfo(imagePath, imageIdentifier)
```
Warning:
Always define Information Requests **before** Image Requests