#################
#### imports ####
#################

from flask import render_template, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import pycountry

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
    if resume_type == "basic_info":
        form = BasicResumeEditForm()
        if form.nation.data == None:
            flash('Error: ' + 'Incomplete form.')
            redirect(url_for('recipes.resume_editing', resume_type=resume_type))
        form.region.choices = [(None, '')] + [(region.code, region.name) for region in pycountry.subdivisions.get(country_code=form.nation.data)]
        if (not form.validate_on_submit()):
            if form.region.data == 'Error':
                flash('Error: ' + 'Illegal region.')
            else:
                flash('Error: ' + str(form.errors))
            db.session.rollback()
            return redirect(url_for('recipes.resume_editing', resume_type=resume_type))
        if form.portrait.data == None and current_user.resume.basic_info == None:
            flash('Error: You must upload a profile picture to get started.')
            db.session.rollback()
            return redirect(url_for('recipes.resume_editing', resume_type=resume_type))
        basic_info = resume.basic_info
        f = form.portrait.data
        avatar_url = ''
        if not f == None:
            avatar_filename = AVATARS.save(f, name=secure_filename(f.filename))
            avatar_url = AVATARS.url(avatar_filename)
        else:
            avatar_url = basic_info.portrait_URL
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
@recipes_blueprint.route('/resume/edit/<string:resume_type>', methods=('GET', ))
@login_required
def resume_editing(resume_type=None):
    kwargs = {}
    if resume_type == None or resume_type == 'basic_info':
        if current_user.resume == None:
            kwargs['basic_info_form'] = BasicResumeEditForm()
            kwargs['has_basic_info_form_data'] = False
        else:
            form = BasicResumeEditForm(obj=current_user.resume.basic_info)
            region_code_of_current_user = current_user.resume.basic_info.region
            region_of_current_user = pycountry.subdivisions.get(code=region_code_of_current_user).name
            form.region.choices = [(region_code_of_current_user, region_of_current_user)] + [(region.code, region.name) for region in pycountry.subdivisions.get(country_code=current_user.resume.basic_info.nation)]
            kwargs['has_basic_info_form_data'] = True
            kwargs['basic_info_form'] = form
    return render_template('recipes/resume_edit.html', **kwargs)

@recipes_blueprint.route('/resume/region/<country_code>')
@login_required
def get_regions(country_code):
    regions = pycountry.subdivisions.get(country_code=country_code)
    res = []
    if regions == None:
        return jsonify({'regions': [('Error', 'Error')]})
    if len(regions) == 0:
        return jsonify({'regions': [(country_code, pycountry.countries.get(alpha_2=country_code).name)]})
    for region in sorted(regions, key=lambda x: x.name):
        res.append((region.code, region.name))
    return jsonify({'regions': res})

@recipes_blueprint.route('/resume', methods=('GET', ))
@login_required
def resume_preview():
    if current_user.resume == None:
        return redirect(url_for('recipes.resume_editing'))
    return render_template('recipes/resume.html')