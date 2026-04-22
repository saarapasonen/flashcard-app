# Pylint Report

**Score: 8.60 / 10**

## Fixed issues

| Warning | Fix |
|---------|-----|
| `W0611` unused-import: `get_db` imported in `app.py` | Removed the unused import |
| `C0411` wrong-import-order in `repositories/users.py` | Moved third-party import before local import |
| `R1731` consider-using-max-builtin in `routes/projects.py` | Replaced `if page < 1: page = 1` with `max()` |
| `R1730` consider-using-min-builtin in `routes/projects.py` | Replaced `if page > total_pages: page = total_pages` with `min()` |

## Remaining warnings and explanations

### C0114 missing-module-docstring (15 occurrences)

Module-level docstrings are missing from most files. These are small, focused modules
(route handlers, repository functions) where the filename and contents make the purpose
clear. Adding a one-line docstring to every module would add noise without improving
readability. Left as is.

### C0116 missing-function-docstring (many occurrences)

Function-level docstrings are missing from route handlers and repository functions.
These functions are short, have descriptive names, and follow consistent patterns
(e.g. `create_card`, `get_by_id`, `delete`). The function names serve as documentation.
Left as is.

### W0613 unused-argument `e` in `db.py:close_db`

The `e` parameter is required by Flask's `teardown_appcontext` callback signature.
Flask passes an optional exception argument to teardown functions. Removing the
parameter would cause a runtime error. Left as is.

### C0302 too-many-lines in `seed.py`

The seed script is 1004 lines (limit 1000), mostly due to the large flashcard data
dictionaries needed to populate 500+ test cards. This is a test data script, not
application code, so the length is acceptable. Left as is.

### R0914 too-many-locals in `seed.py:seed()`

The `seed()` function has 28 local variables (limit 15). This is because it creates
users, projects, flashcards, and sessions in a single function. Splitting it would
add complexity to a straightforward script that runs once. Left as is.

## Full pylint output

```
************* Module app
app.py:1:0: C0114: Missing module docstring (missing-module-docstring)

************* Module db
db.py:1:0: C0114: Missing module docstring (missing-module-docstring)
db.py:16:13: W0613: Unused argument 'e' (unused-argument)

************* Module csrf
csrf.py:1:0: C0114: Missing module docstring (missing-module-docstring)

************* Module auth_utils
auth_utils.py:1:0: C0114: Missing module docstring (missing-module-docstring)

************* Module seed
seed.py:1:0: C0302: Too many lines in module (1004/1000) (too-many-lines)
seed.py:905:0: C0116: Missing function or method docstring (missing-function-docstring)
seed.py:905:0: R0914: Too many local variables (28/15) (too-many-locals)

************* Module routes.auth
routes/auth.py:1:0: C0114: Missing module docstring (missing-module-docstring)
routes/auth.py:14:0: C0116: Missing function or method docstring
routes/auth.py:41:0: C0116: Missing function or method docstring
routes/auth.py:61:0: C0116: Missing function or method docstring

************* Module routes.browse
routes/browse.py:1:0: C0114: Missing module docstring (missing-module-docstring)
routes/browse.py:12:0: C0116: Missing function or method docstring
routes/browse.py:24:0: C0116: Missing function or method docstring
routes/browse.py:36:0: C0116: Missing function or method docstring

************* Module routes.flashcards
routes/flashcards.py:1:0: C0114: Missing module docstring (missing-module-docstring)
routes/flashcards.py:26:0: C0116: Missing function or method docstring
routes/flashcards.py:61:0: C0116: Missing function or method docstring
routes/flashcards.py:102:0: C0116: Missing function or method docstring

************* Module routes.projects
routes/projects.py:1:0: C0114: Missing module docstring (missing-module-docstring)
routes/projects.py:14:0: C0116: Missing function or method docstring
routes/projects.py:22:0: C0116: Missing function or method docstring
routes/projects.py:39:0: C0116: Missing function or method docstring
routes/projects.py:75:0: C0116: Missing function or method docstring
routes/projects.py:103:0: C0116: Missing function or method docstring

************* Module routes.search
routes/search.py:1:0: C0114: Missing module docstring (missing-module-docstring)
routes/search.py:12:0: C0116: Missing function or method docstring

************* Module routes.sessions
routes/sessions.py:1:0: C0114: Missing module docstring (missing-module-docstring)
routes/sessions.py:28:0: C0116: Missing function or method docstring
routes/sessions.py:58:0: C0116: Missing function or method docstring
routes/sessions.py:106:0: C0116: Missing function or method docstring
routes/sessions.py:158:0: C0116: Missing function or method docstring
routes/sessions.py:202:0: C0116: Missing function or method docstring
routes/sessions.py:229:0: C0116: Missing function or method docstring
routes/sessions.py:248:0: C0116: Missing function or method docstring

************* Module routes.user
routes/user.py:1:0: C0114: Missing module docstring (missing-module-docstring)
routes/user.py:10:0: C0116: Missing function or method docstring

************* Module repositories.flashcards_repo
repositories/flashcards_repo.py:1:0: C0114: Missing module docstring
repositories/flashcards_repo.py: C0116 x8: Missing function or method docstring

************* Module repositories.projects_repo
repositories/projects_repo.py:1:0: C0114: Missing module docstring
repositories/projects_repo.py: C0116 x8: Missing function or method docstring

************* Module repositories.sessions_repo
repositories/sessions_repo.py:1:0: C0114: Missing module docstring
repositories/sessions_repo.py: C0116 x13: Missing function or method docstring

************* Module repositories.stats_repo
repositories/stats_repo.py:1:0: C0114: Missing module docstring
repositories/stats_repo.py: C0116 x4: Missing function or method docstring

************* Module repositories.users
repositories/users.py:1:0: C0114: Missing module docstring
repositories/users.py: C0116 x4: Missing function or method docstring

-------------------------------------------------------------------
Your code has been rated at 8.60/10
```
