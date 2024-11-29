import os
from flask import Flask, jsonify, request, render_template, redirect, url_for
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
CORS(app)  

# 配置数据库
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cars.db'  # 使用SQLite数据库
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭修改跟踪
db = SQLAlchemy(app)  # 初始化数据库

# 定义汽车模型
class Car(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(100), nullable=False)  # 汽车名称
    image = db.Column(db.String(200), nullable=False)  # 汽车图片URL
    description = db.Column(db.String(200), nullable=False)  # 汽车描述

# 添加评论模型
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    likes = db.Column(db.Integer, default=0)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=True)
    
    # 建立回复关系
    replies = db.relationship('Comment', backref=db.backref('parent', remote_side=[id]),
                            lazy='dynamic')

# 添加文章模型
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    car_id = db.Column(db.Integer, db.ForeignKey('car.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 建立与汽车的关系
    car = db.relationship('Car', backref=db.backref('articles', lazy=True))

# 删除现有数据库文件
# os.remove('cars.db')  # 如果需要删除现有数据库文件，可以取消注释

# 创建数据库和表
with app.app_context():
    db.create_all()  # 创建所有表

    # 添加一些示例数据
    # 示例数据可以在这里添加

@app.route('/admin')
def admin():
    cars = Car.query.all()  # 查询所有汽车
    return render_template('admin.html', cars=cars)  # 渲染admin.html模板

@app.route('/add-car', methods=['POST'])
def add_car():
    # 从表单获取数据
    name = request.form['name']
    image = request.form['image']
    description = request.form['description']
    # 创建新汽车对象
    new_car = Car(name=name, image=image, description=description)
    db.session.add(new_car)  # 添加到数据库会话
    db.session.commit()  # 提交会话
    return redirect(url_for('admin'))  # 重定向到admin页面

@app.route('/update-car/<int:car_id>', methods=['POST'])
def update_car(car_id):
    car = Car.query.get(car_id)  # 获取指定ID的汽车
    if car:
        # 更新汽车信息
        car.name = request.form['name']
        car.image = request.form['image']
        car.description = request.form['description']
        db.session.commit()  # 提交更改
    return redirect(url_for('admin'))  # 重定向到admin页面

@app.route('/delete-car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    car = Car.query.get(car_id)  # 获取指定ID的汽车
    if car:
        db.session.delete(car)  # 从数据库中删除
        db.session.commit()  # 提交更改
    return redirect(url_for('admin'))  # 重定向到admin页面

@app.route('/api/geely-cars', methods=['GET'])
def get_cars():
    cars = Car.query.all()
    return jsonify({
        'cars': [{
            'id': car.id,
            'name': car.name,
            'image': car.image,
            'description': car.description,
            'article': {
                'id': car.articles[0].id,
                'title': car.articles[0].title,
                'content': car.articles[0].content
            } if car.articles else None
        } for car in cars]
    })

@app.route('/api/cars', methods=['POST'])
def create_car():
    data = request.json
    new_car = Car(
        name=data['name'],
        image=data['image'],
        description=data['description']
    )
    db.session.add(new_car)
    db.session.commit()
    return jsonify({'message': 'Car created successfully', 'car': {
        'id': new_car.id,
        'name': new_car.name,
        'image': new_car.image,
        'description': new_car.description
    }}), 201

@app.route('/api/cars/<int:car_id>', methods=['PUT'])
def update_car_api(car_id):
    car = Car.query.get_or_404(car_id)
    data = request.json
    car.name = data['name']
    car.image = data['image']
    car.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Car updated successfully', 'car': {
        'id': car.id,
        'name': car.name,
        'image': car.image,
        'description': car.description
    }})

@app.route('/api/cars/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
    car = Car.query.get_or_404(car_id)
    
    # 删除关联的文章
    Article.query.filter_by(car_id=car_id).delete()
    
    # 删除车辆
    db.session.delete(car)
    db.session.commit()
    return jsonify({'message': '车辆及其文章已删除'})

@app.route('/api/comments', methods=['GET'])
def get_comments():
    sort_by = request.args.get('sort', 'time')  # 默认按时间排序
    # 获取顶层评论（没有父评论的评论）
    if sort_by == 'likes':
        comments = Comment.query.filter_by(parent_id=None).order_by(Comment.likes.desc()).all()
    else:
        comments = Comment.query.filter_by(parent_id=None).order_by(Comment.created_at.desc()).all()
    
    return jsonify({
        'comments': [{
            'id': comment.id,
            'content': comment.content,
            'author': comment.author,
            'created_at': comment.created_at.isoformat(),
            'likes': comment.likes,
            'replies': [{
                'id': reply.id,
                'content': reply.content,
                'author': reply.author,
                'created_at': reply.created_at.isoformat(),
                'likes': reply.likes
            } for reply in comment.replies.order_by(Comment.created_at.desc())]
        } for comment in comments]
    })

@app.route('/api/comments', methods=['POST'])
def create_comment():
    data = request.json
    new_comment = Comment(
        content=data['content'],
        author=data['author'],
        parent_id=data.get('parent_id')
    )
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({
        'id': new_comment.id,
        'content': new_comment.content,
        'author': new_comment.author,
        'created_at': new_comment.created_at.isoformat(),
        'likes': new_comment.likes
    }), 201

@app.route('/api/comments/<int:comment_id>/like', methods=['POST'])
def like_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    comment.likes += 1
    db.session.commit()
    return jsonify({'likes': comment.likes})

@app.route('/api/comments/<int:comment_id>', methods=['DELETE'])
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(comment_id)
    
    # 删除所有回复
    Comment.query.filter_by(parent_id=comment_id).delete()
    
    # 删除评论本身
    db.session.delete(comment)
    db.session.commit()
    return jsonify({'message': '评论删除成功'}), 200

@app.route('/api/articles', methods=['GET'])
def get_articles():
    articles = Article.query.all()
    return jsonify({
        'articles': [{
            'id': article.id,
            'title': article.title,
            'content': article.content,
            'car_id': article.car_id,
            'created_at': article.created_at.isoformat(),
            'car_name': article.car.name
        } for article in articles]
    })

@app.route('/api/articles/<int:article_id>', methods=['GET'])
def get_article(article_id):
    article = Article.query.get_or_404(article_id)
    return jsonify({
        'id': article.id,
        'title': article.title,
        'content': article.content,
        'car_id': article.car_id,
        'created_at': article.created_at.isoformat(),
        'car_name': article.car.name
    })

@app.route('/api/articles', methods=['POST'])
def create_article():
    data = request.json
    new_article = Article(
        title=data['title'],
        content=data['content'],
        car_id=data['car_id']
    )
    db.session.add(new_article)
    db.session.commit()
    return jsonify({'message': 'Article created successfully'}), 201

@app.route('/api/articles/<int:article_id>', methods=['PUT'])
def update_article(article_id):
    article = Article.query.get_or_404(article_id)
    data = request.json
    article.title = data['title']
    article.content = data['content']
    article.car_id = data['car_id']
    db.session.commit()
    return jsonify({'message': 'Article updated successfully'})

@app.route('/api/articles/<int:article_id>', methods=['DELETE'])
def delete_article(article_id):
    article = Article.query.get_or_404(article_id)
    db.session.delete(article)
    db.session.commit()
    return jsonify({'message': 'Article deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)  