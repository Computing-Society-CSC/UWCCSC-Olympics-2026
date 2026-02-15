# main.py - CSC Olympics 2026 后端代码
from flask import Flask, render_template, request, redirect, url_for, jsonify, flash
from pymongo import MongoClient
from bson import ObjectId
from datetime import datetime
import os
from dotenv import load_dotenv
from functools import wraps

# 加载环境变量
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'your-secret-key-2026')

# MongoDB 连接
MONGODB_URI = os.getenv('MONGODB_URI', 'mongodb+srv://Olympics:your-secret-key@cluster0.oxulaan.mongodb.net/olympics2026?retryWrites=true&w=majority')
client = MongoClient(MONGODB_URI)
db = client['olympics2026']

# 集合
houses_collection = db['houses']
players_collection = db['players']
events_collection = db['events']  # 原 match_info
matches_collection = db['matches']

# ============= 初始化默认数据 =============
def init_default_data():
    # 默认学院
    default_houses = [
        {"_id": "A3", "name": "Bari", "color": "#FFD733", "points": 0},
        {"_id": "A4", "name": "Ikhaya", "color": "#FFFFFF", "points": 0},
        {"_id": "A5", "name": "Ruka", "color": "#14B4B7", "points": 0},
        {"_id": "A6", "name": "Meraki", "color": "#0B7FCF", "points": 0},
        {"_id": "B3", "name": "Baile", "color": "#0F5D10", "points": 0},
        {"_id": "B4", "name": "Hogan", "color": "#7D0D0D", "points": 0},
        {"_id": "B5", "name": "Heimat", "color": "#4F0606", "points": 0},
        {"_id": "C3", "name": "Bandele", "color": "#620071", "points": 0},
        {"_id": "C4", "name": "Bayt", "color": "#0B8FAD", "points": 0},
        {"_id": "C5", "name": "Efie", "color": "#E78715", "points": 0},
        {"_id": "C6", "name": "Ohana", "color": "#EF5DC7", "points": 0},
        {"_id": "F0", "name": "Faculty Team", "color": "#000000", "points": 0},
    ]
    
    for house in default_houses:
        if not houses_collection.find_one({"_id": house["_id"]}):
            houses_collection.insert_one(house)
    
    # 默认选手（每个学院一个代表）
    houses = houses_collection.find()
    for house in houses:
        if not players_collection.find_one({"house_id1": house["_id"]}):
            players_collection.insert_one({
                "name": f"{house['_id']} {house['name']}",
                "medals": 0,
                "house_id1": house["_id"],
                "house_id2": None,
                "created_at": datetime.utcnow()
            })

# 启动时初始化
with app.app_context():
    init_default_data()

# ============= 辅助函数 =============
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        key = kwargs.get('key')
        if key != app.secret_key:
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function

def calculate_points(category, position, house_id):
    """计算积分"""
    points_table = {
        'Individual': {'1st': 25, '2nd': 20, '3rd': 15},
        'Team': {'1st': 50, '2nd': 45, '3rd': 40},
        'House': {'1st': 75, '2nd': 65, '3rd': 55}
    }
    
    base_points = points_table.get(category, points_table['Individual'])[position]
    
    # 特殊处理 Baile (B3) 和 Efie (C5)
    if house_id in ['B3', 'C5']:
        return int(base_points * 1.0)  # 目前是1倍，可以改为2倍
    
    return base_points

# ============= 公开路由 =============
@app.route('/')
@app.route('/home')
def home():
    events = list(events_collection.find().sort('status', -1))
    return render_template('all_matches.html', matches=events, route='home')

@app.route('/about/')
def about():
    return render_template('about.html', route='about')

@app.route('/timetable/')
def timetable():
    events = list(events_collection.find().sort('start_time', 1))
    
    timetable_data = {}
    for event in events:
        date = event.get('start_time', '').split(' ')[0]
        if date not in timetable_data:
            timetable_data[date] = []
        timetable_data[date].append(event)
    
    return render_template('timetable.html', timetable_data=timetable_data, route='timetable')

@app.route('/houses_status/')
def houses_status():
    houses = list(houses_collection.find().sort('points', -1))
    
    house_rankings = []
    color_map = {}
    for idx, house in enumerate(houses):
        house_rankings.append({
            'rank': idx + 1,
            'name': house['name'],
            'points': house['points']
        })
        color_map[house['name']] = house['color']
    
    return render_template('houses_status.html', house_rankings=house_rankings, color_map=color_map)

