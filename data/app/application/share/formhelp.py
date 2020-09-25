from flask import flash

def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"錯誤發生在: %s - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')