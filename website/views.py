from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from .models import *
from datetime import datetime
from flask_login import login_required, login_user, logout_user, current_user
from sqlalchemy.sql import func
import numpy as np

views = Blueprint('views', __name__)

@views.route('/')
@views.route('/home')
def home():
    return render_template("home.html", user = current_user)

def format_time(seconds):
    if seconds >= 3600:  # if total time is more than 1 hour
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        return f"{hours} hr, {minutes} min"
    elif seconds >= 60:  # if total time is more than 1 minute
        minutes = seconds // 60
        return f"{minutes} min"
    else:  # if total time is less than 1 minute
        return f"{seconds} sec"

@views.route('/<id>/dashboard')
def showStats(id):
    user = User.query.filter_by(id=id).first()
    if user.name == 'Admin@knowme':
        return redirect(url_for('views.admin_dashboard'))
    stat = user.stats
    timeArray = str(stat.times)
    time = timeArray.split(',')
    time = np.array([int(float(x)) for x in time if x is not ""])
    times = [format_time(x) for x in time]
    attArray = str(stat.attempts)
    att = attArray.split(',')
    atts = np.array([int(float(x)) for x in att if x is not ""])
    list_lb = []
    lb_stats = db.session.query(Stats, User).join(User).order_by(Stats.level.desc(), Stats.sumoftimes.asc(), Stats.sumofattempts.asc()).all()
    for lb_stat, userlb in lb_stats:
        if lb_stat.level != 0:
            temp = [userlb.name, lb_stat.level, format_time(round(lb_stat.sumoftimes/lb_stat.level, 1)), round(lb_stat.sumofattempts/lb_stat.level, 1)]
            list_lb.append(temp)
    return render_template("stats.html", user=current_user, stat=stat, time=times, atts=atts, list_lb=list_lb)

@views.route('/admin-dashboard')
def admin_dashboard():
    list_lb = []
    lb_stats = db.session.query(Stats, User).join(User).order_by(Stats.level.desc(), Stats.sumoftimes.asc(), Stats.sumofattempts.asc()).all()
    for lb_stat, userlb in lb_stats:
        if lb_stat.level != 0:
            timeArray = str(lb_stat.times)
            time = timeArray.split(',')
            times = np.array([int(float(x)) for x in time if x is not ""])
            attArray = str(lb_stat.attempts)
            att = attArray.split(',')
            atts = np.array([int(float(x)) for x in att if x is not ""])
            details = cthink = creativity = intel = knowldg = persp = curious = persev = athink = 0
            cthink += 1 if times[0] < 150 else 0
            cthink += 1 if times[4] < 350 else 0
            cthink += 1 if times[5] < 360 else 0
            details += 1 if atts[0] < 3 else 0
            details += 1 if atts[2] < 3 else 0
            details += 1 if atts[3] < 3 else 0
            details += 1 if atts[5] < 3 else 0
            creativity += 1 if times[1] < 150 else 0
            creativity += 1 if atts[3] < 3 else 0
            creativity += 1 if times[5] < 360 else 0
            intel += 1 if atts[1] < 3 else 0
            intel += 1 if atts[2] < 3 else 0
            intel += 1 if atts[4] < 3 else 0
            intel += 1 if atts[5] < 3 else 0
            knowldg += 1 if atts[2] < 3 else 0
            knowldg += 1 if atts[3] < 3 else 0
            knowldg += 1 if times[4] < 300 else 0
            knowldg += 1 if times[5] < 360 else 0
            persp += 1 if times[3] < 200 else 0
            persp += 1 if times[4] < 300 else 0
            curious += 1 if atts[3] < 3 else 0
            curious += 1 if times[4] < 300 else 0
            curious += 1 if times[5] < 360 else 0
            persev += 1 if times[3] < 200 else 0
            persev += 1 if times[4] < 300 else 0
            persev += 1 if times[5] < 360 else 0
            athink += 1 if atts[3] < 3 else 0 
            athink += 1 if atts[4] < 3 else 0
            athink += 1 if atts[5] < 3 else 0
            attr = []
            x = 'Great Critical Thinking' if cthink == 3 else ('Critical Thinking' if cthink > 0 else '')
            attr.append(x)
            x = 'Great Eye for Details' if details == 4 else ('Eye for Details' if details > 0 else '')
            attr.append(x)
            x = 'Great Creativity' if creativity == 4 else ('Creativity' if creativity > 0 else '')
            attr.append(x)
            x = 'Great Intelligence' if intel == 4 else ('Intelligence' if intel > 0 else '')
            attr.append(x)
            x = 'Great Knowledge' if knowldg == 4 else ('Knowledge' if knowldg > 0 else '')
            attr.append(x)
            x = 'Wide Perspective' if persp == 2 else ('Perspective' if persp > 0 else '')
            attr.append(x)
            x = 'Extreme Curiosity' if curious == 3 else ('Curious' if curious > 0 else '')
            attr.append(x)
            x = 'Extreme Perseverence' if persev == 3 else ('Perseverence' if persev > 0 else '')
            attr.append(x)
            x = 'Great Analytical Thinking' if athink == 3 else ('Analytical Thinking' if athink > 0 else '')
            attr.append(x)
            attr = np.array([x for x in attr if x is not ''])
            temp = [userlb.name, lb_stat.level, format_time(round(lb_stat.sumoftimes/lb_stat.level, 1)), round(lb_stat.sumofattempts/lb_stat.level, 1), attr]
            list_lb.append(temp)
    return render_template("admin.html", user=current_user, list_lb=list_lb, n=len(attr))

