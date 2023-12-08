from flask import Flask, render_template, flash
import sqlite3
from flask import request, url_for, redirect




app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'

@app.route('/', methods = ['POST','GET'])
def index():
    if request.method == 'POST':
        movie_name = request.form['searchInput']
        return redirect(url_for('movie_search',movie_name = movie_name))
    return render_template("index.html")

@app.route('/index/actor', methods = ['POST','GET'])
def index_actor():
    if request.method == 'POST':
        actor_name = request.form['searchInput']
        return redirect(url_for('actor_search',actor_name=actor_name))
    return render_template("index_actor.html")

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    return render_template('404.html'), 404  # 返回模板和状态码

@app.route('/admin_movies', methods=['GET', 'POST'])
def admin_movies():
    # 连接到数据库
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    # 执行查询语句，获取所有电影信息
    query = '''
           SELECT * 
           FROM movie_info 
           JOIN move_box ON movie_info.movie_id = move_box.movie_id
       '''
    cursor.execute(query)
    movies = cursor.fetchall()

    if request.method == 'POST':
        # 获取新增的数据
        new_id = request.form['id']
        new_name = request.form['title']
        new_release_date = request.form['release_date']
        new_country = request.form['country']
        new_type = request.form['type']
        new_year = request.form['year']
        new_box = request.form['box']

        if not new_id or not new_name or not new_release_date or not new_country or not new_type or not new_year or not new_box:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('admin_movies'))
        for movie in movies:
            if movie[0]==new_id:
                flash('Invalid input: id could not be same.')  # 显示错误提示
                return redirect(url_for('admin_movies'))
        # 执行更新语句
        query = "INSERT INTO movie_info (movie_id, movie_name, release_date, country, type, year) VALUES (?, ?, ?, ?, ?, ?)"
        cursor.execute(query, (new_id, new_name, new_release_date, new_country, new_type, new_year))
        query = "INSERT INTO move_box (movie_id, box) VALUES (?, ?)"
        cursor.execute(query, (new_id,new_box))
        conn.commit()
        flash('Item created.')
        cursor.close()
        conn.close()
        return  redirect(url_for('admin_movies'))




    # 关闭游标和连接
    cursor.close()
    conn.close()

    # 将结果传递给前端进行展示和修改
    return render_template('admin_movies.html', movies=movies)

@app.route('/admin_actors', methods=['GET', 'POST'])
def admin_actors():
    # 连接到数据库
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    # 执行查询语句，获取所有电影信息
    query = '''
            SELECT * 
            FROM actor_info 
        '''
    cursor.execute(query)
    actors = cursor.fetchall()

    if request.method == 'POST':
        # 获取新增的数据
        new_id = request.form['id']
        new_name = request.form['title']
        new_gender = request.form['gender']
        new_country = request.form['country']

        if not new_id or not new_name or not new_gender or not new_country:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('admin_actors'))
        # 执行更新语句
        for actor in actors:
            if actor[0]==new_id:
                flash('Invalid input: id could not be same.')  # 显示错误提示
                return redirect(url_for('admin_actors'))
        query = "INSERT INTO actor_info (actor_id, actor_name, gender, country) VALUES (?, ?, ?, ?)"
        cursor.execute(query, (new_id, new_name,new_gender, new_country))
        conn.commit()
        flash('Item created.')
        cursor.close()
        conn.close()
        return redirect(url_for('admin_actors'))




    # 关闭游标和连接
    cursor.close()
    conn.close()

    # 将结果传递给前端进行展示和修改
    return render_template('admin_actors.html', actors=actors)





