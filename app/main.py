import fastapi
import uvicorn
from fastapi.templating import Jinja2Templates

app = fastapi.FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_root(request: Request):
    """ Default route """
    return templates.TemplateResponse("invaders.html", {"request": request})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