@app.route('/<int:event_id>/')
def event_view(event_id):
    event = events_collection.find_one({'_id': event_id})
    if not event:
        return render_template('404.html'), 404
    
    # 获取前三名
    top_3 = []
    for pos in ['1st', '2nd', '3rd']:
        player_id = event.get(f'manual_{pos}_player_id')
        if player_id:
            player = players_collection.find_one({'_id': player_id})
            top_3.append(player)
        else:
            top_3.append(None)
    
    # 获取所有比赛，按轮次分组
    matches = list(matches_collection.find({'event_id': event_id}).sort('round', 1))
    rounds = {}
    for match in matches:
        round_num = match.get('round', 0)
        if round_num not in rounds:
            rounds[round_num] = []
        rounds[round_num].append(match)
    
    # 按轮次排序
    round_matches_list = [rounds[i] for i in sorted(rounds.keys()) if i > 0]
    
    context = {
        'event': event,
        'manual_3places': top_3,
        'round_matches_list': round_matches_list,
        'route': 'event_view',
        'is_football': 'Football' in event.get('name', '')
    }
    
    if 'Football' in event.get('name', ''):
        return render_template('football_match_view.html', **context)
    return render_template('match_view.html', **context)

# ============= 管理路由 =============
@app.route('/<key>/management/')
@login_required
def management_home(key):
    return render_template('management_home.html', key=key)

@app.route('/<key>/management/matches/all/', methods=['GET', 'POST'])
@login_required
def management_matches_all(key):
    if request.method == 'POST':
        # 创建新赛事
        new_event = {
            'name': request.form['name'],
            'start_time': request.form['start_time'],
            'end_time': request.form['end_time'],
            'status': int(request.form['status']),
            'category': request.form['category'],
            'description': request.form['description'],
            'manual_1st_player_id': None,
            'manual_2nd_player_id': None,
            'manual_3rd_player_id': None,
            'hex_icon': None,
            'created_at': datetime.utcnow()
        }
        result = events_collection.insert_one(new_event)
        return redirect(url_for('main.management_matches_all', key=key))
    
    events = list(events_collection.find().sort('status', -1))
    
    events_summary = []
    for event in events:
        winner_name = None
        if event.get('manual_1st_player_id'):
            winner = players_collection.find_one({'_id': event['manual_1st_player_id']})
            if winner:
                winner_name = winner['name']
        
        events_summary.append({
            'id': event['_id'],
            'name': event['name'],
            'status': event['status'],
            'start_time': event['start_time'],
            'end_time': event['end_time'],
            'winner': winner_name
        })
    
    return render_template('management_matches.html', matches=events_summary, key=key)

@app.route('/<key>/management/matches/edit/<int:event_id>/', methods=['GET', 'POST'])
@login_required
def edit_match(key, event_id):
    event = events_collection.find_one({'_id': event_id})
    if not event:
        return render_template('404.html'), 404
    
    if request.method == 'POST':
        if 'delete' in request.form:
            events_collection.delete_one({'_id': event_id})
            matches_collection.delete_many({'event_id': event_id})
            return redirect(url_for('main.management_matches_all', key=key))
        
        # 更新赛事
        events_collection.update_one(
            {'_id': event_id},
            {'$set': {
                'name': request.form['name'],
                'start_time': request.form['start_time'],
                'end_time': request.form['end_time'],
                'status': int(request.form['status']),
                'category': request.form['category'],
                'description': request.form['description']
            }}
        )
        return redirect(url_for('main.management_matches_all', key=key))
    
    return render_template('edit_match.html', event=event, key=key)

@app.route('/<key>/management/players/', methods=['GET', 'POST'])
@login_required
def manage_players(key):
    if request.method == 'POST':
        if 'delete_player' in request.form:
            player_id = int(request.form['delete_player'])
            players_collection.delete_one({'_id': player_id})
            flash('Player deleted successfully!', 'success')
            return redirect(url_for('main.manage_players', key=key))
        
        # 添加新选手
        new_player = {
            'name': request.form['name'],
            'medals': int(request.form['medals']),
            'house_id1': request.form['house1'],
            'house_id2': request.form.get('house2') if request.form.get('house2') != '0' else None,
            'created_at': datetime.utcnow()
        }
        players_collection.insert_one(new_player)
        flash('Player added successfully!', 'success')
        return redirect(url_for('main.manage_players', key=key))
    
    players = list(players_collection.find().sort('name', 1))
    houses = list(houses_collection.find())
    return render_template('manage_players.html', players=players, houses=houses, key=key)

