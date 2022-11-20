from services-backend.routes.base import app
import uvicorn


if __name__ == '__main__':
    uvicorn.run(app)