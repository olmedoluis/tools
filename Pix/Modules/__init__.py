from .Status import router as status_router
from .Add import router as add_router
from .Branch import router as branch_router
from .Commit import router as commit_router
from .Remove import router as remove_router
from .Stash import router as stash_router
from .Patch import router as patch_router
from .Reset import router as reset_router
from .Logs import router as log_router

PIX_STORE = {
    "STATUS": status_router,
    "ADD": add_router,
    "REMOVE": remove_router,
    "COMMIT": commit_router,
    "BRANCH": branch_router,
    "STASH": stash_router,
    "PATCH": patch_router,
    "RESET": reset_router,
    "LOG": log_router,
}