@app.route('/<key>/management/players/edit/<int:player_id>/', methods=['GET', 'POST'])
@login_required
def edit_player(key, player_id):
    player = players_collection.find_one({'_id': player_id})
    if not player:
        return render_template('404.html'), 404
    
    if request.method == 'POST':
        players_collection.update_one(
            {'_id': player_id},
            {'$set': {
                'name': request.form['name'],
                'medals': int(request.form['medals']),
                'house_id1': request.form['house1'],
                'house_id2': request.form.get('house2') if request.form.get('house2') != '0' else None
            }}
        )
        flash('Player updated successfully!', 'success')
        return redirect(url_for('main.manage_players', key=key))
    
    houses = list(houses_collection.find())
    return render_template('edit_player.html', player=player, houses=houses, key=key)

@app.route('/<key>/management/matches/create/<int:event_id>/', methods=['GET', 'POST'])
@login_required
def create_matches(key, event_id):
    if request.method == 'POST':
        participant_names = [name.strip() for name in request.form['participant_names'].split(',')]
        
        # 删除现有比赛
        matches_collection.delete_many({'event_id': event_id})
        
        # 获取选手ID
        player_ids = []
        for name in participant_names:
            player = players_collection.find_one({'name': name})
            if player:
                player_ids.append(player['_id'])
            else:
                flash(f"Player '{name}' not found!", 'error')
                return redirect(url_for('main.create_matches', key=key, event_id=event_id))
        
        # 创建第一轮比赛（每个选手作为胜者，round 0）
        round0_matches = []
        for player_id in player_ids:
            match = {
                'event_id': event_id,
                'round': 0,
                'winner_id': player_id,
                'player1_id': None,
                'player2_id': None,
                'score1': 0,
                'score2': 0,
                'last_match1_id': None,
                'last_match2_id': None
            }
            result = matches_collection.insert_one(match)
            round0_matches.append(result.inserted_id)
        
        # 创建后续轮次
        create_next_round(event_id, round0_matches, 1)
        
        flash('Matches created successfully!', 'success')
        return redirect(url_for('main.create_matches', key=key, event_id=event_id))
    
    return render_template('create_matches.html', key=key)

def create_next_round(event_id, previous_match_ids, round_num):
    """递归创建下一轮比赛"""
    if len(previous_match_ids) <= 1:
        return
    
    next_round_matches = []
    for i in range(0, len(previous_match_ids), 2):
        if i + 1 < len(previous_match_ids):
            match = {
                'event_id': event_id,
                'round': round_num,
                'last_match1_id': previous_match_ids[i],
                'last_match2_id': previous_match_ids[i + 1],
                'player1_id': None,
                'player2_id': None,
                'score1': 0,
                'score2': 0,
                'winner_id': None
            }
            result = matches_collection.insert_one(match)
            next_round_matches.append(result.inserted_id)
    
    # 处理奇数情况
    if len(previous_match_ids) % 2 == 1:
        next_round_matches.append(previous_match_ids[-1])
    
    # 继续创建下一轮
    create_next_round(event_id, next_round_matches, round_num + 1)

@app.route('/<key>/management/matches/all/<int:event_id>/')
@login_required
def management_view_game_matches(key, event_id):
    matches = list(matches_collection.find({'event_id': event_id, 'round': {'$gt': 0}}).sort('round', 1))
    
    match_list = []
    for match in matches:
        player1 = players_collection.find_one({'_id': match.get('player1_id')}) if match.get('player1_id') else None
        player2 = players_collection.find_one({'_id': match.get('player2_id')}) if match.get('player2_id') else None
        winner = players_collection.find_one({'_id': match.get('winner_id')}) if match.get('winner_id') else None
        
        match_list.append({
            'round_number': match['round'],
            'match_id': event_id,
            'match_uni_id': match['_id'],
            'player1_name': player1['name'] if player1 else 'TBD',
            'player2_name': player2['name'] if player2 else 'TBD',
            'score1': match.get('score1', '-'),
            'score2': match.get('score2', '-'),
            'winner_name': winner['name'] if winner else 'TBD'
        })
    
    return render_template('management_view_game_matches.html', key=key, matches=match_list)

