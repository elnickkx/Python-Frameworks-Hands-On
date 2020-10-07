from flask import Flask
from flask import request, render_template, redirect

import sqlite3

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def rootAction():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')  
  cursor = db.cursor()
  
  # # Create tables for first time when you newly lauch the app
  # cursor.execute('CREATE TABLE blogs(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, subtitle TEXT, post TEXT)')
  # cursor.execute('CREATE TABLE logins(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT, password TEXT)')
  
  # execute the left join action on blogs and comments table to publish the Entire history of single Blog
  # cursor.execute('SELECT blogs.id, blogs.title, blogs.subtitle, blogs.post, comments.comment FROM blogs INNER JOIN comments on blogs.title=comments.title ORDER BY blogs.id DESC' )
  
  # extract data from database
  cursor.execute('SELECT * FROM blogs ORDER BY id DESC')
  posts = cursor.fetchall()
  
  cursor.execute('SELECT * FROM comments ORDER BY id ASC')
  comments = cursor.fetchall()
  
  # Close db connection
  db.close()

  return render_template('postLoader.html', posts=posts, comments=comments)

@app.route('/refreshPost', methods=['GET', 'POST'])
def refreshPost():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')  
  cursor = db.cursor()
  
  # extract data from database
  cursor.execute('SELECT * FROM blogs ORDER BY id DESC')
  posts = cursor.fetchall()
  
  cursor.execute('SELECT * FROM approval ORDER BY id ASC')
  comments = cursor.fetchall()
  
  # Close db connection
  db.close()

  return render_template('postLoader.html', posts=posts, comments=comments)


@app.route('/create')
def create():
  return render_template('createPost.html')
  
  
@app.route('/insertData')
def insertData():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')  
  cursor = db.cursor()
  
  title = request.args.get('title')
  subtitle = request.args.get('subtitle')
  _id = request.args.get('_id')
  post = request.args.get('post')
  
  cursor.execute('INSERT INTO blogs(title, subtitle, post) VALUES("%s", "%s", "%s")' % (title, subtitle.replace('"', "'"), post.replace('"', "'")))
  db.commit()
  
  # Close db connection
  db.close()
  
  return redirect('/') 


@app.route('/edit')
def edit():
  # update the posts data
  title = request.args.get('title')
  subtitle = request.args.get('subtitle')
  _id = request.args.get('_id')
  post = request.args.get('post')
  
  return render_template('editPost.html', post=post.replace('"', "'"), title=title, subtitle=subtitle.replace('"', "'"), _id=_id)

  
@app.route('/updatePost/<_id>')
def updatePost(_id):
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')
  cursor = db.cursor()
  
  title = request.args.get('title')
  subtitle = request.args.get('subtitle')
  post = request.args.get('post')
  
  cursor.execute('UPDATE blogs SET title="%s", subtitle="%s", post="%s" WHERE id=%s' % (title, subtitle.replace('"', "'"), post.replace('"', "'"), _id))
  db.commit()  

  # Close db connection
  db.close()
  
  return redirect('/') 


@app.route('/trashPost/<_id>')
def trashPost(_id):
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')  
  cursor = db.cursor()
  
  # lookup for post with the _id, remove that from the source db and commit the changes
  cursor.execute('DELETE FROM blogs WHERE id=%s ' % _id)
  db.commit()
  
  # Close db connection
  db.close()

  return redirect('/')


@app.route('/post/<_id>')
def post(_id):
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')  
  cursor = db.cursor()
  
  # extract data from database for individual post
  cursor.execute('SELECT * FROM blogs WHERE id= %s' % _id)
  post = cursor.fetchone()
  
  # Close db connection
  db.close()

  return render_template('post.html', post=post)


@app.route('/login')
def login():
  return render_template("blogLogin.html")


