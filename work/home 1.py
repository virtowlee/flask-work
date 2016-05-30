from flask import Flask,render_template,redirect,url_for
from flask.ext.script import Manager
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from flask.ext.wtf import Form
from wtforms import StringField,SubmitField,RadioField
from wtforms.validators import Required

app=Flask(__name__)
app.config['SECRET_KEY']='hard to guess string'

manager=Manager(app)
bootstrap=Bootstrap(app)
moment=Moment(app)

class FForm(Form):
   f=RadioField('THE Item',choices=[('0',u'mode'),('1',u'negotiate'),default='0')
   submit=SubmitField('Submit')

class ChForm(Form):
   ch=RadioField('THE MODE',choices=[('0',u'ALL'),('1',u'SRCMAC'),('2',u'DSTMAC'),('3',u'VLAN')],default='0')
   submit=SubmitField('Submit')

class SMForm(Form):
   sm=StringField('THE SRCMAC',validators=[Required()])
   submit=SubmitField('Submit')

class DSForm(Form):
   ds=StringField('THE DSTMAC',validators=[Required()])
   submit=SubmitField('Submit')

class VLANForm(Form):
   vlan=StringField('THE VLAN',validators=[Required()])
   submit=SubmitField('Submit')

class XSForm(Form):
   xs=StringField('THE period',validators=[Required()])
   submit=SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'),500

@app.route('/',methods=['GET','POST'])
def index():
    F=None
    form=FForm()
    if form.validate_on_submit():
       F=form.ch.data
       print F
       if F=='1':
         form.ch.data=''
         return redirect('/xieshang')
       else:
         form.ch.data=''
         return redirect('/mode')
    return render_template('index.html',form=form,F=F)
 
@app.route('/mode',methods=['GET','POST'])
def ch():
    ch=None
    form=ChForm()
    if form.validate_on_submit():
       ch=form.ch.data
       print ch
       if ch=='1':
         t='srcmac'
         f=open('mode.txt','w+')
         f.write(t)
         f.close()
         form.ch.data=''
         return redirect('/srcmac')
       elif ch=='2':
         t='dstmac'
         f=open('mode.txt','w+')
         f.write(t)
         f.close()
         form.ch.data=''
         return redirect('/dstmac')
       elif ch=='3':
         t='vlan'
         f=open('mode.txt','w+')
         f.write(t)
         f.close()
         form.ch.data=''
         return redirect('/vlan')
       else:
         t='all'
         f=open('mode.txt','w+')
         f.write(t)
         f.close()
         form.ch.data=''
         return redirect('/out')
    return render_template('auth/mode.html',form=form,ch=ch)


@app.route('/xieshang',methods=['GET','POST'])
def XS():
    xs=None
    form=xsForm()
    if form.validate_on_submit():
       xs=form.xs.data
       f=open('xs.txt','w+')
       f.write(xs)
       f.close()
       form.xs.data=''
       return redirect('/out')
    return render_template('auth/xieshang.html',form=form,xs=xs)

@app.route('/srcmac',methods=['GET','POST'])
def SM():
    sm=None
    form=SMForm()
    if form.validate_on_submit():
       sm=form.sm.data
       f=open('src.txt','w+')
       f.write(sm)
       f.close()
       form.sm.data=''
       return redirect('/out')
    return render_template('auth/srcmac.html',form=form,sm=sm)

@app.route('/dstmac',methods=['GET','POST'])
def DS():
    ds=None
    form=DSForm()
    if form.validate_on_submit():
       ds=form.ds.data
       print ds
       f=open('dst.txt','w+')
       f.write(ds)
       f.close()
       form.ds.data=''
       return redirect('/out')
    return render_template('auth/dstmac.html',form=form,ds=ds)

@app.route('/vlan',methods=['GET','POST'])
def VL():
    vlan=None
    form=VLANForm()
    if form.validate_on_submit():
       vlan=form.vlan.data
       print vlan
       f=open('vlan.txt','w+')
       f.write(vlan)
       f.close()
       form.vlan.data=''
       return redirect('/out')
    return render_template('auth/vlan.html',form=form,vlan=vlan)

@app.route('/out')
def Loginout():
    f=open('mode.txt')
    m=f.read()
    print m
    if m=='all':
       n='all'
    elif m=='srcmac':
       f=open('src.txt')
       n=f.read()
    elif m=='dstmac':
       f=open('dst.txt')
       n=f.read()
    else:
       f=open('vlan.txt')
       n=f.read()
    return render_template('auth/out.html',m=m,n=n) 


if __name__=='__main__':
   manager.run()
