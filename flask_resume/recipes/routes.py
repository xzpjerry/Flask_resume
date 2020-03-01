#################
#### imports ####
#################

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename

from . import recipes_blueprint
from .views import BasicResumeEditForm
from flask_resume import AVATARS, db
from flask_resume.models import Basic_info, Resume

################
#### routes ####
################
@recipes_blueprint.route('/index', methods=('GET',))
@recipes_blueprint.route('/', methods=('GET',))
def index(): 
    return render_template('recipes/index.html')

@recipes_blueprint.route('/resume/edit/<string:resume_type>', methods=('POST',))
@login_required
def edit_resume(resume_type):
    resume = current_user.resume
    if resume == None:
        resume = Resume()
        current_user.resume = resume
        db.session.add(resume)
        db.session.commit()
    if resume_type == "basic_info":
        form = BasicResumeEditForm()
        if not form.validate_on_submit():
            flash('Illegal input data.')
            return redirect(url_for('recipes.edit_resume'))
        basic_info = resume.basic_info
        f = form.portrait.data
        avatar_filename = AVATARS.save(f, name=secure_filename(f.filename))
        avatar_url = AVATARS.url(avatar_filename)
        if basic_info == None:
            resume.basic_info = Basic_info(name = form.name.data, nation = form.nation.data, region = form.region.data, birth = form.birth.data, portrait_URL = avatar_url)
            db.session.add(resume.basic_info)
        else:
            basic_info.name = form.name.data
            basic_info.nation = form.nation.data
            basic_info.region = form.region.data
            basic_info.birth = form.birth.data
            basic_info.portrait_URL = avatar_url
        db.session.commit()
    return redirect(url_for('recipes.resume_preview'))

@recipes_blueprint.route('/resume/edit', methods=('GET', ))
@login_required
def resume_editing():
    kwargs = {}
    if current_user.resume == None:
        kwargs['basic_info_form'] = BasicResumeEditForm()
        kwargs['has_basic_info_form_data'] = False
    else:
        kwargs['basic_info_form'] = BasicResumeEditForm(obj=current_user.resume.basic_info)
        kwargs['has_basic_info_form_data'] = True
    return render_template('recipes/resume_edit.html', **kwargs)

@recipes_blueprint.route('/resume', methods=('GET', ))
@login_required
def resume_preview():
    if current_user.resume == None:
        flash('You have not created your resume, please complete this form to make your resume.')
        return redirect(url_for('recipes.resume_editing'))
    return render_template('recipes/resume.html')