from .Status import Router as StatusRouter
from .Add import Router as AddRouter
from .Branch import Router as BranchRouter
from .Commit import Router as CommitRouter
from .Remove import Router as RemoveRouter
from .Stash import Router as StashRouter
from .Patch import Router as PatchRouter
from .Reset import Router as ResetRouter

PIX_STORE = {
    "Status": StatusRouter,
    "Add": AddRouter,
    "Remove": RemoveRouter,
    "Commit": CommitRouter,
    "Branch": BranchRouter,
    "Stash": StashRouter,
    "Patch": PatchRouter,
    "Reset": ResetRouter,
}

