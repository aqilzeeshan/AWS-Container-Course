"Demo Flask application"
import os

from werkzeug.middleware.proxy_fix import ProxyFix
from flask import Flask, render_template, render_template_string, url_for, redirect, flash, g, request
from flask_wtf import FlaskForm
import urllib3
from wtforms import StringField, HiddenField, validators

import config

import swagger_client
from swagger_client.rest import ApiException
from swagger_client.models import Employee

configuration = swagger_client.Configuration()
# move this to an environment variable!
configuration.host = config.API_ENDPOINT
api_instance = swagger_client.EmployeeApi(swagger_client.ApiClient(configuration))

application = Flask(__name__)
application.secret_key = config.FLASK_SECRET
# fix for c9 proxy previewer
application.wsgi_app = ProxyFix(application.wsgi_app, x_proto=1)

badges = {
    "apple" : "Mac User",
    "windows" : "Windows User",
    "linux" : "Linux User",
    "video-camera" : "Digital Content Star",
    "trophy" : "Employee of the Month",
    "camera" : "Photographer",
    "plane" : "Frequent Flier",
    "paperclip" : "Paperclip Afficionado",
    "coffee" : "Coffee Snob",
    "gamepad" : "Gamer",
    "bug" : "Bugfixer",
    "umbrella" : "Seattle Fan",
}

### FlaskForm set up
class EmployeeForm(FlaskForm):
    """flask_wtf form class"""
    employee_id = HiddenField()
    fullname = StringField(u'Full Name', [validators.InputRequired()])
    location = StringField(u'Location', [validators.InputRequired()])
    job_title = StringField(u'Job Title', [validators.InputRequired()])
    badges = HiddenField(u'Badges')

@application.before_request
def before_request():
    "Set up globals referenced in jinja templates"
    g.hostname = os.uname().nodename

@application.before_first_request
def before_first_request():
    "configure samesite cookies if we are on SSL"
    if request.scheme == "https":
        application.config['SESSION_COOKIE_SAMESITE'] = "None"
        application.config['SESSION_COOKIE_SECURE'] = True


@application.errorhandler(Exception)
def all_exception_handler(error):
    print(error)
    if isinstance(error, ApiException):
        if "Amazon.DynamoDBv2.Model.ResourceNotFoundException" in error.body.decode("utf-8"):
            return render_template('error.html', error="Error: The API cannot find the Dynamo table")
        return render_template('error.html', error="Error: An API exception occured"), 500
    if isinstance(error, urllib3.exceptions.MaxRetryError):
        return render_template('error.html', error="Error: The API isn't ready"), 500
    return render_template('error.html', error="An error occurred"), 500

@application.route("/")
def home():
    "Home screen"
    response = api_instance.employee_get()
    
    return render_template_string("""
        {% extends "main.html" %}
        {% block headtitle %}Corporate Directory - Home{% endblock %}
        {% block headnav %}
        <a class="btn btn-outline-primary" href="{{ url_for('add') }}">Add</a>
        {% endblock %}
        {% block body %}
            {%  if not employees %}<h4>Empty Directory</h4>{% endif %}

            <table class="table table-bordered">
              <tbody>
            {% for employee in employees %}
                <tr>
                  <td><a href="{{ url_for('view', employee_id=employee.id) }}">{{employee.fullname}}</a>
                  {% for badge in badges %}
                  {% if badge in employee['badges'] %}
                  <i class="fa fa-{{badge}}" title="{{badges[badge]}}"></i>
                  {% endif %}
                  {% endfor %}
                  <br/>
                  <small>{{employee.location}}</small>
                  </td>
                  <td width="100">
                  <a href="{{ url_for('delete', employee_id=employee.id) }}"><span class="fa fa-remove" aria-hidden="true"></span> delete</a>
                  </td>
                </tr>
            {% endfor %}

              </tbody>
            </table>
        {% endblock %}
    """, employees=response.employees, message=response.message, badges=badges)

@application.route("/add")
def add():
    "Add an employee"
    form = EmployeeForm()
    return render_template("view-edit.html", form=form, badges=badges)

@application.route("/edit/<employee_id>")
def edit(employee_id):
    "Edit an employee"

    response = api_instance.employee_id_get(employee_id)

    form = EmployeeForm()
    form.employee_id.data = response.employee.id
    form.fullname.data = response.employee.fullname
    form.location.data = response.employee.location
    form.job_title.data = response.employee.job_title
    if response.employee.badges:
        form.badges.data = response.employee.badges

    return render_template("view-edit.html", form=form, badges=badges, message=response.message)

@application.route("/save", methods=['POST'])
def save():
    "Save an employee"
    form = EmployeeForm()

    badges_arr = None
    if form.badges:
        badges_arr = form.badges.data.split(',')

    employee = Employee(
        fullname=form.fullname.data,
        job_title=form.job_title.data,
        location=form.location.data,
        badges=badges_arr
    )

    if form.validate_on_submit():
        if form.employee_id.data:
            employee.id = form.employee_id.data
            api_instance.employee_put(body=employee)
        else:
            api_instance.employee_post(body=employee)

        flash("Saved!")
        return redirect(url_for("home"))
    else:
        return "Form failed validate"

@application.route("/employee/<employee_id>")
def view(employee_id):
    "View an employee"
    response = api_instance.employee_id_get(employee_id)
    form = EmployeeForm()

    return render_template_string("""
        {% extends "main.html" %}
        {% block headtitle %}Corporate Directory - {{employee.fullname}}{% endblock %}
        {% block headnav %}
            <a class="btn btn-outline-primary" href="{{ url_for("edit", employee_id=employee.id) }}">Edit</a>
            <a class="btn btn-outline-primary" href="{{ url_for('home') }}">Home</a>
        {% endblock %}
        {% block body %}

  <div class="row">
    <div class="col-md-12">
      <div class="form-group row">
        <label class="col-sm-2">{{form.fullname.label}}</label>
        <div class="col-sm-10">
        {{employee.fullname}}
        </div>
      </div>
      <div class="form-group row">
        <label class="col-sm-2">{{form.location.label}}</label>
        <div class="col-sm-10">
        {{employee.location}}
        </div>
      </div>
      <div class="form-group row">
        <label class="col-sm-2">{{form.job_title.label}}</label>
        <div class="col-sm-10">
        {{employee.job_title}}
        </div>
      </div>
      {% for badge in badges %}
      <div class="form-check">
        {% if badge in employee['badges'] %}
        <span class="badge badge-primary"><i class="fa fa-{{badge}}"></i> {{badges[badge]}}</span>
        {% endif %}
      </div>
      {% endfor %}
      &nbsp;
    </div>
  </div>
</form>
        {% endblock %}
    """, form=form, employee=response.employee, message=response.message, badges=badges)

@application.route("/delete/<employee_id>")
def delete(employee_id):
    "delete employee route"
    api_instance.employee_id_delete(id=employee_id)
    flash("Deleted!")
    return redirect(url_for("home"))


if __name__ == "__main__":
    application.run(debug=True)
