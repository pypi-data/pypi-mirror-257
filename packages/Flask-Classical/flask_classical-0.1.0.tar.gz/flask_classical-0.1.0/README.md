# Flask-Classical

Flask extension for providing class-based views.

The following views are provided:
CreateView, EditView, DeleteView


## Installation

```bash
$ pip install Flask-Classical
```


## Usage

First create and initialize the `cbv` object:

```python
from flask_cbv import Cbv
cbv = Cbv(db, wtf)
# db is your Flask-Alchemist instance
# wtf is your Flask-Formist instance
```

And then you can add routes, for example:

```python
entries_blueprint.add_url_rule(
    "/<int:obj_id>/edit/",
    view_func=login_required(
        cbv.EditView.as_view(
            "edit_entry",
            form_cls=EntryForm,
            template="entries/edit_entry.html",
            obj_cls=Entry,
            blueprint="entries",
            validators=(current_user_is_author,),
        )
    ),
    methods=("GET", "POST"),
)
```


## License

`Flask-Classical` was created by Rafal Padkowski. It is licensed under the terms
of the MIT license.