def timesec(start_time_str, end_time_str):
    start_time = datetime.strptime(start_time_str.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
    end_time = datetime.strptime(end_time_str.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
    return (end_time - start_time).total_seconds()


@views.route('<id>/<lvl>/starttimer')
def timer(id, lvl):
    user = User.query.filter_by(id=id).first()
    user.buffertime = datetime.now()
    user.flag = True
    db.session.commit()
    if int(lvl)==0:
        return redirect(url_for('views.level1', id=id))
    if int(lvl)==1:
        return redirect(url_for('views.level2', id=id))
    if int(lvl)==2:
        return render_template("dead1.html", user=current_user)
    if int(lvl)==3:
        return redirect(url_for('views.level4', id=id))
    if int(lvl)==4:
        return render_template("dead2.html", user=current_user)
    if int(lvl)==5:
        return redirect(url_for('views.level6', id=id))

    return 'not a valid level'


@views.route('<id>/level1', methods=['GET', 'POST'])
def level1(id):
    if request.method=='POST':
        user = User.query.filter_by(id=id).first()
        stat = user.stats
        answer = str(request.form.get('answer'))

        if answer.lower() == "libra":
            if stat.level == 0:
                end_time = datetime.now()
                time_diff_seconds = timesec(user.buffertime, end_time)

                stat.sumoftimes = stat.sumoftimes + time_diff_seconds
                stat.sumofattempts = stat.sumofattempts + user.bufferattempt + 1

                timeArray = str(stat.times)
                time = timeArray.split(',')
                time.append(time_diff_seconds)
                times = ','.join(str(x) for x in time)

                attArray = str(stat.attempts)
                att = attArray.split(',')
                att.append(user.bufferattempt+1)
                attempts = ','.join(str(y) for y in att)

                print(times)
                print(attempts)
                
                stat.times = times
                stat.attempts = attempts
                stat.level = 1
                user.bufferattempt = 0
                db.session.commit()
            return redirect(url_for('views.buffer'))
        else:
            user.bufferattempt = user.bufferattempt + 1
            db.session.commit()
            flash('Oops, that is not my sign :(', category='error')

    return render_template('level1.html', user = current_user)

@views.route('<id>/level2', methods=['GET', 'POST'])
def level2(id):
    if request.method=='POST':
        user = User.query.filter_by(id=id).first()
        stat = user.stats
        answer = str(request.form.get('answer'))

        if answer.lower() == "riddle":
            if stat.level == 1:
                end_time = datetime.now()
                time_diff_seconds = timesec(user.buffertime, end_time)

                stat.sumoftimes = stat.sumoftimes + time_diff_seconds
                stat.sumofattempts = stat.sumofattempts + user.bufferattempt + 1

                timeArray = str(stat.times)
                time = timeArray.split(',')
                time.append(time_diff_seconds)
                times = ','.join(str(x) for x in time)

                attArray = str(stat.attempts)
                att = attArray.split(',')
                att.append(user.bufferattempt+1)
                attempts = ','.join(str(y) for y in att)

                print(times)
                print(attempts)
                
                stat.times = times
                stat.attempts = attempts
                stat.level = 2
                user.bufferattempt = 0
                db.session.commit()
            
            return render_template('dead1.html', user = current_user)
        else:
            user.bufferattempt = user.bufferattempt + 1
            db.session.commit()
            flash('Oops, that is not the correct answer :(', category='error')

    return render_template('level2.html', user = current_user)

@views.route('<id>/level3', methods=['GET', 'POST'])
def level3(id):
    user = User.query.filter_by(id=id).first()
    goat = user.goat
    if request.method=='POST':
        stat = user.stats
        goat = user.goat
        if str(goat)=='messi' or str(goat)=='mbappe' or str(goat)=='neymar':
            ans = str(request.form.get('answer'))
            if ans.lower()=='dead':
                user.bufferattempt = user.bufferattempt + 1
                db.session.commit()
                return render_template('end.html', user=current_user)
            else:
                user.bufferattempt = user.bufferattempt + 1
                db.session.commit()
                flash('It\'s not the right answer')
            return render_template('level3.html', user=current_user, goat=goat)
        elif str(goat)=='cr7':
            ans = str(request.form.get('answer'))
            if ans.lower()=='good':
                if stat.level == 2:
                    end_time = datetime.now()
                    time_diff_seconds = timesec(user.buffertime, end_time)

                    stat.sumoftimes = stat.sumoftimes + time_diff_seconds
                    stat.sumofattempts = stat.sumofattempts + user.bufferattempt + 1

                    timeArray = str(stat.times)
                    time = timeArray.split(',')
                    time.append(time_diff_seconds)
                    times = ','.join(str(x) for x in time)

                    attArray = str(stat.attempts)
                    att = attArray.split(',')
                    att.append(user.bufferattempt+1)
                    attempts = ','.join(str(y) for y in att)

                    print(times)
                    print(attempts)
                    
                    stat.times = times
                    stat.attempts = attempts
                    stat.level = 3
                    user.bufferattempt = 0
                    db.session.commit()

                return render_template('buffer.html', user=current_user)
            else:
                user.bufferattempt = user.bufferattempt + 1
                db.session.commit()
                flash('It\'s not the right answer')
            return render_template('level3.html', user=current_user)
    return render_template('level3.html', user=current_user, goat=goat)

@views.route('<id>/level4', methods=['GET', 'POST'])
def level4(id):
    if request.method=='POST':
        user = User.query.filter_by(id=id).first()
        stat = user.stats
        answer = str(request.form.get('answer'))
        
        if answer.lower() == "marvel":
            if stat.level == 3:
                end_time = datetime.now()
                time_diff_seconds = timesec(user.buffertime, end_time)

                stat.sumoftimes = stat.sumoftimes + time_diff_seconds
                stat.sumofattempts = stat.sumofattempts + user.bufferattempt + 1

                timeArray = str(stat.times)
                time = timeArray.split(',')
                time.append(time_diff_seconds)
                times = ','.join(str(x) for x in time)

                attArray = str(stat.attempts)
                att = attArray.split(',')
                att.append(user.bufferattempt+1)
                attempts = ','.join(str(y) for y in att)

                print(times)
                print(attempts)
                
                stat.times = times
                stat.attempts = attempts
                stat.level = 4
                user.bufferattempt = 0
                db.session.commit()

            return render_template('dead2.html', user = current_user)
        else:
            user.bufferattempt = user.bufferattempt + 1
            db.session.commit()
            flash('Oops, that is not the answer :(', category='error')

    return render_template('level4.html', user = current_user)

@views.route('<id>/level5', methods=['GET', 'POST'])
def level5(id):
    user = User.query.filter_by(id=id).first()
    char = user.goat
    if request.method=='POST':
        stat = user.stats
        char = user.goat
        answer = str(request.form.get('answer'))

        if char=='tom':
            if answer.lower() == "m122":
                if stat.level == 4:
                    end_time = datetime.now()
                    time_diff_seconds = timesec(user.buffertime, end_time)

                    stat.sumoftimes = stat.sumoftimes + time_diff_seconds
                    stat.sumofattempts = stat.sumofattempts + user.bufferattempt + 1

                    timeArray = str(stat.times)
                    time = timeArray.split(',')
                    time.append(time_diff_seconds)
                    times = ','.join(str(x) for x in time)

                    attArray = str(stat.attempts)
                    att = attArray.split(',')
                    att.append(user.bufferattempt+1)
                    attempts = ','.join(str(y) for y in att)

                    print(times)
                    print(attempts)
                    
                    stat.times = times
                    stat.attempts = attempts
                    stat.level = 5
                    user.bufferattempt = 0
                    db.session.commit()

                return redirect(url_for('views.buffer'))
            else:
                user.bufferattempt = user.bufferattempt + 1
                db.session.commit()
                flash('Oops, that is not the answer :(', category='error')
        else:
            if answer.lower() == "m122":
                user.bufferattempt = user.bufferattempt + 1
                db.session.commit()
                return render_template('end.html', user = current_user)
            else:
                user.bufferattempt = user.bufferattempt + 1
                db.session.commit()
                flash('Oops, that is not the answer :(', category='error')

    return render_template('level5.html', user = current_user)

@views.route('<id>/level6', methods=['GET', 'POST'])
def level6(id):
    if request.method=='POST':
        user = User.query.filter_by(id=id).first()
        stat = user.stats
        answer = str(request.form.get('answer'))
        if answer.lower() == "20022b":
            if stat.level == 5:
                end_time = datetime.now()
                time_diff_seconds = timesec(user.buffertime, end_time)

                stat.sumoftimes = stat.sumoftimes + time_diff_seconds
                stat.sumofattempts = stat.sumofattempts + user.bufferattempt+ 1

                timeArray = str(stat.times)
                time = timeArray.split(',')
                time.append(time_diff_seconds)
                times = ','.join(str(x) for x in time)
                
                attArray = str(stat.attempts)
                att = attArray.split(',')
                att.append(user.bufferattempt+1)
                attempts = ','.join(str(y) for y in att)

                print(times)
                print(attempts)

                stat.times = times
                stat.attempts = attempts
                stat.level = 6
                user.bufferattempt = 0
                db.session.commit()

            return render_template('win.html', user = current_user)
        else:
            user.bufferattempt = user.bufferattempt + 1
            db.session.commit()
            flash('Oops, that is not the answer :(', category='error')

    return render_template('level6.html', user = current_user)

@views.route('<id>/<lvl>/<goat>/starttimer', endpoint='start_timer')
def timer(id, lvl, goat):
    user = User.query.filter_by(id=id).first()
    if user.bufferattempt == 0:
        user.buffertime = datetime.now()
    user.goat = goat
    print(goat)
    db.session.commit()
    
    if int(lvl)==2:
        return redirect(url_for('views.level3', id=id))
    else:
        return redirect(url_for('views.level5', id=id))

@views.route('/level_cleared')
def buffer():
    return render_template('buffer.html', user = current_user)

@views.route('<id>/<lvl>/dd', methods=['GET','POST'])
def ded(id, lvl):
    user = User.query.filter_by(id=id).first()
    if int(lvl)==2:
        return render_template('dead1.html', user = current_user)
    else:
        return render_template('dead2.html', user = current_user)
    
@views.route('delete/<user_id>')
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    stats = Stats.query.filter_by(author=user_id).first()
    logout_user()
    db.session.delete(user)
    db.session.delete(stats)
    db.session.commit()
    flash('Account successfully deleted!', category='successs')
    return redirect(url_for('views.home'))