from flask import Flask,render_template,redirect,url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField
from wtforms.validators import Required

app=Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'

manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)

class NameForm(Form):
   name=StringField('THE MODE',validators=[Required()])
   submit=SubmitField('Submit')

class SMForm(Form):
   sm=StringField('THE SRCMAC',validators=[Required()])
   submit=SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.route('/',methods=['GET','POST'])
def index():
    name=None
    form=NameForm()
    if form.validate_on_submit():
        name=form.name.data
        print name
        f=open('mode.txt','w+')
        f.write(name)
        f.close()
        form.name.data=''
        return redirect('/srcmac')
    return render_template('index.html',form=form,name=name)

@app.route('/srcmac',methods=['GET','POST'])
def SM():
    sm=None
    form=SMForm()
    if form.validate_on_submit():
                  sm=form.sm.data
                  f=open('src.txt','w+')
                  f.write(sm)
                  f.close()
    return render_template('auth/srcmac.html',form=form,sm=sm)

if __name__=='__main__':
   manager.run()
