from .Status import router as StatusRouter
from .Add import router as AddRouter
from .Branch import router as BranchRouter
from .Commit import router as CommitRouter
from .Remove import router as RemoveRouter
from .Stash import router as StashRouter
from .Patch import router as PatchRouter
from .Reset import router as ResetRouter
from .Logs import router as LogRouter

PIX_STORE = {
    "STATUS": StatusRouter,
    "ADD": AddRouter,
    "REMOVE": RemoveRouter,
    "COMMIT": CommitRouter,
    "BRANCH": BranchRouter,
    "STASH": StashRouter,
    "PATCH": PatchRouter,
    "RESET": ResetRouter,
    "LOG": LogRouter,
}
