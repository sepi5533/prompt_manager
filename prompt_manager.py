#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
프롬프트 관리 시스템
SQLite3 데이터베이스 기반 프롬프트 CRUD 관리
"""

import sqlite3
import json
import os
from datetime import datetime
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash, send_from_directory
import pyperclip

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

# Static 파일 경로 설정
@app.route('/css/<path:filename>')
def serve_css(filename):
    """CSS 파일 서빙"""
    # 환경별 CSS 경로 자동 감지
    if os.environ.get('COMMON_STYLE_PATH'):
        # Docker 환경
        external_style_path = os.environ.get('COMMON_STYLE_PATH')
    else:
        # 로컬 환경
        external_style_path = r'C:\cursorai_working\common_style'
    
    print(f"CSS 요청: {filename}")
    print(f"CSS 경로: {external_style_path}")
    print(f"전체 경로: {os.path.join(external_style_path, filename)}")
    print(f"파일 존재: {os.path.exists(os.path.join(external_style_path, filename))}")
    return send_from_directory(external_style_path, filename)

# 데이터베이스 초기화
def init_db():
    """데이터베이스 테이블 생성"""
    conn = sqlite3.connect('prompts.db')
    cursor = conn.cursor()
    
    # 프롬프트 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS prompts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            category TEXT NOT NULL,
            description TEXT,
            tags TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 카테고리 테이블 생성
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            color TEXT DEFAULT '#6366f1',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 기본 카테고리 추가
    default_categories = [
        ('일반', '#6366f1'),
        ('개발', '#10b981'),
        ('문서작성', '#f59e0b'),
        ('분석', '#8b5cf6'),
        ('번역', '#06b6d4'),
        ('기타', '#64748b')
    ]
    
    for category, color in default_categories:
        try:
            cursor.execute('INSERT INTO categories (name, color) VALUES (?, ?)', (category, color))
        except sqlite3.IntegrityError:
            pass  # 이미 존재하는 카테고리는 무시
    
    conn.commit()
    conn.close()

def get_db_connection():
    """데이터베이스 연결"""
    conn = sqlite3.connect('prompts.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    """메인 페이지 - 프롬프트 목록"""
    conn = get_db_connection()
    
    # 검색 파라미터
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    
    # 쿼리 구성
    query = '''
        SELECT p.*, c.name as category_name, c.color as category_color 
        FROM prompts p 
        LEFT JOIN categories c ON p.category = c.name
        WHERE 1=1
    '''
    params = []
    
    if search:
        query += ' AND (p.title LIKE ? OR p.content LIKE ? OR p.description LIKE ?)'
        search_param = f'%{search}%'
        params.extend([search_param, search_param, search_param])
    
    if category:
        query += ' AND p.category = ?'
        params.append(category)
    
    query += ' ORDER BY p.updated_at DESC'
    
    prompts = conn.execute(query, params).fetchall()
    
    # 카테고리 목록
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    
    # 오늘 업데이트된 프롬프트 수 계산
    from datetime import datetime
    today = datetime.now().strftime('%Y-%m-%d')
    today_prompts = conn.execute('''
        SELECT COUNT(*) as count 
        FROM prompts 
        WHERE DATE(updated_at) = ?
    ''', (today,)).fetchone()
    today_count = today_prompts['count'] if today_prompts else 0
    
    conn.close()
    
    return render_template('index.html', prompts=prompts, categories=categories, search=search, selected_category=category, today_count=today_count)

@app.route('/prompt/new', methods=['GET', 'POST'])
def new_prompt():
    """새 프롬프트 등록"""
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        description = request.form.get('description', '')
        tags = request.form.get('tags', '')
        
        if not title or not content or not category:
            flash('제목, 내용, 카테고리는 필수입니다.', 'error')
            return redirect(url_for('new_prompt'))
        
        conn = get_db_connection()
        conn.execute('''
            INSERT INTO prompts (title, content, category, description, tags)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, content, category, description, tags))
        conn.commit()
        conn.close()
        
        flash('프롬프트가 성공적으로 등록되었습니다.', 'success')
        return redirect(url_for('index'))
    
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    
    return render_template('new_prompt.html', categories=categories)

@app.route('/prompt/<int:id>')
def view_prompt(id):
    """프롬프트 상세 보기"""
    conn = get_db_connection()
    prompt = conn.execute('''
        SELECT p.*, c.name as category_name, c.color as category_color 
        FROM prompts p 
        LEFT JOIN categories c ON p.category = c.name
        WHERE p.id = ?
    ''', (id,)).fetchone()
    conn.close()
    
    if prompt is None:
        flash('프롬프트를 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))
    
    return render_template('view_prompt.html', prompt=prompt)

@app.route('/prompt/<int:id>/edit', methods=['GET', 'POST'])
def edit_prompt(id):
    """프롬프트 수정"""
    conn = get_db_connection()
    
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        category = request.form['category']
        description = request.form.get('description', '')
        tags = request.form.get('tags', '')
        
        if not title or not content or not category:
            flash('제목, 내용, 카테고리는 필수입니다.', 'error')
            return redirect(url_for('edit_prompt', id=id))
        
        conn.execute('''
            UPDATE prompts 
            SET title = ?, content = ?, category = ?, description = ?, tags = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (title, content, category, description, tags, id))
        conn.commit()
        conn.close()
        
        flash('프롬프트가 성공적으로 수정되었습니다.', 'success')
        return redirect(url_for('view_prompt', id=id))
    
    prompt = conn.execute('SELECT * FROM prompts WHERE id = ?', (id,)).fetchone()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    
    if prompt is None:
        flash('프롬프트를 찾을 수 없습니다.', 'error')
        return redirect(url_for('index'))
    
    return render_template('edit_prompt.html', prompt=prompt, categories=categories)

@app.route('/prompt/<int:id>/delete', methods=['POST'])
def delete_prompt(id):
    """프롬프트 삭제"""
    conn = get_db_connection()
    conn.execute('DELETE FROM prompts WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    
    flash('프롬프트가 삭제되었습니다.', 'success')
    return redirect(url_for('index'))

@app.route('/api/copy/<int:id>')
def copy_prompt(id):
    """프롬프트 클립보드 복사"""
    conn = get_db_connection()
    prompt = conn.execute('SELECT content FROM prompts WHERE id = ?', (id,)).fetchone()
    conn.close()
    
    if prompt:
        # Docker 환경에서는 클립보드 기능을 사용할 수 없으므로 텍스트만 반환
        if os.environ.get('COMMON_STYLE_PATH'):  # Docker 환경
            return jsonify({
                'success': True, 
                'message': '프롬프트 내용이 아래에 표시됩니다. 텍스트를 선택하여 복사해주세요.',
                'content': prompt['content'],
                'is_docker': True
            })
        else:  # 로컬 환경
            try:
                pyperclip.copy(prompt['content'])
                return jsonify({'success': True, 'message': '클립보드에 복사되었습니다.'})
            except Exception as e:
                return jsonify({'success': False, 'message': f'복사 실패: {str(e)}'})
    
    return jsonify({'success': False, 'message': '프롬프트를 찾을 수 없습니다.'})

@app.route('/categories')
def categories():
    """카테고리 관리"""
    conn = get_db_connection()
    categories = conn.execute('SELECT * FROM categories ORDER BY name').fetchall()
    conn.close()
    
    return render_template('categories.html', categories=categories)

@app.route('/category/new', methods=['POST'])
def new_category():
    """새 카테고리 추가"""
    name = request.form['name']
    color = request.form.get('color', '#6366f1')
    
    if not name:
        flash('카테고리 이름은 필수입니다.', 'error')
        return redirect(url_for('categories'))
    
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO categories (name, color) VALUES (?, ?)', (name, color))
        conn.commit()
        flash('카테고리가 추가되었습니다.', 'success')
    except sqlite3.IntegrityError:
        flash('이미 존재하는 카테고리입니다.', 'error')
    finally:
        conn.close()
    
    return redirect(url_for('categories'))

@app.route('/category/<int:id>/delete', methods=['POST'])
def delete_category(id):
    """카테고리 삭제"""
    conn = get_db_connection()
    
    # 해당 카테고리를 사용하는 프롬프트가 있는지 확인
    count = conn.execute('SELECT COUNT(*) FROM prompts WHERE category = (SELECT name FROM categories WHERE id = ?)', (id,)).fetchone()[0]
    
    if count > 0:
        flash('이 카테고리를 사용하는 프롬프트가 있어 삭제할 수 없습니다.', 'error')
    else:
        conn.execute('DELETE FROM categories WHERE id = ?', (id,))
        conn.commit()
        flash('카테고리가 삭제되었습니다.', 'success')
    
    conn.close()
    return redirect(url_for('categories'))

if __name__ == '__main__':
    init_db()
    # Docker 환경에서는 debug=False로 설정
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000) 