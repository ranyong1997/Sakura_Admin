import uvicorn
import sys
from pathlib import Path
import colorama

sys.path.append(str(Path(__file__).absolute().parent.parent))  # 修复没有模块名称

from app import create_application

colorama.init(autoreset=True)
app = create_application()

if __name__ == '__main__':
    uvicorn.run("app:app", host="127.0.0.0", port=8000, reload=True)