@app.route('/actor/edit/<int:actor_id>', methods=['GET', 'POST'])
def edit_actor(actor_id):
    # 连接到数据库
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    query = '''
        SELECT * 
        FROM actor_info    
        WHERE actor_id = ?
    '''
    cursor.execute(query, (actor_id,))
    actor = cursor.fetchall()

    if request.method == 'POST':
        # 获取新增的数据
        new_name = request.form['title']
        new_gender = request.form['gender']
        new_country = request.form['country']

        if not new_name or not new_gender or not new_country:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('admin_actors'))
        # 执行更新语句
        query = "UPDATE actor_info SET actor_name=?, gender=?, country=?WHERE actor_id=?"
        cursor.execute(query, (new_name, new_gender, new_country, actor[0][0]))
        conn.commit()
        flash('Item created.')
        cursor.close()
        conn.close()
        return redirect(url_for('admin_actors'))

    # 关闭游标和连接
    cursor.close()
    conn.close()
    return render_template('edit_actor.html', actor=actor)  # 传入被编辑的电影记录


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    # 连接到数据库
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    query = '''
        SELECT * 
        FROM movie_info 
        JOIN move_box ON movie_info.movie_id = move_box.movie_id
        WHERE movie_info.movie_id = ?
    '''
    cursor.execute(query, (movie_id,))
    movie = cursor.fetchall()


    if request.method == 'POST':  # 处理编辑表单的提交请求
        new_name = request.form['title']
        new_release_date = request.form['release_date']
        new_country = request.form['country']
        new_type = request.form['type']
        new_year = request.form['year']
        new_box = request.form['box']

        if not new_name or not new_release_date or not new_country or not new_type or not new_year or not new_box:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('admin_movies'))
        # 执行更新语句
        query = "UPDATE movie_info SET movie_name=?, release_date=?, country=?, type=?, year=? WHERE movie_id=?"
        cursor.execute(query, (new_name, new_release_date, new_country, new_type, new_year,movie[0][0]))
        query = "UPDATE move_box SET box = ? WHERE movie_id=?"
        cursor.execute(query, (new_box,movie[0][0] ))
        conn.commit()
        flash('Item created.')
        cursor.close()
        conn.close()
        return redirect(url_for('admin_movies'))

    # 关闭游标和连接
    cursor.close()
    conn.close()
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    query = "DELETE FROM movie_info WHERE movie_id = ?"
    cursor.execute(query, (movie_id,))
    query = "DELETE FROM move_box WHERE movie_id = ?"
    cursor.execute(query, (movie_id,))

    conn.commit()
    cursor.close()
    conn.close()
    flash('Item deleted.')
    return redirect(url_for('admin_movies'))


@app.route('/actor/delete/<int:actor_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete_actor(actor_id):
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    query = "DELETE FROM actor_info WHERE actor_id = ?"
    cursor.execute(query, (actor_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Item deleted.')
    return redirect(url_for('admin_actors'))



@app.route('/movie/<string:movie_name>')
def movie_search(movie_name):
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    #查询电影
    query = '''
            SELECT * 
            FROM movie_info 
            JOIN move_box ON movie_info.movie_id = move_box.movie_id
            WHERE movie_info.movie_name = ?
        '''
    cursor.execute(query, (movie_name,))
    movie = cursor.fetchall()
    #查询导演
    query = '''
            SELECT actor_name
            FROM movie_info,actor_info,movie_actor_relation
            WHERE movie_info.movie_id=movie_actor_relation.movie_id 
            AND movie_actor_relation.actor_id = actor_info.actor_id
            AND movie_actor_relation.relation_type = '导演'
            AND movie_info.movie_name = ?   
    '''
    cursor.execute(query, (movie_name,))
    director = cursor.fetchall()
    # 查询演员
    query = '''
                SELECT actor_name
                FROM movie_info,actor_info,movie_actor_relation
                WHERE movie_info.movie_id=movie_actor_relation.movie_id 
                AND movie_actor_relation.actor_id = actor_info.actor_id
                AND movie_actor_relation.relation_type = '主演'
                AND movie_info.movie_name = ?   
        '''
    cursor.execute(query, (movie_name,))
    actor = cursor.fetchall()

    # 关闭游标和连接
    cursor.close()
    conn.close()
    if not movie:
        flash('电影未录入.')
        return redirect(url_for('index'))
    return render_template('movie.html', movie=movie, director=director, actor=actor)

@app.route('/actor/<string:actor_name>')
def actor_search(actor_name):
    conn = sqlite3.connect('movie.db')
    cursor = conn.cursor()
    #查询电影
    query = '''
            SELECT * 
            FROM actor_info 
            WHERE actor_name = ?
        '''
    cursor.execute(query, (actor_name,))
    actor = cursor.fetchall()
    #查询导演的电影
    query = '''
                SELECT movie_info.movie_name
                FROM movie_info,actor_info,movie_actor_relation
                WHERE movie_info.movie_id=movie_actor_relation.movie_id 
                AND movie_actor_relation.actor_id = actor_info.actor_id
                AND movie_actor_relation.relation_type = '导演'
                AND actor_name = ?   
             '''
    cursor.execute(query, (actor_name,))
    direct_movie = cursor.fetchall()
    # 查询主演的电影
    query = '''
                SELECT movie_info.movie_name
                FROM movie_info,actor_info,movie_actor_relation
                WHERE movie_info.movie_id=movie_actor_relation.movie_id 
                AND movie_actor_relation.actor_id = actor_info.actor_id
                AND movie_actor_relation.relation_type = '主演'
                AND actor_name = ?   
        '''
    cursor.execute(query, (actor_name,))
    act_movie = cursor.fetchall()

    # 关闭游标和连接
    cursor.close()
    conn.close()
    if not actor:
        flash('演员未录入.')
        return redirect(url_for('index_actor'))
    return render_template('actor.html', actor=actor, direct_movie=direct_movie, act_movie=act_movie)