import uvicorn
from config import configs


def main() -> None:
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=7212,
        reload=configs.debug_mode,
        use_colors=True,
        proxy_headers=True,
    )


if __name__ == "__main__":
    main()
