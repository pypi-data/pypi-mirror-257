from flask import abort, flash, redirect, url_for
from flask.views import View
from flask_auxs import NotAllowed, PermissionDenied, error_obj_not_found, get_cancel


class Cbv:
    def __init__(self, db, wtf):
        self.db = db
        self.wtf = wtf

        self.CreateView = self.get_create_view()
        self.EditDeleteView = self.get_edit_delete_view()
        self.EditView = self.get_edit_view()
        self.DeleteView = self.get_delete_view()

    def save_obj(self, form, obj, message=None, redirect_url=None, blueprint=None):
        with self.db.Session() as db_session:
            form.populate_obj(obj)

            with db_session.begin():
                db_session.add(obj)

            if message is None:
                flash(f"{obj.__class__.__name__} '{obj}' has been saved", "success")
            else:
                flash(message, "success")

            if redirect_url is None:
                redirect_url = url_for(
                    f"{blueprint}.{obj.__class__.__name__.lower()}_detail",
                    obj_id=obj.id,
                )

        return redirect(redirect_url)

    def can_modify_obj(self, view, obj_id):
        with self.db.Session() as db_session:
            view.obj = db_session.get(view.obj_cls, obj_id)

        if not view.obj:
            return error_obj_not_found(view.obj_cls, view.blueprint)

        view.obj_cls_name = view.obj.__class__.__name__
        view.obj_cls_name_lower = view.obj_cls_name.lower()

        view.cancel_url = url_for(
            f"{view.blueprint}.{view.obj_cls_name_lower}_detail",
            obj_id=obj_id,
        )

        try:
            for validator in view.validators:
                validator(view.obj)
        except PermissionDenied:
            abort(403)
        except NotAllowed as e:
            flash(str(e), "warning")
            return redirect(view.cancel_url)

    def get_create_view(self):
        cbv_self = self

        class CreateView(View):
            def __init__(self, form_cls, template, obj_cls, blueprint):
                self.form_cls = form_cls
                self.template = template
                self.obj_cls = obj_cls
                self.blueprint = blueprint

            def dispatch_request(self):
                return cbv_self.wtf.handle_form(
                    form_cls=self.form_cls,
                    template=self.template,
                    on_success=self.on_success,
                    cancel_url=get_cancel(),
                )

            def on_success(self, form):
                self.obj = self.obj_cls()
                return cbv_self.save_obj(form, self.obj, blueprint=self.blueprint)

        return CreateView

    def get_edit_delete_view(self):
        cbv_self = self

        class EditDeleteView(View):
            def __init__(
                self, form_cls, template, obj_cls, blueprint, validators=tuple()
            ):
                self.form_cls = form_cls
                self.template = template
                self.obj_cls = obj_cls
                self.blueprint = blueprint
                self.validators = validators

            def dispatch_request(self, obj_id):
                redirect_response = cbv_self.can_modify_obj(self, obj_id)

                if redirect_response:
                    return redirect_response
                else:
                    return cbv_self.wtf.handle_form(
                        form_cls=self.form_cls,
                        template=self.template,
                        on_success=self.on_success,
                        cancel_url=self.cancel_url,
                        obj=self.obj,
                    )

            def on_success(self, form):
                pass

        return EditDeleteView

    def get_edit_view(self):
        cbv_self = self

        class EditView(cbv_self.EditDeleteView):
            def on_success(self, form):
                return cbv_self.save_obj(form, self.obj, blueprint=self.blueprint)

        return EditView

    def get_delete_view(self):
        cbv_self = self

        class DeleteView(self.EditDeleteView):
            def on_success(self, _form):
                with cbv_self.db.Session() as db_session, db_session.begin():
                    db_session.delete(self.obj)

                    flash(
                        f"{self.obj_cls_name} '{self.obj}' has been deleted",
                        "success",
                    )
                    redirect_url = url_for(
                        f"{self.blueprint}.{self.obj_cls_name_lower}_index"
                    )

                return redirect(redirect_url)

        return DeleteView
