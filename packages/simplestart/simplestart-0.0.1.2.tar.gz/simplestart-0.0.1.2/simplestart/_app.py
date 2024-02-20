from starlette.applications import Starlette
from starlette.responses import JSONResponse, StreamingResponse
from starlette.routing import Route, Mount
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware

from server import *
import server
import io

middleware = [
    Middleware(CORSMiddleware, allow_origins=['*'], allow_methods=["*"])
]


async def media_handler(request):
    return await server.media_handler(request)

routes = [
    Mount('/media', app=Starlette(routes=[
        Route("/{filename:path}", endpoint=media_handler),
    ])),
]

app = Starlette(middleware=middleware, routes=routes)

def is_directory_exists(directory_path):
    return os.path.exists(directory_path) and os.path.isdir(directory_path)

# 创建一个静态文件实例
if is_directory_exists("components"):
    static_files = StaticFiles(directory='components')
    # 将静态文件实例挂载到路径上
    app.mount('/components', static_files)

#
@app.route('/hello')
async def _home(request):
    return await server.home(request)


# Serve static files
@app.route("/")
async def _static_root(request):
    print("static root")
    return await server.send_static(request)

@app.route("/{path}")
async def _send_static(request):
    return await server.send_static(request)

#这个对于发布后的版本刷新 /pages/...有用
@app.route("/pages/{path}")
async def _send_static(request):
    return await server.send_static(request)

@app.route("/assets/{path}")
async def _send_static_resource(request):
    return await server.send_static_resource(request)

#这里不能带子目录，否则不能映射到这里。通过ss.config["videopath"]实现真正的子目录
@app.route("/video/{filename}")
async def _serve_video(request):
    return await server.serve_video(request)

#测试
@app.route("/image/{filename}")
async def image(request):
    print("图片")
    
    image_path = request.path_params['filename']
    #hard coded for now
    image_path = "./media/images/" + image_path
    with open(image_path, 'rb') as f:
        image_data = f.read()
    
    return StreamingResponse(io.BytesIO(image_data), media_type="image/jpeg")

#end 静态文件处理， for host:8000 server

#start other handlers
@app.route("/api/init")
async def _init_system(request):
    return await server.init_system(request)

@app.route("/api/page/main/{clientid}")
async def _init_main(request):   
    return await server.init_main(request)


@app.route("/api/page/more/{pagename}/{clientid}")
async def _page_init(request):      
    return await server.page_init(request)

@app.websocket_route('/api/stream') 
async def _websocket_endpoint(websocket):   
    await server.websocket_endpoint(websocket)
    

@app.on_event("startup")
async def _startup():
    '''
    host = os.environ['host']
    port = os.environ['port']
    protocol = os.environ['protocol']
    print("开机参数", host, port )
    '''
    await server.startup()
    
@app.route('/users', methods=['GET'])
async def _get_users(request):
    pass

#end others

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)