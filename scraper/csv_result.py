import pandas as pd


def export_csv_result(comments, output_filepath):
    rows = build_rows(comments)
    data_frame = build_data_frame(rows)

    table = pd.DataFrame(data_frame, columns=get_columns())
    table.to_csv(output_filepath)

    return []


def build_rows(comments):
    rows = []
    for comment in comments:
        rows.append(build_comment_row(comment))

        if 'thread' in comment:
            for thread_comment in comment['thread']:
                rows.append(build_reply_row(thread_comment, comment['id']))

    return rows


def build_comment_row(comment):
    return {
        **build_empty_row(''),
        'id': comment['id'],
        'content': comment['content'],
        'date_created': comment['date_created'],
        'num_likes': comment['num_likes'],
        'num_dislikes': comment['num_dislikes'],
        'username': comment['user']['name']
    }


def build_reply_row(comment, parent_id):
    return {
        **build_empty_row(''),
        'reply_id': comment['id'],
        'reply_to': parent_id,
        'reply_content': comment['content'],
        'reply_date_created': comment['date_created'],
        'reply_num_likes': comment['num_likes'],
        'reply_num_dislikes': comment['num_dislikes'],
        'reply_username': comment['user']['name'],
    }


def build_data_frame(comment_rows):
    data = build_empty_row([])

    for row in comment_rows:
        for col in row.keys():
            data[col].append(row[col])

    return data


def build_empty_row(default_value=''):
    column = {}
    for col in get_columns():
        column[col] = default_value.copy() if isinstance(default_value, list) else default_value

    return column


COLUMNS = ['id', 'content', 'date_created', 'num_likes', 'num_dislikes', 'username', 'reply_to']


def get_columns():
    columns = []
    for col in COLUMNS:
        columns.append(col)

    for col in COLUMNS:
        if col != 'reply_to':
            columns.append(f'reply_{col}')

    return columns
