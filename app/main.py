import uvicorn

if __name__ == "__main__":
    # запуск роутера
    uvicorn.run(
        "app.routers:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