@app.route('/verifyLogin', methods=['GET', 'POST'])
def verifyLogin():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')
  cursor = db.cursor()
  
  if request.method == 'POST':  
    username = request.form['username']
    password = request.form['password']

    # extract data from database for individual post
    cursor.execute('SELECT * FROM logins')
    history = cursor.fetchall()
    
    # extract data from database
    cursor.execute('SELECT * FROM blogs ORDER BY id DESC')
    posts = cursor.fetchall()
    
    cursor.execute('SELECT * FROM comments ORDER BY id ASC')
    comments = cursor.fetchall()
  
    # Close db connection
    db.close()

    try:
      for login in history:
        if username == login[1]:
          if password == login[2]:
            return render_template('postViewer.html', posts=posts, comments=comments)

          else:
            return render_template('blogLogin.html', info="Invalid Username and Password, Please try with the Right One !!!")

        else:
          pass
    
    except Exception as err:
      print(str(err))
      return render_template('blogLogin.html', info="Invalid Username and Password, Please try with the Right One !!!")

      
  else:
    return render_template('failure.html', info=request.method)
 

@app.route('/registerForm')
def registerForm():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')  
  cursor = db.cursor()
  
  # # Create tables for first time when you newly lauch the app
  # cursor.execute('CREATE TABLE logins(id INTEGER PRIMARY KEY AUTOINCREMENT,username TEXT, password TEXT)')
  
  # Close db connection
  db.close()
  
  return render_template("registerUser.html")
  

@app.route('/registerUser', methods=['GET', 'POST'])
def registerUser():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')
  cursor = db.cursor()
  
  if request.method == 'POST':  
    username = request.form['username']
    password = request.form['password']
    
  # register User for blogging account
  cursor.execute('INSERT INTO logins(username, password) VALUES("%s", "%s")' % (username, password))
  
  db.commit()
  
  # close the connection
  db.close()
  
  return render_template('postViewer.html', info="Start publishing your creative Blogs with us !!! " )

  
@app.route('/comment/<_title>')
def navComment(_title):
  return render_template("postComment.html", title=_title)
  
@app.route('/postComment', methods=['GET', 'POST'])
def postComment():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')
  cursor = db.cursor()
  
  # data from comment form
  title = request.args.get("title")
  comment = request.form['comment'].replace('"', "'")
  
  # initialise comment table for post for the first time
  # cursor.execute('CREATE TABLE comments(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, comment TEXT)')
  
  # insert data into comment table
  cursor.execute('INSERT INTO comments(title, comment) VALUES("%s", "%s")' % (title, comment))
  db.commit()
  
  # close the connection
  db.close()
  
  return redirect('/')

@app.route('/commentAction')
def commentAction():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')
  cursor = db.cursor()
  
  # extract data from database
  cursor.execute('SELECT * FROM blogs ORDER BY id DESC')
  posts = cursor.fetchall()
  
  cursor.execute('SELECT * FROM approval ORDER BY id ASC')
  comments = cursor.fetchall()
  
  return render_template('postViewer.html', posts=posts, comments=comments)

@app.route('/delComment/<_id>')
def delComment(_id):
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')
  cursor = db.cursor()
  
  # lookup for post with the _id, remove that from the source db and commit the changes
  cursor.execute('DELETE FROM comments WHERE id=%s ' % _id)
  db.commit()
  
  # Close db connection
  db.close()

  return redirect('/commentAction')

@app.route('/approveComment')
def approveComment():
  # Connect to sqlite3 database
  db = sqlite3.connect('blogger.db')
  cursor = db.cursor()
  
  # # initialise comment table for post for the first time
  # cursor.execute('CREATE TABLE approval(id INTEGER PRIMARY KEY AUTOINCREMENT,title TEXT, comment TEXT)')
  
  title = request.args.get('title')
  comment = request.args.get('comment')
  _id = request.args.get('_id')
  # lookup for post with the _id, remove that from the source db and commit the changes
  cursor.execute('INSERT INTO approval(title, comment) VALUES("%s", "%s") ' % (title, comment ))
  db.commit()
  
  # lookup for post that is approved and removing that from blogger (users) db
  cursor.execute('DELETE FROM comments WHERE id=%s ' % _id)
  db.commit()
  
  # Close db connection
  db.close()

  return redirect('/commentAction')



if __name__ == '__main__':
  app.run(debug=True, threaded=True)
  