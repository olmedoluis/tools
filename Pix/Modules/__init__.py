from .Status import Router as StatusRouter
from .Add import router as AddRouter
from .Branch import Router as BranchRouter
from .Commit import Router as CommitRouter
from .Remove import Router as RemoveRouter
from .Stash import Router as StashRouter
from .Patch import Router as PatchRouter
from .Reset import Router as ResetRouter

PIX_STORE = {
    "STATUS": StatusRouter,
    "ADD": AddRouter,
    "REMOVE": RemoveRouter,
    "COMMIT": CommitRouter,
    "BRANCH": BranchRouter,
    "STASH": StashRouter,
    "PATCH": PatchRouter,
    "RESET": ResetRouter,
}