@app.route('/<key>/management/matches/all/<int:event_id>/<int:match_id>/', methods=['GET', 'POST'])
@login_required
def management_upload_scores(key, event_id, match_id):
    match = matches_collection.find_one({'_id': match_id})
    if not match:
        return "Match not found", 404
    
    if request.method == 'POST':
        score1 = int(request.form['score1'])
        score2 = int(request.form['score2'])
        winner_id = int(request.form['winner'])
        
        # 更新比赛
        matches_collection.update_one(
            {'_id': match_id},
            {'$set': {
                'score1': score1,
                'score2': score2,
                'winner_id': winner_id
            }}
        )
        
        # 更新下一轮
        if match['round'] in [1, 2]:
            next_matches = matches_collection.find({
                '$or': [
                    {'last_match1_id': match_id},
                    {'last_match2_id': match_id}
                ],
                'round': match['round'] + 1,
                'event_id': event_id
            })
            
            for next_match in next_matches:
                if next_match.get('last_match1_id') == match_id:
                    matches_collection.update_one(
                        {'_id': next_match['_id']},
                        {'$set': {'player1_id': winner_id}}
                    )
                elif next_match.get('last_match2_id') == match_id:
                    matches_collection.update_one(
                        {'_id': next_match['_id']},
                        {'$set': {'player2_id': winner_id}}
                    )
        
        flash('Scores updated successfully!', 'success')
        return redirect(url_for('main.management_view_game_matches', key=key, event_id=event_id))
    
    # 获取选手用于下拉框
    players = []
    if match.get('player1_id'):
        p1 = players_collection.find_one({'_id': match['player1_id']})
        if p1:
            players.append((p1['_id'], p1['name']))
    if match.get('player2_id'):
        p2 = players_collection.find_one({'_id': match['player2_id']})
        if p2:
            players.append((p2['_id'], p2['name']))
    
    return render_template('management_upload_scores.html', key=key, match=match, players=players)

@app.route('/<key>/management/matches/all/<int:event_id>/win/', methods=['GET', 'POST'])
@login_required
def management_save_winner(key, event_id):
    event = events_collection.find_one({'_id': event_id})
    if not event:
        return "Event not found", 404
    
    if request.method == 'POST':
        first_name = request.form['first_place']
        second_name = request.form['second_place']
        third_name = request.form['third_place']
        
        first = players_collection.find_one({'name': first_name})
        second = players_collection.find_one({'name': second_name})
        third = players_collection.find_one({'name': third_name})
        
        if first and second and third:
            # 更新赛事前三名
            events_collection.update_one(
                {'_id': event_id},
                {'$set': {
                    'manual_1st_player_id': first['_id'],
                    'manual_2nd_player_id': second['_id'],
                    'manual_3rd_player_id': third['_id'],
                    'status': 2  # 标记为已完成
                }}
            )
            
            # 计算并更新学院积分
            category = event.get('category', 'Individual')
            
            for player, position in [(first, '1st'), (second, '2nd'), (third, '3rd')]:
                house_id = player['house_id1']
                points = calculate_points(category, position, house_id)
                
                houses_collection.update_one(
                    {'_id': house_id},
                    {'$inc': {'points': points}}
                )
            
            flash('Winners and house points updated successfully!', 'success')
        else:
            flash('One or more players not found!', 'error')
        
        return redirect(url_for('main.management_matches_all', key=key))
    
    return render_template('management_commit_winner.html', key=key, event=event)

@app.route('/<key>/management/house_rankings/', methods=['GET', 'POST'])
@login_required
def house_rankings(key):
    if request.method == 'POST':
        house_id = request.form['house_id']
        points = int(request.form['points'])
        
        houses_collection.update_one(
            {'_id': house_id},
            {'$set': {'points': points}}
        )
        flash('House points updated!', 'success')
        return redirect(url_for('main.house_rankings', key=key))
    
    houses = list(houses_collection.find().sort('points', -1))
    return render_template('management_house_rankings.html', key=key, houses=houses)

# ============= API 路由 =============
@app.route('/autocomplete/players', methods=['GET'])
def autocomplete_players():
    query = request.args.get('q', '')
    players = list(players_collection.find(
        {'name': {'$regex': query, '$options': 'i'}}
    ).limit(5))
    return jsonify([p['name'] for p in players])

if __name__ == '__main__':
    app.run(debug=True)